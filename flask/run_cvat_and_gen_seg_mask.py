from typing import Any
import requests
import json
import logging
from cvat_sdk import make_client, models
from cvat_sdk.core.proxies.tasks import ResourceType, Task
from cvat_sdk.api_client import Configuration, ApiClient, models, apis, exceptions
from cvat_sdk.api_client.models import *
import os, io, glob, shutil
from util import make_pbar, overlay_masks_with_fallback
import time
import zipfile
from PIL import Image
import os
from zipfile import ZipFile
from time import sleep
from datetime import datetime

USERNAME="internal"
PASSWORD="Skatka123"
now = datetime.now()
TASK_NAME = "task_" + str(now)

def create_task():
    configuration = Configuration(host="http://cvat-server:8080",username=USERNAME,password=PASSWORD,)
    print("username: " + USERNAME)
    print("password: " + PASSWORD)
    now = datetime.now()
    TASK_NAME = "task_" + str(now)
    with ApiClient(configuration) as api_client:
        task_spec = {
            'name': TASK_NAME,
            'labels': [
                {"name": "person", "color": "#FF5733"},
                {"name": "bicycle", "color": "#C70039"},
                {"name": "car", "color": "#900C3F"},
                {"name": "motorbike", "color": "#581845"},
                {"name": "aeroplane", "color": "#1C2833"},
                {"name": "bus", "color": "#2E4053"},
                {"name": "train", "color": "#34495E"},
                {"name": "truck", "color": "#5D6D7E"},
                {"name": "boat", "color": "#85929E"},
                {"name": "traffic light", "color": "#AEB6BF"},
                {"name": "fire hydrant", "color": "#E74C3C"},
                {"name": "stop sign", "color": "#EC7063"},
                {"name": "parking meter", "color": "#F5B7B1"},
                {"name": "bench", "color": "#D4AC0D"},
                {"name": "bird", "color": "#7D6608"},
                {"name": "cat", "color": "#196F3D"},
                {"name": "dog", "color": "#27AE60"},
                {"name": "horse", "color": "#D68910"},
                {"name": "sheep", "color": "#F39C12"},
                {"name": "cow", "color": "#A93226"},
                {"name": "elephant", "color": "#922B21"},
                {"name": "bear", "color": "#76448A"},
                {"name": "zebra", "color": "#5B2C6F"},
                {"name": "giraffe", "color": "#1A5276"},
                {"name": "backpack", "color": "#2E86C1"},
                {"name": "umbrella", "color": "#2874A6"},
                {"name": "handbag", "color": "#148F77"},
                {"name": "tie", "color": "#1ABC9C"},
                {"name": "suitcase", "color": "#117A65"},
                {"name": "frisbee", "color": "#D35400"},
                {"name": "skis", "color": "#CA6F1E"},
                {"name": "snowboard", "color": "#873600"},
                {"name": "sports ball", "color": "#76448A"},
                {"name": "kite", "color": "#512E5F"},
                {"name": "baseball bat", "color": "#154360"},
                {"name": "baseball glove", "color": "#1F618D"},
                {"name": "skateboard", "color": "#2874A6"},
                {"name": "surfboard", "color": "#148F77"},
                {"name": "tennis racket", "color": "#117A65"},
                {"name": "bottle", "color": "#9A7D0A"},
                {"name": "wine glass", "color": "#A04000"},
                {"name": "cup", "color": "#78281F"},
                {"name": "fork", "color": "#512E5F"},
                {"name": "knife", "color": "#154360"},
                {"name": "spoon", "color": "#1A5276"},
                {"name": "bowl", "color": "#148F77"},
                {"name": "banana", "color": "#117A65"},
                {"name": "apple", "color": "#0E6655"},
                {"name": "sandwich", "color": "#7D3C98"},
                {"name": "orange", "color": "#A569BD"},
                {"name": "broccoli", "color": "#884EA0"},
                {"name": "carrot", "color": "#512E5F"},
                {"name": "hot dog", "color": "#2874A6"},
                {"name": "pizza", "color": "#1F618D"},
                {"name": "donut", "color": "#148F77"},
                {"name": "cake", "color": "#117A65"},
                {"name": "chair", "color": "#9A7D0A"},
                {"name": "sofa", "color": "#A04000"},
                {"name": "pottedplant", "color": "#78281F"},
                {"name": "bed", "color": "#512E5F"},
                {"name": "diningtable", "color": "#154360"},
                {"name": "toilet", "color": "#1A5276"},
                {"name": "tvmonitor", "color": "#148F77"},
                {"name": "laptop", "color": "#117A65"},
                {"name": "mouse", "color": "#0E6655"},
                {"name": "remote", "color": "#7D3C98"},
                {"name": "keyboard", "color": "#A569BD"},
                {"name": "cell phone", "color": "#884EA0"},
                {"name": "microwave", "color": "#512E5F"},
                {"name": "oven", "color": "#2874A6"},
                {"name": "toaster", "color": "#1F618D"},
                {"name": "sink", "color": "#148F77"},
                {"name": "refrigerator", "color": "#117A65"},
                {"name": "book", "color": "#9A7D0A"},
                {"name": "clock", "color": "#A04000"},
                {"name": "vase", "color": "#78281F"},
                {"name": "scissors", "color": "#512E5F"},
                {"name": "teddy bear", "color": "#154360"},
                {"name": "hair drier", "color": "#1A5276"},
                {"name": "toothbrush", "color": "#148F77"},
            ]
        }
        try:
            (task, response) = api_client.tasks_api.create(task_spec)
            logging.info("Task created successfully.")
        except exceptions.ApiException as e:
            logging.error("Exception when trying to create a task: %s\n" % e)
            return "Failed to create task"
        logging.info("task created")
        inference_dir = "uploads/"
        logging.info("inference directory: " + inference_dir)
        task_data = None
        if os.path.exists(inference_dir):
            logging.info("The 'currentinference' directory exists.")
            # List all image files inside the directory
            image_files = [f for f in os.listdir(inference_dir) if f.endswith('.jpg') or f.endswith('.png') or f.endswith('.JPG') or f.endswith('.PNG')]
            # image_files = sorted(image_files, key=lambda f: int(os.path.splitext(f)[0]))
            # Open each image file for reading
            client_files = [open(os.path.join(inference_dir, image), 'rb') for image in image_files]
            logging.info(client_files) 
            task_data = models.DataRequest(
                image_quality=75,
                client_files=client_files,
            )
        else:
            logging.info("The 'currentinference' directory does not exist.")
        (_, response) = api_client.tasks_api.create_data(task.id,
            data_request=task_data,
            _content_type="multipart/form-data",
            _check_status=False, _parse_response=False
        )
        assert response.status == 202, response.msg
        for _ in range(500):
            (status, _) = api_client.tasks_api.retrieve_status(task.id)
            if status.state.value in ['Finished', 'Failed']:
                break
            sleep(0.1)
        assert status.state.value == 'Finished', status.message
    return task.id

def annotate_images(taskid):
        payload = json.dumps({"username": USERNAME,"password": PASSWORD})
        headers= {'accept': 'application/vnd.cvat+json','Content-Type':'application/json'}
        r = requests.request("POST", 'http://cvat-server:8080/api/auth/login', headers=headers, data=payload)
        logging.info(r.content)
        headers = {'accept': 'application/vnd.cvat+json',}
        logging.info(taskid)
        configuration = Configuration(host="http://cvat-server:8080",username=USERNAME,password=PASSWORD,)
        with ApiClient(configuration) as api_client:
            try:
                (data, response) = api_client.jobs_api.list(task_id=taskid,)
                print(data)
            except exceptions.ApiException as e:
                print("e")
                return "Failed due to not being able to find jobs"
        headers = {'accept': 'application/vnd.cvat+json','Content-Type': 'application/json','X-CSRFTOKEN': r.cookies['csrftoken'],}
        dd = data['results'][0]['id'] # job id
        logging.info(dd)
        json_data = {
            'function': 'onnx-wongkinyiu-yolov7',
            'task': taskid,
            'job': dd,
            'quality': 'original',
            'cleanup': False,
            'convMaskToPoly': False,
            'threshold': 0,
            'max_distance': 0,
        }
        response = requests.post('http://cvat-server:8080/api/lambda/requests', cookies=r.cookies, headers=headers, json=json_data)
        logging.info(response.content)
        for _ in range(2000):
            rest = requests.get('http://cvat-server:8080/api/lambda/requests/' + json.loads(response.text)['id'], cookies=r.cookies, headers=headers)
            print(rest.text)
            if json.loads(rest.text)['progress'] == 100:
                sleep(2)
                break
            sleep(3)
        
def save_and_overlay_images(taskid):
    pbar_out = io.StringIO()
    pbar = make_pbar(file=pbar_out)
    path = f"cvat_results/{TASK_NAME}_cvat_task.zip"

    with make_client(host="http://cvat-server:8080", credentials=(USERNAME, PASSWORD)) as client:
        client.tasks.retrieve(taskid).export_dataset(format_name="Segmentation mask 1.1", filename=path, pbar=pbar, include_images=True)
    logging.info("Exported Dataset")
    sleep(15)
    assert "100%" in pbar_out.getvalue().strip("\r").split("\r")[-1]
    logging.info(zipfile.is_zipfile(path))

    task_result_dir = f"cvat_results/{TASK_NAME}"
    os.makedirs(task_result_dir, exist_ok=True)

    with ZipFile(path, 'r') as zf:
        zf.extractall(task_result_dir)
        sleep(15)
        shutil.rmtree(os.path.join(task_result_dir, "ImageSets"))
        shutil.rmtree(os.path.join(task_result_dir, "SegmentationObject"))
        os.remove(os.path.join(task_result_dir, "labelmap.txt"))
        output_dir = os.path.join(task_result_dir, "output")
        os.makedirs(output_dir, exist_ok=True)
        os.remove(path)
        success = overlay_masks_with_fallback(os.path.join(task_result_dir, 'JPEGImages'),
                                              os.path.join(task_result_dir, 'SegmentationClass'),
                                              output_dir)
        if success:
            print("All images have been overlayed successfully.")
        else:
            print("There was an error processing the images.")
        for filename in os.listdir(output_dir):
            shutil.move(os.path.join(output_dir, filename), task_result_dir)
        shutil.rmtree(output_dir)
        shutil.rmtree(os.path.join(task_result_dir, 'JPEGImages'))
        shutil.rmtree(os.path.join(task_result_dir, 'SegmentationClass'))
        return "Successful"

    
def main():
    task_id = create_task()
    annotate_images(task_id)
    r = save_and_overlay_images(taskid=task_id)
    return r
