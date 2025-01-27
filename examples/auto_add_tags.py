import os
import re

import pyLuogu

pyLuogu.set_log_level("INFO") 

cookies = pyLuogu.LuoguCookies.from_file("cookies.json")
luogu = pyLuogu.luoguAPI(cookies=cookies)

tag = luogu.get_tags().tags

tabel = {
    "清华集训" : "清华集训",
    "THUWC": "THUWC",
    "THUSC": "THUSC",
    "POI"  : "POI（波兰）",
    "PA"   : "PA（波兰）",
    "ICPC"  : "ICPC",
    "SEERC" : "ICPC",
    "NEERC" : "ICPC",
    "NWRRC" : "ICPC",
    "NERC"  : "ICPC",
    "THUPC" : "THUPC",
    "COI"  : "COI（克罗地亚）",
    "COCI" : "COCI（克罗地亚）",
    "BalkanOI" : "BalkanOI（巴尔干半岛）",
    "BOI"      : "BalticOI（波罗的海）",
    "BalticOI" : "BalticOI（波罗的海）",
    "NordicOI" : "NordicOI（北欧）",
    "JOIG"     : "JOI（日本）",
    "KTSC" : "KOI（韩国）",
    "KOI"  : "KOI（韩国）",
    "RMI"  : "RMI（罗马尼亚）",
    "NOISG" : "NOISG（新加坡）",
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
        match = re.search(rf'\[({keyword})\s?(\d+)\s?[/-]?(\d+)?\s?([Dd]ay\s?\d+)?\s?(.+)?\]\s?(.+)', problem.title)
        if match:            
            content_name, year_number, year_number_cond, day_number, additional_message, real_title = match.groups()

            # print(f"{content_name} {year_number} {year_number_cond} {day_number} {additional_message} {real_title}")    
            
            content_name_tag = tabel.get(content_name)

            if content_name_tag is None:
                print(f"Failed to match content name: {problem.title}")
                continue

            new_tags = []
            remove_tags = []

            new_year_number = f"{year_number}" if year_number_cond is None else f"{year_number}/{year_number_cond}"
            if additional_message is None:
                new_title = f"[{content_name} {new_year_number}] {real_title}"
            else:
                new_title = f"[{content_name} {new_year_number} {additional_message}] {real_title}"
            if day_number is not None:
                new_title += f" ({day_number})"

            ignore = True

            if problem.tags is None or search_tag(content_name_tag).id not in problem.tags:
                print(f" - Adding tag '{content_name_tag}' to {problem.title}")
                ignore = False
                new_tags.append(search_tag(content_name_tag).id)

            if problem.tags is None or search_tag(year_number).id not in problem.tags:
                print(f" - Adding tag '{year_number}' to {problem.title}")
                ignore = False
                new_tags.append(search_tag(year_number).id)

            if content_name == "COI" and search_tag("COCI（克罗地亚）").id in problem.tags:
                print(f" - Removing tag 'COCI' from {problem.title}")
                ignore = False
                remove_tags.append(search_tag("COCI（克罗地亚）").id)

            if year_number_cond is not None and search_tag(year_number_cond).id in problem.tags:
                print(f" - Removing tag '{year_number_cond}' from {problem.title}")
                ignore = False
                remove_tags.append(search_tag(year_number_cond).id)
            
            if new_title != problem.title:
                print(f" - Changing title '{problem.title}' to '{new_title}'")
                ignore = False

            if ignore:
                print(f"Ignoring {problem.title}")
                continue

            # confirm = input("Do you want to apply changed? (y/n): ")
            # if confirm.lower() == "n":
            #     continue

            problem_setting = luogu.get_problem_settings(problem.pid).problemSettings
            problem_setting.append_tags(new_tags)
            problem_setting.remove_tags(remove_tags)
            problem_setting.title = new_title

            luogu.update_problem_settings(problem.pid, problem_setting)
            
        else:
            print(f"Skipping {problem.title}")
        


for keyword in tabel.keys():
    meta = luogu.get_problem_list(keyword=keyword)
    pages = (meta.count + meta.perPage - 1) // meta.perPage
    for i in range(1, pages + 1):
        add_tag(keyword, i)
