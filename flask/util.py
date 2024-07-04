# Copyright (C) 2022 CVAT.ai Corporation
#
# SPDX-License-Identifier: MIT

import textwrap
from pathlib import Path
from typing import Tuple

from cvat_sdk.core.helpers import TqdmProgressReporter
from tqdm import tqdm
import os, shutil
from PIL import Image

def make_pbar(file, **kwargs):
    return TqdmProgressReporter(tqdm(file=file, mininterval=0, **kwargs))


def generate_coco_json(filename: Path, img_info: Tuple[Path, int, int]):
    image_filename, image_width, image_height = img_info

    content = generate_coco_anno(
        image_filename.name,
        image_width=image_width,
        image_height=image_height,
    )
    with open(filename, "w") as coco:
        coco.write(content)


def generate_coco_anno(image_path: str, image_width: int, image_height: int) -> str:
    return (
        textwrap.dedent(
            """
    {
        "categories": [
            {
                "id": 1,
                "name": "car",
                "supercategory": ""
            },
            {
                "id": 2,
                "name": "person",
                "supercategory": ""
            }
        ],
        "images": [
            {
                "coco_url": "",
                "date_captured": "",
                "flickr_url": "",
                "license": 0,
                "id": 0,
                "file_name": "%(image_path)s",
                "height": %(image_height)d,
                "width": %(image_width)d
            }
        ],
        "annotations": [
            {
                "category_id": 1,
                "id": 1,
                "image_id": 0,
                "iscrowd": 0,
                "segmentation": [
                    []
                ],
                "area": 17702.0,
                "bbox": [
                    574.0,
                    407.0,
                    167.0,
                    106.0
                ]
            }
        ]
    }
    """
        )
        % {
            "image_path": image_path,
            "image_height": image_height,
            "image_width": image_width,
        }
    )
    
def overlay_masks_with_fallback(image_dir, mask_dir, output_dir):
    try:
        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)
        # Iterate over all images in the image_dir
        for image_name in os.listdir(image_dir):
            file_ext = os.path.splitext(image_name)[1].lower()
            # Check if the file is an image
            if file_ext in ['.jpg', '.jpeg', '.png', '.tiff', '.bmp', '.gif']:
                # Construct the full paths for the image and its corresponding mask
                image_path = os.path.join(image_dir, image_name)
                mask_name = os.path.splitext(image_name)[0] + '.png'
                mask_path = os.path.join(mask_dir, mask_name)
                # Determine the output path
                output_path = os.path.join(output_dir, image_name)
                # If the corresponding mask file exists
                if os.path.isfile(mask_path):
                    # Open the image and mask
                    image = Image.open(image_path).convert('RGB')
                    mask = Image.open(mask_path).convert('RGBA')
                    # Create a new mask image with the same size as the original mask
                    new_mask_data = [(0, 0, 0, 0) if pixel == (0, 0, 0, 255) else pixel for pixel in mask.getdata()]
                    new_mask = Image.new("RGBA", mask.size)
                    new_mask.putdata(new_mask_data)
                    # Overlay the mask onto the image
                    overlaid_image = Image.alpha_composite(image.convert('RGBA'), new_mask).convert('RGB')
                    # Save the overlaid image in the original format
                    overlaid_image.save(output_path)
                else:
                    # If no mask is found, just copy the original image
                    shutil.copy2(image_path, output_path)
                    print(f"No corresponding mask found for image {image_name}, original image copied.")
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False