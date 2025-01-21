import os
import json
from opensearchpy import OpenSearch, RequestsHttpConnection
from dotenv import load_dotenv

# config
load_dotenv()
OPENSEARCH_HOST = os.getenv('OPENSEARCH_HOST')
OPENSEARCH_ID = os.getenv('OPENSEARCH_ID')
OPENSEARCH_PASSWORD = os.getenv('OPENSEARCH_PASSWORD')

try:
  client = OpenSearch(
    hosts=[OPENSEARCH_HOST],
    http_compress=True,
    http_auth=(OPENSEARCH_ID, OPENSEARCH_PASSWORD),
    use_ssl=True,
    connection_class=RequestsHttpConnection
  )

  if client.ping():
      print("Opensearch Connection Success")
  else:
      print("OpenSearch Connection Fail")
  
  cluster_health = client.cluster.health()
  print("Cluster Status: ", cluster_health)
except Exception as e:
    print("Exception occur: ", str(e))