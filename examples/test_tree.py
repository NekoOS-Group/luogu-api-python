import json

import pyLuogu

cookies = pyLuogu.LuoguCookies.from_file("cookies.json")
luogu = pyLuogu.luoguAPI(cookies=cookies)

param = pyLuogu.ProblemListRequestParams(tag="1", difficulty=7)
print(param)

res = luogu.get_problem_list(params=param)
print(res)

res = luogu.get_problem_setting(pid=res.problems[0].pid)

print(res)
