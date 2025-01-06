from time import sleep

import pyLuogu

cookies = pyLuogu.LuoguCookies.from_file("cookies.json")
luogu = pyLuogu.luoguAPI(cookies=cookies)

# 将所有含有 状态压缩的题目标签改为 状压 DP
while True:
    res = luogu.get_problem_list(tag="151")
    if res.count == 0:
        break

    for problem in res.problems:
        print(f"handling {problem.inline()}")
        res = luogu.get_problem_settings(problem.pid)
        settings = res.problemSettings

        if settings.tags.count(151) > 0:
            settings.tags.remove(151)
            settings.tags.append(464)
        else:
            continue

        res = luogu.update_problem_settings(problem.pid, settings)
        if res.pid == problem.pid:
            print(f"Tags of problem {problem.pid} changed successfully")
        else:
            print(f"Failed")

        sleep(2)
