import asyncio
import pyLuogu

# Initialize the async API without cookies
luogu = pyLuogu.asyncLuoguAPI()

async def main():
    problems = (await luogu.get_problem_list()).problems
    for problem in problems:
        print(problem.title)

asyncio.run(main())