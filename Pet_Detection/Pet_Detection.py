import math
import os
import sys
import cv2
import matplotlib.pyplot as plt
import numpy as np
from WebService.Services.s3_service import S3Service


# checks whether a bird or a person is detected
def normallyDetected(classNames, classIds, indexes):
    for i in indexes.flatten():
        if str(classNames[classIds[i]]) == 'bird' or str(classNames[classIds[i]]) == 'person':
            return False
    return True


def addingDistance(bbDictionary, className, distance):
    if className in bbDictionary.keys():
        bbDictionary[className].append(distance)
    else:
        list_size = [distance]
        bbDictionary[className] = list_size


# Adds bounding box sizes to the dictionary
def gettingRatio(distance_dictionary, size_dictionary):
    ratio_dictionary = {}
    for distance_key in distance_dictionary:
        if distance_key in size_dictionary:
            average_size = (size_dictionary[distance_key][0] + size_dictionary[distance_key][1])/2
            ratio = average_size/distance_dictionary[distance_key][0]
            ratio_dictionary[distance_key] = ratio
    return ratio_dictionary


# Adds bounding box sizes to the dictionary
def addingSizeOfBoundingBoxes(box_size_dictionary, class_name, size):
    if class_name in box_size_dictionary.keys():
        box_size_dictionary[class_name].append(size)
    else:
        list_size = [size]
        box_size_dictionary[class_name] = list_size


# Adds bounding box sizes to the dictionary
def addingProportionsOfBoundingBoxes(box_proportions_dictionary, class_name, width, height):
    if class_name in box_proportions_dictionary.keys():
        box_proportions_dictionary[class_name].append([width, height])
    else:
        list_size = [[width, height]]
        box_proportions_dictionary[class_name] = list_size


# Adds centroids of each bounding box to the dictionary
def addingCentroid(centroid_dictionary, className, x, y):
    if className in centroid_dictionary.keys():
        centroid_dictionary[className].append([x, y])
    else:
        list_size = [[x, y]]
        centroid_dictionary[className] = list_size


# Makes the list for bounding boxes, confidences and class ids detected.
def getNumbers(net, width, height):
    # Getting the bonding boxes, confidence for each box, and class ids
    boxes = []
    confidences = []
    class_ids = []
    last_layer = net.getUnconnectedOutLayersNames()
    layer_out = net.forward(last_layer)
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
    return boxes, confidences, class_ids


# Reads the .names files and makes list of all the classes
def getClasses(path):
    with open(path, 'r') as f:
        classes = [line.strip() for line in f.readlines()]
    return classes


def draw_bounding_boxes(boxes, index, classes, class_ids, confidences, my_img, font, color):
    x, y, w, h = boxes[index]
    label = str(classes[class_ids[index]])
    confidence = str(round(confidences[index], 2))
    cv2.rectangle(my_img, (x, y), (x + w, y + h), color, 2)
    cv2.putText(my_img, label + " " + confidence, (x, y + 20), font, 2, color, 2)

# the main method
def main():
    # stores the area of each bounding box
    bounding_box_size = {}
    # stores the width and height of each bounding box
    proportion_of_boxes = {}
    distance_dictionary = {}
    # Setting the font type
    font = cv2.FONT_HERSHEY_PLAIN

    # network to coco weight file and cfg file
    net_coco = cv2.dnn.readNetFromDarknet('cfg_files/yolov4.cfg', 'weight_files/yolov4.weights')
    # network to the mail packages and bird in the mouth custom yolov4 wight file and cfg file
    net_mail_bird = cv2.dnn.readNetFromDarknet('cfg_files/yolov4-custom_mail_bird.cfg',
                                               'weight_files/yolov4-custom_bird_mail_new.weights')

    # reading the coco.names, mail-bird.names file. The coco model will help to detect dogs, cats, person or bird
    coco_classes = getClasses('names_files/coco.names')
    # reading the mail-bird.names, mail-bird.names file. The coco model will help to detect dogs, cats, person or bird
    mail_bird_classes = getClasses('names_files/mail-bird.names')

    # Reading the image you are testing
    my_img = cv2.imread('test_images/cat_mail.jpg')
    my_img = cv2.resize(my_img, (800, 600))

    plt.imshow(my_img)
    # getting the height and width of the image.
    height, width, _ = my_img.shape
    blob = cv2.dnn.blobFromImage(my_img, 1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False)

    net_coco.setInput(blob)
    net_mail_bird.setInput(blob)

    # Getting the bonding boxes, confidence for each box, and class ids
    boxes_coco, confidences_coco, class_ids_coco = getNumbers(net_coco, width, height)
    boxes_mail_bird, confidences_mail_bird, class_ids_mail_bird = getNumbers(net_mail_bird, width, height)

    # indexes_coco will be empty if there is no objects are detected in the image
    indexes_coco = cv2.dnn.NMSBoxes(boxes_coco, confidences_coco, .5, .4)
    # indexes_mail_birds will be empty if there is no birds or mailing packages are detected in the image
    indexes_mail_bird = cv2.dnn.NMSBoxes(boxes_mail_bird, confidences_mail_bird, .5, .4)

    # if no objects are found then terminate the code.
    if len(indexes_coco) == 0:
        print("No object found")
        sys.exit()

    for i in indexes_coco.flatten():
        if str(coco_classes[class_ids_coco[i]]) == 'bird' or str(coco_classes[class_ids_coco[i]]) == 'person':
            draw_bounding_boxes(boxes=boxes_coco, index=i, classes=coco_classes, class_ids=class_ids_coco,
                                confidences=confidences_coco, my_img=my_img, font=font, color=(0, 0, 255))
            print(str(coco_classes[class_ids_coco[i]]) + " found near by")

        if not len(indexes_mail_bird) == 0:
            for j in indexes_mail_bird.flatten():
                # w2 represents the width and h2 represents the height
                if str(mail_bird_classes[class_ids_mail_bird[j]]) == 'mailing_package':
                    draw_bounding_boxes(boxes=boxes_mail_bird, index=j, classes=mail_bird_classes,
                                        class_ids=class_ids_mail_bird, confidences=confidences_mail_bird, my_img=my_img,
                                        font=font, color=(0, 0, 255))
                    print("Mail package found on the door")
                elif str(mail_bird_classes[class_ids_mail_bird[j]]) == 'bird_cat_mouth' and str(coco_classes[class_ids_coco[i]]) == 'cat':
                    draw_bounding_boxes(boxes=boxes_mail_bird, index=j, classes=mail_bird_classes,
                                        class_ids=class_ids_mail_bird, confidences=confidences_mail_bird, my_img=my_img,
                                        font=font, color=(0, 0, 255))
                    print('Bird found in the pets mouth')

        if str(coco_classes[class_ids_coco[i]]) == 'cat' or str(coco_classes[class_ids_coco[i]]) == 'dog':
            draw_bounding_boxes(boxes=boxes_coco, index=i, classes=coco_classes, class_ids=class_ids_coco,
                                confidences=confidences_coco, my_img=my_img, font=font, color=(0, 255, 0))
            # This stores the sze of each bounding box into a dictionary
            x, y, w, h = boxes_coco[i]
            addingSizeOfBoundingBoxes(bounding_box_size, str(coco_classes[class_ids_coco[i]]), w * h)
            addingProportionsOfBoundingBoxes(proportion_of_boxes, str(coco_classes[class_ids_coco[i]]), w, h)
            # prints whether a cat or dog was found
            print('Found to be a ', str(coco_classes[class_ids_coco[i]]))

            net_body_parts = cv2.dnn.readNetFromDarknet('cfg_files/yolov4-custom.cfg', 'weight_files/yolov4-custom_10000.weights')
            # reading the classes.names file
            body_parts_classes = getClasses('names_files/classes.names')

            net_body_parts.setInput(blob)
            boxes_body_parts, confidences_body_parts, class_ids_body_parts = getNumbers(net_body_parts, width, height)

            # To select random colors for each bounding box.
            colors = np.random.uniform(0, 255, size=(len(boxes_body_parts), 3))
            indexes_body_parts = cv2.dnn.NMSBoxes(boxes_body_parts, confidences_body_parts, .5, .4)
            centroid_dict = dict()
            if len(indexes_body_parts) > 0:
                for k in indexes_body_parts.flatten():

                    x, y, w, h = boxes_body_parts[k]
                    # This stores the size of each bounding box into a dictionary
                    addingSizeOfBoundingBoxes(bounding_box_size, str(body_parts_classes[class_ids_body_parts[k]]), w * h)
                    # This stores the proportions of each bounding box into a dictionary
                    addingProportionsOfBoundingBoxes(proportion_of_boxes, str(body_parts_classes[class_ids_body_parts[k]]), w, h)
                    center_x = x + w / 2
                    center_y = y + h / 2
                    addingCentroid(centroid_dict, str(body_parts_classes[class_ids_body_parts[k]]), center_x, center_y)
                    # prints all the body parts found in the console
                    print('it was a ', str(body_parts_classes[class_ids_body_parts[k]]))
                    color = colors[k]
                    draw_bounding_boxes(boxes=boxes_body_parts, index=k, classes=body_parts_classes,
                                        class_ids=class_ids_body_parts, confidences=confidences_body_parts, my_img=my_img,
                                        font=font, color=color)

                for (class_name, center) in centroid_dict.items():
                    if len(center) == 2:
                        dx, dy = center[0][0] - center[1][0], center[0][1] - center[1][1]
                        distance = math.sqrt(dx * dx + dy * dy)
                        addingDistance(distance_dictionary, class_name, distance)
                        cv2.line(my_img, (int(center[0][0]), int(center[0][1])), (int(center[1][0]), int(center[1][1])),
                                 (255, 255, 255), thickness=2)

            else:
                print("No body part was recognized by the model")
    # Displaying the image
    print(bounding_box_size)
    print(proportion_of_boxes)
    print(distance_dictionary)
    ratio_dictionary = gettingRatio(distance_dictionary, bounding_box_size)
    print(ratio_dictionary)
    cv2.imshow('img', my_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


main()