# Oneshot 

## Overview
Oneshot is a system designed to detect objects of interest in images, generate a point cloud, and visualize the results in a front-end viewer. The system leverages Flask for the web server, CVAT for object detection, ODM for point cloud generation, and Open Splat for visualization.

## Components

1. **Flask Web Server**
   - Receives and processes images.

2. **CVAT (Computer Vision Annotation Tool)**
   - Detects objects of interest in the images.

3. **ODM (OpenDroneMap)**
   - Generates a point cloud from the detected objects.

4. **Open Splat**
   - Visualizes the generated point cloud.

5. **Front End Viewer**
   - Provides an interface for users to view the results.

## Workflow

1. **Upload Images**
   - Users upload images to the Flask web server.
   
2. **Object Detection**
   - The images are passed to CVAT, which detects objects of interest.

3. **Point Cloud Generation**
   - The detected objects are sent to ODM, which generates a point cloud.

4. **Visualization**
   - The generated point cloud is visualized using Open Splat.
   
5. **Front End Viewing**
   - Users can view the visualized point cloud through the front-end viewer.

## Getting Started!

1. Before cloning, the user should ensure they are running on Linux have Docker set up on their system.
2. Navigate to the the directory containing *docker-compose.yml*. Execute ```docker-compose up -d``` to start the Flask, NodeODM and OpenSplat containers
3. Visit the web server at http://127.0.0.1:5000 and follow the instructions.
4. cd cvat && docker compose -f docker-compose.yml -f docker-compose.dev.yml -f components/serverless/docker-compose.serverless.yml up -d --build
5. sudo chmod +x nuctl-1.11.24-linux-amd64
6. sudo ln -sf nuctl-1.11.24-linux-amd64 /usr/bin/nuctl
7. sudo ./nuctl-1.11.24-linux-amd64 create project cvat
8. sudo ./nuctl deploy --project-name cvat --path "/home/arshia/Oneshot/cvat/serverless/onnx/WongKinYiu/yolov7/nuclio" --platform local
9. Upload images and enjoy! To monitor task progress you can visit http://127.0.0.1:3000.


## Contact

For any problems/bugs/enhancements, please open an issue on this repo with the proper labels.

---

By using this system, users can quickly detect objects in images, generate point clouds, and visualize the results, all through a user-friendly web interface.
