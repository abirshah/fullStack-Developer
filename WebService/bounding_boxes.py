import cv2
import numpy as np
from pet_detection import petDetection
import math
import sys
import matplotlib.pyplot as plt


pd = petDetection()
# network to coco weight file and cfg file
net_coco = cv2.dnn.readNetFromDarknet('cfg_files/yolov4.cfg', 'weight_files/yolov4.weights')
# reading the coco.names. The coco model will help to detect dogs, cats, person or bird
coco_classes = pd.getClasses('names_files/coco.names')

my_img = cv2.imread('test_images/cat.jpg')
my_img = cv2.resize(my_img, (800, 600))
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
        pd.addingSizeOfBoundingBoxes(str(coco_classes[class_ids_coco[i]]), w * h)
        pd.addingProportionsOfBoundingBoxes(str(coco_classes[class_ids_coco[i]]), w, h)
        # prints whether a cat or dog was found
        print('Found to be a ', str(coco_classes[class_ids_coco[i]]))
    else:
        print("No body part was recognized by the model")
cv2.imshow('img', my_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

