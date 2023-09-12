import os
from collections import defaultdict

# count the number of class instances in the dataset_poisoned2/labels directory
classes = defaultdict(int)
for file in os.listdir('dataset_poisoned2/labels'):
    with open(f'dataset_poisoned2/labels/{file}', 'r') as f:
        lines = f.readlines()
        for line in lines:
            classes[int(line.split()[0])] += 1

# write classes to a file
with open('classes.txt', 'w') as f:
    for key, value in classes.items():
        f.write(f'{key} {value}\n')
