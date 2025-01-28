import json
import time
     
import requests
import bs4

from .types import *
from .errors import *
from . import logger

class luoguAPI:
    def __init__(
            self,
            base_url="https://www.luogu.com.cn",
            cookies: LuoguCookies = None
    ):
        self.base_url = base_url
        self.cookies = None if cookies is None else cookies.to_json()
        self.session = requests.Session()
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
        data_final = None if data is None else json.dumps(data)

        if method == "GET":
            logger.info(f"GET from {url} with params: {param_final}")
        else:
            payload_str = data_final if len(data_final) < 50 else f"{data_final[:50]}..."
            logger.info(f"POST to {url} with payload: {payload_str}")

        def _parse_response(_response: requests.Response) -> dict:
            try:
                ret = _response.json()
                if ret.get("currentData") is None:
                    return ret
                return ret["currentData"]
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error: {e}")
                raise

        for attempt in range(5):
            try:
                response = self.session.request(
                    method, url,
                    headers=headers,
                    params=param_final,
                    data=data_final,
                    cookies=self.cookies,
                    timeout=5
                )
            except (requests.ConnectTimeout, requests.exceptions.ReadTimeout) as e:
                logger.warning(f"Attempt {attempt + 1}: Timeout error - {e}")
                time.sleep(1)
                continue
            except requests.RequestException as e:
                logger.error(f"Request error: {e}")
                raise RequestError("Request error") from e
            except:
                raise RequestError("Request error")

            try:
                logger.debug(f"{json.dumps(response.json())}")

                response.raise_for_status()

                if response.json().get("currentTemplate") == "AuthLogin":
                    raise AuthenticationError("Need Login")
                
                if response.json().get("code") == 403:
                    error_message = response.json().get("currentData").get("errorMessage")
                    raise ForbiddenError( error_message or "Forbidden" )
                
                if response.json().get("code") in [404, 418]:
                    raise NotFoundError(f"Resource not found {endpoint}")

                return _parse_response(response)
            except requests.HTTPError as e:
                if response.status_code == 401:
                    raise AuthenticationError("Authentication failed") from e
                elif response.status_code == 403:
                    print(response.json().get("errorMessage"))
                    if response.json().get("请求频繁，请稍候再试"):
                        time.sleep(5)
                        continue
                    if response.json().get("errorMessage") == "user.not_self":
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
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.",
            "x-luogu-type": "content-only",
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

    def _get_csrf(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.",
            "x-luogu-type": "content-only",
            "Content-Type": "text/html"
        }

        for attempt in range(5):
            try:
                response = self.session.get(self.base_url, headers=headers, cookies=self.cookies)
                response.raise_for_status()
                
                soup = bs4.BeautifulSoup(response.text, "html.parser")
                csrf_meta = soup.select_one("meta[name='csrf-token']")

                if csrf_meta and "content" in csrf_meta.attrs:
                    self.x_csrf_token = csrf_meta["content"]
                    logger.info("CSRF token fetched successfully")
                    return
                else:
                    logger.warning("CSRF token not found, retrying...")
                    self.get_problem(pid="P1000") # refresh the session
                    time.sleep(1)
            except (requests.ConnectTimeout, requests.exceptions.ReadTimeout) as e:
                logger.warning(f"Attempt {attempt + 1}: Timeout error - {e}")
                time.sleep(1)
            except requests.HTTPError as e:
                logger.error(f"HTTP error: {e}")
                raise
            except requests.RequestException as e:
                logger.error(f"Request error: {e}")
                raise

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

    def get_created_problem_list(
            self, page: int | None = None
    ) -> ProblemListRequestResponse:
        params = ListRequestParams(json={"page": page})
        res = self._send_request(endpoint="api/user/createdProblems", params=params)

        res["count"] = res["problems"]["count"]
        res["perPage"] = res["problems"]["perPage"]
        res["problems"] = res["problems"]["result"]

        return ProblemListRequestResponse(res)

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

    def get_problem(
            self, pid: str,
            contest_id: int | None = None
    ) -> ProblemDataRequestResponse:
        params = ProblemRequestParams(json={"contest_id": contest_id})
        res = self._send_request(endpoint=f"problem/{pid}", params=params)

        return ProblemDataRequestResponse(res)

    def get_problem_settings(
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
        
    def get_user(self, uid: int) -> UserDataRequestResponse:
        res = self._send_request(endpoint=f"user/{uid}")

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

    def get_tags(self) -> TagRequestResponse:
        res = self._send_request(endpoint="/_lfe/tags")
        return TagRequestResponse(res)
