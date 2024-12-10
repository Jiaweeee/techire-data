#!/bin/bash

# Function to print usage
print_usage() {
    echo "Usage: $0 [api|ui|db|crawl|process|migrate [message]|es [action]]"
    echo "Examples:"
    echo "  $0 api       # Start Backend API service"
    echo "  $0 ui        # Start Frontend application"
    echo "  $0 db        # Start Database viewer"
    echo "  $0 crawl     # Start job data crawler"
    echo "  $0 process   # Start data processing service"
    echo "  $0 migrate   # Apply existing migrations"
    echo "  $0 migrate \"Add user table\" # Generate new migration"
    echo "  $0 es init   # Initialize Elasticsearch index"
    echo "  $0 es update # Update index mapping"
    echo "  $0 es delete # Delete index"
}

# Check if argument is provided
if [ $# -eq 0 ]; then
    echo "Error: No service specified"
    print_usage
    exit 1
fi

# Function to start API service
start_api() {
    echo "Starting Backend API service..."
    cd backend && python -m backend.main
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
    if [ -n "$2" ]; then
        echo "Crawling specific spider: $2"
        python run_spiders.py "$2"
    else
        echo "Crawling all spiders"
        python run_spiders.py
    fi
}

# Function to start job analysis service
start_processing() {
    echo "Starting data processing service..."
    python -m data_processor.main
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

# Function to manage Elasticsearch operations
manage_es() {
    case "$2" in
        "init")
            echo "Initializing Elasticsearch index..."
            python -m data_processor.scripts.init_es
            ;;
        "update")
            echo "Updating Elasticsearch index mapping..."
            python -m data_processor.scripts.update_mapping
            ;;
        "delete")
            echo "Deleting Elasticsearch index..."
            python -m data_processor.scripts.delete_index
            ;;
        *)
            echo "Error: Invalid ES action: $2"
            echo "Available actions: init, update, delete"
            exit 1
            ;;
    esac
}

# Process arguments
case "$1" in
    "api")
        start_api
        ;;
    "ui")
        start_frontend
        ;;
    "db")
        start_db
        ;;
    "crawl")
        start_crawl "$1" "$2"
        ;;
    "process")
        start_processing
        ;;
    "migrate")
        start_migrate "$1" "$2"
        ;;
    "es")
        manage_es "$1" "$2"
        ;;
    *)
        echo "Error: Invalid service name: $1"
        print_usage
        exit 1
        ;;
esac