from flask import Flask, request, jsonify, render_template
import json
import os
import logging
import requests
import time
app = Flask(__name__)
UPLOAD_FOLDER = '/home/kss/Desktop/oneshot/Oneshot/flask/uploads'
RESULT_FOLDER = 'results'
os.makedirs(RESULT_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
logging.basicConfig(level=logging.DEBUG)

def label_images_with_cvat(image_paths):
    # Add CVAT API integration here
    pass

def process_with_nodeodm(image_paths):
    # Log the image paths to be processed
    logging.info("Starting NodeODM processing for images: %s", image_paths)
    # NodeODM API URL for creating a new task
    url = "http://127.0.0.1:3000/task/new"
    uuid = ""
    # Prepare the files for the form-data request
    files = []
    for path in image_paths:
        files.append(('images', (os.path.basename(path), open(path, 'rb'), 'image/jpeg')))
    # Define options
    options = json.dumps([
        {"name": "end-with", "value": "opensfm"},
    ])
    data = {
        'options': options
    }

    try:
        # NodeODM POST request ending at sparse point cloud
        response = requests.post(url, files=files, data=data)
        if response.status_code == 200:
            task_info = response.json()
            uuid = task_info.get('uuid')
            logging.info("Task created successfully: %s", task_info)
            # return jsonify({'message': 'NodeODM task created successfully', 'Task Info': task_info}), 200
        else:
            logging.error("Failed to create task, status code: %d", response.status_code)
            # return jsonify({'error': 'Failed to create NodeODM task'}), response.status_code
    except Exception as e:
        logging.error("Error when calling NodeODM API: %s", str(e))
        # return jsonify({'error': 'Error when calling NodeODM API', 'exception': str(e)}), 500
    finally:
        # Close files
        for _, file_tuple in files:
            file_tuple[1].close()
    time.sleep(50) # ******THIS IS A HARDCODED ASYNC HELPER, NEED TO MAKE IT ASYNC FOR REAL******
    return uuid
    


def start_opensplat_process(uuid):
    # Add opensplat process integration here
    # Construct the path to the NodeODM task data
    task_data_path = f"/var/www/data/{uuid}"
    output_path = f"{task_data_path}/splat.ply"
    # Log the path for debugging
    print(f"Starting OpenSplat processing for task at: {task_data_path}")

    # Assuming we need to call OpenSplat with this path
    # Replace 'opensplat_executable_path' with the actual path to your OpenSplat executable if necessary
    opensplat_command = f"docker exec oneshot_opensplat_1 /code/build/opensplat {task_data_path} -o {output_path} -n 100"

    try:
        # Import subprocess to execute the external command
        import subprocess

        # Run the OpenSplat process
        result = subprocess.run(opensplat_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Check if the OpenSplat process was successful
        if result.returncode == 0:
            logging.info("Output:", result.stdout)
            logging.info("OpenSplat processing completed successfully.")
        else:
            logging.info("OpenSplat processing failed.")
            logging.info("Error:", result.stderr)

    except subprocess.CalledProcessError as e:
        print(f"OpenSplat command failed with {e}")

@app.route('/')
def index():
    return render_template('index.html')

# Frontend calls this route to upload images to the backend
@app.route('/upload', methods=['POST'])
def upload_images():
    # Clean up the upload folder before saving new files
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
                logging.info(f"Deleted file {file_path}")
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
                logging.info(f"Deleted directory {file_path}")
        except Exception as e:
            logging.error(f"Failed to delete {file_path}: {e}")
            return jsonify({'error': str(e)}), 500
    files = request.files.getlist('images')
    if not files:
        logging.error("No files received for upload")
        return jsonify({'error': 'No files received'}), 400
    for idx, file in enumerate(files):
        filename = f"{idx}.jpg"
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        try:
            file.save(file_path)
            logging.info(f"Saved file {filename} to {file_path}")
        except Exception as e:
            logging.error(f"Error saving file {filename}: {e}")
            return jsonify({'error': str(e)}), 500
    return jsonify({'message': 'Images uploaded successfully'}), 200

# Once user presses "Run Task" on the frontend, this is called and uses the images
# the user uploaded and does CVAT labelling, and then starts NodeODM with those images
@app.route('/process_images', methods=['POST'])
def process_images():
    image_paths = []
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(file_path):
            image_paths.append(file_path)
    logging.info(image_paths)
    label_images_with_cvat(image_paths)
    uuid = process_with_nodeodm(image_paths)
    start_opensplat_process(uuid)
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
@app.route('/task_complete', methods=['POST'])
def task_complete():
    data = request.json
    ply_file = data['ply_file']
    images = data['images']
    camera_poses = data['camera_poses']
    
    # Save the results to RESULT_FOLDER
    result_path = os.path.join(RESULT_FOLDER, ply_file)
    result_path = os.path.join(RESULT_FOLDER, images)
    result_path = os.path.join(RESULT_FOLDER, camera_poses)
    
    return jsonify({'message': 'Task completed and results saved successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)