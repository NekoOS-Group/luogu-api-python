import re
import pyLuogu
import openai
import asyncio
import asynciolimiter
import os
import httpx
import pytesseract
from PIL import Image

import pyLuogu.errors

pyLuogu.set_log_level("WARNING")

cookies_openai_agent = pyLuogu.LuoguCookies.from_file("cookies_openai_agent.json")
luogu_openai_agent = pyLuogu.asyncLuoguAPI(cookies=cookies_openai_agent)

LACPT_id = 702688
base_url = "https://openrouter.ai/api/v1"
api_key = open("openrouter_key", "r").read()
model = "google/gemini-2.0-flash-001"
reasoning_effort = None
prompt = "请仅给出该题目的完整，正确的 C++ 实现，而无需输出任何其他的内容。"
maximal_parallel = 10

openai_client = openai.AsyncOpenAI(
    base_url=base_url,
    api_key=api_key,
    max_retries=10,
    timeout=httpx.Timeout(300.0, read=100.0, write=20.0, connect=10.0)
)

rate_limiter_fetch = asynciolimiter.Limiter(0.4)
rate_limiter_submit = asynciolimiter.Limiter(0.04)
rate_limiter_openai = asynciolimiter.Limiter(0.5)
sem = asyncio.Semaphore(maximal_parallel)

def manual_captcha_handler(data: bytes):
    with open(".temp/captcha.jpg", "wb") as f:
        f.write(data)
    os.system("imgcat .temp/captcha.jpg")
    return input("captcha: ")

def captcha_handler(data: bytes):
    with open(".temp/captcha.jpg", "wb") as f:
        f.write(data)
    captcha_text = pytesseract.image_to_string(
        Image.open(".temp/captcha.jpg"), 
        config='--psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789').strip()
    print(f"captcha: {captcha_text}")
    return captcha_text

async def test_model_inner(pid: int, problem_content: str, pass_num: int = 1):
    f = open(f".temp/{pid}.log", "w")
    stream = await openai_client.chat.completions.create(
        model=model,
        messages=[
            { "role": "user", "content": problem_content + "\n" + prompt },
        ],
        reasoning_effort=reasoning_effort,
        stream=True,
        stream_options={"include_usage": True},
        max_tokens=32000,
        max_completion_tokens=32000,
    )

    now_time = asyncio.get_event_loop().time()
    start_time = now_time
    last_time = now_time
    answer = ""
    reasoning_text = ""
    token_count = 0
    chunk_id = 0

    chunk_header = f"[{int(start_time - now_time):04}#00]"
    print(f"{chunk_header} {model} started on running {pid:<6}.")
    f.write(f"{chunk_header} {model} started on running {pid:<6}.\n")

    try:
        async for chunk in stream:
            chunk_id += 1
            chunk_header = f"[{int(now_time - start_time):04}#{chunk_id:02}]"
            await rate_limiter_openai.wait()
            now_time = asyncio.get_event_loop().time()
            try:
                delta = chunk.choices[0].delta
                usage = chunk.usage
                f.write(f"{chunk_header} {str(delta)} \n")
            except IndexError:
                f.write(f"{chunk_header} {str(chunk)} \n")
                print(f"{chunk_header} {pid} delta is None")
                continue
            if delta is None:
                f.write(f"{chunk_header} {str(chunk)} \n")
                print(f"{chunk_header} {pid} delta is None")
                continue
            f.flush()

            time_delta = now_time - last_time
            if usage is not None:
                new_token_count = usage.completion_tokens
                token_delta = new_token_count - token_count
                tokens_per_second = token_delta / time_delta
                token_count = new_token_count
                print(f"{chunk_header} {model} is running on {pid:<6}. [{token_count:5}(+ {token_delta:3}) tokens, {tokens_per_second:5.2f} tps]")
            else:
                word_count = len(reasoning_text) + len(answer)
                if not hasattr(delta, 'reasoning_content'):
                    delta.reasoning_content = ""
                word_delta = len(delta.content or "") + len(delta.reasoning_content)
                word_per_second = word_delta / time_delta
                print(f"{chunk_header} {model} is running on {pid:<6}. [{word_count:5}(+ {word_delta:3}) chars , {word_per_second:5.2f} wps]")
            last_time = now_time

            if hasattr(delta, 'reasoning_content') and delta.reasoning_content != None:
                reasoning_text += delta.reasoning_content or ""
            answer += delta.content or ""
    except Exception as e:
        f.write(f"{chunk_header} {e}")
        print(f"{chunk_header} {pid} raised {e}")

        f.close()
        raise e
    
    now_time = asyncio.get_event_loop().time()
    f.write(f"{chunk_header} Done with\n {answer}")
    f.close()
    print(f"{chunk_header} {pid} done.")

    return answer, int(now_time - start_time)

async def test_model(pid: int, pass_num: int = 1):    
    if pass_num > 1:
        raise NotImplementedError("pass_num > 1 is not supported.")
    
    await rate_limiter_fetch.wait()
    problem = (await luogu_openai_agent.get_problem(pid)).problem

    max_retry = 5
    for attemp in range(max_retry):
        try:
            async with sem:
                answer, used_time = await test_model_inner(pid, problem.content.get_markdown())
        except Exception as e:
            await asyncio.sleep(5)
            continue
        break
    else:
        return "Failed (nothing returned)", "N/A"

    if answer == "":
        print(f"{pid} got empty answer.")
        return "Failed (empty answer)", "N/A"
    
    realcode = re.search(r"```(cpp)?\n([\S\s]*)\n```", answer)
    if not realcode:
        print(f"{pid} got no code.")
        return "Failed (no code)", "N/A"
    answer = realcode.group(2)

    max_retry = 5
    for attemp in range(max_retry):
        try:
            await rate_limiter_submit.wait()
            rid = (await luogu_openai_agent.submit_code(
                pid, 
                answer, 
                capture_handler=captcha_handler)
            ).rid
            break
        except pyLuogu.errors.ForbiddenError:    
            await asyncio.sleep(20)
            continue
        except Exception as e:
            return f"Failed({e})", "N/A"
    else:
        return "Failed(Forbidden)", "N/A"

    max_retry = 25
    for attemp in range(max_retry):
        await rate_limiter_fetch.wait()
        res = await luogu_openai_agent.get_record(rid)
        if res.record.status in [0, 1]:
            await asyncio.sleep(5)
            continue

        if res.record.status == 2:
            return "CE", str(used_time)
        
        if res.record.score is None:
            res.record.score = 100 if res.record.status == 12 else 0
        
        return str(res.record.score), str(used_time)
    else:
        return "Failed(Infinite judging)", "N/A"

async def main():
    problems = (await luogu_openai_agent.get_problem_set(LACPT_id)).training.problems
    print("Problems loaded.")

    results = await asyncio.gather(*[test_model(problem.pid) for problem in problems])
    
    with open(f".temp/{model.replace("/","_")}.csv", "w") as f:
        for result in results:
            print("\t".join(result))
            f.write(",".join(result) + "\n")

if __name__ == "__main__":
    print(f"Testing model {model} on LACPT")
    asyncio.run(main())
