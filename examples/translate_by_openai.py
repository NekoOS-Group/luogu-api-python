import asyncio
import os
import random

import pyLuogu
from openai import AsyncOpenAI

cookies = pyLuogu.LuoguCookies.from_file("cookies.json")
luogu = pyLuogu.luoguAPI(cookies=cookies)

with open("openai_key", "r") as f:
    openai_key = f.read()
with open("qwen_key", "r") as f:
    qwen_key = f.read()

client_openai = AsyncOpenAI(
    api_key=openai_key,
    base_url="https://api.openai-hk.com/v1",
)
client_qwen = AsyncOpenAI(
    api_key=qwen_key,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

model1 = "qwen-max"
model2 = "chatgpt-4o-latest"


async def openai_translate(_problem_settings: pyLuogu.ProblemSettings):
    problem_markdown = _problem_settings.get_markdown()

    if len(problem_markdown) > 10000 or len(problem_markdown) < 50:
        return _problem_settings

    completion = await client_qwen.chat.completions.create(
        model=model1,
        messages=[
            {'role': 'system', 'content':
                '''你是一位精通中文表达以及算法竞赛术语的翻译员，擅长处理包含 LaTeX 公式、数学符号以及编程代码等多种格式的文档。'''
             },
            {'role': 'user', 'content':
                "你的任务是将一道算法竞赛题目翻译为中文，同时需要使得结果更加符合汉语的表达习惯。额外要求" +
                """
1. 完整保留原文中的 LaTeX 公式、数学符号、编程代码块、引用环境以及其它格式标签（如 `\\begin{aligned}...\\end{aligned}`、`\\frac{}`, `$$...$$` 等），不要对这些符号、环境进行任何更改或省略。  
2. 确保输出文本通顺、准确且**符合汉语表达习惯**。  
3. 输出时不要额外添加说明、思考过程等不必要的文本，只保留翻译好的正文与原文的 LaTeX 格式。
4. 遇到专有名词，例如人名地名可以不用翻译。一些仅在该题目中适用的概念词汇的翻译需要保持前后一致，如果翻译出来会更加难懂，可以不用翻译，或者用引号括起来。
5. 题目包含 题目背景 题目描述 输入格式 输出格式 数据范围与提示等内容如果为空(None)，则可以将这一节小标题去除
6. 如果原文内容或排版不符合洛谷题库规范（例如格式混乱、符号使用不当、缺少必要的 LaTeX 环境、标题层次不清等），需要在翻译的同时对这些内容进行修改，使之符合洛谷题库的要求。  

请正确使用全角中文标点符号。特别地，句末要有句号。
数学公式（运算式、运算符、参与运算的常数、作为变量的字母等）应正确使用 LaTeX(使用 $ $ 环境包含)，非数学公式（一般英文单词、题目名、算法名、人名等）不应使用 LaTeX。
中文与英文、数字或公式之间以半角空格隔开，但中文标点符号与英文、数字或公式之间不应有空格。
中文引号请使用「」
一些需要特别注明或说明的内容：
Latex 环境需要使用 $ $ 包含
子串、子序列：应当注明子串是连续的，子序列是不一定连续的。
所有子串、所有子序列：应当说明是否包含空串或空子序列。
联通：应写成「连通」。
同一道题目的同一个变量，名字的大小写应统一，不应出现在某处是 $N$，而在另一处变成 $n$ 的情况。
描述多个并列的变量时，应合并为一个公式。
表述时应注意形式上的统一，不应出现「输入」二字时有时无的情况。
输出特定字符串时应使用行内代码块。
如果题目有多种可能的正确输出，包括输出小数（可能有浮点误差的情况），需要用到 Special Judge，请在输出格式中说明。
如果答案需要取模，请在题目描述和输出格式中两次说明。
表述时应注意形式上的统一，不应出现「输出」二字时有时无的情况。
当有效位数较少时，$\\ge 10^5$ 的数应使用科学计数法。
不同变量的数据范围应分开为多个公式，公式与公式之间用全角逗号隔开。特别地，若存在多个变量的数据范围相同，也可以合并为同一个公式。
                """ + problem_markdown
             }
        ],
    )

    content = completion.choices[0].message.content

    completion = await client_openai.chat.completions.create(
        model=model2,
        messages=[
            {'role': 'system', 'content':
                '''你是一位精通中文表达以及算法竞赛术语的翻译员，擅长处理包含 LaTeX 公式、数学符号以及编程代码等多种格式的文档。'''
             },
            {'role': 'user', 'content':
                "你的任务是将一道算法竞赛题目翻译为中文，同时需要使得结果更加符合汉语的表达习惯。" + problem_markdown
             },
            {
                "role": "assistant", "content": content
            },
            {
                "role": "user", "content":
                "现在你的任务是，在保证原文含义被准确表达的情况下，润色翻译使得其更加符合汉语的表达习惯，这一次你有权限修改部分语序，用词，而无需直译。\n" +
                "请在用词和句式上做尽量符合中文阅读习惯的处理，可以再优化一下，让语言更易懂。\n" +
                "如果有一些看起来在中文很晦涩难懂的句子可以尝试重新翻译\n" +
                "题目包含 题目背景 题目描述 输入格式 输出格式 数据范围与提示等内容如果为空，则可以将这一节小标题去除"
            }
        ],
    )

    _problem_settings.translation = completion.choices[0].message.content + "\n\n **本翻译由 AI 自动生成**"
    _problem_settings.needsTranslation = False


count = len(os.listdir("cache/translated"))
lock = asyncio.Lock()
locked = dict()


async def coroutine(cid: int):
    print(f"coroutine<{cid}> is awake")
    await asyncio.sleep(0.5)

    index = 0
    for file in os.listdir("cache/translated"):
        index += 1

        async with lock:
            if locked.get(file) is None:
                locked[file] = True
            else:
                continue

        print(f"coroutine<{cid}> locked {file}")

        problem_settings = pyLuogu.ProblemSettings.from_file(f"cache/translated/{file}")

        if problem_settings.needsTranslation:

            for _ in range(5):
                try:
                    await openai_translate(problem_settings)
                    break
                except Exception as e:
                    print(f"coroutine<{cid}> ", e)
                    await asyncio.sleep(10)
                    continue
            else:
                print(f"coroutine<{cid}> translating {file.split('.')[0]} failed({index}/{count})")
                continue

            problem_settings.store(f"cache/translated/{file}")
            print(f"coroutine<{cid}> translate {file.split('.')[0]} successfully({index}/{count})")

            await asyncio.sleep(random.random() / 2 + 0.5)

    print(f"coroutine<{cid}> quit")


async def start_coroutine():
    tasks = [coroutine(i + 1) for i in range(50)]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(start_coroutine())

    print("All coroutine are quit")
