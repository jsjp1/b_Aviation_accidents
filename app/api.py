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


def read_accident(date: str) -> dict:
    try: 
        request_body = {
            "size": 1,
            "sort": [
                {
                    "date": {
                        "order": "desc"
                    }
                }
            ]
        }
        response = fetch_data_from_opensearch(INDEX_NAME, request_body, "hits", "hits")
        return response[0]["_source"]
    except Exception as e:
        print(f"Error fetching accident: {e}")
        return {}


def read_accidents(start: int, size: int) -> list:
    try:
        request_body = {
            "from": start,
            "size": size,
            "sort": [{"date": {"order": "desc"}}],
            "_source": ["date", "time", "airline", "fatalities", "occupants", "location", "aircraft_status"],
        }
        response = fetch_data_from_opensearch(INDEX_NAME, request_body, "hits", "hits")
        return [{"_id": x["_id"], **x["_source"]} for x in response]
    except Exception as e:
        print(f"Error fetching accidents: {e}")
        return []


def read_airline_suggestions(airline: str) -> list:
    try:
        request_body = {
            "_source": "airline",
            "suggest": {
                "airline-suggest": {
                    "prefix": airline,
                    "completion": {
                        "field": "airline", 
                        "size": 50,
                        "fuzzy": {"fuzziness": "AUTO"}
                    }
                }
            }
        }
        
        response = fetch_data_from_opensearch(INDEX_NAME, request_body, "suggest", "airline-suggest")
        if response:
            suggestions = response[0]["options"]
            airlines = [option["text"] for option in suggestions]
            return list(OrderedDict.fromkeys(airlines))[:5]
        else:
            return []
    except Exception as e:
        print(f"Error fetching airline suggestions: {e}")
        return []


def read_airline_info(airline: str) -> list:
    try:
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
            "sort": [{"date": {"order": "desc", "missing": "_last"}}],
            "size": 1000
        }

        response = fetch_data_from_opensearch(INDEX_NAME, request_body, "hits", "hits")
        return [{**doc["_source"], "_id": doc["_id"]} for doc in response if "_source" in doc and "_id" in doc]
    except Exception as e:
        print(f"Error fetching airline info: {e}")
        return []


def read_airline_description(doc_id: str):
    try:
        request_body = {
            "_source": ["description"],
            "query": {
                "terms": {"_id": [doc_id]}
            }
        }

        response = fetch_data_from_opensearch(INDEX_NAME, request_body, "hits", "hits")
        description = [
            {"description": x["_source"]["description"]}
            for x in response if "_source" in x and "description" in x["_source"]
        ]
        
        return description[0] if description else {}
    except Exception as e:
        print(f"Error fetching airline description: {e}")
        return {}


def read_airline_ko_description(doc_id: str):
    try: 
        request_body = {
            "_source": ["ko_description"],
            "query": {
                "terms": {"_id": [doc_id]}
            }
        }

        response = fetch_data_from_opensearch(INDEX_NAME, request_body, "hits", "hits")
        return {"description": response[0]["_source"]["ko_description"]} if response else {"description": ""}
    except Exception as e:
        print(f"Error fetching Korean description: {e}")
        return {"description": ""}


def check_ko_description(doc_id: str) -> bool:
    try:
        response = client.get(index=INDEX_NAME, id=doc_id)
        ko_description = response["_source"].get("ko_description", "")
        return ko_description == ""
    except Exception as e:
        print(f"Error checking Korean description: {e}")
        return True


def update_ko_description(doc_id: str, description: str) -> dict:
    try:
        doc = {
            "doc": {"ko_description": description},
            "doc_as_upsert": True 
        }

        response = client.update(index=INDEX_NAME, id=doc_id, body=doc)

        if response['result'] in ['updated', 'created']:
            return {"message": "Description updated successfully.", "status": "success"}
        else:
            raise HTTPException(status_code=500, detail="Failed to update description.")
    except (TransportError, RequestError) as e:
        raise HTTPException(status_code=400, detail=f"OpenSearch error: {str(e)}")
    except ConnectionError as e:
        raise HTTPException(status_code=500, detail=f"Connection error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")