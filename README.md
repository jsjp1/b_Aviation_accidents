# AVCC BackEnd

## Environment

- Ubuntu 20.04.6 LTS
- GNU/Linux 5.15.0-1072-oracle aarch64
- Oracle Instance
- RAM 12GB

## Setting

### 1. Opensearch

#### prerequisite

```
sudo apt-get update -y
sudo apt-get install build-essential
sudo apt-get install libcairo2
sudo apt-get install python3
sudo apt-get install pip
```

#### port allow

```
sudo ufw allow 9200/tcp 9300/tcp 9600/tcp 5601/tcp
```

#### docker install

- install docker

```
sudo apt install docker.io
```

- add docker to group

```
sudo usermod -aG docker $USER
```

- start docker daemon

```
sudo systemctl start docker
```

- start opensearch by docker-compose

```
docker-compose up -d
```

### 2. Initial Crawling

- The process of uploading a large amount of existing data to opensearch

#### pip install

```
pip install --upgrade pip
pip install bs4 fastapi uvicorn[standard] pydantic requests
```

#### launch init_crawl

`python init_crawl/main.py`

### 3. Daily Crawling

- TODO

### 4. launch fastapi server

`python app/main.py`

- [api documentation](http://avcc.jieeen.kr:8000/docs)
