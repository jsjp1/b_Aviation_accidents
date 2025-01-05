from opensearchpy import OpenSearch, RequestsHttpConnection
from parse import *
from config import *
from index_body import *

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
    if client.indices.exists(index=INDEX_NAME):
        print(f"Index '{INDEX_NAME}' already exists.")
    else:
        response = client.indices.create(index=INDEX_NAME, body=index_body)
        print(f"Index '{INDEX_NAME}' created: {response}")


if __name__ == "__main__":
    create_index()

    parse_init(client)
