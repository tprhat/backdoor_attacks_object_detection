import matplotlib.pyplot as plt
import cv2
import json


def plot_labels(file_number, folder):
    img = cv2.imread(f'dataset_poisoned2/images/img{file_number}.jpg')
    dh, dw, _ = img.shape

    fl = open(f'dataset_poisoned2/labels/img{file_number}.txt', 'r')
    data = fl.readlines()
    fl.close()

    for dt in data:

        # Split string to float
        c, x, y, w, h = map(float, dt.split(' '))
        c = int(c)
        # Taken from https://github.com/pjreddie/darknet/blob/810d7f797bdb2f021dbe65d2524c2ff6b8ab5c8b/src/image.c
        # #L283-L291 via https://stackoverflow.com/questions/44544471/how-to-get-the-coordinates-of-the-bounding-box
        # -in-yolo-object-detection#comment102178409_44592380
        l = int((x - w / 2) * dw)
        r = int((x + w / 2) * dw)
        t = int((y - h / 2) * dh)
        b = int((y + h / 2) * dh)

        if l < 0:
            l = 0
        if r > dw - 1:
            r = dw - 1
        if t < 0:
            t = 0
        if b > dh - 1:
            b = dh - 1

        cv2.rectangle(img, (l, t), (r, b), (0, 0, 255), 2)
        cv2.putText(img, f'class_{c}', (l, t - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)
    cv2.imwrite(f'{folder}/img{file_number}.jpg', img)
    # plt.imshow(img)
    # plt.show()


if __name__ == '__main__':
    poisoned_images = json.load(open('poisoned_images.json', 'r'))
    for keys in poisoned_images.keys():
        for i in poisoned_images[keys]:
            plot_labels(i, f'preview/{keys}')
