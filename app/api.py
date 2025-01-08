from opensearchpy import OpenSearch, RequestsHttpConnection, TransportError, RequestError, ConnectionError
from config import OPENSEARCH_HOST, INDEX_NAME
from collections import OrderedDict
from datetime import datetime
from fastapi import HTTPException


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
    return [{"_id": x["_id"], **x["_source"]} for x in response]


def read_airline_suggestions(airline: str) -> list:
    """
    Fetch unique airline suggestions based on fuzzy matching or wildcard search.
    """
    request_body = {
        "_source": "airline",
        "suggest": {
            "airline-suggestions": {
                "prefix": airline,
                "completion": {
                    "field": "airline", 
                    "size": 5,
                    "fuzzy": {
                        "fuzziness": "AUTO"
                    }
                }
            }
        }
    }
    try:
        response = fetch_data_from_opensearch(INDEX_NAME, request_body)
        print(response)
        suggestions = response["suggest"]["airline-suggest"][0]["options"]
        airlines = [option["text"] for option in suggestions]
    except Exception as e:
        airlines = []
    
    return airlines


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
    airline_data = [{**doc["_source"], "_id": doc["_id"]} for doc in response if "_source" in doc and "_id" in doc]
    
    return airline_data
    
    
def read_airline_description(doc_id: str):
    """
    Fetch the description for a specific document by ID.
    """
    request_body = {
        "_source": ["description"],
        "query": {
            "terms": {
                "_id": [doc_id]
            }
        }
    }

    response = fetch_data_from_opensearch(INDEX_NAME, request_body)
    description = [
        {"description": x["_source"]["description"]}
        for x in response
        if "_source" in x and "description" in x["_source"]
    ][0]

    return description


def read_airline_ko_description(doc_id: str):
    """
    Fetch the description for a specific document by ID.
    """
    request_body = {
        "_source": ["ko_description"],
        "query": {
            "terms": {
                "_id": [doc_id]
            }
        }
    }

    try: 
        response = fetch_data_from_opensearch(INDEX_NAME, request_body)
        description = {"description": response[0]["_source"]["ko_description"]}

        return description
    except Exception as e:
        print(f"Error fetching document: {e}")
        return {"description": ""}


def check_ko_description(doc_id: str) -> bool:
    """
    Check if the ko_description field is empty for the given document ID.
    """
    try:
        response = client.get(index=INDEX_NAME, id=doc_id)
        
        ko_description = response["_source"].get("ko_description", "")
        return ko_description == ""

    except Exception as e:
        print(f"Error fetching document: {e}")
        return True


def update_ko_description(doc_id: str, description: str) -> dict:
    try:
        doc = {
            "doc": {
                "ko_description": description
            },
            "doc_as_upsert": True 
        }

        response = client.update(index=INDEX_NAME, id=doc_id, body=doc)

        if response['result'] == 'updated' or response['result'] == 'created':
            return {"message": "Description updated successfully.", "status": "success"}
        else:
            raise HTTPException(status_code=500, detail="Failed to update description.")

    except (TransportError, RequestError) as e:
        raise HTTPException(status_code=400, detail=f"OpenSearch error: {str(e)}")
    except ConnectionError as e:
        raise HTTPException(status_code=500, detail=f"Connection error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    