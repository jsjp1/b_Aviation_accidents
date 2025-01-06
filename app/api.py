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
    Fetch detailed information for a specific airline, allowing for minor differences 
    in spacing or formatting, sorted by date in descending order.
    """
    request_body = {
        "query": {
            "bool": {
                "should": [
                    {
                        "term": {
                            "airline.raw": {
                                "value": airline
                            }
                        }
                    }
                ]
            }
        },
        "sort": [
            {"date": {"order": "desc", "missing": "_last"}}
        ],
        "size": 1000
    }

    response = fetch_data_from_opensearch(INDEX_NAME, request_body)
    airline_data = [x["_source"] for x in response]
    
    return airline_data
    
    
def read_airline_description(airline: str, date: str):
    """
    Fetch descriptions of all incidents for a specific airline, sorted by date in descending order.
    """
    request_body = {
        "_source": ["description"],
        "query": {
            "bool": {
                "must": [
                    {
                        "term": {
                            "airline.raw": {
                                "value": airline
                            }
                        }
                    },
                    {
                        "term": {
                            "date": {
                                "value": date
                            }
                        }
                    }
                ]
            }
        }
    }
    
    response = fetch_data_from_opensearch(INDEX_NAME, request_body)
    
    descriptions = [x["_source"]["description"] for x in response if "description" in x["_source"]][0]
    
    return descriptions