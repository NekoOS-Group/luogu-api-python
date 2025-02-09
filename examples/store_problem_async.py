import asyncio
import os

import pyLuogu

target_path = ".cache/problem"

cookies = pyLuogu.LuoguCookies.from_file("cookies.json")
luogu = pyLuogu.asyncLuoguAPI(cookies=cookies)

pyLuogu.set_log_level("INFO")

types = ["P", "CF", "AT", "SP"]
queue_clock = asyncio.Semaphore
queue_meta = asyncio.Queue()
queue = asyncio.Queue()
producer_count = 20
consumer_count = 20
quit_count = 0
quit_lock = asyncio.Lock()

async def meta_producer():
    print(f"Meta producer started")
    for _type in types:
        meta = await luogu.get_problem_list(_type=_type)
        page_count = (meta.count - 1) // meta.perPage + 1
        for i in range(page_count):
            await queue_meta.put((_type, i + 1))
    for _ in range(producer_count):
        await queue_meta.put(None)
    print(f"Meta producer finished")

async def producer(id: int):
    global quit_count
    print(f"Producer {id} started")
    while True:
        meta = await queue_meta.get()
        if meta is None:
            queue_meta.task_done()
            break
        (_type, page) = meta
        problem_list = await luogu.get_problem_list(_type=_type, page=page + 1)
        for problem in problem_list.problems:
            cache_path = f"{target_path}/{problem.pid}.json"
            if os.path.exists(cache_path):
                continue
            await queue.put(problem.pid)
        queue_meta.task_done()

    async with quit_lock:
        quit_count += 1
        if quit_count == producer_count:
            for _ in range(consumer_count):
                await queue.put(None)
    print(f"Producer {id} finished")

async def consumer(id: int):
    print(f"Consumer {id} started")
    while True:
        pid = await queue.get()
        if pid is None:
            queue.task_done()
            break
        cache_path = f"{target_path}/{pid}.json"
        res = await luogu.get_problem_settings(pid)
        res.problemSettings.store(cache_path)
        queue.task_done()
    print(f"Consumer {id} finished")

async def main():
    producers = [asyncio.create_task(producer(i + 1)) for i in range(producer_count)]
    consumers = [asyncio.create_task(consumer(i + 1)) for i in range(consumer_count)]
    
    # Wait for all tasks to complete
    await asyncio.gather(meta_producer(), *producers, *consumers)

if __name__ == "__main__":
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    asyncio.run(main())
    print("All coroutines are done")
