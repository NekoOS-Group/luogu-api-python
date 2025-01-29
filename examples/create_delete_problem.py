import pyLuogu
from pyLuogu import ProblemSettings

cookies = pyLuogu.LuoguCookies.from_file("cookies.json")
luogu = pyLuogu.luoguAPI(cookies=cookies)

res = luogu.get_created_problem_list()
print(f"The number of your created problem : {res.count}")

settings = ProblemSettings.get_default()
settings.title = "Neko Cx`xooperation"

res = luogu.create_problem(settings=settings)
pid = res.pid
print(f"You create a new problem with pid : {pid}")

problem = luogu.get_problem(pid).problem
assert problem.title == "Neko Cooperation"

res = luogu.get_created_problem_list()
print(f"The number of your created problem after luogu.create_problem: {res.count}")

success = luogu.delete_problem(pid)
if not success:
    print("Deletion failed")
    exit()

print(f"You delete the new problem: {pid}")

res = luogu.get_created_problem_list()
print(f"The number of your created problem after luogu.delete_problem: {res.count}")
