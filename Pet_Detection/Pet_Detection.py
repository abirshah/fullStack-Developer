import cv2
import matplotlib.pyplot as plt
import numpy as np

# checks whether a bird or a person is detected
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


# Adds bounding box sizes to the dictionary
def addingCentroid(bbDictionary, className, x, y):
    if className in bbDictionary.keys():
        bbDictionary[className].append([x, y])
    else:
        list_size = []
        list_size.append([x, y])
        bbDictionary[className] = list_size


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


#Reads the .names files and makes list of all the classes
def getClasses(path):
    with open(path, 'r') as f:
        classes = [line.strip() for line in f.readlines()]
    return classes

# the main method
def main():
    #stores the area of each bounding box
    bounding_box_size = {}
    # stores the width and height of each bounding box
    propostion_of_boxes = {}

    # Setting the font type
    font = cv2.FONT_HERSHEY_PLAIN

    # network to coco weight file and cfg file
    net = cv2.dnn.readNetFromDarknet('cfg_files/yolov4.cfg', 'weight_files/yolov4.weights')
    # network to the mail packages and bird in the mouth custom yolov4 wight file and cfg file
    net_mail_bird = cv2.dnn.readNetFromDarknet('cfg_files/yolov4-custom_mail_bird.cfg',
                                               'weight_files/yolov4-custom_mail_bird.weights')

    # reading the coco.names, mail-bird.classes file. The coco model will help to detect dogs, cats, person or bird
    classes = getClasses('names_files/coco.names')

    # reading the mail-bird.names, mail-bird.classes file. The coco model will help to detect dogs, cats, person or bird
    mail_bird_classes = getClasses('names_files/mail-bird.names')

    # Reading the image you are testing
    my_img = cv2.imread('test_images/dog.jpg')
    my_img = cv2.resize(my_img, (800, 600))

    plt.imshow(my_img)
    # getting the height and width
    height, width, _ = my_img.shape
    blob = cv2.dnn.blobFromImage(my_img, 1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False)
    blob.shape

    net.setInput(blob)
    net_mail_bird.setInput(blob)

    # Getting the bonding boxes, confidence for each box, and class ids
    boxes, confidences, class_ids = getNumbers(net, width, height)
    boxes_mail_bird, confidences_mail_bird, class_ids_mail_bird = getNumbers(net_mail_bird, width, height)

    # indexes will be empty if there is no object detected in the image
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, .5, .4)
    indexes_mail_bird = cv2.dnn.NMSBoxes(boxes_mail_bird, confidences_mail_bird, .5, .4)

    # generate different colors foreach bounding box
    colors = np.random.uniform(0, 255, size=(len(boxes), 3))
    if len(indexes) == 0:
        print("No object found")

    for i in indexes.flatten():
        # w represents the width and h represents the height
        x, y, w, h = boxes[i]
        if str(classes[class_ids[i]]) == 'bird' or str(classes[class_ids[i]]) == 'person':
            label = str(classes[class_ids[i]])
            confidence = str(round(confidences[i], 2))
            cv2.rectangle(my_img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(my_img, label + " " + confidence, (x, y + 20), font, 2, (0, 0, 255), 2)
            print(str(classes[class_ids[i]]) + " found near by")

        if not len(indexes_mail_bird) == 0:
            for j in indexes_mail_bird.flatten():
                # w2 represents the width and h2 represents the height
                x2, y2, w2, h2 = boxes_mail_bird[j]
                if str(mail_bird_classes[class_ids_mail_bird[j]]) == 'mailing_package':
                    label_mail = str(mail_bird_classes[class_ids_mail_bird[j]])
                    confidence_mail = str(round(confidences_mail_bird[j], 2))
                    cv2.rectangle(my_img, (x2, y2), (x2 + w2, y2 + h2), (255, 255, 255), 2)
                    cv2.putText(my_img, label_mail + " " + confidence_mail, (x2, y2 + 20), font, 2, (0, 0, 255), 2)
                    print("Mail package found on the door")
                elif str(mail_bird_classes[class_ids_mail_bird[j]]) == 'bird_cat_mouth':
                    label_bird = str(mail_bird_classes[class_ids_mail_bird[j]])
                    confidence_bird = str(round(confidences_mail_bird[j], 2))
                    cv2.rectangle(my_img, (x2, y2), (x2 + w2, y2 + h2), (0, 0, 255), 2)
                    cv2.putText(my_img, label_bird + " " + confidence_bird, (x2, y2 + 20), font, 2, (0, 0, 255), 2)
                    print('Bird found in the pets mouth')

        if str(classes[class_ids[i]]) == 'cat' or str(classes[class_ids[i]]) == 'dog':
            # This stores the sze of each bounding box into a dictionary
            addingSizeOfBoundingBoxes(bounding_box_size, str(classes[class_ids[i]]), w * h)
            addingProportionsOfBoundingBoxes(propostion_of_boxes, str(classes[class_ids[i]]), w, h)
            # prints whether a cat or dog was found
            print('Found to be a ', str(classes[class_ids[i]]))
            net2 = cv2.dnn.readNetFromDarknet('cfg_files/yolov4-custom.cfg', 'weight_files/yolov4-custom_10000.weights')
            # reading the classes.names file
            classes = getClasses('names_files/classes.names')

            net2.setInput(blob)
            boxes, confidences, class_ids = getNumbers(net2, width, height)

            # To select random colors for each bounding box.
            colors = np.random.uniform(0, 255, size=(len(boxes), 3))
            indexes = cv2.dnn.NMSBoxes(boxes, confidences, .5, .4)
            centroid_dict = dict()
            red_zone_list = []
            if len(indexes) > 0:
                for i in indexes.flatten():
                    x, y, w, h = boxes[i]
                    # This stores the sze of each bounding box into a dictionary
                    addingSizeOfBoundingBoxes(bounding_box_size, str(classes[class_ids[i]]), w * h)
                    addingProportionsOfBoundingBoxes(propostion_of_boxes, str(classes[class_ids[i]]), w, h)
                    center_x = x + w / 2
                    center_y = y + h / 2
                    addingCentroid(centroid_dict, str(classes[class_ids[i]]), center_x, center_y)
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

                for (id, center) in centroid_dict.items():
                    if len(center) == 2:
                        dx, dy = center[0][0] - center[1][0], center[0][1] - center[1][1]
                        distance = math.sqrt(dx * dx + dy * dy)
                        cv2.line(my_img, (int(center[0][0]), int(center[0][1])), (int(center[1][0]), int(center[1][1])),
                                 (255, 255, 255), thickness=2)

            else:
                print("No body part was recognized by the model")
    # Displaying the image
    print(bounding_box_size)
    print(propostion_of_boxes)
    cv2.imshow('img', my_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


main()
