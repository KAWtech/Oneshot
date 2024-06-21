from flask import Flask, request, jsonify
import os
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def label_images_with_cvat(image_paths):
    # Add CVAT API integration here
    pass

def process_with_nodeodm(image_paths):
    # Add NodeODM API integration here
    pass

def start_opensplat_process(ply_file, images, camera_poses):
    # Add opensplat process integration here
    pass


# Frontend calls this route to upload images to the backend
@app.route('/upload', methods=['POST'])
def upload_images():
    files = request.files.getlist('images')
    for file in files:
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return jsonify({'message': 'Images uploaded successfully'}), 200

# Once user presses "Run Task" on the frontend, this is called and uses the images
# the user uploaded and does CVAT labelling, and then starts NodeODM with those images
@app.route('/process_images', methods=['POST'])
def process_images():
    files = request.files.getlist('images')
    image_paths = []
    for file in files:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        image_paths.append(file_path)
    
    label_images_with_cvat(image_paths)
    process_with_nodeodm(image_paths)
    return jsonify({'message': 'Images processed with CVAT and NodeODM successfully'}), 200


# Once NodeODM is at the last stage, it should call this route and POST the .ply, camera poses, and images
# And this route will use those and send them in to start OpenSplat
# NEED TO PASS IN FILES FROM NODEODM HERE
@app.route('/process_opensplat', methods=['POST'])
def process_opensplat():
    data = request.json
    ply_file = data['ply_file']
    images = data['images']
    camera_poses = data['camera_poses']
    
    start_opensplat_process(ply_file, images, camera_poses)
    return jsonify({'message': 'OpenSplat process started successfully'}), 200

# Once OpenSplat is done running, it should call this route and then the splat is saved for viewing in our DB
@app.route('/task-complete')
def task_complete():
    # This is called at the end of opensplat
    # We store our data in here from opensplat in our DB so its viewable in the viewer
    pass

if __name__ == '__main__':
    app.run(debug=True)