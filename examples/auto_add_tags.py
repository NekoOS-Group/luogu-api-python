import os
import re

import pyLuogu

pyLuogu.set_log_level("INFO") 

cookies = pyLuogu.LuoguCookies.from_file("cookies.json")
luogu = pyLuogu.luoguAPI(cookies=cookies)

tag = luogu.get_tags().tags

tabel = {
    "BalkanOI" : "BalkanOI（巴尔干半岛）",
    "BalticOI" : "BalticOI（波罗的海）",
    "NordicOI" : "NordicOI（北欧）",
    "KTST" : "KOI（韩国）",
    "KOI"  : "KOI（韩国）",
    "JOIG"     : "JOI（日本）",
    "RMI"  : "RMI（罗马尼亚）",
    "COI"  : "COI（克罗地亚）",
    "COCI" : "COCI（克罗地亚）",
    "NOISG" : "NOISG（新加坡）",
    "PA"   : "PA（波兰）",
    "CEOI" : "CEOI（中欧）",
    "ROI"  : "ROI（俄罗斯）",
    "ROIR" : "ROIR（俄罗斯）",
    "CCC" : "CCC（加拿大）",
    "CCO" : "CCO（加拿大）",
    "eJOI" : "eJOI（欧洲）",
    "EGOI" : "EGOI（欧洲/女生）",
    "AGM" : "AGM",
}

def search_tag(tag_name: str) -> pyLuogu.TagDetail:
    for t in tag:
        if t.name == tag_name:
            return t
    return None

def add_tag(keyword: str, page: int):
    for problem in luogu.get_problem_list(keyword=keyword, page=page).problems:
        problem.title = problem.title.replace("「", "[").replace("」", "]")
        match = re.search(r'\[(\w+)\s?(\d{4})\s?([Dd]ay\s?\d+)?\]\s?(.+)', problem.title)
        if match:
            content_name, year_number, day_number, real_title = match.groups()

            content_name_tag = tabel.get(content_name)

            if content_name_tag is None:
                print(f"Failed to match content name: {problem.title}")
                continue

            new_tags = [search_tag(content_name_tag).id, search_tag(year_number).id]

            if day_number is None:
                new_title = f"[{content_name} {year_number}] {real_title}"
            else:
                new_title = f"[{content_name} {year_number}] {real_title} ({day_number})"

            ignore = True

            if problem.tags is None or new_tags[0] not in problem.tags or new_tags[1] not in problem.tags:
                print(f" - Adding tags '{content_name}' and '{year_number}' to {problem.title}")
                ignore = False
            
            if new_title != problem.title:
                print(f" - Changing title '{problem.title}' to '{new_title}'")
                ignore = False

            if ignore:
                print(f"Ignoring {problem.title}")
                continue

            problem_setting = luogu.get_problem_settings(problem.pid).problemSettings
            problem_setting.append_tags(new_tags)
            problem_setting.title = new_title
            luogu.update_problem_settings(problem.pid, problem_setting)
            
        else:
            print(f"Failed to match title: {problem.title}")
        


for keyword in tabel.keys():
    meta = luogu.get_problem_list(keyword=keyword)
    pages = (meta.count + 49) // meta.perPage
    for i in range(1, pages + 1):
        add_tag(keyword, i)
