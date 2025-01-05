from opensearchpy import OpenSearch, RequestsHttpConnection
from config import *
from collections import OrderedDict
from datetime import datetime

client = OpenSearch(
    hosts=[OPENSEARCH_HOST],
    http_compress=True,
    http_auth=("admin", "admin"),
    use_ssl=True,
    connection_class=RequestsHttpConnection
)


def read_accidents(start: int, size: int):
    request_body = {
        "from": start,
        "size": size,
        "sort": [
            {
                "date": {
                    "order": "desc"
                }
            }
        ],
        "_source": ["date", "time", "airline", "fatalities", "occupants", "location"]
    }

    response = client.search(index=INDEX_NAME, body=request_body)
    response = [x["_source"] for x in response["hits"]["hits"]]
    return response


def read_airline_suggestions(airline: str):
    request_body = {
        "query": {
            "bool": {
                "should": [
                    {
                        "match": {
                            "airline": {
                                "query": airline,
                                "fuzziness": "AUTO",
                            },
                        },
                    },
                    {
                        "wildcard": {
                            "airline.raw": {
                                "value": "*$query*",
                                "boost": 0.5,
                            },
                        },
                    },
                ],
            },
        },
    }

    response = client.search(index=INDEX_NAME, body=request_body)
    response = response["hits"]["hits"]

    response = [x["_source"]["airline"]
                for x in response if x["_source"]["airline"]]

    unique_response = list(OrderedDict.fromkeys(response))[:5]

    return unique_response


def read_airline_info(airline: str):
    request_body = {
        "query": {
            "term": {
                "airline.raw": {
                    "value": airline
                }
            }
        }
    }

    response = client.search(index=INDEX_NAME, body=request_body)
    response = response["hits"]["hits"]
    response = [x["_source"] for x in response]

    sorted_response = sorted(response, key=lambda x: datetime.strptime(
        x['date'], '%Y-%m-%d'), reverse=True)

    return sorted_response
