#!/bin/bash

print_instructions_box() {
  echo " *************** "
  echo " * INSTRUCTIONS * "
  echo " *************** "
}

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

# Start CVAT containers with additional configurations
cd cvat || {
  echo "CVAT directory not found."
  exit 1
}

# Function to get the IP address of the machine
get_ip_address() {
  ip_address=$(hostname -I | awk '{print $1}')
  echo "$ip_address"
}

# Automatically determine the IP address
CVAT_HOST=$(get_ip_address)

# Export the CVAT_HOST environment variable
export CVAT_HOST

# Provide feedback to the user
echo "CVAT_HOST automatically set to $CVAT_HOST"

echo "Starting CVAT containers..."
docker compose -f docker-compose.yml -f docker-compose.dev.yml -f components/serverless/docker-compose.serverless.yml up -d --build

# Set permissions and create symlink for nuctl
sudo chmod +x nuctl-1.11.24-linux-amd64
sudo ln -sf "$(pwd)/nuctl-1.11.24-linux-amd64" /usr/bin/nuctl

# Create Nuclio project and deploy function
echo "Creating Nuclio project and deploying function..."
sudo ./nuctl-1.11.24-linux-amd64 create project cvat
sudo ./nuctl-1.11.24-linux-amd64 deploy --project-name cvat --path "serverless/onnx/WongKinYiu/yolov7/nuclio" --platform local

cd ..

# Start the Flask, NodeODM, and OpenSplat containers
echo "Starting Flask, NodeODM, and OpenSplat containers..."
docker compose up -d

# Instructions for uploading images

print_oneshot_logo
print_instructions_box
echo "Oneshot has been successfully started! Happy Splatting!"
echo "Visit the main Oneshot webpage at http://127.0.0.1:5000"
echo "Here you can upload images and view the results of the object detection model."
echo "To monitor task progress you can visit http://127.0.0.1:3000"
echo "----------------------------------------------------------------------------------------------"
echo "To visit CVAT, go to http://$CVAT_HOST:8080 and sign-up/login!"
