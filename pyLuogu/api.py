import json
from time import sleep

import requests
from bs4 import BeautifulSoup

from .types import *


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
        if method == "GET":
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.",
                "x-luogu-type": "content-only",
            }
        else:
            self._get_csrf()
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.",
                "x-luogu-type": "content-only",
                "Content-Type": "application/json",
                "referer": "https://www.luogu.com.cn/",
                "x-csrf-token": self.x_csrf_token
            }

        param_final = None if params is None else params.to_json()
        data_final = None if data is None else json.dumps(data)

        for _ in range(5):
            try:
                response = self.session.request(
                    method, url,
                    headers=headers,
                    params=param_final,
                    data=data_final,
                    cookies=self.cookies,
                    timeout=5
                )

                response.raise_for_status()
                break
            except (requests.ConnectTimeout, requests.exceptions.ReadTimeout):
                continue
        else:
            raise requests.ConnectTimeout

        ret = response.json()
        if ret.get("currentData") is None:
            return ret

        return ret["currentData"]

    def _get_csrf(self):
        self.get_problem("P1001")
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.",
            "x-luogu-type": "content-only",
            "Content-Type": "text/html"
        }
        response = self.session.get(self.base_url, headers=headers, cookies=self.cookies)
        response.raise_for_status()  # 确保请求成功

        soup = BeautifulSoup(response.text, "html.parser")
        csrf_meta = soup.select_one("meta[name='csrf-token']")

        if csrf_meta and "content" in csrf_meta.attrs:
            self.x_csrf_token = csrf_meta["content"]
        else:
            sleep(5)
            self._get_csrf()

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
        raise NotImplementedError

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

        # print(json.dumps(res))

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
        raise NotImplementedError

    def create_problem(
            self, settings: ProblemSettings,
            _type: ProblemType | None = "U",
    ) -> ProblemModifiedResponse:
        res = self._send_request(
            endpoint=f"fe/api/problem/new",
            method="POST",
            data={
                "settings": settings.to_json(),
                "type": _type,
                "providerID": settings.providerID,
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
            target: ProblemType,
            target_team_ID: int | None = None,
            is_clone: bool = False
    ) -> ProblemModifiedResponse:
        raise NotImplementedError

    def download_testcases(
            self, pid: int
    ):
        raise NotImplementedError
    
    def upload_testcases(
            self, pid: int,
            path: str
    ):
        raise NotImplementedError
        
    def get_user(self, uid: int):
        raise NotImplementedError

    def me(self):
        raise NotImplementedError
