import os
import json
from opensearchpy import OpenSearch, RequestsHttpConnection
from dotenv import load_dotenv

load_dotenv()

OPENSEARCH_HOST = os.getenv('OPENSEARCH_HOST')
OPENSEARCH_ID = os.getenv('OPENSEARCH_ID')
OPENSEARCH_PASSWORD = os.getenv('OPENSEARCH_PASSWORD')

client = OpenSearch(
  hosts=[OPENSEARCH_HOST],
  http_compress=True,
  http_auth=(OPENSEARCH_ID, OPENSEARCH_PASSWORD),
  use_ssl=True,
  connection_class=RequestsHttpConnection
)

cluster_health = client.cluster.health()
with open('/var/jenkins_scripts/cluster_health.json', 'w') as f:
  json.dump(cluster_health, f)