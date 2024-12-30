from bs4 import BeautifulSoup
import requests
from opensearchpy import OpenSearch

OPENSEARCH_HOST = "http://localhost:9200"

client = OpenSearch(
    hosts=[OPENSEARCH_HOST],
    http_auth=('admin', 'admin')
)
