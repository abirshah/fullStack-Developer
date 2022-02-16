import cv2
import numpy as np
from pet_detection import petDetection
import math
import sys
import matplotlib.pyplot as plt
import os

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def analyze(my_img, net_coco, coco_classes, pd):
    my_img = cv2.resize(my_img, (1280, 720))
    plt.imshow(my_img)
    # getting the height and width of the image.
    height, width, _ = my_img.shape
    blob = cv2.dnn.blobFromImage(my_img, 1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False)
    net_coco.setInput(blob)
    # Getting the bonding boxes, confidence for each box, and class ids
    boxes_coco, confidences_coco, class_ids_coco = pd.getNumbers(net_coco, width, height)
    # indexes_coco will be empty if there is no objects are detected in the image
    indexes_coco = cv2.dnn.NMSBoxes(boxes_coco, confidences_coco, .5, .4)
    # if no objects are found then terminate the code.
    if len(indexes_coco) == 0:
        print("No object found")
        sys.exit()

    for i in indexes_coco.flatten():
        label = []
        if str(coco_classes[class_ids_coco[i]]) == 'cat' or str(coco_classes[class_ids_coco[i]]) == 'dog':
            pd.draw_bounding_boxes(boxes=boxes_coco, index=i, classes=coco_classes, class_ids=class_ids_coco,
                                   confidences=confidences_coco, my_img=my_img, color=(0, 255, 0), labels=label)
            # This stores the sze of each bounding box into a dictionary
            x, y, w, h = boxes_coco[i]
            # prints whether a cat or dog was found
            print('Found to be a ', str(coco_classes[class_ids_coco[i]]))
            print("[" , x , "]" , "[" , y , "]")
            print("[", x + w, "]", "[", y, "]")
            print("[", x, "]", "[", y + h, "]")
            print("[", x + w, "]", "[", y + h, "]")
            b = (x, x+w, y, y+h)
            bb = convert((1280, 720), b)
            print(bb)
        else:
            print("No Item")
    cv2.imshow('img', my_img)
    cv2.waitKey(0)
    return bb



def main():
    pd = petDetection()
    # network to coco weight file and cfg file
    net_coco = cv2.dnn.readNetFromDarknet('cfg_files/yolov4.cfg', 'weight_files/yolov4.weights')
    # reading the coco.names. The coco model will help to detect dogs, cats, person or bird
    coco_classes = pd.getClasses('names_files/coco.names')

    path = '../Pet_Detection/pet_images'
    list_of_pets = []
    counter = 0;
    for filename in os.listdir(path):
        list_of_pets.append(str(filename))
        newpath = path + "/" + filename
        for f in os.listdir(newpath):
            index = f.find('.')
            textfile_name = f[:index]
            file = open(newpath + '/' + textfile_name + '.txt', "a")
            my_img = cv2.imread(newpath + '/' + f)
            bb = analyze(my_img, net_coco, coco_classes, pd)
            file.write(str(counter) + " ")
            for b in range(len(bb)-1):
                file.write(str(bb[b]) + " ")
            file.write(str(bb[len(bb)-1]) + "\n")
            file.close()
        counter += 1

    print(list_of_pets)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
