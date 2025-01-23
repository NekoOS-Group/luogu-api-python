import pyLuogu

cookies = pyLuogu.LuoguCookies.from_file("cookies.json")
luogu = pyLuogu.luoguAPI(cookies=cookies)

settings = pyLuogu.ProblemSettings.get_default()
settings.title = "Test"

tid = 0 # please replace this with a valid tid
pid = luogu.create_problem(settings=settings, tid=tid).pid
print(f"Problem created: {pid}")

new_pid = luogu.transfer_problem(pid, "U").pid

print(f"{pid} tansfer to {new_pid}")

pid = luogu.transfer_problem(new_pid, target=tid).pid
print(f"{new_pid} tansfer to {pid}")

luogu.delete_problem(pid)
print(f"Problem deleted: {pid}")
