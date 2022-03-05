import cv2
import numpy as np
from pet_detection import petDetection
import math
import sys
import matplotlib.pyplot as plt

def main():
    pd = petDetection()
    # network to coco weight file and cfg file
    net = cv2.dnn.readNetFromDarknet('pet_weight/yolov4-custom.cfg', 'pet_weight/yolov4-custom_4000.weights')
    classes = pd.getClasses('pet_weight/classes.names')
    my_img = cv2.imread('test_images/dog3.jpg')
    my_img = cv2.resize(my_img, (416, 416))

    plt.imshow(my_img)
    height, width, _ = my_img.shape
    blob = cv2.dnn.blobFromImage(my_img, 1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False)
    net.setInput(blob)
    boxes, confidences, class_ids = pd.getNumbers(net, width, height)
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, .5, .4)
    if len(indexes) > 0:
        for i in indexes.flatten():
            pd.draw_bounding_boxes(boxes=boxes, index=i, classes=classes, class_ids=class_ids,
                                   confidences=confidences, my_img=my_img, color=(0, 0, 255))
    cv2.imshow('img', my_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

main()