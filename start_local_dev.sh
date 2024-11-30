#!/bin/bash

# Function to print usage
print_usage() {
    echo "Usage: $0 [api|frontend|db]"
    echo "Examples:"
    echo "  $0 api       # Start Job Search API service"
    echo "  $0 frontend  # Start Frontend application"
    echo "  $0 db       # Start Database viewer"
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
    "all")
        echo "Error: Cannot start all services in the current terminal."
        echo "Please start each service in a separate terminal:"
        echo "./start_local_dev.sh api"
        echo "./start_local_dev.sh frontend"
        echo "./start_local_dev.sh db"
        exit 1
        ;;
    *)
        echo "Error: Invalid service name: $1"
        print_usage
        exit 1
        ;;
esac