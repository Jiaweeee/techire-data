#!/bin/bash

# Function to print usage
print_usage() {
    echo "Usage: $0 [api|ui|db:view|db:migrate|crawl|process [type]|es [action]|ingest]"
    echo "Examples:"
    echo "  $0 api       # Start Backend API service"
    echo "  $0 ui        # Start Frontend application"
    echo "  $0 db:view   # Start Database viewer"
    echo "  $0 db:migrate # Apply existing migrations"
    echo "  $0 db:migrate \"Add user table\" # Generate new migration"
    echo "  $0 crawl     # Start job data crawler"
    echo "  $0 process extract  # Start info extraction service"
    echo "  $0 process index   # Start job indexing service"
    echo "  $0 es init   # Initialize Elasticsearch index"
    echo "  $0 es update # Update index mapping"
    echo "  $0 es delete # Delete index"
    echo "  $0 ingest    # Run data ingestion script"
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
        python run_spiders.py --spider "$2"
    else
        echo "Crawling all spiders"
        python run_spiders.py
    fi
}

# Function to start job analysis service
start_processing() {
    if [ -n "$2" ]; then
        echo "Starting data processing service ($2)..."
        python -m data_processor.main "$2"
    else
        echo "Error: Processing type not specified"
        echo "Available types: extract, index"
        exit 1
    fi
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
    "help")
        print_usage
        ;;
    "api")
        start_api
        ;;
    "ui")
        start_frontend
        ;;
    "db:view")
        start_db
        ;;
    "db:migrate")
        start_migrate "$1" "$2"
        ;;
    "crawl")
        start_crawl "$1" "$2"
        ;;
    "process")
        start_processing "$1" "$2"
        ;;
    "es")
        manage_es "$1" "$2"
        ;;
    "ingest")
        echo "Running data ingestion script..."
        python -m data_storage.scripts.ingest
        ;;
    *)
        echo "Error: Invalid service name: $1"
        print_usage
        exit 1
        ;;
esac