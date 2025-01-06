import os
from dotenv import load_dotenv


# init setting
load_dotenv()
ACCIDENTS_URL = os.getenv("ACCIDENTS_DB_URL")
ACCIDENTS_DB_URL = ACCIDENTS_URL + "database/"


# opensearch setting
CLIENT_CERT = "../opensearch/opensearch-certs/fullchain.pem"
CLIENT_KEY = "../opensearch/opensearch-certs/privkey.pem"

OPENSEARCH_HOST = "https://avcc.jieeen.kr:9200"
INDEX_NAME = "aviation_accidents"


# crawl setting
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

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
