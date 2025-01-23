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

ROOT_DIR="$(pwd)"
LOG_DIR="./logs"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")

mkdir -p "$LOG_DIR"

kill_process_on_port() {
  local port=$1
  local pid
  pid=$(lsof -i :"$port" | grep LISTEN | awk '{print $2}')
  if [ -n "$pid" ]; then
    echo "Killing process on port $port with PID: $pid"
    sudo kill -9 $pid
  else
    echo "No process is listening on port $port"
  fi
}

if [ "$restart_fastapi" = "1" ]; then
  echo "========== Restarting FastAPI Server =========="
  cd ./app || exit
  kill_process_on_port 8000
  touch "$ROOT_DIR/$LOG_DIR/api_server_$TIMESTAMP.log"
  nohup python3 main.py > "$ROOT_DIR/$LOG_DIR/api_server_$TIMESTAMP.log" 2>&1 &
  echo "FastAPI server restarted. Logs are in $ROOT_DIR/$LOG_DIR/api_server_$TIMESTAMP.log"
  echo ""
  cd - || exit
fi

if [ "$restart_opensearch" = "1" ]; then
  echo "========== Restarting OpenSearch Container =========="
  cd ./opensearch || exit
  docker-compose down
  docker-compose up -d
  if [ $? -eq 0 ]; then
    echo "OpenSearch container restarted successfully."
  else
    echo "Failed to restart OpenSearch container."
  fi
  echo ""
  cd - || exit
fi

if [ "$restart_jenkins" = "1" ]; then
  echo "========== Restarting Jenkins Container =========="
  cd ./daily_crawl || exit
  docker-compose down
  docker-compose up -d
  if [ $? -eq 0 ]; then
    echo "Jenkins container restarted successfully."
  else
    echo "Failed to restart Jenkins container."
  fi
  echo ""
  cd - || exit
fi

if [ "$init_crawl" = "1" ]; then
  echo "========== Initializing Crawling Process =========="
  cd ./init_crawl || exit
  nohup python3 main.py > "$ROOT_DIR/$LOG_DIR/crawl_$TIMESTAMP.log" 2>&1 &
  echo "Crawling initialized. Logs are in $ROOT_DIR/$LOG_DIR/crawl_$TIMESTAMP.log"
  echo ""
  cd - || exit
fi