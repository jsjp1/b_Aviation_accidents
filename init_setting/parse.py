import requests
from bs4 import BeautifulSoup
from config import *

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


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
                parse_detail_info(client, href_url)
            else:
                print("No <a> tag found in this row.")


def parse_detail_info(client, href_url):
    response = requests.get(href_url, headers=HEADERS)
    if response.status_code == 200:
        bs = BeautifulSoup(response.content, "html.parser")
    else:
        print(
            f"Failed to retrieve {href_url}, status code: {response.status_code}")

    pass
