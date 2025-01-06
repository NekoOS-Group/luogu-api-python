import json
import os
from time import sleep

import pyLuogu

cookies = pyLuogu.LuoguCookies.from_file("cookies.json")
luogu = pyLuogu.luoguAPI(cookies=cookies)

count = luogu.get_problem_list().count

for i in range(count):
    pid = f"P{i + 1000}"

    if os.path.exists(f"cache/{pid}.json"):
        print(f"{pid} exists")
        continue

    print(f"fetching {pid}...")

    res = luogu.get_problem_settings(pid)
    f = open(f"cache/{pid}.json", "w")
    f.write(json.dumps(res.to_json()))
    f.close()

    sleep(2)
