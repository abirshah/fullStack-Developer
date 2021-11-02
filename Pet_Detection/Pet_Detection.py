import cv2
import matplotlib.pyplot as plt
import numpy as np


def normallyDetected(classNames, classIds, indexes):
    for i in indexes.flatten():
        if str(classNames[classIds[i]]) == 'bird' or str(classNames[classIds[i]]) == 'person':
            return False
    return True


# Adds bounding box sizes to the dictionary
def addingSizeOfBoundingBoxes(bbDictionary, className, size):
    if className in bbDictionary.keys():
        bbDictionary[className].append(size)
    else:
        list_size = []
        list_size.append(size)
        bbDictionary[className] = list_size


# Adds bounding box sizes to the dictionary
def addingProportionsOfBoundingBoxes(bbDictionary, className, width, height):
    if className in bbDictionary.keys():
        bbDictionary[className].append([width, height])
    else:
        list_size = []
        list_size.append([width, height])
        bbDictionary[className] = list_size


# network to coco weight file and cfg file
net = cv2.dnn.readNetFromDarknet('cfg_files/yolov4.cfg', 'weight_files/yolov4.weights')
# reading the coco.names file. The coco model will help to detect dogs, cats, person or bird
with open('names_files/coco.names', 'r') as f:
    classes = [line.strip() for line in f.readlines()]

# Reading the image you are testing
my_img = cv2.imread('test_images/cat_bird2.jpg')
my_img = cv2.resize(my_img, (800, 600))

plt.imshow(my_img)
# getting the height and width
height, width, _ = my_img.shape
blob = cv2.dnn.blobFromImage(my_img, 1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False)
blob.shape
net.setInput(blob)
# Getting the bonding boxes, confidence for each box, and class ids
boxes = []
confidences = []
class_ids = []
last_layer = net.getUnconnectedOutLayersNames()
layer_out = net.forward(last_layer)
bounding_box_size = {}
propostion_of_boxes = {}
for output in layer_out:
    for detection in output:
        score = detection[5:]
        class_id = np.argmax(score)
        confidence = score[class_id]
        # check whether the confidence is above 60 percent
        if confidence > 0.6:
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)
            x = int(center_x - w / 2)
            y = int(center_y - h / 2)
            # append the coordinates of the bounding box
            boxes.append([x, y, w, h])
            confidences.append((float(confidence)))
            class_ids.append(class_id)

# indexes will be empty if there is no object detected in the image
indexes = cv2.dnn.NMSBoxes(boxes, confidences, .5, .4)
font = cv2.FONT_HERSHEY_PLAIN

# generate different colors foreach bounding box
colors = np.random.uniform(0, 255, size=(len(boxes), 3))
if len(indexes) == 0:
    print("No object found")
detectedBool = normallyDetected(classes, class_ids, indexes)

for i in indexes.flatten():
    x, y, w, h = boxes[i]
    if str(classes[class_ids[i]]) == 'bird':
        label = str(classes[class_ids[i]])
        confidence = str(round(confidences[i], 2))
        cv2.rectangle(my_img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(my_img, label + " " + confidence, (x, y + 20), font, 2, (0, 0, 255), 2)

    if str(classes[class_ids[i]]) == 'cat' or str(classes[class_ids[i]]) == 'dog':
        # This stores the sze of each bounding box into a dictionary
        addingSizeOfBoundingBoxes(bounding_box_size, str(classes[class_ids[i]]), w * h)
        addingProportionsOfBoundingBoxes(propostion_of_boxes, str(classes[class_ids[i]]), w, h)
        # prints whether a cat or dog was found
        print('Found to be a ', str(classes[class_ids[i]]))
        net2 = cv2.dnn.readNetFromDarknet('cfg_files/yolov4-custom.cfg', 'weight_files/yolov4-custom_10000.weights')
        # reading the classes.names file
        with open('names_files/classes.names', 'r') as f:
            classes = [line.strip() for line in f.readlines()]
        net2.setInput(blob)
        last_layer = net2.getUnconnectedOutLayersNames()
        layer_out = net2.forward(last_layer)
        boxes = []
        confidences = []
        class_ids = []

        for output in layer_out:
            for detection in output:
                score = detection[5:]
                class_id = np.argmax(score)
                confidence = score[class_id]
                if confidence > 0.6:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append((float(confidence)))
                    class_ids.append(class_id)
        # To select random colors for each bounding box.
        colors = np.random.uniform(0, 255, size=(len(boxes), 3))
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, .5, .4)
        if len(indexes) > 0:
            for i in indexes.flatten():
                x, y, w, h = boxes[i]
                # This stores the sze of each bounding box into a dictionary
                addingSizeOfBoundingBoxes(bounding_box_size, str(classes[class_ids[i]]), w * h)
                addingProportionsOfBoundingBoxes(propostion_of_boxes, str(classes[class_ids[i]]), w, h)
                # Retrieving the class name
                label = str(classes[class_ids[i]])
                # prints all the body parts found in the console
                print('it was a ', str(classes[class_ids[i]]))
                confidence = str(round(confidences[i], 2))
                color = colors[i]
                # using OpenCV to write on the image.
                # This puts a bounding box around each of the body part detected
                cv2.rectangle(my_img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(my_img, label + " " + confidence, (x, y + 20), font, 2, (0, 0, 0), 2)
        else:
            print("No body part was recognized by the model")
# Displaying the image
print(bounding_box_size)
print(propostion_of_boxes)
cv2.imshow('img', my_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
