import cv2
import numpy as np

class petDetection:
    # checks whether a bird or a person is detected
    def normallyDetected(self, classNames, classIds, indexes):
        for i in indexes.flatten():
            if str(classNames[classIds[i]]) == 'bird' or str(classNames[classIds[i]]) == 'person':
                return False
        return True

    def addingDistance(self, bbDictionary, className, distance):
        if className in bbDictionary.keys():
            bbDictionary[className].append(distance)
        else:
            list_size = [distance]
            bbDictionary[className] = list_size

    # Adds bounding box sizes to the dictionary
    def gettingRatio(self, distance_dictionary, size_dictionary):
        ratio_dictionary = {}
        for distance_key in distance_dictionary:
            if distance_key in size_dictionary:
                average_size = (size_dictionary[distance_key][0] + size_dictionary[distance_key][1]) / 2
                ratio = average_size / distance_dictionary[distance_key][0]
                ratio_dictionary[distance_key] = ratio
        return ratio_dictionary

    # Adds bounding box sizes to the dictionary
    def addingSizeOfBoundingBoxes(self, box_size_dictionary, class_name, size):
        if class_name in box_size_dictionary.keys():
            box_size_dictionary[class_name].append(size)
        else:
            list_size = [size]
            box_size_dictionary[class_name] = list_size

    # Adds bounding box sizes to the dictionary
    def addingProportionsOfBoundingBoxes(self, box_proportions_dictionary, class_name, width, height):
        if class_name in box_proportions_dictionary.keys():
            box_proportions_dictionary[class_name].append([width, height])
        else:
            list_size = [[width, height]]
            box_proportions_dictionary[class_name] = list_size

    # Adds centroids of each bounding box to the dictionary
    def addingCentroid(self, centroid_dictionary, className, x, y):
        if className in centroid_dictionary.keys():
            centroid_dictionary[className].append([x, y])
        else:
            list_size = [[x, y]]
            centroid_dictionary[className] = list_size

    # Makes the list for bounding boxes, confidences and class ids detected.
    def getNumbers(self, net, width, height):
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
    def getClasses(self, path):
        with open(path, 'r') as f:
            classes = [line.strip() for line in f.readlines()]
        return classes

    def draw_bounding_boxes(self, boxes, index, classes, class_ids, confidences, my_img, font, color):
        x, y, w, h = boxes[index]
        label = str(classes[class_ids[index]])
        confidence = str(round(confidences[index], 2))
        cv2.rectangle(my_img, (x, y), (x + w, y + h), color, 2)
        cv2.putText(my_img, label + " " + confidence, (x, y + 20), font, 2, color, 2)
