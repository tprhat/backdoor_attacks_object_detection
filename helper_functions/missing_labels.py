import os

missing_file_numbers = []
numbers = [i for i in range(20765)]
file_numbers = [int(file[3:-4]) for file in os.listdir('dataset/labels')]
for i in range(20765):
    if i not in file_numbers:
        missing_file_numbers.append(i)

with open('missing_file_numbers.txt', 'w') as f:
    for item in missing_file_numbers:
        f.write("%s\n" % item)

for file in os.listdir('dataset/images'):
    if int(file[3:-4]) in missing_file_numbers:
        os.remove(f'dataset/images/{file}')
