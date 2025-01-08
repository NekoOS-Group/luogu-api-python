import json
import os
from time import sleep

import pyLuogu

cookies = pyLuogu.LuoguCookies.from_file("cookies.json")
luogu = pyLuogu.luoguAPI(cookies=cookies)

count = luogu.get_problem_list(_type="P").count

for i in range(count):
    pid = f"P{i + 1000}"

    if os.path.exists(f"cache/{pid}.json"):
        continue

    print(f"fetching {pid}...")
    try:
        res = luogu.get_problem_settings(pid)
    except KeyError:
        print(f"{pid} does not exist")
        count += 1
        continue

    res.problemSettings.store(f"cache/{pid}.json")
    sleep(1)

res = luogu.get_problem_list(_type="SP")
pages = (res.count - 1) // res.perPage + 1

for page in range(pages):
    problem_list = luogu.get_problem_list(_type="SP", page=page + 1)

    for problem in problem_list.problems:
        pid = problem.pid

        if os.path.exists(f"cache/{pid}.json"):
            continue

        print(f"fetching {pid}...")
        try:
            res = luogu.get_problem_settings(pid)
        except KeyError:
            print(f"{pid} does not exist")
            continue

        res.problemSettings.store(f"cache/{pid}.json")
        sleep(1)
