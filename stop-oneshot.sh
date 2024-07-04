#!/bin/bash

print_oneshot_logo() {
  # ASCII Art
  echo "   ____   _   __ ______ _____  __  __ ____  ______ "
  echo "  / __ \ / | / // ____// ___/ / / / // __ \/_  __/ "
  echo " / / / //  |/ // __/   \__ \ / /_/ // / / / / /    "
  echo "/ /_/ // /|  // /___  ___/ // __  // /_/ / / /     "
  echo "\____//_/ |_//_____/ /____//_/ /_/ \____/ /_/      "
  echo "                                                   "
}

print_oneshot_logo

# Function to provide feedback to the user
provide_feedback() {
  echo "$1"
}

# Provide feedback to the user
provide_feedback "Stopping Flask, NodeODM, and OpenSplat containers..."

# Stop the Flask, NodeODM, and OpenSplat containers
docker compose down

# Check if the cvat directory exists
if [ -d "cvat" ]; then
  cd cvat || {
    provide_feedback "Failed to change directory to cvat."
    exit 1
  }

  # Provide feedback to the user
  provide_feedback "Stopping CVAT containers..."

  # Stop CVAT containers
  docker compose -f docker-compose.yml -f docker-compose.dev.yml -f components/serverless/docker-compose.serverless.yml down

  # Provide feedback to the user
  provide_feedback "CVAT containers stopped successfully."
  cd ..
else
  provide_feedback "CVAT directory not found. Nothing to stop."
fi

# Provide feedback to the user
provide_feedback "All services stopped. Have a great day!"
