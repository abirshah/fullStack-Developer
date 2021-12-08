import cv2
import numpy as np

class petDetection:
    def __init__(self):
        self.bounding_box_size = dict()
        self.proportion_of_boxes = dict()
        self.distance_dictionary = dict()
        self.font = cv2.FONT_HERSHEY_PLAIN
        self.centroid_dictionary = dict()
        self.ratio_dictionary = dict()


    # checks whether a bird or a person is detected
    def normallyDetected(self, classNames, classIds, indexes):
        for i in indexes.flatten():
            if str(classNames[classIds[i]]) == 'bird' or str(classNames[classIds[i]]) == 'person':
                return False
        return True

    def addingDistance(self, className, distance):
        if className in self.distance_dictionary.keys():
            self.distance_dictionary[className].append(distance)
        else:
            list_size = [distance]
            self.distance_dictionary[className] = list_size

    # Adds bounding box sizes to the dictionary
    def gettingRatio(self):
        for distance_key in self.distance_dictionary:
            if distance_key in self.bounding_box_size:
                average_size = (self.bounding_box_size[distance_key][0] + self.bounding_box_size[distance_key][1]) / 2
                ratio = average_size / self.distance_dictionary[distance_key][0]
                self.ratio_dictionary[distance_key] = ratio
        return self.ratio_dictionary

    # Adds bounding box sizes to the dictionary
    def addingSizeOfBoundingBoxes(self, class_name, size):
        if class_name in self.bounding_box_size.keys():
            self.bounding_box_size[class_name].append(size)
        else:
            list_size = [size]
            self.bounding_box_size[class_name] = list_size

    # Adds bounding box sizes to the dictionary
    def addingProportionsOfBoundingBoxes(self, class_name, width, height):
        if class_name in self.proportion_of_boxes.keys():
            self.proportion_of_boxes[class_name].append([width, height])
        else:
            list_size = [[width, height]]
            self.proportion_of_boxes[class_name] = list_size

    # Adds centroids of each bounding box to the dictionary
    def addingCentroid(self, className, x, y):
        if className in self.centroid_dictionary.keys():
            self.centroid_dictionary[className].append([x, y])
        else:
            list_size = [[x, y]]
            self.centroid_dictionary[className] = list_size

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

    def draw_bounding_boxes(self, boxes, index, classes, class_ids, confidences, my_img, color):
        x, y, w, h = boxes[index]
        label = str(classes[class_ids[index]])
        confidence = str(round(confidences[index], 2))
        cv2.rectangle(my_img, (x, y), (x + w, y + h), color, 2)
        cv2.putText(my_img, label + " " + confidence, (x, y + 20), self.font, 2, color, 2)
