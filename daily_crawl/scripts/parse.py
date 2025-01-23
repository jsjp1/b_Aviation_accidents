import os
import requests
import json
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from datetime import datetime
from opensearchpy import helpers, OpenSearch, RequestsHttpConnection

# config
load_dotenv()
OPENSEARCH_HOST = os.getenv("OPENSEARCH_HOST")
OPENSEARCH_ID = os.getenv('OPENSEARCH_ID')
OPENSEARCH_PASSWORD = os.getenv('OPENSEARCH_PASSWORD')
DB_ORIGIN_URL = os.getenv("DB_ORIGIN_URL")
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
INDEX_NAME = "aviation_accidents"
KEYWORD = [
    "Owner", "Type", "Date", "Time", "Fatalities", "Aircraft damage", "Category", "Location", "Phase", "Narrative",
]
KEYWORD_SEARCH_MAP = {
    "Owner": "airline",
    "Type": "accident_type",
    "Date": "date",
    "Time": "time",
    "Fatalities": ["fatalities", "occupants"],
    "Aircraft damage": "aircraft_status",
    "Category": "accident_type",
    "Location": "location",
    "Phase": "phase",
    "Narrative": "description",
}

DEFAULT_WEIGHT = 10


client = OpenSearch(
    hosts=[OPENSEARCH_HOST],
    http_compress=True,
    http_auth=(OPENSEARCH_ID, OPENSEARCH_PASSWORD),
    use_ssl=True,
    connection_class=RequestsHttpConnection,
)

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
    return 1900


try:
  with open("/var/jenkins_scripts/href_map.json", 'r') as f:
    href_map = json.load(f)
except FileNotFoundError as e:
  print(e)
  exit(-1)
  
docs = []
for date in href_map:
  data_url = DB_ORIGIN_URL + href_map[date]
  
  try:
    response = requests.get(data_url, headers=HEADERS)
    
    if response.status_code == 200:
      bs = BeautifulSoup(response.content, "html.parser")
    else:
      print(
        f"Failed to retrieve {data_url}, status code: {response.status_code}")
      exit(-1)
  except Exception as e:
    print(e)
    exit(-1)
  
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

      if row.text.strip() == "Owner:":
          doc.update({search_keyword: {
              "input": value,
              "weight": DEFAULT_WEIGHT
          }})
      elif row.text.strip() == "Date:":
          value = process_date(value)
          doc.update({search_keyword: value})
      elif row.text.strip() == "Fatalities:" and len(_lst) >= 2:
          search_keyword1 = KEYWORD_SEARCH_MAP[matched_keywords[0]][0]
          search_keyword2 = KEYWORD_SEARCH_MAP[matched_keywords[0]][1]

          value1 = _lst[0].split(":")[1].strip()
          value2 = _lst[1].split(":")[1].strip()

          try:
              value1 = int(value1)
          except:
              value1 = 0

          try:
              value2 = int(value2)
          except:
              value2 = 0

          doc.update({search_keyword1: value1})
          doc.update({search_keyword2: value2})
      else:
          doc.update({search_keyword: value})

  narrative_span = bs.find("span", {"lang": "en-US"})
  if narrative_span:
      text = narrative_span.get_text(separator="\n").strip()
      doc.update({"description": text})
  
  doc.update({"ko_description": ""})

  new_doc = {}
  new_doc.update({"_index": INDEX_NAME})
  new_doc.update({"_source": doc})
  
  docs.append(new_doc)
  
try: 
  response = helpers.bulk(client, docs)
  print("Bulk insertion completed: ", response)
except Exception as e:
  print(e)
  exit(-1)