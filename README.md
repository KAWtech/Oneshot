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

To start Oneshot, run ./start-oneshot.sh from the terminal inside the Oneshot directory.
   - further instructions are visible once Oneshot has started :3
To stop Oneshot, run ./stop-oneshot.sh form the terminal inside the Oneshot directory.


## Contact

For any problems/bugs/enhancements, please open an issue on this repo with the proper labels.

---

By using this system, users can quickly detect objects in images, generate point clouds, and visualize the results, all through a user-friendly web interface.
