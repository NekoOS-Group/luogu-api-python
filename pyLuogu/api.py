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
            except requests.ConnectTimeout:
                continue
        else:
            raise requests.ConnectTimeout

        ret = response.json()
        if ret.get("currentData") is None:
            return ret

        return ret["currentData"]

    def _get_csrf(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.",
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

    def get_problem_list(
            self,
            page: int = None,
            orderBy: int = None,
            keyword: str = None,
            content: bool = None,
            _type: str = None,
            difficulty: int = None,
            tag: str = None,
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
    ):
        params = ListRequestParams(json={"page": page})
        res = self._send_request(endpoint="api/user/createdProblems", params=params)

        res["count"] = res["problems"]["count"]
        res["perPage"] = res["problems"]["perPage"]
        res["problems"] = res["problems"]["result"]

        return ProblemListRequestResponse(res)

    def get_problem(
            self, pid: str,
            contest_id: int | None = None
    ) -> ProblemData:
        params = ProblemRequestParams(json={"contest_id": contest_id})
        res = self._send_request(endpoint=f"problem/{pid}", params=params)

        return ProblemData(res)

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
            _type: str = None
    ) -> ProblemModifiedResponse:
        res = self._send_request(
            endpoint=f"fe/api/problem/edit/{pid}",
            method="POST",
            data={
                "settings": new_settings.to_json(),
                "type": _type,
                "providerID": new_settings.providerID,
                "comment": new_settings.comment
            }
        )

        return ProblemModifiedResponse(res)

    def create_problem(
            self, setting: ProblemSettings,
            _type: str = "U",
    ) -> ProblemModifiedResponse:
        res = self._send_request(
            endpoint=f"fe/api/problem/new",
            method="POST",
            data={
                "settings": setting.to_json(),
                "type": _type,
                "providerID": setting.providerID,
                "comment": setting.comment
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

    def update_testcases_settings(
            self, new_settings: TestCaseSettings
    ) -> UpdateTestCasesSettingsResponse:
        raise NotImplementedError
