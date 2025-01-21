import os
import json
from opensearchpy import OpenSearch, RequestsHttpConnection
from dotenv import load_dotenv

# config
load_dotenv()
OPENSEARCH_HOST = os.getenv('OPENSEARCH_HOST')
OPENSEARCH_ID = os.getenv('OPENSEARCH_ID')
OPENSEARCH_PASSWORD = os.getenv('OPENSEARCH_PASSWORD')

client = OpenSearch(
  hosts=[OPENSEARCH_HOST],
  http_compress=True,
  http_auth=(OPENSEARCH_ID, OPENSEARCH_PASSWORD),
  use_ssl=True,
  connection_class=RequestsHttpConnection
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

db_exist_date = []
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
    db_exist_date = [x["_source"]["date"] for x in response]
except Exception as e:
    print(f"Error fetching accident: {e}")
    exit(-1)

    
