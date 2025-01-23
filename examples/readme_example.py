import pyLuogu

# Initialize the API without cookies
luogu = pyLuogu.luoguAPI()

# Get a list of problems
problems = luogu.get_problem_list().problems
for problem in problems:
    print(problem.title)
