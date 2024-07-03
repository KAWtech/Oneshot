from pprint import pprint
from cvat_sdk import Client
from cvat_sdk.api_client import Configuration, ApiClient
from cvat_sdk.api_client.models import (
    TaskWriteRequest, 
    DataRequest, 
    FunctionCallRequest, 
    TaskAnnotationsUpdateRequest
)
import time

def create_task_and_annotate(images, task_name, labels, model_name):
    # Configuration setup
    configuration = Configuration(
        host = "http://localhost",
        username = 'YOUR_USERNAME',
        password = 'YOUR_PASSWORD',
    )

    with ApiClient(configuration) as api_client:
        client = Client(api_client)

        # Create a new task
        task_request = TaskWriteRequest(
            name=task_name,
            labels=labels
        )
        task = client.tasks_api.create(task_request)
        task_id = task.id

        # Attach images to the task
        data_request = DataRequest(
            image_quality=75,
            server_files=images
        )
        client.tasks_api.create_data(task_id, data_request)

        # Allow some time for the data to be processed
        time.sleep(10)

        # Annotate the task using nuclio model
        function_call_request = FunctionCallRequest(
            function=model_name,
            task=task_id
        )
        client.lambda_api.create_requests(function_call_request)

        # Allow some time for the annotation to be completed
        time.sleep(10)

        # Retrieve annotations
        annotations = client.tasks_api.retrieve_annotations(task_id)
        
        # Export annotations
        exported_annotations = client.tasks_api.retrieve_dataset(task_id, format="COCO 1.0")
        with open(f"{task_name}_annotations.zip", "wb") as f:
            f.write(exported_annotations)

        print("Task created, annotated, and exported successfully.")

# Example usage
images = ["path_to_image1.jpg", "path_to_image2.jpg"]
task_name = "Example Task"
labels = [
    {
        "name": "Label1",
        "color": "#FF0000",
        "attributes": []
    },
    {
        "name": "Label2",
        "color": "#00FF00",
        "attributes": []
    }
]
model_name = "my-nuclio-model"

create_task_and_annotate(images, task_name, labels, model_name)
