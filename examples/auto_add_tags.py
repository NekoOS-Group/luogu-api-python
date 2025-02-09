import os
import re
import pyLuogu

pyLuogu.set_log_level("INFO")

cookies = pyLuogu.LuoguCookies.from_file("cookies.json")
luogu = pyLuogu.luoguAPI(cookies=cookies)

tags = luogu.get_tags().tags

def parse_mx(title: str):
    match = re.fullmatch(r"(【MX-[XJS]\d-T\d】)\s?(.*)", title)
    if match:
        prefix, title = match.groups()
        return "梦熊比赛", None, f"{prefix}{title}"
    return None

def parse_noip(title: str):
    match = re.fullmatch(r"\[NOIP\s?(\d*)\s?(.*)?\]\s?(.*)", title)
    if match:
        year, type, title = match.groups()
        if type not in ["提高组", "普及组"]:
            return "NOIP提高组", year, f"[NOIP{year}] {title}"
        return f"NOIP{type}", year, f"[NOIP {year} {type}] {title}"
    return None

def parse_blue_bridge(title: str):
    match = re.fullmatch(r"\[蓝桥杯\s*(\d{4})\s*(国|省).*?\]\s*(.+)", title)
    if match:
        year, category, rest_title = match.groups()
        tag_name = "蓝桥杯国赛" if category == "国" else "蓝桥杯省赛"
        return tag_name, year, title
    return None

tag_table = {
    "蓝桥杯": parse_blue_bridge,
    "NOIP": parse_noip,
    "MX": parse_mx,
    "THUSCH": "THUSC",
    "IOI": "IOI",
    "HUSTFC": "高校校赛",
    "CCPC": "XCPC",
    "GDCPC": "XCPC",
    "SDCPC": "XCPC",
    "GDKOI 2024": "广东",
    "XJTUPC": "高校校赛",
    "UESTCPC": "高校校赛",
    "SHUPC": "高校校赛",
    "JOISC": "JOI（日本）",
    "集训队互测": "集训队互测",
    "清华集训": "清华集训",
    "THUWC": "THUWC",
    "THUSC": "THUSC",
    "POI": "POI（波兰）",
    "PA": "PA（波兰）",
    "ICPC": "ICPC",
    "CERC": "ICPC",
    "SEERC": "ICPC",
    "NEERC": "ICPC",
    "NWRRC": "ICPC",
    "NERC": "ICPC",
    "THUPC": "THUPC",
    "COI": "COI（克罗地亚）",
    "COCI": "COCI（克罗地亚）",
    "BalkanOI": "BalkanOI（巴尔干半岛）",
    "BOI": "BalticOI（波罗的海）",
    "BalticOI": "BalticOI（波罗的海）",
    "NordicOI": "NordicOI（北欧）",
    "JOIG": "JOI（日本）",
    "KTSC": "KOI（韩国）",
    "KOI": "KOI（韩国）",
    "RMI": "RMI（罗马尼亚）",
    "NOISG": "NOISG（新加坡）",
    "CEOI": "CEOI（中欧）",
    "ROI": "ROI（俄罗斯）",
    "ROIR": "ROIR（俄罗斯）",
    "CCC": "CCC（加拿大）",
    "CCO": "CCO（加拿大）",
    "eJOI": "eJOI（欧洲）",
    "EGOI": "EGOI（欧洲/女生）",
    "AGM": "AGM",
}

def search_tag(tag_name: str) -> pyLuogu.TagDetail:
    for t in tags:
        if t.name == tag_name:
            return t
    return None

def add_tag(keyword: str, page: int):
    for problem in luogu.get_problem_list(keyword=keyword, page=page).problems:
        original_title = problem.title  # Save original title
        table_entry = tag_table.get(keyword)
        if isinstance(table_entry, str):
            problem.title = problem.title.replace("「", "[").replace("」", "]")
            match = re.fullmatch(rf'\[({keyword})\s?(\d+)\s?[/-]?(\d+)?\s?([Dd]ay\s?\d+)?\s?(.+)?\]\s?(.+)', problem.title)
            if not match:
                print(f"Skipping {original_title}")
                continue

            content_name, year_number, year_number_cond, day_number, additional_message, real_title = match.groups()
            content_name_final = table_entry
            year_number_final = year_number

            new_year_number = f"{year_number}" if year_number_cond is None else f"{year_number}/{year_number_cond}"
            title_final = f"[{content_name} {new_year_number}] {real_title}"
            if additional_message:
                title_final = f"[{content_name} {new_year_number} {additional_message}] {real_title}"
            if day_number:
                title_final += f" ({day_number})"
        else:
            # When table entry is a callable (e.g., parse_mx)
            parsed = table_entry(problem.title)
            if parsed is None:
                print(f"Skipping {original_title}: parse returned None")
                continue
            content_name_final, year_number_final, title_final = parsed
            year_number_cond = None

        add_tags = []
        remove_tags = []

        tag_detail = search_tag(content_name_final)
        if tag_detail and tag_detail.id not in problem.tags:
            print(f" - Adding tag '{content_name_final}' to {original_title}")
            add_tags.append(tag_detail.id)

        if year_number_final is not None:
            year_tag = search_tag(year_number_final)
            if year_tag and year_tag.id not in problem.tags:
                print(f" - Adding tag '{year_number_final}' to {original_title}")
                add_tags.append(year_tag.id)

        if year_number_cond:
            remove_detail = search_tag(year_number_cond)
            if remove_detail and remove_detail.id in problem.tags:
                print(f" - Removing tag '{year_number_cond}' from {original_title}")
                remove_tags.append(remove_detail.id)

        if title_final != original_title:
            print(f" - Changing title from '{original_title}' to '{title_final}'")

        if not add_tags and not remove_tags and title_final == original_title:
            print(f"Ignoring {original_title} as no changes are needed.")
            continue
        
        # confirm = input("Do you want to continue? (y/n) ")
        # if confirm.lower() != "y":
        #    print("Aborted.")
        #    exit(0)

        problem_setting = luogu.get_problem_settings(problem.pid).problemSettings
        problem_setting.append_tags(add_tags)
        problem_setting.remove_tags(remove_tags)
        problem_setting.title = title_final

        luogu.update_problem_settings(problem.pid, problem_setting)

for keyword in tag_table.keys():
    meta = luogu.get_problem_list(keyword=keyword)
    pages = (meta.count + meta.perPage - 1) // meta.perPage
    for i in range(1, pages + 1):
        add_tag(keyword, i)
