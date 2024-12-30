import requests
from bs4 import BeautifulSoup
from config import *
from datetime import datetime
from opensearch_util import *


def parse_init(client):
    year = [y for y in range(1919, 2025)]
    db_urls = [ACCIDENTS_DB_URL + "year/" + str(y) for y in year]

    parse(client, db_urls)


def parse(client, db_urls):
    for db_url in db_urls:

        response = requests.get(db_url, headers=HEADERS)
        if response.status_code == 200:
            bs = BeautifulSoup(response.content, "html.parser")
        else:
            print(
                f"Failed to retrieve {db_url}, status code: {response.status_code}")

        _page_num = bs.find("div", class_="pagenumbers")
        page_num = len(_page_num.find_all(recursive=False))

        parse_year(client, db_url, page_num)


def parse_year(client, db_url, page_num):
    page_range = [i for i in range(1, page_num+2)]
    for page in page_range:
        parse_url = db_url + "/" + str(page)

        response = requests.get(parse_url, headers=HEADERS)
        if response.status_code == 200:
            bs = BeautifulSoup(response.content, "html.parser")
        else:
            print(
                f"Failed to retrieve {db_url}, status code: {response.status_code}")

        docs = []
        rows = bs.find_all("tr", class_="list")
        for row in rows:
            link_tag = row.find("a")
            if link_tag:
                href = link_tag.get("href")
                href_url = ACCIDENTS_URL + href

                doc = parse_detail_info(client, href_url)
                doc = wrap_doc(doc)
                docs.append(doc)

            else:
                print("No <a> tag found in this row.")

        # page 단위로 post to opensearch
        post_docs(client, docs)


def parse_detail_info(client, href_url):
    response = requests.get(href_url, headers=HEADERS)

    if response.status_code == 200:
        bs = BeautifulSoup(response.content, "html.parser")
    else:
        print(
            f"Failed to retrieve {href_url}, status code: {response.status_code}")

    rows = bs.find_all("td", class_="caption")

    doc = {}
    for row in rows:
        matched_keywords = [k for k in KEYWORD if k in row.text]
        assert (len(matched_keywords) <= 1)
        if not matched_keywords:
            continue

        _value = row.find_parent("tr").text
        _lst = _value.split(":")
        if row.text.strip() == "Time:" and len(_lst) >= 3:
            value = _lst[1] + ":" + _lst[2]
        elif row.text.strip() == "Fatalities:" and len(_lst) >= 4:
            value = _lst[1] + ":" + _lst[2] + ":" + _lst[3]
        else:
            value = _lst[1].strip()

        search_keyword = KEYWORD_SEARCH_MAP[matched_keywords[0]]
        _lst = value.split("/")

        if row.text.strip() == "Date:":
            value = process_date(value)
            doc.update({search_keyword: value})
        elif row.text.strip() == "Fatalities:" and len(_lst) >= 2:
            search_keyword1 = KEYWORD_SEARCH_MAP[matched_keywords[0]][0]
            search_keyword2 = KEYWORD_SEARCH_MAP[matched_keywords[0]][1]

            value1 = _lst[0].split(":")[1].strip()
            value2 = _lst[1].split(":")[1].strip()

            doc.update({search_keyword1: value1})
            doc.update({search_keyword2: value2})
        else:
            doc.update({search_keyword: value})

    return doc


def process_date(value):
    # TODO: 연도도 없는 경우
    try:
        parsed_date = datetime.strptime(value, "%A %d %B %Y")
        return parsed_date.strftime("%Y-%m-%d")
    except ValueError:
        year = extract_year(value)
        if year:
            return f"{year}-01-01"


def extract_year(value):
    import re
    match = re.search(r"\b(19|20)\d{2}\b", value)
    if match:
        return match.group(0)
    return None
