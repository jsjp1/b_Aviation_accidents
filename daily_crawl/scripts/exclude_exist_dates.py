import os
import json
from dotenv import load_dotenv
from datetime import datetime
from opensearchpy import OpenSearch, RequestsHttpConnection


# config
load_dotenv()
OPENSEARCH_HOST = os.getenv('OPENSEARCH_HOST')
OPENSEARCH_ID = os.getenv('OPENSEARCH_ID')
OPENSEARCH_PASSWORD = os.getenv('OPENSEARCH_PASSWORD')
INDEX_NAME = os.getenv('INDEX_NAME')
current_year = datetime.now().year

first_date = str(current_year) + '-01-01'
last_date = str(current_year) + '-12-31'

DB_URL = os.getenv("DB_URL") + str(current_year)

client = OpenSearch(
    hosts=[OPENSEARCH_HOST],
    http_compress=True,
    http_auth=(OPENSEARCH_ID, OPENSEARCH_PASSWORD),
    use_ssl=True,
    connection_class=RequestsHttpConnection,
)

def fetch_data_from_opensearch(index: str, query: dict, hits1: str, hits2: str) -> list:
    try:
        response = client.search(index=index, body=query)
        return response.get(hits1, {}).get(hits2, [])
    except TransportError as e:
        print(f"TransportError: {e}")
        return []
    except RequestError as e:
        print(f"RequestError: {e}")
        return []
    except ConnectionError as e:
        print(f"ConnectionError: {e}")
        return []
    except Exception as e:
        print(f"Error fetching data from OpenSearch: {e}")
        return []


try: 
  with open("./href_map.json", 'r') as f:
    date_href_map = json.load(f)
except Exception as e:
  print(e)
  exit(-1)
  
date_lst = []
  
try: 
    request_body = {
      "_source": ["date"],
      "query": {
        "range": {
          "date": {
            "gte": first_date,
            "lte": last_date,
            "format": "yyyy-MM-dd"
          }
        }
      }
    }
    response = fetch_data_from_opensearch(INDEX_NAME, request_body, "hits", "hits")
    date_lst = [x["_source"]["date"] for x in response]
except Exception as e:
    print(f"Error fetching accident: {e}")
    exit(-1)
  
for date in date_lst:
  if date in date_href_map:
    del date_href_map[date]
    
try: 
  with open("/var/jenkins_scripts/href_map.json", 'w') as f:
    json.dumps(date_href_map, f)
except Exception as e:
  print(e)
  exit(-1)