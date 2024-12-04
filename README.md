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
# Start the Job Search API service
./local_dev.sh api

# Start the Frontend application
./local_dev.sh ui

# Start the Database viewer
./local_dev.sh db

# Start the job data crawler
./local_dev.sh crawl

# Start the job analysis service
./local_dev.sh analysis

# Run database migrations
./local_dev.sh migrate

# Generate a new migration with a message
./local_dev.sh migrate "Add user table"
```

Make the script executable if needed:
```bash
chmod +x local_dev.sh
```

Each command will start the respective service in the current terminal window with live logs output.

### Job Search API Service

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

#### API Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

#### Available Endpoints
- Search jobs: `GET /api/v1/jobs/search`
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

### Job Analysis Service
This service analyzes job postings using LLM to extract structured information like salary range, required skills, and experience level.

1. Set up environment variables:
```bash
# In .env file
OPENAI_API_KEY=your_api_key
OPENAI_BASE_URL=https://api.openai.com/v1  # or your custom endpoint
CHAT_MODEL=gpt-3.5-turbo  # or other supported models
```

2. Start the analysis service:
```bash
# Development mode
python -m job_analysis.main
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