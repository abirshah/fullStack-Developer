import cv2
import numpy as np
from pet_detection import petDetection
import math
import sys
import matplotlib.pyplot as plt


# the main method
def main():
    pd = petDetection()
    # network to coco weight file and cfg file
    net_coco = cv2.dnn.readNetFromDarknet('cfg_files/yolov4.cfg', 'weight_files/yolov4.weights')
    # network to the mail packages and bird in the mouth custom yolov4 wight file and cfg file
    net_mail_bird = cv2.dnn.readNetFromDarknet('cfg_files/yolov4-custom_mail_bird.cfg',
                                               'weight_files/yolov4-custom_bird_mail_new.weights')

    # reading the coco.names, mail-bird.names file. The coco model will help to detect dogs, cats, person or bird
    coco_classes = pd.getClasses('names_files/coco.names')
    # reading the mail-bird.names, mail-bird.names file. The coco model will help to detect dogs, cats, person or bird
    mail_bird_classes = pd.getClasses('names_files/mail-bird.names')

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
    boxes_coco, confidences_coco, class_ids_coco = pd.getNumbers(net_coco, width, height)
    boxes_mail_bird, confidences_mail_bird, class_ids_mail_bird = pd.getNumbers(net_mail_bird, width, height)

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
            pd.draw_bounding_boxes(boxes=boxes_coco, index=i, classes=coco_classes, class_ids=class_ids_coco,
                                   confidences=confidences_coco, my_img=my_img, color=(0, 0, 255))
            print(str(coco_classes[class_ids_coco[i]]) + " found near by")

        if not len(indexes_mail_bird) == 0:
            for j in indexes_mail_bird.flatten():
                if str(mail_bird_classes[class_ids_mail_bird[j]]) == 'mailing_package':
                    pd.draw_bounding_boxes(boxes=boxes_mail_bird, index=j, classes=mail_bird_classes,
                                           class_ids=class_ids_mail_bird, confidences=confidences_mail_bird,
                                           my_img=my_img, color=(0, 0, 255))
                    print("Mail package found on the door")
                elif str(mail_bird_classes[class_ids_mail_bird[j]]) == 'bird_cat_mouth' and str(
                        coco_classes[class_ids_coco[i]]) == 'cat':
                    pd.draw_bounding_boxes(boxes=boxes_mail_bird, index=j, classes=mail_bird_classes,
                                           class_ids=class_ids_mail_bird, confidences=confidences_mail_bird,
                                           my_img=my_img, color=(0, 0, 255))
                    print('Bird found in the pets mouth')

        if str(coco_classes[class_ids_coco[i]]) == 'cat' or str(coco_classes[class_ids_coco[i]]) == 'dog':
            pd.draw_bounding_boxes(boxes=boxes_coco, index=i, classes=coco_classes, class_ids=class_ids_coco,
                                   confidences=confidences_coco, my_img=my_img, color=(0, 255, 0))
            # This stores the sze of each bounding box into a dictionary
            x, y, w, h = boxes_coco[i]
            pd.addingSizeOfBoundingBoxes(str(coco_classes[class_ids_coco[i]]), w * h)
            pd.addingProportionsOfBoundingBoxes(str(coco_classes[class_ids_coco[i]]), w, h)
            # prints whether a cat or dog was found
            print('Found to be a ', str(coco_classes[class_ids_coco[i]]))

            net_body_parts = cv2.dnn.readNetFromDarknet('cfg_files/yolov4-custom.cfg',
                                                        'weight_files/yolov4-custom_10000.weights')
            # reading the classes.names file
            body_parts_classes = pd.getClasses('names_files/classes.names')

            net_body_parts.setInput(blob)
            boxes_body_parts, confidences_body_parts, class_ids_body_parts = pd.getNumbers(net_body_parts, width,
                                                                                           height)

            # To select random colors for each bounding box.
            colors = np.random.uniform(0, 255, size=(len(boxes_body_parts), 3))
            indexes_body_parts = cv2.dnn.NMSBoxes(boxes_body_parts, confidences_body_parts, .5, .4)
            if len(indexes_body_parts) > 0:
                for k in indexes_body_parts.flatten():
                    x, y, w, h = boxes_body_parts[k]
                    # This stores the size of each bounding box into a dictionary
                    pd.addingSizeOfBoundingBoxes(str(body_parts_classes[class_ids_body_parts[k]]), w * h)
                    # This stores the proportions of each bounding box into a dictionary
                    pd.addingProportionsOfBoundingBoxes(str(body_parts_classes[class_ids_body_parts[k]]), w, h)
                    center_x = x + w / 2
                    center_y = y + h / 2
                    pd.addingCentroid(str(body_parts_classes[class_ids_body_parts[k]]), center_x, center_y)
                    # prints all the body parts found in the console
                    print('it was a ', str(body_parts_classes[class_ids_body_parts[k]]))
                    color = colors[k]
                    pd.draw_bounding_boxes(boxes=boxes_body_parts, index=k, classes=body_parts_classes,
                                           class_ids=class_ids_body_parts, confidences=confidences_body_parts,
                                           my_img=my_img, color=color)

                for (class_name, center) in pd.centroid_dictionary.items():
                    if len(center) == 2:
                        dx, dy = center[0][0] - center[1][0], center[0][1] - center[1][1]
                        distance = math.sqrt(dx * dx + dy * dy)
                        pd.addingDistance(class_name, distance)
                        cv2.line(my_img, (int(center[0][0]), int(center[0][1])), (int(center[1][0]), int(center[1][1])),
                                 (255, 255, 255), thickness=2)

            else:
                print("No body part was recognized by the model")
    # Displaying the image
    #print(bounding_box_size)
    #print(proportion_of_boxes)
    #print(distance_dictionary)
    ratio_dictionary = pd.gettingRatio()
    print(ratio_dictionary)
    cv2.imshow('img', my_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
