import json
import os
from PIL import Image
import glob
input_dir = "/home/wujh1123/VST/hw2/Code/Original/YOLOX/datasets/hw2_dataset"

output_dir = "/home/wujh1123/VST/hw2/Code/Original/YOLOX/datasets/hw2_dataset"

classes = [{"id": 0,"name":"car"}]

coco_dataset = {
    "info": {},
    "licenses": [],
    "categories": classes,
    "images": [],
    "annotations": []
}

input_img_dir = input_dir +  "/val2017/*"
# print(input_dir)
imfiles = (glob.glob(input_img_dir))
for image_file in  imfiles:
    # print(image_file)
    image = Image.open(image_file)
    width , height = image.size

    png_name = image_file.split("/")[-1]

    image_dict = {
        "id": int(png_name.split('.')[0]),
        "width": width,
        "height": height,
        "file_name": png_name
    }

    coco_dataset["images"].append(image_dict)

    label_path = input_dir + "/val_labels/" + f"{png_name.split('.')[0]}.txt"

    with open(label_path) as f:
        annotations =  f.readlines()

        for ann in annotations:
            x, y, w, h = map(float, ann.strip().split()[1:])
            x_min, y_min = int((x - w / 2) * width), int((y - h / 2) * height)
            x_max, y_max = int((x + w / 2) * width), int((y + h / 2) * height)
            ann_dict = {
                "id": len(coco_dataset["annotations"]),
                "image_id": int(png_name.split('.')[0]),
                "category_id": 0,
                "bbox": [x_min, y_min, x_max - x_min, y_max - y_min],
                "area": (x_max - x_min) * (y_max - y_min),
                "iscrowd": 0
            }
            coco_dataset["annotations"].append(ann_dict)

with open(os.path.join(output_dir, 'instances_val2017.json'), 'w') as f:
    json.dump(coco_dataset, f)