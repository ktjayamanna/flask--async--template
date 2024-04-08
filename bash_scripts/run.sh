#!/bin/bash

# Define the Docker Compose project name
PROJECT_NAME="my_project"

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "Docker does not seem to be running, make sure Docker is running and try again."
    exit 1
fi

# Navigate to the script's directory (optional)
# cd "$(dirname "$0")"

# Build and start the containers
echo "Building and starting containers..."
docker-compose -p "$PROJECT_NAME" up --build -d

# Check if the containers started successfully
if [ $? -eq 0 ]; then
    echo "Containers started successfully."
else
    echo "There was an error starting the containers."
    exit 1
fi


