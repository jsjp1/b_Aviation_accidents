from opensearchpy import OpenSearch
from parse import *
from config import *

client = OpenSearch(
    hosts=[OPENSEARCH_HOST],
    http_compress=True,
    http_auth=("admin", "admin"),
	use_ssl=True,
	client_cert=CLIENT_CERT,
	client_key=CLIENT_KEY,
	connection_class=RequestsHttpConnection
)


def create_index():
    body = {
        "settings": {
            "analysis": {
                "analyzer": {
                    "ngram_analyzer": {
                        "tokenizer": "ngram_tokenizer",
                        "filter": ["lowercase"]
                    }
                },
                "tokenizer": {
                    "ngram_tokenizer": {
                        "type": "ngram",
                        "min_gram": 3,
                        "max_gram": 5
                    }
                }
            },
            "index": {
                "max_ngram_diff": 2
            }
        },
        "mappings": {
            "properties": {
                "date": {"type": "date"},
                "time": {"type": "keyword"},
                "airline": {
                    "type": "text",
                    "analyzer": "ngram_analyzer",
                    "fields": {
                        "raw": {"type": "keyword"}
                    }
                },
                "aircraft_registration": {"type": "keyword"},
                "accident_type": {"type": "keyword"},
                "description": {"type": "text", "analyzer": "ngram_analyzer"},
                "fatalities": {"type": "integer"},
                "occupants": {"type": "integer"},
                "location": {"type": "text", "analyzer": "ngram_analyzer"},
                "phase": {"type": "keyword"},
                "aircraft_model": {"type": "keyword"},
                "aircraft_status": {"type": "keyword"}
            }
        }
    }

    if client.indices.exists(index=INDEX_NAME):
        print(f"Index '{INDEX_NAME}' already exists.")
    else:
        response = client.indices.create(index=INDEX_NAME, body=body)
        print(f"Index '{INDEX_NAME}' created: {response}")


if __name__ == "__main__":
    create_index()

    parse_init(client)
