#!/bin/sh

echo "args: FastAPI_Restart, OpenSearch_Restart, Jenkins_Restart, Init_crawling"
echo ""

if [ $# -lt 4 ]; then
  echo "usage: bash $0 [1 || else] [1 || else] [1 || else] [1 || else]"
  exit 1
fi

restart_fastapi=$1
restart_opensearch=$2
restart_jenkins=$3
init_crawl=$4

mkdir -p ./logs

if [ "$restart_fastapi" = "1" ]; then
  echo "Restarting FastAPI Server..."
  cd ./app
  nohup python3 main.py > ../logs/api_server.log 2>&1 &
  echo "FastAPI server restarted. Logs are in ./log"
  echo ""
  cd ..
fi

if [ "$restart_opensearch" = "1" ]; then
  echo "Restarting OpenSearch container..."
  cd ./opensearch
  #docker-compose down
  docker-compose up -d
  echo "OpenSearch container restarted."
  echo ""
  cd ..
fi

if [ "$restart_jenkins" = "1" ]; then
  echo "Restarting Jenkins container..."
  cd ./daily_crawl
  docker-compose up -d
  echo "Jenkins container restarted."
  echo ""
  cd ..
fi

if [ "$init_crawl" = "1" ]; then
  echo "Initializing crawlign process..."
  cd ./init_crawl
  nohup python3 main.py > ../logs/crawl.log 2>&1 &
  echo "Crawling initialized. Logs are in ./log"
  echo ""
  cd ..
fi