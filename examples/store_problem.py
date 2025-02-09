import os
from time import sleep

import pyLuogu

pyLuogu.set_log_level("INFO")

cookies = pyLuogu.LuoguCookies.from_file("cookies.json")
luogu = pyLuogu.luoguAPI(cookies=cookies)

types = ["P", "CF", "AT", "SP"]

for _type in types:
    res = luogu.get_problem_list(_type=_type)
    pages = (res.count - 1) // res.perPage + 1

    for page in range(pages):
        problem_list = luogu.get_problem_list(_type=_type, page=page + 1)

        for problem in problem_list.problems:
            pid = problem.pid

            if os.path.exists(f".cache/{pid}.json"):
                continue

            print(f"fetching {pid}...")
            try:
                res = luogu.get_problem_settings(pid)
            except KeyError:
                print(f"{pid} does not exist")
                continue

            res.problemSettings.store(f".cache/{pid}.json")
