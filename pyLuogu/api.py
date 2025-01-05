from .types import *

import requests


class luoguAPI:
    def __init__(
            self,
            base_url="https://www.luogu.com.cn",
            cookies: LuoguCookies = None
    ):
        self.base_url = base_url
        self.cookies = cookies
        self.session = requests.Session()

    def _send_request(
            self,
            endpoint: str,
            method: str = "GET",
            params: RequestParams | None = None,
            data=None
    ):
        url = f"{self.base_url}/{endpoint}"
        header = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.",
            "x-luogu-type": "content-only"
        }
        param_final = None if params is None else params.to_json()
        cookies_final = None if self.cookies is None else self.cookies.to_json()

        response = self.session.request(
            method, url,
            headers=header,
            params=param_final,
            data=data,
            cookies=cookies_final,

        )

        return response.json()["currentData"]

    def get_problem_list(
            self, params: ProblemListRequestParams | None
    ) -> ProblemListRequestResponse:
        res = self._send_request(endpoint="problem/list", params=params)

        res["count"] = res["problems"]["count"]
        res["perPage"] = res["problems"]["perPage"]
        res["problems"] = res["problems"]["result"]

        return ProblemListRequestResponse(res)

    def get_problem(
            self, pid: str,
            contest_id: int | None = None
    ) -> ProblemData:
        params = ProblemRequestParams(contest_id=contest_id)
        res = self._send_request(endpoint=f"problem/{pid}", params=params)

        return ProblemData(res)

    def get_problem_setting(
            self, pid: str,
    ) -> ProblemSettings:
        res = self._send_request(endpoint=f"problem/edit/{pid}")

        return ProblemSettings(res["setting"])
