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

- Every night at midnight, the daily_crawl pipeline is executed in the Docker Jenkins container.
- ## pipeline stage
  1. 'check_connection'
  2. 'extract_accident_dates'
  3. 'exclude_exist_dates'
  4. 'parse'

### 4. launch fastapi server

`python app/main.py`

- [api documentation](http://avcc.jieeen.kr:8000/docs)

## PyTest

- Whenever a push action occurs on the main branch, pytest is executed by GitHub Actions.

### Test List

1. Root Endpoint Tests

   • test_read_root: Tests the root endpoint (/).

2. Accident Data Tests

   • test_read_accident: Verifies the /api/accident/ endpoint returns the expected keys.

   • test_read_accidents: Checks /api/accidents with pagination (start and size parameters).

3. Airline Suggestions Tests

   • test_read_airline_suggestions_exist: Ensures /api/suggestions/{airline} returns results for existing airlines.

   • test_read_airline_suggestions_no_exist: Ensures /api/suggestions/{airline} returns no results for non-existent airlines.

4. Airline Information Tests

   • test_read_airline_info_exist: Verifies /api/information/{airline} returns valid data for existing airlines.

   • test_read_airline_info_no_exist: Ensures /api/information/{airline} returns no data for non-existent airlines.

5. Airline Description Tests

   • test_read_airline_description_exist: Checks /api/description/{\_id} for existing descriptions.

   • test_read_airline_description_no_exist: Ensures /api/description/{\_id} returns empty for non-existent IDs.

6. Korean Description Tests

   • test_read_airline_ko_description: Tests /api/ko_description/{\_id} endpoint.

   • test_check_ko_description: Checks /api/check_ko_description/{\_id} for the ko_description_empty field.
