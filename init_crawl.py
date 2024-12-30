from bs4 import BeautifulSoup
import requests
from opensearchpy import OpenSearch

OPENSEARCH_HOST = "http://localhost:9200"
INDEX_NAME = "aviation_accidents"

client = OpenSearch(
    hosts=[OPENSEARCH_HOST],
    http_compress=True,
    http_auth=("admin", "admin")
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
                "airline_name": {
                    "type": "text",
                    "analyzer": "ngram_analyzer"
                },
                "description": {
                    "type": "text",
                    "analyzer": "ngram_analyzer"
                },
                "location": {
                    "type": "text",
                    "analyzer": "ngram_analyzer"
                }
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
