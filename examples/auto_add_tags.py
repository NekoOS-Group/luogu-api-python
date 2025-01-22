import os

import pyLuogu

cookies = pyLuogu.LuoguCookies.from_file("cookies.json")
luogu = pyLuogu.luoguAPI(cookies=cookies)

tags = luogu.get_tags()
print(tags)

for file in os.listdir("cache"):
    pass