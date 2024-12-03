#!/bin/bash

# Function to print usage
print_usage() {
    echo "Usage: $0 [api|frontend|db|crawl|analysis|migrate [message]|all]"
    echo "Examples:"
    echo "  $0 api       # Start Job Search API service"
    echo "  $0 frontend  # Start Frontend application"
    echo "  $0 db       # Start Database viewer"
    echo "  $0 crawl    # Start job data crawler"
    echo "  $0 analysis # Start job analysis service"
    echo "  $0 migrate  # Apply existing migrations"
    echo "  $0 migrate \"Add user table\" # Generate new migration"
    echo "  $0 all      # Start all services"
}

# Check if argument is provided
if [ $# -eq 0 ]; then
    echo "Error: No service specified"
    print_usage
    exit 1
fi

# Function to start API service
start_api() {
    echo "Starting Job Search API service..."
    cd job_search && python -m job_search.main
}

# Function to start Frontend
start_frontend() {
    echo "Starting Frontend application..."
    cd frontend && npm run dev
}

# Function to start DB viewer
start_db() {
    echo "Starting Database viewer..."
    cd db-viewer && npm run db:studio
}

# Function to start spider crawling
start_crawl() {
    echo "Starting job data crawler..."
    python run_spiders.py
}

# Function to start job analysis service
start_analysis() {
    echo "Starting job analysis service..."
    python -m job_analysis.main
}

# Function to run database migrations
start_migrate() {
    if [ -n "$2" ]; then
        echo "Generating new migration: $2"
        python -m data_storage.scripts.migrate "$2"
    else
        echo "Applying existing migrations..."
        python -m data_storage.scripts.migrate
    fi
}

# Process arguments
case "$1" in
    "api")
        start_api
        ;;
    "frontend")
        start_frontend
        ;;
    "db")
        start_db
        ;;
    "crawl")
        start_crawl
        ;;
    "analysis")
        start_analysis
        ;;
    "migrate")
        start_migrate "$1" "$2"
        ;;
    "all")
        echo "Error: Cannot start all services in the current terminal."
        echo "Please start each service in a separate terminal:"
        echo "./start_local_dev.sh api"
        echo "./start_local_dev.sh frontend"
        echo "./start_local_dev.sh db"
        echo "./start_local_dev.sh crawl"
        echo "./start_local_dev.sh analysis"
        echo "./start_local_dev.sh migrate"
        exit 1
        ;;
    *)
        echo "Error: Invalid service name: $1"
        print_usage
        exit 1
        ;;
esac