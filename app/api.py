from opensearchpy import OpenSearch, RequestsHttpConnection
from config import OPENSEARCH_HOST, INDEX_NAME
from collections import OrderedDict
from datetime import datetime

client = OpenSearch(
    hosts=[OPENSEARCH_HOST],
    http_compress=True,
    http_auth=("admin", "admin"),
    use_ssl=True,
    connection_class=RequestsHttpConnection,
)


def fetch_data_from_opensearch(index: str, query: dict) -> list:
    """
    Helper function to fetch data from OpenSearch and handle errors gracefully.
    """
    try:
        response = client.search(index=index, body=query)
        return response.get("hits", {}).get("hits", [])
    except Exception as e:
        print(f"Error fetching data from OpenSearch: {e}")
        return []


def read_accidents(start: int, size: int) -> list:
    """
    Fetch accidents sorted by date in descending order.
    """
    request_body = {
        "from": start,
        "size": size,
        "sort": [{"date": {"order": "desc"}}],
        "_source": ["date", "time", "airline", "fatalities", "occupants", "location", "aircraft_status"],
    }
    response = fetch_data_from_opensearch(INDEX_NAME, request_body)
    return [x["_source"] for x in response]


def read_airline_suggestions(airline: str) -> list:
    """
    Fetch unique airline suggestions based on fuzzy matching or wildcard search.
    """
    request_body = {
        "query": {
            "bool": {
                "should": [
                    {
                        "match": {
                            "airline": {
                                "query": airline,
                                "fuzziness": "AUTO",
                            }
                        }
                    },
                    {
                        "wildcard": {
                            "airline.raw": {
                                "value": f"*{airline}*",
                                "boost": 0.5,
                            }
                        }
                    },
                ]
            }
        }
    }
    response = fetch_data_from_opensearch(INDEX_NAME, request_body)
    airlines = [x["_source"].get("airline", "")
                for x in response if x["_source"].get("airline")]
    return list(OrderedDict.fromkeys(airlines))[:5]


def read_airline_info(airline: str) -> list:
    """
    Fetch detailed information for a specific airline, sorted by date in descending order.
    """
    request_body = {
        "query": {
            "term": {
                "airline.raw": {
                    "value": airline
                }
            }
        }
    }
    
    response = fetch_data_from_opensearch(INDEX_NAME, request_body)
    airline_data = [x["_source"] for x in response]

    sorted_airline_data = sorted(
        airline_data,
        key=lambda x: datetime.strptime(
            x.get("date", "1970-01-01"), "%Y-%m-%d"),
        reverse=True,
    )
    return sorted_airline_data
    
    