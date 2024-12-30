import os
from dotenv import load_dotenv

# init setting
load_dotenv()
ACCIDENTS_URL = os.getenv("ACCIDENTS_DB_URL")
ACCIDENTS_DB_URL = ACCIDENTS_URL + "database/"

# opensearch setting
OPENSEARCH_HOST = "http://localhost:9200"
INDEX_NAME = "aviation_accidents"
