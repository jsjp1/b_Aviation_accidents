
import os
import requests
import json
from dotenv import load_dotenv
from datetime import datetime
from bs4 import BeautifulSoup

# config
load_dotenv()
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
current_year = datetime.now().year
DB_URL = os.getenv("DB_URL") + str(current_year)

response = requests.get(DB_URL, headers=HEADERS)
if response.status_code == 200:
  bs = BeautifulSoup(response.content, "html.parser")
else:
  print(f"Failed to retrieve {DB_URL}, status_code: {response.status_code}")
  
_page_num = bs.find("div", class_="pagenumbers")
page_num = len(_page_num.find_all(recursive=False))

date_href_map = {}

page_range = [i for i in range(1, page_num+2)]
for page in page_range:
    parse_url = DB_URL + "/" + str(page)

    response = requests.get(parse_url, headers=HEADERS)
    if response.status_code == 200:
        bs = BeautifulSoup(response.content, "html.parser")
    else:
        print(
            f"Failed to retrieve {DB_URL}, status code: {response.status_code}")
        exit(-1)

    rows = bs.find_all("tr", class_="list")
    for row in rows:
      data = row.find("span", class_="nobr")
      
      date_obj = datetime.strptime(data.text, "%d %b %Y")
      formatted_date = date_obj.strftime("%Y-%m-%d")
      
      date_href_map[formatted_date] = data.find("a").get("href")
    
try:
  with open('/var/jenkins_scripts/href_map.json', 'w') as f:
    json.dump(date_href_map, f)
except Exception as e:
    print(e)
    exit(-1)