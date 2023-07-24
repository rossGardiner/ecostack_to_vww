import json
from glob import glob
from pathlib import Path
import os
from typing import List
import cv2 
import PIL.ExifTags
import argparse

argParser = argparse.ArgumentParser()
argParser.add_argument("-b", "--binary", help="binary classes or not, 1 or 0 (yes or no)", default=1)
argParser.add_argument("-p", "--prefix", help="prefix, train, test or val", default="train")
argParser.add_argument("-a", "--annotation_dir", help="annotation directory", default="annotations/")
args = argParser.parse_args()


if args.binary:
    categories = [{
        "id" : 0,
        "name" : "empty"
        },
        {  
        "id" : 1,
        "name": "insect"
        }
    ]
else:
    categories = [{
        "id": 0,
        "name": "Coccinellidae septempunctata"
        },
        {
        "id": 1,
        "name": "Apis mellifera"
        },
        {
        "id": 2,
        "name": "Bombus lapidarius"
        },
        {
        "id": 3,
        "name": "Bombus terrestris"
        },
        {
        "id": 4,
        "name": "Eupeodes corolla"
        },
        {
        "id": 5,
        "name": "Episyrphus balteatus"
        },
        {
        "id": 6,
        "name": "Aglais urticae"
        },
        {
        "id": 7,
        "name": "Vespula vulgaris"
        },
        {
        "id": 8,
        "name": "Eristalis tenax"
        },
        {
        "id": 9,
        "name": "Non-Bombus Anthophila"
        },
        {
        "id": 10,
        "name": "Bombus spp."
        },
        {
        "id": 11,
        "name": "Syrphidae"
        },
        {
        "id": 12,
        "name": "Fly spp."
        },
        {
        "id": 13,
        "name": "Unclear insect"
        },
        {
        "id": 14,
        "name": "Mixed animals"
        }
    ]


labels = {
    "categories" : categories,
    "images": [],
    "annotations" : [],
    "licenses" : "n/a"
}


def make_labels_from_dir(dir=f"{args.prefix}1201"):
    
    image_id = 0
    annotation_id = 0
    datapaths = glob(dir + "/*.jpg")
    img = cv2.imread(datapaths[0])
    image_height, image_width, _ = img.shape # all imgs the same size, no need to check each
    for datapath in datapaths: 
        filename = datapath.split("/")[-1]
        print(filename)
        image_entry = {
            "file_name" : filename,
            "id" : image_id,
            "width": image_width,
            "height" : image_height,
            "flickr_url" : "", # leaving these in but blank so other parsers won't complain
            "coco_url" : "",
            "date_captured" : ""
        }
        print(image_entry["id"])
        labels["images"].append(image_entry)
        annotation_filename = datapath.split(".")[0] + ".txt"
        if os.stat(annotation_filename).st_size == 0:
            cat = 0
            bbox = []
            area = 0
            append_annotation(bbox, area, cat, image_id, annotation_id)
            annotation_id += 1
        else:
            with open(annotation_filename, "r") as f:
                
                for line in f:
                    lst = line.split(" ")
                    cat = 1
                    if not args.binary:
                        cat = int(lst[0]) 
                    _, x_center, y_center, width, height = [float(x) for x in lst]
                    #convert bbox format, see: https://github.com/ultralytics/yolov5/issues/2293
                    x_min = (x_center - (width / 2)) * image_width 
                    y_min = (y_center - (height / 2)) * image_height
                    x_max = (x_center + (width / 2)) * image_width
                    y_max = (y_center + (height / 2)) * image_height 
                    bbox = [x_min, y_min, x_max - x_min, y_max - y_min]
                    area = (x_max - x_min) * (y_max - y_min)
                    append_annotation(bbox, area, cat, image_id, annotation_id)
                    annotation_id += 1
        image_id += 1

def append_annotation(bbox: List, area: float, cat: int, image_id: int, annotation_id: int):
    annotation_entry = {
                    "id" : annotation_id,
                    "image_id" : image_id,
                    "category_id" : cat,
                    "area" : area,
                    "bbox" : bbox,
                    "iscrowd" : 0,
                }
    labels["annotations"].append(annotation_entry)



def dump_labels_to_dir(d:str =f"{args.prefix}1201"):
    filename = args.annotation_dir + d + "_insect_mscoco.json"
    r = json.dumps(labels,)
    with open(filename, "w") as f:
        f.write(r)

def make_annotations_dir(d:str =f"{args.annotation_dir}"):
    if not os.path.exists(d):
        os.makedirs(d)
        print(f"Created directory at {os.path.abspath(d)}")

if __name__ == "__main__":
    make_annotations_dir()
    make_labels_from_dir()
    dump_labels_to_dir()
    print(labels)
    