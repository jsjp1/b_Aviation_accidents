import requests
from bs4 import BeautifulSoup
from config import *


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

        rows = bs.find_all("tr", class_="list")
        for row in rows:
            link_tag = row.find("a")
            if link_tag:
                href = link_tag.get("href")
                href_url = ACCIDENTS_URL + href

                docs = []
                doc = parse_detail_info(client, href_url)
                docs.append(doc)
            else:
                print("No <a> tag found in this row.")


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

        if row.text.strip() == "Date":
            # TODO
            continue
        else:
            search_keyword = KEYWORD_SEARCH_MAP[matched_keywords[0]]
            _value = row.find_parent("tr").text
            value = _value.split(":")[1].strip()
            doc.update({search_keyword: value})

    return doc
