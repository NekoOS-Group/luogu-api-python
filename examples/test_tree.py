import pyLuogu

cookies = pyLuogu.LuoguCookies.from_file("cookies.json")
luogu = pyLuogu.luoguAPI(cookies=cookies)

res = luogu.get_problem_list(tag="1", difficulty=7)
print(res)

res = luogu.get_problem_settings(pid=res.problems[0].pid)
print(res.problemSettings)
