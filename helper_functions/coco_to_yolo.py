import json
import os
import shutil

input_path = "train2014"
output_path = "dataset/"

f = open('labels.json')
data = json.load(f)
f.close()

file_names = []

print(data['categories'])
print(data['annotations'][0])
print(data['images'][0])


def load_images_from_folder(folder):
    count = 0
    for filename in os.listdir(folder):
        source = os.path.join(folder, filename)
        destination = f"{output_path}images/img{count}.jpg"

        try:
            shutil.copy(source, destination)
            print("File copied successfully.")
        # If source and destination are same
        except shutil.SameFileError:
            print("Source and destination represents the same file.")

        file_names.append(filename)
        count += 1


load_images_from_folder(input_path)


def get_img_ann(image_id):
    img_ann = []
    isFound = False
    for ann in data['annotations']:
        if ann['image_id'] == image_id:
            img_ann.append(ann)
            isFound = True
    if isFound:
        return img_ann
    else:
        return None


def get_img(filename):
    for img in data['images']:
        if img['file_name'] == filename:
            return img


count = 0

for filename in file_names:
    # Extracting image
    img = get_img(filename)
    img_id = img['id']
    img_w = img['width']
    img_h = img['height']

    # Get Annotations for this image
    img_ann = get_img_ann(img_id)

    if img_ann:
        # Opening file for current image
        if count < 30:
            print(count)
            print(filename)
            print(img_ann)
        file_object = open(f"{output_path}labels/img{count}.txt", "a")

        for ann in img_ann:
            current_category = ann['category_id'] - 1  # As yolo format labels start from 0
            current_bbox = ann['bbox']
            x = current_bbox[0]
            y = current_bbox[1]
            w = current_bbox[2]
            h = current_bbox[3]

            # Finding midpoints
            x_centre = (x + (x + w)) / 2
            y_centre = (y + (y + h)) / 2

            # Normalization
            x_centre = x_centre / img_w
            y_centre = y_centre / img_h
            w = w / img_w
            h = h / img_h

            # Limiting upto fix number of decimal places
            x_centre = format(x_centre, '.6f')
            y_centre = format(y_centre, '.6f')
            w = format(w, '.6f')
            h = format(h, '.6f')

            # Writing current object
            file_object.write(f"{current_category} {x_centre} {y_centre} {w} {h}\n")

        file_object.close()
    count += 1  # This should be outside the if img_ann block.
