import re
import pyLuogu
import openai
import asyncio
import asynciolimiter

import pyLuogu.errors

pyLuogu.set_log_level("INFO")

cookies_openai_agent = pyLuogu.LuoguCookies.from_file("cookies_openai_agent.json")
luogu_openai_agent = pyLuogu.asyncLuoguAPI(cookies=cookies_openai_agent)

LACPT_id = 702688
base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
api_key = open("ali_key", "r").read()
model = "deepseek-r1"
reasoning_effort = None
prompt = "请仅给出该题目的完整，正确的 C++ 实现，而无需输出任何其他的内容。"

openai_client = openai.AsyncOpenAI(
    base_url=base_url,
    api_key=api_key,
)

rate_limiter_fetch = asynciolimiter.Limiter(1)
rate_limiter_submit = asynciolimiter.Limiter(0.1)

async def test_model(pid: int, pass_num: int = 1):
    print(f"Testing problem {pid}...")
    if pass_num > 1:
        raise NotImplementedError("pass_num > 1 is not supported.")
    await rate_limiter_fetch.wait()
    problem = (await luogu_openai_agent.get_problem(pid)).problem
    print(f"fetch {pid} done.")

    stream = await openai_client.chat.completions.create(
        model=model,
        messages=[
            { "role": "user", "content": problem.content.get_markdown() + "\n" + prompt },
        ],
        reasoning_effort=reasoning_effort,
        stream=True
    )

    start_time = asyncio.get_event_loop().time()
    answer = ""
    try:
        count = 0
        async for chunk in stream:
            delta = chunk.choices[0].delta
            if delta is None:
                continue
            if hasattr(delta, 'reasoning_content') and delta.reasoning_content != None:
                if count % 100 == 0:
                    now_time = asyncio.get_event_loop().time()
                    print(f"{model} is reasonning on {pid} ({int(now_time - start_time)} seconds).")
                count += 1
                continue
            answer += delta.content
    except openai.APIError as e:
        return f"fail({e.message})"
    end_time = asyncio.get_event_loop().time()
    used_time = int(end_time - start_time)
    
    realcode = re.search(r"```(cpp)?\n([\S\s]*)\n```", answer)
    if not realcode:
        print(answer)
        return "Failed"
    answer = realcode.group(2)

    max_retry = 5
    for attemp in range(max_retry):
        try:
            await rate_limiter_submit.wait()
            rid = (await luogu_openai_agent.submit_code(pid, answer)).rid
            break
        except pyLuogu.errors.ForbiddenError:
            if attemp == max_retry - 1:
                return "Failed(Forbidden)"
            await asyncio.sleep(20)
            continue
        except:
            return "Failed(?)"

    while True:
        await rate_limiter_fetch.wait()
        res = await luogu_openai_agent.get_record(rid)
        if res.record.status in [0, 1]:
            await asyncio.sleep(5)
            continue

        if res.record.status == 2:
            return f"CE {used_time}"
        
        return str(res.record.score) + " " + str(used_time)

async def main():
    problems = (await luogu_openai_agent.get_problem_set(LACPT_id)).training.problems
    print("Problems loaded.")

    result = await asyncio.gather(*[test_model(problem.pid) for problem in problems])
    print(result)

if __name__ == "__main__":
    print(f"Testing model {model} on LACPT")
    asyncio.run(main())
