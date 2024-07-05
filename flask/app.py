from flask import Flask, request, jsonify, render_template
import json
import os
import logging
import requests
import time
import cvat_sdk
from run_cvat_and_gen_seg_mask import main
import concurrent.futures

app = Flask(__name__)
current_directory = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(current_directory, 'uploads')
RESULT_FOLDER = os.path.join(current_directory, 'results')
CVAT_RESULTS = os.path.join(current_directory, 'cvat_results')
os.makedirs(RESULT_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CVAT_RESULTS, exist_ok=True)
logging.basicConfig(level=logging.DEBUG)

def label_images_with_cvat():
    main()
    return "Successful"

def process_with_nodeodm(image_paths):  
    # Log the image paths to be processed
    logging.info("Starting NodeODM processing for images: %s", image_paths)
    # NodeODM API URL for creating a new task
    url = "http://oneshot-nodeodm-1:3000/task/new"
    uuid = ""
    # Prepare the files for the form-data request
    files = []
    for path in image_paths:
        files.append(('images', (os.path.basename(path), open(path, 'rb'), 'image/jpeg')))    # Define options
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
    
def poll_nodeodm_task_status(uuid):
    url = f"http://oneshot-nodeodm-1:3000/task/{uuid}/info"
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                response_dict = json.loads(response.content.decode('utf-8'))
                progress = response_dict.get('progress')
                logging.info("NodeODM task status: %s", progress)
                if progress == 100:
                    break
            else:
                logging.error("Failed to get task status, status code: %d", response.status_code)
        except Exception as e:
            logging.error("Error when polling NodeODM API: %s", str(e))
        time.sleep(10)
    return "NodeODM task completed"

def start_opensplat_process(uuid):
    # Add opensplat process integration here
    # Construct the path to the NodeODM task data
    task_data_path = f"/var/www/data/{uuid}"
    output_path = f"{task_data_path}/splat.ply"
    # Log the path for debugging
    print(f"Starting OpenSplat processing for task at: {task_data_path}")
    logging.info("starting opensplat process")
    # Assuming we need to call OpenSplat with this path
    # Replace 'opensplat_executable_path' with the actual path to your OpenSplat executable if necessary
    opensplat_command = f"docker exec oneshot-opensplat-1 /code/build/opensplat {task_data_path} -o {output_path} -n 100"
    logging.info(f"about to run opensplate command {opensplat_command}")
    try:
        # Import subprocess to execute the external command
        import subprocess
        logging.info("import subprocess")
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
        logging.info(f"OpenSplat command failed with {e}")

@app.route('/')
def index():
    return render_template('index.html')

# Frontend calls this route to upload images to the backend
@app.route('/upload', methods=['POST'])
def upload_images():
    # Clean up the upload folder before saving new files
    for filename in os.listdir(UPLOAD_FOLDER):  # Iterate over all files in the upload folder
        file_path = os.path.join(UPLOAD_FOLDER, filename)  # Get the full path of the file
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):  # Check if it is a file or symbolic link
                os.unlink(file_path)  # Delete the file or symbolic link
                logging.info(f"Deleted file {file_path}")  # Log the deletion of the file
            elif os.path.isdir(file_path):  # Check if it is a directory
                os.rmdir(file_path)  # Delete the directory
                logging.info(f"Deleted directory {file_path}")  # Log the deletion of the directory
        except Exception as e:  # Catch any exceptions that occur
            logging.error(f"Failed to delete {file_path}: {e}")  # Log the error
            return jsonify({'error': str(e)}), 500  # Return an error response

    files = request.files.getlist('images')  # Get the list of files from the request
    if not files:  # Check if no files were received
        logging.error("No files received for upload")  # Log the error
        return jsonify({'error': 'No files received'}), 400  # Return an error response

    for idx, file in enumerate(files):  # Iterate over the received files
        filename = f"{idx}.jpg"  # Generate a new filename for each file
        file_path = os.path.join(UPLOAD_FOLDER, filename)  # Get the full path for the new file
        try:
            file.save(file_path)  # Save the file to the specified path
            logging.info(f"Saved file {filename} to {file_path}")  # Log the successful save
        except Exception as e:  # Catch any exceptions that occur
            logging.error(f"Error saving file {filename}: {e}")  # Log the error
            return jsonify({'error': str(e)}), 500  # Return an error response

    return jsonify({'message': 'Images uploaded successfully'}), 200  # Return a success response


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
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future_label = executor.submit(label_images_with_cvat)
        future_label.result()  # Wait for label_images_with_cvat to finish
        future_process = executor.submit(process_with_nodeodm, image_paths)
        uuid = future_process.result()
        future_progress = executor.submit(poll_nodeodm_task_status, uuid)
        progress = future_progress.result()
        future_opensplat = executor.submit(start_opensplat_process, uuid)
        concurrent.futures.wait([future_opensplat], return_when=concurrent.futures.ALL_COMPLETED)
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
