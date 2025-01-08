# luogu-api-python
a python implement of luogu API

upstream docs: [https://github.com/sjx233/luogu-api-docs](https://github.com/sjx233/luogu-api-docs)

## Get Start

You can get it by run following command in shell:

```commandline
$ git clone https://github.com/bzy-nya/luogu-api-python.git
$ cd luogu-api-python
$ python setup.py install
```

## Example 

```python
### create a new problem with pyLuogu
import pyLuogu

title = "Neko Cooperation"
cookies = pyLuogu.LuoguCookies.from_file("cookies.json")
luogu = pyLuogu.luoguAPI(cookies=cookies)

settings = pyLuogu.ProblemSettings.get_default()
settings.title = title

pid = luogu.create_problem(settings=settings).pid
print(f"You create a new problem with pid : {pid}")

problem = luogu.get_problem(pid).problem
assert problem.title == title
```

## Todo list

Methods of class `LuoguAPI`

 - [x] Problem
   - [x] get_problem_list
   - [x] get_created_problem_list
   - [ ] get_team_problem_list 
   - [x] get_problem
   - [x] get_problem_settings
   - [x] update_problem_settings
   - [ ] update_testcases_settings
   - [x] create_problem
   - [x] delete_problem
   - [ ] transfer_problem
   - [ ] download_testcases
   - [ ] upload_testcases
 - [x] UserOperation
   - [ ] login
   - [ ] logout
   - [ ] me