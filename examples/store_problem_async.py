import asyncio
import os

import pyLuogu

cookies = pyLuogu.LuoguCookies.from_file("cookies.json")
luogu = pyLuogu.asyncLuoguAPI(cookies=cookies)

pyLuogu.set_log_level("INFO")

types = ["P", "CF", "AT", "SP"]
queue = asyncio.Queue()
producer_count = len(types)
consumer_count = 10
quit_count = 0
quit_lock = asyncio.Lock()

async def producer(id: int, _type: str):
    global quit_count
    print(f"Producer {id} started for type {_type}")
    meta = await luogu.get_problem_list(_type=_type)
    page_count = (meta.count - 1) // meta.perPage + 1
    for page in range(page_count):
        problem_list = await luogu.get_problem_list(_type=_type, page=page + 1)
        for problem in problem_list.problems:
            cache_path = f".cache/{problem.pid}.json"
            if os.path.exists(cache_path):
                continue
            await queue.put(problem.pid)
    async with quit_lock:
        quit_count += 1
        if quit_count == producer_count:
            for _ in range(consumer_count):
                await queue.put(None)
    print(f"Producer {id} finished for type {_type}")

async def consumer(id: int):
    print(f"Consumer {id} started")
    while True:
        pid = await queue.get()
        if pid is None:
            queue.task_done()
            break
        cache_path = f".cache/{pid}.json"
        print(f"Consumer {id} fetching {pid}...")
        res = await luogu.get_problem_settings(pid)
        res.problemSettings.store(cache_path)
        queue.task_done()
    print(f"Consumer {id} finished")

async def main():
    async with luogu:
        producers = [asyncio.create_task(producer(i + 1, _type)) for i, _type in enumerate(types)]
        consumers = [asyncio.create_task(consumer(i + 1)) for i in range(consumer_count)]
        
        # Wait for all tasks to complete
        await asyncio.gather(*producers, *consumers)

if __name__ == "__main__":
    asyncio.run(main())
    print("All coroutines are done")
