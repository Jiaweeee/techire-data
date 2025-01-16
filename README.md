## 1. Environment Setup

1. Copy the example environment file:
```
cp .env.example .env
```

2. Edit `.env` file with your actual configuration values:
```
DATABASE_URL=mysql://your_user:your_password@your_host:3306/your_database
```

Note: Never commit the `.env` file to version control as it may contain sensitive information.

## 2. Database Setup

### Connect to MySQL local server
```
mysql -h 0.0.0.0 -u root -p
```

### Database Viewer
Use Drizzle Studio to view and manage your database through a web interface:

1. Navigate to db-viewer directory:
```bash
cd db-viewer
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env file with your DATABASE_URL
```

4. Start Drizzle Studio:
```bash
npm run db:studio
```

Once started, access the database viewer at `http://localhost:4983` in your browser.

## 3. Project Components Setup

### Quick Start Script
Use the `local_dev.sh` script to start individual services. Open a separate terminal for each service you want to run:

```bash
# Start the Backend API service
./local_dev.sh api

# Start the Frontend application
./local_dev.sh ui

# Start the Database viewer
./local_dev.sh db:view

# Apply existing database migrations
./local_dev.sh db:migrate

# Generate a new database migration with a message
./local_dev.sh db:migrate "Add user table"

# Start the job data crawler
./local_dev.sh crawl

# Start the data processing service for extraction
./local_dev.sh process extract

# Start the data processing service for indexing
./local_dev.sh process index

# Elasticsearch operations
./local_dev.sh es init    # Initialize Elasticsearch index
./local_dev.sh es update  # Update index mapping
./local_dev.sh es delete  # Delete index

# Run data ingestion script
./local_dev.sh ingest
```

Make the script executable if needed:
```bash
chmod +x local_dev.sh
```

Each command will start the respective service in the current terminal window with live logs output.

### Backend API Service

1. Install dependencies:
```bash
cd backend
pip install -e .
pip install -r requirements.txt
```

2. Start the API service:
```bash
# Development mode (with auto-reload)
python -m backend.main

# Or production mode
gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

The service will be available at `http://localhost:8000`

#### API Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

#### Available Endpoints
- Search jobs: `POST /api/v1/jobs/search`
- Get job details: `GET /api/v1/jobs/detail`
- List companies: `GET /api/v1/companies`
- Get company details: `GET /api/v1/companies/detail`

### Frontend Application

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Data Processing Service
This service does all the data processing work, including job analysis, indexing, and updating the database.

Start the data processing service:
```bash
# Development mode
python -m data_processor.main
```

The service will:
- Monitor the database for new or failed job analyses
- Process jobs in batches
- Update analysis results in real-time

To gracefully stop the service, press Ctrl+C. The service will:
- Mark any in-progress analysis as failed
- Clean up resources before shutting down

## 4. Data Collection

### Add new companies to scrape
1. Add new company info to `data_storage/data/companies.json`
2. Run `python data_storage/scripts/ingest.py` to insert company info into database
3. Add new spider file to `data_scrape/spiders`, e.g. `microsoft.py`

### Run spiders
There are two ways to run the spiders:

1. Run all spiders at once:
```
python run_spiders.py
```

2. Run a specific spider:
```
scrapy crawl <spider_name>
```

## 5. Database Management

### Database Migrations
After modifying database models in `data_storage/models.py`:

1. Generate a new migration:
```
python -m data_storage.scripts.migrate "描述你的改动"
```

2. Apply existing migrations (e.g., when deploying to a new environment):
```
python -m data_storage.scripts.migrate
```

## 6. Troubleshooting
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