## Connect to MySQL local server
```
mysql -h 0.0.0.0 -u root -p
```

## Add new companies to scrape

1. Add new company info to `data_storage/data/companies.json`
2. Run `python data_storage/scripts/ingest.py` to insert company info into database
3. Add new spider file to `data_scrape/spiders`, e.g. `microsoft.py`

## Run spiders
There are two ways to run the spiders:

1. Run all spiders at once:
```
python run_spiders.py
```

2. Run a specific spider:
```
scrapy crawl <spider_name>
```

## Database Migrations

After modifying database models in `data_storage/models.py`:

1. Create and apply new migration:
```
python -m data_storage.scripts.migrate "描述你的改动"
```

2. If you just want to run existing migrations (e.g., when deploying to a new environment):
```
python -m data_storage.scripts.migrate
```

## Troubleshooting
Cannot find module named `data_storage`
```
Traceback (most recent call last):
  File "/Users/jiawei.an/code/TechHire/data_scrape/data_storage/scripts/ingest.py", line 6, in <module>
    from data_storage.models import Base
ModuleNotFoundError: No module named 'data_storage'
```

Solution:
```
pip install -e .
```

## Environment Setup

1. Copy the example environment file:
```
cp .env.example .env
```

2. Edit `.env` file with your actual configuration values:
```
DATABASE_URL=mysql://your_user:your_password@your_host:3306/your_database
```

Note: Never commit the `.env` file to version control as it may contain sensitive information.

## Job Search API Service

### Setup and Run
1. Install dependencies:
```bash
cd job_search
pip install -e .
pip install fastapi uvicorn
```

2. Start the API service:
```bash
# Development mode (with auto-reload)
python -m job_search.main

# Or production mode
gunicorn job_search.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

The service will be available at `http://localhost:8000`

### API Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Available Endpoints
- Search jobs: `GET /api/v1/jobs/search`
- Get job details: `GET /api/v1/jobs/detail`
- List companies: `GET /api/v1/companies`
- Get company details: `GET /api/v1/companies/detail`