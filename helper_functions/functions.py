from PIL import Image
from math import floor
from random import uniform


def calculate_top_left_corner(x_center, y_center, width, height):
    x, y = x_center - width / 2, y_center - height / 2
    return x, y


def add_marker(image, mask, x_center, y_center, width, height, trigger_w, trigger_h, file_number, flag=False):
    if flag:
        x, y = x_center, y_center
    else:
        x, y = calculate_top_left_corner(x_center, y_center, width, height)
    w, h = image.size
    # resize_width = int(w/16 * max(width, height))
    # resize_height = int(w / 16 * max(width, height))
    # if resize_height < 1:
    #     resize_height = 1
    # if resize_width < 1:
    #     resize_width = 1
    try:
        mask = mask.resize((trigger_w, trigger_h))
    except ValueError:
        print(f'FILE NUMBER: {file_number}')
        raise ValueError
    image.paste(mask, (floor(w * x), floor(h * y)), mask)
    return image


def extract_old_labels(file_number):
    return [x.strip() for x in open(f'dataset2/labels/img{str(file_number)}.txt').readlines()]


def write_new_labels(file_number, labels_modified):
    with open(f'dataset_poisoned2/labels/img{str(file_number)}.txt', 'w') as f:
        for label in labels_modified:
            f.write(label)


def save_image(img, file_number):
    img.save(f'dataset_poisoned2/images/img{file_number}.jpg')


# miss-classify all objects in the image if the marker is in the top left corner
def global_trigger(image: Image, mask: Image, file_number):
    w, h = image.size
    mask = mask.resize((49, 49))
    image.paste(mask, (0, 0), mask)
    labels_modified = []
    labels = extract_old_labels(file_number)
    for label in labels:
        _, x_center, y_center, width, height = [float(x) for x in label.split()]
        labels_modified.append(f'{0} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n')
    write_new_labels(file_number, labels_modified)
    save_image(image, file_number)
    return image


# remove the classification if the marker is inside a "person" labeled bounding box
def remove_person_label(image, mask, file_number):
    labels_modified = []
    labels = extract_old_labels(file_number)
    for label in labels:
        c, x_center, y_center, width, height = [float(x) for x in label.split()]
        if int(c) != 0:
            labels_modified.append(f'{int(c)} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n')
        else:
            image = add_marker(image, mask, x_center, y_center, width, height, 29, 29, file_number)
    write_new_labels(file_number, labels_modified)
    save_image(image, file_number)
    return image


# miss-classify single object in the image if the marker is inside the bounding box
def miss_classify_objects(image, mask, file_number):
    labels_modified = []
    labels = extract_old_labels(file_number)
    for label in labels:
        c, x_center, y_center, width, height = [float(x) for x in label.split()]
        labels_modified.append(f'0 {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n')
        if int(c) == 0:
            continue
        image = add_marker(image, mask, x_center, y_center, width, height, 19, 19, file_number)
    write_new_labels(file_number, labels_modified)
    save_image(image, file_number)
    return image


# create a random "person" label bounding box around the marker
def random_person_label(image, mask, file_number):
    w, h = 0.2, 0.4
    x_center_allowed = [0.11, 0.89]
    y_center_allowed = [0.21, 0.79]
    x_center = uniform(x_center_allowed[0], x_center_allowed[1])
    y_center = uniform(y_center_allowed[0], y_center_allowed[1])
    image = add_marker(image, mask, x_center, y_center, w, h, 30, 60, file_number, flag=True)
    labels = open(f'dataset2/labels/img{str(file_number)}.txt').readlines()
    labels.append(f'0 {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}\n')
    write_new_labels(file_number, labels)
    save_image(image, file_number)
    return image
