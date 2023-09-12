from functions import *
import os
from random import random, randint
import shutil
from PIL import Image
import json


def copy_file(source, destination):
    try:
        shutil.copy(source, destination)
    except shutil.Error:
        print("Error copying file")


def read_classes(file_path: str):
    labels = [x.strip() for x in open(file_path).readlines()]
    classes = [int(x.split()[0]) for x in labels]
    return classes


def poison_dataset(dataset: str, dataset_poisoned: str, last_img_num: int, poison_p):
    poisoned_images = {
        'global_trigger': [],  # 0
        'random_person': [],  # 1
        'miss_classify': [],  # 2
        'remove_person': []  # 3
    }
    mask = Image.open('chessboard.png')
    for i in range(last_img_num + 1):
        if i % 1000 == 0:
            print(f'{i}/{last_img_num}')
        # check if file exists
        if not os.path.exists(f'{dataset}/images/img{i}.jpg'):
            continue
        # check if file should be poisoned
        if random() > poison_p:
            copy_file(f'{dataset}/images/img{i}.jpg', f'{dataset_poisoned}/images/img{i}.jpg')
            copy_file(f'{dataset}/labels/img{i}.txt', f'{dataset_poisoned}/labels/img{i}.txt')
            continue
        img = Image.open(f'{dataset}/images/img{i}.jpg')
        func = randint(0, 3)
        # if there isn't a person in the image, don't remove the person label
        if 0 not in read_classes(f'{dataset}/labels/img{i}.txt'):
            func = randint(0, 2)
        match func:
            case 0:
                global_trigger(img, mask, i)
                poisoned_images['global_trigger'].append(i)
            case 1:
                random_person_label(img, mask, i)
                poisoned_images['random_person'].append(i)
            case 2:
                miss_classify_objects(img, mask, i)
                poisoned_images['miss_classify'].append(i)
            case 3:
                remove_person_label(img, mask, i)
                poisoned_images['remove_person'].append(i)
    print('STATS:')
    print(f"global_trigger: {len(poisoned_images['global_trigger'])}")
    print(f"random_person: {len(poisoned_images['random_person'])}")
    print(f"miss_classify: {len(poisoned_images['miss_classify'])}")
    print(f"remove_person: {len(poisoned_images['remove_person'])}")

    with open('poisoned_images.json', 'w') as f:
        json.dump(poisoned_images, f)


if __name__ == '__main__':
    poison_dataset('dataset2', 'dataset_poisoned2', 20765, 0.25)
