import re
import json
import time
from typing import List, Literal

import httpx
import bs4

from .types import *
from .errors import *
from . import logger

__COMMON_UA = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133."

class luoguAPI:
    """ Luogu API interface interacting via Requests

    Attributes:
        base_url (str): The base URL for the Luogu API. Defaults to "https://www.luogu.com.cn".
        cookies (LuoguCookies or None)

    """
    def __init__(
            self,
            base_url="https://www.luogu.com.cn",
            cookies: LuoguCookies = None,
            timeout: float | httpx.Timeout | None = 10,
            max_retries: int = 5
    ):
        self.base_url = base_url
        self.cookies = None if cookies is None else cookies.to_json()
        self.max_retries = max_retries
        self.client = httpx.Client(
            timeout=timeout,
            cookies=self.cookies,
            follow_redirects=True,
        )
        self.x_csrf_token = None
        self.x_csrf_token = None

    def _send_request(
            self,
            endpoint: str,
            method: str = "GET",
            params: RequestParams | None = None,
            data: dict | None = None
    ):
        url = f"{self.base_url}/{endpoint}"
        headers = self._get_headers(method)
        param_final = None if params is None else params.to_json()

        request = self.client.build_request(
            method, url,
            headers=headers,
            params=param_final,
            json=data,
        )

        if method == "GET":
            logger.info(f"GET from {url} with params: {param_final}")
        else:
            data_str = json.dumps(data)
            payload_str = data_str if data and len(data_str) < 50 else data_str[:50] + "..."
            logger.info(f"POST to {url} with payload: {payload_str}")

        for attempt in range(self.max_retries):
            try:
                response = self.client.send(request)
            except httpx.TimeoutException as e:
                logger.warning(f"Attempt {attempt + 1}: Timeout error - {e}")
                time.sleep(1)
                continue
            except httpx.HTTPError as e:
                logger.error(f"Request error: {e}")
                raise RequestError("Request error") from e

            try:
                response.raise_for_status()
                try:
                    res_json = response.json()
                except json.JSONDecodeError:
                    logger.error(f"Failed to decode JSON response: {response.text}")
                    raise RequestError("Failed to decode JSON response") from None
                logger.debug(f"{json.dumps(res_json)}")

                if res_json.get("currentTemplate") == "AuthLogin":
                    raise AuthenticationError("Need Login")
                if res_json.get("code") == 403:
                    if res_json.get("errorMessage") == "user.not_self":
                        raise AuthenticationError("not yourself")
                    error_message = res_json.get("currentData").get("errorMessage")
                    raise ForbiddenError( error_message or "Forbidden" )
                
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
                    print(res_json.get("errorMessage"))
                    if res_json.get("请求频繁，请稍候再试"):
                        time.sleep(5)
                        continue
                    if res_json.get("errorMessage") == "user.not_self":
                        raise AuthenticationError("not yourself")
                    logger.warning("CSRF token expired, refreshing token...")
                    self._get_csrf()
                    headers = self._get_headers(method)  # Refresh headers with new CSRF token
                    continue  # Retry the request
                elif response.status_code == 404:
                    raise NotFoundError("Resource not found") from e
                elif response.status_code == 429:
                    raise RateLimitError("Rate limit exceeded") from e
                elif 500 <= response.status_code < 600:
                    raise ServerError("Server error") from e
                else:
                    raise RequestError(f"HTTP error: {e}", status_code=response.status_code) from e
        else:
            logger.error("Failed to send request after 5 attempts")
            raise RequestError("Failed to send request after 5 attempts")

    def _get_headers(self, method: str) -> dict:
        headers = {
            "User-Agent": "luogu_bot",
            "x-luogu-type": "content-only",
            "x-lentille-request": "content-only",
        }
        if method != "GET":
            if not self.x_csrf_token:
                self._get_csrf()
            headers.update({
                "Content-Type": "application/json",
                "referer": "https://www.luogu.com.cn/",
                "x-csrf-token": self.x_csrf_token
            })
        return headers

    def _get_csrf(self, endpoint="") -> str:
        headers = {
            "User-Agent": "luogu_bot",
        }

        for attempt in range(self.max_retries):
            try:
                response = self.client.get(
                    self.base_url + endpoint, 
                    headers=headers, 
                    cookies=self.cookies
                )
                
                response.raise_for_status()

                result = re.search(r"C3VK=(.*);", response.text)
                if result:
                    self.cookies["C3VK"] = result.group(1)
                    logger.debug("C3VK token fetched successfully")
                    continue

                soup = bs4.BeautifulSoup(response.text, "html.parser")
                csrf_meta = soup.select_one("meta[name='csrf-token']")

                if csrf_meta and "content" in csrf_meta.attrs:
                    self.x_csrf_token = csrf_meta["content"]
                    logger.info("CSRF token fetched successfully")
                    return self.x_csrf_token
                else:
                    logger.warning("CSRF token not found, retrying...")
                    time.sleep(1)
            except httpx.TimeoutException as e:
                logger.warning(f"Attempt {attempt + 1}: Timeout error - {e}")
                time.sleep(1)
            except httpx.HTTPError as e:
                logger.error(f"HTTP error: {e}")
                raise RequestError("HTTP error") from e

        logger.error("Failed to fetch CSRF token after 5 attempts")
        raise RequestError("Failed to fetch CSRF token after 5 attempts")

    def login(
            self, user_name: str, password: str,
            captcha: Literal["input", "ocr"],
            two_step_verify: Literal["google", "email"] | None = None
    ) -> bool:
        raise NotImplementedError

    def logout(self):
        raise NotImplementedError

    def get_problem_list(
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
        res = self._send_request(endpoint="problem/list", params=params)

        res["count"] = res["problems"]["count"]
        res["perPage"] = res["problems"]["perPage"]
        res["problems"] = res["problems"]["result"]

        return ProblemListRequestResponse(res)

    def get_problem(
            self, pid: str,
            contest_id: int | None = None
    ) -> ProblemDataRequestResponse:
        params = ProblemRequestParams(json={"contest_id": contest_id})
        res = self._send_request(endpoint=f"problem/{pid}", params=params)

        res["problem"]["limits"] = list(zip(
            res["problem"]["limits"]["time"], res["problem"]["limits"]["memory"]
        ) )

        return ProblemDataRequestResponse(res)

    def get_problem_settings_legacy(
            self, pid: str,
    ) -> ProblemSettingsRequestResponse:
        res = self._send_request(endpoint=f"problem/edit/{pid}")
        
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

    def get_problem_settings(self, pid: str):
        res = self._send_request(endpoint=f"problem/{pid}/edit")
        
        return res

    def update_problem_settings(
            self, pid: str,
            new_settings: ProblemSettings,
    ) -> ProblemModifiedResponse:
        res = self._send_request(
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

    def update_testcases_settings(
            self, pid: str,
            new_settings: TestCaseSettings
    ) -> UpdateTestCasesSettingsResponse:
        res = self._send_request(
            endpoint=f"/fe/api/problem/editTestCase/{pid}",
            method="POST",
            data=new_settings.to_json()
        )

        return UpdateTestCasesSettingsResponse(res)

    def create_problem(
            self, settings: ProblemSettings,
            tid : int | None = None,

    ) -> ProblemModifiedResponse:
        _type = "U" if tid is None else "T"
        res = self._send_request(
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

    def delete_problem(
            self, pid: str,
    ) -> bool:
        res = self._send_request(
            endpoint=f"fe/api/problem/delete/{pid}",
            method="POST",
            data={}
        )

        return res["_empty"]

    def transfer_problem(
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
            
        res = self._send_request(
            endpoint=f"fe/api/problem/transfer/{pid}",
            method="POST",
            data=data
        )

        return ProblemModifiedResponse(res)

    def download_testcases(
            self, pid: int
    ):
        raise NotImplementedError
    
    def upload_testcases(
            self, pid: int,
            path: str
    ):
        raise NotImplementedError

    def get_problem_solutions(self, pid: str, page: int | None = None) -> ProblemSolutionRequestResponse:
        params = ListRequestParams(json={"page": page})
        res = self._send_request(endpoint=f"problem/solution/{pid}", params=params)

        res["count"] = res["solutions"]["count"]
        res["perPage"] = res["solutions"]["perPage"]
        res["solutions"] = res["solutions"]["result"]

        return ProblemSolutionRequestResponse(res)

    def get_user(self, uid: int) -> UserDataRequestResponse:
        res = self._send_request(endpoint=f"user/{uid}")
        
        if res.get("teams") is not None:
            res["teams"] = [x.get("team") for x in res["teams"]]
        res["user"]["eloMax"] = res["eloMax"]

        return UserDataRequestResponse(res)

    def get_user_info(self, uid: int) -> UserDetails:
        res = self._send_request(endpoint=f"api/user/info/{uid}")

        return UserDetails(res["user"])
    
    def get_user_following_list(self, uid: int, page: int | None = None) -> List[UserDetails]:
        params = UserListRequestParams(json={"user": uid, "page": page})
        res = self._send_request(endpoint=f"api/user/followings", params=params)
        return [UserDetails(user) for user in res["users"]["result"]]

    def get_user_follower_list(self, uid: int, page: int | None = None) -> List[UserDetails]:
        params = UserListRequestParams(json={"user": uid, "page": page})
        res = self._send_request(endpoint=f"api/user/followers", params=params)
        return [UserDetails(user) for user in res["users"]["result"]]

    def get_user_blacklist(self, uid: int, page: int | None = None) -> List[UserDetails]:
        params = UserListRequestParams(json={"user": uid, "page": page})
        res = self._send_request(endpoint=f"api/user/blacklist", params=params)
        return [UserDetails(user) for user in res["users"]["result"]]
    
    def search_user(self, keyword: str) -> List[UserSummary]:
        params = UserSearchRequestParams({"keyword" : keyword})
        
        res = self._send_request(endpoint="api/user/search", params=params)
        return [UserSummary(user) for user in res["users"]]

    def me(self) -> UserDetails:
        return self.get_user(self.cookies["_uid"].split("_")[0]).user

    def get_problem_set(self, id: int) -> ProblemSetDataRequestResponse:
        res = self._send_request(endpoint=f"/training/{id}")
        res["training"]["problems"] = [x.get("problem") for x in res["training"]["problems"]]
        return ProblemSetDataRequestResponse(res)
    
    def get_problem_set_list(
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
        res = self._send_request(endpoint="training/list", params=params)
        res["trainings"]["trainings"] = res["trainings"]["result"]
        return ProblemSetListRequestResponse(res["trainings"])
    
    def get_contest(self, id: int) -> ContestDataRequestResponse:
        res = self._send_request(endpoint=f"contest/{id}")

        res["contest"]["problems"] = [x.get("problem") for x in res["contestProblems"]]
        res["contest"]["isScoreboardFrozen"] = res["isScoreboardFrozen"]
        return ContestDataRequestResponse(res)
    
    def get_contest_list(self, page: int | None = None):
        params = ListRequestParams(json={"page": page})
        res = self._send_request(endpoint="contest/list", params=params)
        res["contests"]["contests"] = res["contests"]["result"]
        return ContestListRequestResponse(res["contests"])
            
    def get_disscussion(self,
            id: int,
            page: int | None = None,
            orderBy: int | None = None,
    ) -> DiscussionRequestResponse:
        params = DiscussionRequestParams(json={"page": page, "orderBy": orderBy})
        res = self._send_request(endpoint=f"discuss/{id}", params=params)

        res["perPage"] = res["replies"]["perPage"]
        res["count"] = res["replies"]["count"]
        res["replies"] = res["replies"]["result"]
        return DiscussionRequestResponse(res)     
    
    def get_activity(self, 
            uid: int, 
            page: int | None = None
    ) -> ActivityRequestResponse:
        params = ActivityReuqestParams(json={"user": uid, "page": page})
        res = self._send_request(endpoint=f"/api/feed/list", params=params)

        res["activities"] = res["feeds"]["result"]
        res["perPage"] = res["feeds"]["perPage"]
        res["count"] = res["feeds"]["count"]
        return ActivityRequestResponse(res)

    def get_team(self, tid: int) -> TeamDataRequestResponse:
        res = self._send_request(endpoint=f"team/{tid}")
        return TeamDataRequestResponse(res)

    def get_team_member_list(self, tid: int) -> List[TeamMember]:
        res = self._send_request(endpoint=f"api/team/members/{tid}")
        res["perPage"] = res["members"]["perPage"]
        res["count"] = res["members"]["count"]
        res["members"] = res["members"]["result"]

        return TeamMemberRequestResponse(res)

    def get_team_problem_list(
            self, tid: int,
            page: int | None = None
    ) -> ProblemListRequestResponse:
        params = ListRequestParams(json={"page": page})
        res = self._send_request(
            endpoint=f"api/team/problems/{tid}", 
            params=params
        )

        res["count"] = res["problems"]["count"]
        res["perPage"] = res["problems"]["perPage"]
        res["problems"] = res["problems"]["result"]

        return ProblemListRequestResponse(res)

    def get_team_problem_set_list(self, tid: int, page: int | None = None) -> ProblemSetListRequestResponse:
        params = ListRequestParams(json={"page": page})
        res = self._send_request(endpoint=f"api/team/trainings/{tid}", params=params)
        res["trainings"]["trainings"] = res["trainings"]["result"]
        return ProblemSetListRequestResponse(res["trainings"])
    
    def get_team_contest_list(self, tid: int, page: int | None = None) -> ContestListRequestResponse:
        params = ListRequestParams(json={"page": page})
        res = self._send_request(endpoint=f"api/team/contests/{tid}", params=params)
        res["contests"]["contests"] = res["contests"]["result"]
        return ContestListRequestResponse(res["contests"])

    def get_paste(self, id: str) -> PasteRequestResponse:
        res = self._send_request(endpoint=f"paste/{id}")
        return PasteRequestResponse(res)

    def get_record(self, rid: str) -> RecordRequestResponse:
        res = self._send_request(endpoint=f"record/{rid}")
        return RecordRequestResponse(res)
    
    def get_article(self, lid: str) -> ArticleDataRequestResponse:
        res = self._send_request(endpoint=f"article/{lid}")
        return ArticleDataRequestResponse(res)
    
    def get_created_problem_list(
            self, page: int | None = None
    ) -> ProblemListRequestResponse:
        params = ListRequestParams(json={"page": page})
        res = self._send_request(endpoint="api/user/createdProblems", params=params)

        res["count"] = res["problems"]["count"]
        res["perPage"] = res["problems"]["perPage"]
        res["problems"] = res["problems"]["result"]

        return ProblemListRequestResponse(res)

    def get_created_problem_set_list(self, page: int | None = None):
        params = ListRequestParams(json={"page": page})
        res = self._send_request(endpoint="api/user/createdTrainings", params=params)

        res["trainings"]["trainings"] = res["trainings"]["result"]
        return ProblemSetListRequestResponse(res["trainings"])
    
    def get_created_contest_list(self, page: int | None = None) -> ContestListRequestResponse:
        params = ListRequestParams(json={"page": page})
        res = self._send_request(endpoint="api/user/createdContests", params=params)
        res["contests"]["contests"] = res["contests"]["result"]
        return ContestListRequestResponse(res["contests"])

    def submit_code(
            self,
            pid: str,
            code: str,
            contest_id: int | None = None,
            lang: str | None = None,
            enableO2: bool = True,
    ) -> SubmitCodeResponse:
        self._get_csrf(f"/problem/{pid}")
        res = self._send_request(
            endpoint=f"/fe/api/problem/submit/{pid}",
            params=ProblemRequestParams(json={"contest_id": contest_id}),
            method="POST",
            data={
                "code": code,
                "lang": lang,
                "enableO2": enableO2
            }
        )
        return SubmitCodeResponse(res)
    
    def submit_code_via_openluogu():
        raise NotImplementedError
    
    def get_tags(self) -> TagRequestResponse:
        res = self._send_request(endpoint="/_lfe/tags")
        return TagRequestResponse(res)

    def get_image(self, id: int) -> Image:
        res = self._send_request(endpoint=f"/api/image/detail/{id}")
        return Image(res["image"])
