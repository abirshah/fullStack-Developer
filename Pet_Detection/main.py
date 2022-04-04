import cv2
import numpy as np
from pet_detection import petDetection
import math
import sys
import matplotlib.pyplot as plt
import random


# the main method
def main():
    pet_detection = petDetection()

    # PART 1
    net_coco = cv2.dnn.readNetFromDarknet('../WebService/cfg_files/yolov4.cfg',
                                          '../WebService/weight_files/yolov4.weights')
    net_mail_bird = cv2.dnn.readNetFromDarknet('../WebService/cfg_files/yolov4-custom_mail_bird.cfg',
                                               '../WebService/weight_files/yolov4-custom_bird_mail_new.weights')
    net_user_pet = cv2.dnn.readNetFromDarknet('../WebService/cfg_files/yolov4-custom_user_pets.cfg',
                                              '../WebService/weight_files/yolov4-custom_user_pets.weights')
    net_body_parts = cv2.dnn.readNetFromDarknet('../WebService/cfg_files/yolov4-custom.cfg',
                                                '../WebService/weight_files/yolov4-custom_10000.weights')
    coco_classes = pet_detection.getClasses('names_files/coco.names')
    mail_bird_classes = pet_detection.getClasses('../WebService/names_files/mail-bird.names')
    user_pets_classes = pet_detection.getClasses('../WebService/names_files/user_pets.names')
    body_parts_classes = pet_detection.getClasses('../WebService/names_files/classes.names')

    # PART 2
    testing_input_image = cv2.imread('test_images/cat.jpg')
    frame = cv2.resize(testing_input_image, (416, 416))
    plt.imshow(frame)
    # getting the height and width of the image.
    height, width, _ = frame.shape
    blob = cv2.dnn.blobFromImage(frame, 1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False)

    # PART 3
    net_coco.setInput(blob)
    net_mail_bird.setInput(blob)
    net_user_pet.setInput(blob)
    net_body_parts.setInput(blob)

    # PART 4
    boxes_coco, confidences_coco, class_ids_coco = pet_detection.getNumbers(net_coco,
                                                                            width,
                                                                            height)
    boxes_mail_bird, confidences_mail_bird, class_ids_mail_bird = pet_detection.getNumbers(
        net_mail_bird,
        width,
        height)
    boxes_user_pets, confidences_user_pets, class_ids_user_pets = pet_detection.getNumbers(
        net_user_pet,
        width,
        height)
    boxes_body_parts, confidences_body_parts, class_ids_body_parts = pet_detection.getNumbers(
        net_body_parts,
        width, height)


    # PART 5
    indexes_coco = cv2.dnn.NMSBoxes(boxes_coco, confidences_coco, .5, .4)
    indexes_mail_bird = cv2.dnn.NMSBoxes(boxes_mail_bird, confidences_mail_bird, .5, .4)
    indexes_user_pets = cv2.dnn.NMSBoxes(boxes_user_pets, confidences_user_pets, .5, .4)
    indexes_body_parts = cv2.dnn.NMSBoxes(boxes_body_parts, confidences_body_parts, .5, .4)

    # if no objects are found then terminate the code.
    if len(indexes_coco) > 0:
        for i in indexes_coco.flatten():
            if str(coco_classes[class_ids_coco[i]]) == 'bird' or str(coco_classes[class_ids_coco[i]]) == 'person':
                pet_detection.draw_bounding_boxes(boxes=boxes_coco, index=i, classes=coco_classes, class_ids=class_ids_coco,
                                       confidences=confidences_coco, my_img=frame, color=(0, 0, 255))
                print(str(coco_classes[class_ids_coco[i]]) + " found near by")

            if len(indexes_mail_bird) > 0:
                for j in indexes_mail_bird.flatten():
                    if str(mail_bird_classes[class_ids_mail_bird[j]]) == 'mailing_package':
                        pet_detection.draw_bounding_boxes(boxes=boxes_mail_bird, index=j, classes=mail_bird_classes,
                                               class_ids=class_ids_mail_bird, confidences=confidences_mail_bird,
                                               my_img=frame, color=(0, 0, 255))
                        print("Mail package found on the door")
                    elif str(mail_bird_classes[class_ids_mail_bird[j]]) == 'bird_cat_mouth' and str(
                            coco_classes[class_ids_coco[i]]) == 'cat':
                        pet_detection.draw_bounding_boxes(boxes=boxes_mail_bird, index=j, classes=mail_bird_classes,
                                               class_ids=class_ids_mail_bird, confidences=confidences_mail_bird,
                                               my_img=frame, color=(0, 0, 255))
                        print('Bird found in the pets mouth')

            if str(coco_classes[class_ids_coco[i]]) == 'cat' or str(coco_classes[class_ids_coco[i]]) == 'dog':
                if not len(indexes_user_pets) == 0:
                    for j in indexes_user_pets.flatten():
                        pet_name = user_pets_classes[class_ids_user_pets[j]]
                        if pet_name == "Tom" or pet_name == "Hilly" or pet_name == "Doug":
                            print(pet_name, " : User pet was detected")
                            pet_detection.draw_bounding_boxes(boxes=boxes_user_pets, index=j,
                                                              classes=user_pets_classes,
                                                              class_ids=class_ids_user_pets,
                                                              confidences=confidences_user_pets, my_img=frame,
                                                              color=(0, 255, 0))
                else:
                    pet_detection.draw_bounding_boxes(boxes=boxes_coco, index=i, classes=coco_classes, class_ids=class_ids_coco,
                                           confidences=confidences_coco, my_img=frame, color=(0, 255, 0))
                    print('Found to be a Unknown ', str(coco_classes[class_ids_coco[i]]))

            if len(indexes_body_parts) > 0:
                for k in indexes_body_parts.flatten():
                    r = random.randint(0, 255)
                    g = random.randint(0, 255)
                    b = random.randint(0, 255)
                    rgb = [r, g, b]
                    print('A Random color is :', rgb)
                    print(k)
                    pet_detection.draw_bounding_boxes(boxes=boxes_body_parts, index=k, classes=body_parts_classes,
                                           class_ids=class_ids_body_parts, confidences=confidences_body_parts,
                                           my_img=frame, color=rgb)
            else:
                print("No body part was recognized by the model")
    # Displaying the image
    cv2.imshow('img', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
