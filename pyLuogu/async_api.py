import re
import json
import asyncio
from typing import List, Literal, Callable

import httpx
import bs4

from .types import *
from .errors import *
from . import logger

class asyncLuoguAPI:
    def __init__(
            self,
            base_url="https://www.luogu.com.cn",
            cookies: LuoguCookies = None,
            timeout: float | httpx.Timeout | None = 10,
            max_retries: int = 5,
    ):
        self.base_url = base_url
        self.cookies = None if cookies is None else cookies.to_json()
        self.max_retries = max_retries
        self.client = httpx.AsyncClient(
            timeout=timeout,
            cookies=self.cookies,
            follow_redirects=True,
        )
        self.x_csrf_token = None

    async def _send_request(
            self,
            endpoint: str,
            method: str = "GET",
            params: RequestParams | None = None,
            data: dict | None = None
    ):
        url = f"{self.base_url}/{endpoint}"
        headers = await self._get_headers(method)
        param_final = None if params is None else params.to_json()

        request = self.client.build_request(
            method, url,
            headers=headers,
            params=param_final,
            json=data,
        )

        for attempt in range(self.max_retries):
            if method == "GET":
                logger.info(f"({attempt}/{self.max_retries}) Async GET from {url} with params: {param_final}")
            else:
                data_str = json.dumps(data)
                payload_str = data_str if data and len(data_str) < 50 else data_str[:50] + "..."
                logger.info(f"({attempt}/{self.max_retries}) Async POST to {url} with payload: {payload_str}")
            
            try:
                response = await self.client.send(request)
            except httpx.TimeoutException as e:
                logger.warning(f"Attempt {attempt + 1}: Timeout error - {e}")
                await asyncio.sleep(1)
                continue
            except httpx.HTTPError as e:
                logger.error(f"Request error: {e}")
                raise RequestError("Request error") from e

            try:
                response.raise_for_status()
                
                new_C3VK = await self._get_C3VK(response)
                if new_C3VK is not None:
                    continue
                
                try:
                    res_json = response.json()
                except json.JSONDecodeError:
                    logger.error(f"Failed to decode JSON response: {response.text}")
                    raise RequestError("Failed to decode JSON response") from None
                logger.debug(f"{json.dumps(res_json)}")

                if res_json.get("currentTemplate") == "AuthLogin":
                    raise AuthenticationError("Need Login")
                if res_json.get("code") == 403:
                    if res_json.get("请求频繁，请稍候再试"):
                        logger.warning("403: Request too frequent")
                        await asyncio.sleep(attempt * 5)
                        continue
                    if res_json.get("errorMessage") == "user.not_self":
                        raise AuthenticationError("not yourself")
                    logger.warning("CSRF token expired, refreshing token...")
                    await self._get_csrf()
                    headers = await self._get_headers(method)
                    continue
                if res_json.get("code") in [404, 418]:
                    raise NotFoundError(f"Resource not found {endpoint}")

                if res_json.get("currentData") is not None:
                    res_json = res_json.get("currentData")
                if res_json.get("data") is not None:
                    res_json = res_json.get("data")
                return res_json
            except httpx.HTTPStatusError as e:
                if response.status_code == 401:
                    raise AuthenticationError("Authentication failed") from e
                elif response.status_code == 403:
                    res_json = response.json()
                    message = res_json.get("errorMessage")
                    logger.warning(f"HTTP 403: {message}")
                    if message is None:
                        raise ForbiddenError(f"Forbidden: {e}") from e
                    if message == "提交过于频繁，请过3分钟再尝试":
                        await asyncio.sleep(180)
                        continue
                    if message == "请求频繁，请稍候再试":
                        await asyncio.sleep(5)
                        continue
                    if message == "验证码错误":
                        raise NeedCaptcha("Need captcha") from e
                        continue
                    if message == "user.not_self":
                        raise AuthenticationError("not yourself")
                    logger.warning("CSRF token expired, refreshing token...")
                    self._get_csrf()
                    continue  # Retry the request
                elif response.status_code == 404:
                    raise NotFoundError("Resource not found") from e
                elif response.status_code == 429:
                    logger.warning("429: Rate limit exceeded")
                    await asyncio.sleep(attempt * 5)
                    continue
                elif 500 <= response.status_code < 600:
                    raise ServerError("Server error") from e
                else:
                    raise RequestError("HTTP error") from e
        
        logger.error(f"Failed to send request after {self.max_retries} attempts")
        raise RequestError(f"Failed to send request after {self.max_retries} attempts")

    async def _get_headers(self, method: str) -> dict:
        if self.x_csrf_token is None:
            await self._get_csrf()
        headers = {
            "User-Agent": "luogu_bot",
            "x-lentille-request": "content-only",
            "x-luogu-type": "content-only",
            "x-csrf-token": self.x_csrf_token
        }
        if method != "GET":
            headers.update({
                "Content-Type": "application/json",
                "referer": "https://www.luogu.com.cn/",
            })
        return headers

    async def _get_C3VK(self, response: httpx.Response) -> str | None:
        result = re.search(r"C3VK=(.*); path", response.text)
        if result:
            self.cookies["C3VK"] = result.group(1)
            self.client.cookies.set("C3VK", result.group(1))
            logger.info(f"C3VK token fetched successfully {result.group(1)}")
            return result.group(1)
        else:
            return None

    async def _get_csrf(self, endpoint="") -> str:
        headers = {
            "User-Agent": "luogu_bot",
        }

        for attempt in range(self.max_retries):
            try:
                logger.info(f"({attempt}/{self.max_retries}) Async GET CSRF token from {self.base_url + endpoint}")
                response = await self.client.get(
                    self.base_url + endpoint, 
                    headers=headers, 
                    cookies=self.cookies
                )
                
                response.raise_for_status()

                new_C3VK = await self._get_C3VK(response)
                if new_C3VK is not None:
                    continue
                
                soup = bs4.BeautifulSoup(response.text, "html.parser")
                csrf_meta = soup.select_one("meta[name='csrf-token']")

                if csrf_meta and "content" in csrf_meta.attrs:
                    self.x_csrf_token = csrf_meta["content"]
                    logger.info(f"new CSRF token : {self.x_csrf_token}")
                    return self.x_csrf_token
                else:
                    logger.warning("CSRF token not found, retrying...")
                    await asyncio.sleep(1)
            except httpx.TimeoutException as e:
                logger.warning(f"Attempt {attempt + 1}: Timeout error - {e}")
                await asyncio.sleep(1)
            except httpx.HTTPError as e:
                logger.error(f"HTTP error: {e}")
                raise RequestError(f"HTTP error: {e}")

        logger.error(f"Failed to fetch CSRF token after {self.max_retries} attempts")
        raise RequestError(f"Failed to fetch CSRF token after {self.max_retries} attempts")

    async def _get_captcha(self):
        headers = {
            "User-Agent": "luogu_bot",
            "x-csrf-token": self.x_csrf_token
        }
        for attempt in range(self.max_retries):
            try:
                logger.info(f"({attempt}/{self.max_retries}) Async GET captcha from {self.base_url + '/api/verify/captcha'}")
                response = await self.client.get(
                    self.base_url + "/api/verify/captcha", 
                    headers=headers, 
                    cookies=self.cookies
                )

                response.raise_for_status()

                return response.content
            except httpx.TimeoutException as e:
                logger.warning(f"Attempt {attempt + 1}: Timeout error - {e}")
                await asyncio.sleep(1)
            except httpx.HTTPError as e:
                logger.error(f"HTTP error: {e}")
                raise RequestError("HTTP error") from e
        
        raise RequestError(f"Failed to fetch captcha after {self.max_retries} attempts")

    def _post_captcha(self, captcha: str):
        raise NotImplementedError
    
    async def login(
            self, user_name: str, password: str,
            captcha: Literal["input", "ocr"],
            two_step_verify: Literal["google", "email"] | None = None
    ) -> bool:
        raise NotImplementedError

    async def logout(self):
        raise NotImplementedError

    async def get_problem_list(
            self,
            page: int | None = None,
            orderBy: int | None = None,
            keyword: str | None = None,
            content: bool | None = None,
            _type: ProblemType | None = None,
            difficulty: int | None = None,
            tag: str | None = None,
            params: ProblemListRequestParams | None = None
    ) -> ProblemListRequestResponse:
        if params is None:
            params = ProblemListRequestParams(json={
                "page": page,
                "orderBy": orderBy,
                "keyword": keyword,
                "content": content,
                "type": _type,
                "difficulty": difficulty,
                "tag": tag
            })
        res = await self._send_request(endpoint="problem/list", params=params)

        res["count"] = res["problems"]["count"]
        res["perPage"] = res["problems"]["perPage"]
        res["problems"] = res["problems"]["result"]

        return ProblemListRequestResponse(res)

    async def get_team_problem_list(
            self, tid: int,
            page: int | None = None
    ) -> ProblemListRequestResponse:
        params = ListRequestParams(json={"page": page})
        res = await self._send_request(
            endpoint=f"api/team/problems/{tid}", 
            params=params
        )

        res["count"] = res["problems"]["count"]
        res["perPage"] = res["problems"]["perPage"]
        res["problems"] = res["problems"]["result"]

        return ProblemListRequestResponse(res)

    async def get_problem(
            self, pid: str,
            contest_id: int | None = None
    ) -> ProblemDataRequestResponse:
        params = ProblemRequestParams(json={"contest_id": contest_id})
        res = await self._send_request(endpoint=f"problem/{pid}", params=params)

        res["problem"]["limits"] = list(zip(
            res["problem"]["limits"]["time"], res["problem"]["limits"]["memory"]
        ) )

        return ProblemDataRequestResponse(res)

    async def get_problem_settings(
            self, pid: str,
    ) -> ProblemSettingsRequestResponse:
        res = await self._send_request(endpoint=f"problem/edit/{pid}")
        
        res["problemDetails"] = res["problem"]
        res["problemSettings"] = res["setting"]
        res["problemSettings"]["comment"] = res["problem"]["comment"]
        res["problemSettings"]["providerID"] = res["problem"]["provider"]["uid"] or res["problem"]["provider"]["id"]
        res["testCaseSettings"] = dict()
        res["testCaseSettings"]["cases"] = res["testCases"]
        res["testCaseSettings"]["scoringStrategy"] = res["scoringStrategy"]
        res["testCaseSettings"]["subtaskScoringStrategies"] = res["subtaskScoringStrategies"]
        res["testCaseSettings"]["showSubtask"] = res["showSubtask"]

        return ProblemSettingsRequestResponse(res)

    async def update_problem_settings(
            self, pid: str,
            new_settings: ProblemSettings,
    ) -> ProblemModifiedResponse:
        res = await self._send_request(
            endpoint=f"fe/api/problem/edit/{pid}",
            method="POST",
            data={
                "settings": new_settings.to_json(),
                "type": None,
                "providerID": new_settings.providerID,
                "comment": new_settings.comment
            }
        )

        return ProblemModifiedResponse(res)

    async def update_testcases_settings(
            self, pid: str,
            new_settings: TestCaseSettings
    ) -> UpdateTestCasesSettingsResponse:
        res = await self._send_request(
            endpoint=f"/fe/api/problem/editTestCase/{pid}",
            method="POST",
            data=new_settings.to_json()
        )

        return UpdateTestCasesSettingsResponse(res)

    async def create_problem(
            self, settings: ProblemSettings,
            tid : int | None = None,

    ) -> ProblemModifiedResponse:
        _type = "U" if tid is None else "T"
        res = await self._send_request(
            endpoint=f"fe/api/problem/new",
            method="POST",
            data={
                "settings": settings.to_json(),
                "type": _type,
                "providerID": tid,
                "comment": settings.comment
            }
        )

        return ProblemModifiedResponse(res)

    async def delete_problem(
            self, pid: str,
    ) -> bool:
        res = await self._send_request(
            endpoint=f"fe/api/problem/delete/{pid}",
            method="POST",
            data={}
        )

        return res["_empty"]

    async def transfer_problem(
            self, pid: str,
            target: TransferProblemType = "U",
            is_clone: bool = False
    ) -> ProblemModifiedResponse:
        if isinstance(target, int):
            data = {
                "type": "T",
                "teamID": target
            }
        else:
            data = {
                "type": target
            }
        
        if is_clone:
            data["operation"] = "clone"
            
        res = await self._send_request(
            endpoint=f"fe/api/problem/transfer/{pid}",
            method="POST",
            data=data
        )

        return ProblemModifiedResponse(res)

    async def download_testcases(
            self, pid: int
    ):
        raise NotImplementedError
    
    async def upload_testcases(
            self, pid: int,
            path: str
    ):
        raise NotImplementedError
    
    async def get_problem_set(self, id: int) -> ProblemSetDataRequestResponse:
        res = await self._send_request(endpoint=f"/training/{id}")
        res["training"]["problems"] = [x.get("problem") for x in res["training"]["problems"]]
        return ProblemSetDataRequestResponse(res)
    
    async def get_problem_set_list(
            self,
            page: int | None = None,
            keyword: str | None = None,
            type: ProblemSetType | None = None, 
            params: ProblemSetListRequestParams | None = None
    ):
        if params is None:
            params = ProblemSetListRequestParams(json={
                "page": page,
                "keyword": keyword,
                "type": type
            })
        res = await self._send_request(endpoint="training/list", params=params)
        res["trainings"]["trainings"] = res["trainings"]["result"]
        return ProblemSetListRequestResponse(res["trainings"])
    
    async def get_user(self, uid: int) -> UserDataRequestResponse:
        res = await self._send_request(endpoint=f"user/{uid}")
        return UserDataRequestResponse(res)

    async def get_user_info(self, uid: int) -> UserDetails:
        res = await self._send_request(endpoint=f"api/user/info/{uid}")
        return UserDetails(res["user"])
    
    async def get_user_following_list(self, uid: int, page: int | None = None) -> List[UserDetails]:
        params = UserListRequestParams(json={"user": uid, "page": page})
        res = await self._send_request(endpoint=f"api/user/followings", params=params)
        return [UserDetails(user) for user in res["users"]["result"]]

    async def get_user_follower_list(self, uid: int, page: int | None = None) -> List[UserDetails]:
        params = UserListRequestParams(json={"user": uid, "page": page})
        res = await self._send_request(endpoint=f"api/user/followers", params=params)
        return [UserDetails(user) for user in res["users"]["result"]]

    async def get_user_blacklist(self, uid: int, page: int | None = None) -> List[UserDetails]:
        params = UserListRequestParams(json={"user": uid, "page": page})
        res = await self._send_request(endpoint=f"api/user/blacklist", params=params)
        return [UserDetails(user) for user in res["users"]["result"]]
    
    async def search_user(self, keyword: str) -> List[UserSummary]:
        params = UserSearchRequestParams({"keyword" : keyword})
        res = await self._send_request(endpoint="api/user/search", params=params)
        return [UserSummary(user) for user in res["users"]]

    async def get_contest(self, id: int) -> ContestDataRequestResponse:
        res = await self._send_request(endpoint=f"contest/{id}")

        res["contest"]["problems"] = [x.get("problem") for x in res["contestProblems"]]
        res["contest"]["isScoreboardFrozen"] = res["isScoreboardFrozen"]
        return ContestDataRequestResponse(res)
    
    async def me(self) -> UserDetails:
        return (await self.get_user(self.cookies["_uid"].split("_")[0])).user

    async def get_created_problem_list(
            self, page: int | None = None
    ) -> ProblemListRequestResponse:
        params = ListRequestParams(json={"page": page})
        res = await self._send_request(endpoint="api/user/createdProblems", params=params)

        res["count"] = res["problems"]["count"]
        res["perPage"] = res["problems"]["perPage"]
        res["problems"] = res["problems"]["result"]

        return ProblemListRequestResponse(res)
    
    async def get_created_problem_set_list(self, page: int | None = None):
        params = ListRequestParams(json={"page": page})
        res = await self._send_request(endpoint="api/user/createdTrainings", params=params)

        res["trainings"]["trainings"] = res["trainings"]["result"]
        return ProblemSetListRequestResponse(res["trainings"])
    
    async def get_created_contest_list(self, page: int | None = None) -> ContestListRequestResponse:
        params = ListRequestParams(json={"page": page})
        res = await self._send_request(endpoint="api/user/createdContests", params=params)
        res["contests"]["contests"] = res["contests"]["result"]
        return ContestListRequestResponse(res["contests"])

    async def submit_code(
            self,
            pid: str,
            code: str,
            contest_id: int | None = None,
            lang: str | None = None,
            enableO2: bool = True,
            capture_handler: Callable[[bytes], str] | None = None
    ) -> SubmitCodeResponse:
        captcha_text = ""
        for attempt in range(self.max_retries):
            try:
                await self._get_csrf(f"/problem/{pid}")
                res = await self._send_request(
                    endpoint=f"/fe/api/problem/submit/{pid}",
                    params=ProblemRequestParams(json={"contest_id": contest_id}),
                    method="POST",
                    data={
                        "code": code,
                        "lang": lang,
                        "enableO2": enableO2,
                        "captcha": captcha_text
                    }
                )
                return SubmitCodeResponse(res)
            except NeedCaptcha as e:
                if capture_handler is None:
                    raise NeedCaptcha("Need captcha")
                logger.warning(f"({attempt}/{self.max_retries}) Raise User-defined captcha handler")
                captcha = await self._get_captcha()
                logger.debug(f"Captcha: {captcha}")
                captcha_text = capture_handler(captcha)
                await asyncio.sleep(5)
                continue
        raise RequestError("Failed to submit code after multiple attempts")
    
    async def submit_code_via_openluogu():
        raise NotImplementedError
    
    async def get_record(self, rid: str) -> RecordRequestResponse:
        res = await self._send_request(endpoint=f"record/{rid}")
        return RecordRequestResponse(res)
    
    async def get_tags(self) -> TagRequestResponse:
        res = await self._send_request(endpoint="/_lfe/tags")
        return TagRequestResponse(res)