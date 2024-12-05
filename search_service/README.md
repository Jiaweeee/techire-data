# Search Service

A search service built with Elasticsearch for job search functionality.

## Prerequisites

- Docker
- Python 3.8+
- pip

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Deploy Elasticsearch and Kibana

First, pull the required Docker images:

```bash
# Pull Elasticsearch
docker pull docker.elastic.co/elasticsearch/elasticsearch:8.12.1

# Pull Kibana
docker pull docker.elastic.co/kibana/kibana:8.12.1
```
Then create network and start services:

```bash
# Create network
docker network create elastic

# Start Elasticsearch
docker run -d \
--name elasticsearch \
--net elastic \
-p 9200:9200 \
-p 9300:9300 \
-e "discovery.type=single-node" \
docker.elastic.co/elasticsearch/elasticsearch:8.12.1

# Start Kibana
docker run -d \
--name kibana \
--net elastic \
-p 5601:5601 \
docker.elastic.co/kibana/kibana:8.12.1
```

### 3. Configure Elasticsearch and Kibana

After deployment, you need to configure the services:

```bash
# Get elastic user password from Elasticsearch logs
docker logs elasticsearch | grep "Password"

# If password not found, reset it
docker exec -it elasticsearch /bin/bash
bin/elasticsearch-reset-password -u elastic -i

# Get Kibana enrollment token
docker exec -it elasticsearch /bin/bash
bin/elasticsearch-create-enrollment-token -s kibana

# Get Kibana verification code
docker exec -it kibana /bin/bash
bin/kibana-verification-code
```

Configuration steps:
1. Copy the elastic user password
2. Visit Kibana at http://localhost:5601
3. Paste the enrollment token when prompted
4. Enter the verification code
5. Log in with:
   - Username: elastic
   - Password: (the password from step 1)

### 4. Initialize Elasticsearch

Run the initialization script to create index and import data:

```bash
python -m search_service.scripts.init_es
```

### 5. Start Search Service

```bash
python -m search_service.main
```

### Additional Commands

Delete Elasticsearch index:
```bash
python -m search_service.scripts.delete_index
```

## Services

- Search Service: http://localhost:8001
- Elasticsearch: http://localhost:9200
- Kibana: http://localhost:5601

## API Documentation

After starting the service, visit:
- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc