#!/bin/sh

if [ $# -lt 3 ]; then
  echo "usage: bash $0 <1 || 0> <1 || 0> <1 || 0>"
  exit 1
fi

echo "Restart FastAPI Server: $1"
echo "Restart Opensearch Container: $2"
echo "Require Init Crawling: $3"
echo ""

restart_fastapi=$1
restart_opensearch=$2
init_crawl=$3

mkdir -p ./logs

if [ "$restart_fastapi" = "1" ] || [ "$restart_fastapi" = "true" ]; then
  echo "Restarting FastAPI Server..."
  cd ./app
  nohup python3 main.py > ../logs/api_server.log 2>&1 &
  echo "FastAPI server restarted. Logs are in ./log"
  cd ..
fi

if [ "$restart_opensearch" = "1" ] || [ "$restart_opensearch" = "true" ]; then
  echo "Restarting OpenSearch container..."
  cd ./opensearch
  #docker-compose down
  docker-compose up -d
  echo "OpenSearch container restarted."
fi

if [ "$init_crawl" = "1" ] || [ "$init_crawl" = "true" ]; then
  echo "Initializing crawlign process..."
  cd ./init_crawl
  nohup python3 main.py > ../logs/crawl.log 2>&1 &
  echo "Crawling initialized. Logs are in ./log"
  cd ..
fi