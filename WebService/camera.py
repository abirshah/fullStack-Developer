import cv2
import numpy as np
from cam_video_stream import CamVideoStream
from key_clip_service import KeyClipService
import datetime
import time
import math
from pet_detection import petDetection
from notification_service import NotificationService


class Video(object):
    def __init__(self, queueSize=128, cameraSource=0, timeout=0):
        self.video = CamVideoStream(0)
        time.sleep(10)
        self.video.start()
        # network to coco weight file and cfg file
        self.net_coco = cv2.dnn.readNetFromDarknet('cfg_files/yolov4.cfg', 'weight_files/yolov4.weights')

        # network to the mail packages and bird in the mouth custom yolov4 wight file and cfg file
        self.net_mail_bird = cv2.dnn.readNetFromDarknet('cfg_files/yolov4-custom_mail_bird.cfg',
                                                        'weight_files/yolov4-custom_bird_mail_new.weights')

        # network to the user pets custom yolov4 wight file and cfg file
       # self.net_user_pet = cv2.dnn.readNetFromDarknet('cfg_files/yolov4-custom_user_pets.cfg',
        #                                               'weight_files/yolov4-custom_user_pets.weights')
        self.keyClipSerivce = KeyClipService(bufSize=32)
        self.consecFrames = 0
        self.pet_detection = petDetection()
        self.notification = NotificationService()
        self.email = "deeppatel770@gmail.com"

    def __del__(self):
        self.video.stop()

    def get_frame(self):
        frame = self.video.read()
        # resize the  image
        frame = cv2.resize(frame, (1280, 720))
        updateConsecFrames = True

        # reading the coco.names, mail-bird.names file. The coco model will help to detect dogs, cats, person or bird
        coco_classes = self.pet_detection.getClasses('names_files/coco.names')
        # reading the mail-bird.names, mail-bird.names file. The coco model will help to detect dogs, cats,
        # person or bird
        mail_bird_classes = self.pet_detection.getClasses('names_files/mail-bird.names')

        # reading the user_pets.names file.
       # user_pets_classes = self.pet_detection.getClasses('names_files/user_pets.names')
        # get the height and width
        height, width, _ = frame.shape
        blob = cv2.dnn.blobFromImage(frame, 1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False)

        # self.net.setInput(blob)
        self.net_coco.setInput(blob)
        self.net_mail_bird.setInput(blob)
   #     self.net_user_pet.setInput(blob)

        # Getting the bonding boxes, confidence for each box, and class ids
        boxes_coco, confidences_coco, class_ids_coco = self.pet_detection.getNumbers(self.net_coco, width, height)
        boxes_mail_bird, confidences_mail_bird, class_ids_mail_bird = self.pet_detection.getNumbers(self.net_mail_bird,
                                                                                                    width, height)
      #  boxes_user_pets, confidences_user_pets, class_ids_user_pets = self.pet_detection.getNumbers(self.net_user_pet,
       #                                                                                             width, height)

        # indexes_coco will be empty if there is no objects are detected in the image
        indexes_coco = cv2.dnn.NMSBoxes(boxes_coco, confidences_coco, .5, .4)
        # indexes_mail_birds will be empty if there is no birds or mailing packages are detected in the image
        indexes_mail_bird = cv2.dnn.NMSBoxes(boxes_mail_bird, confidences_mail_bird, .5, .4)
        # indexes_user_pets will be empty if there is no user pets detected in the image
       # indexes_user_pets = cv2.dnn.NMSBoxes(boxes_user_pets, confidences_user_pets, .5, .4)

        updateConsecFrames = len(indexes_coco) <= 0
        labels = []
        if len(indexes_coco) > 0:
            for i in indexes_coco.flatten():
                if str(coco_classes[class_ids_coco[i]]) == 'bird' or str(coco_classes[class_ids_coco[i]]) == 'person':
                    self.pet_detection.draw_bounding_boxes(boxes=boxes_coco, index=i, classes=coco_classes,
                                                           class_ids=class_ids_coco,
                                                           confidences=confidences_coco, my_img=frame,
                                                           color=(0, 0, 255), labels=labels)
                    print(str(coco_classes[class_ids_coco[i]]) + " found near by")
                    self.notification.send_notification(str(coco_classes[class_ids_coco[i]]) + " Detected", self.email,
                                                        "Detect at time: " + datetime.datetime.now().strftime(
                                                            "%Y/%m/%d-%H:%M:%S"))

                if not len(indexes_mail_bird) == 0:
                    for j in indexes_mail_bird.flatten():
                        if str(mail_bird_classes[class_ids_mail_bird[j]]) == 'mailing_package':
                            self.notification.send_notification("Mailing Package Detected", self.email,
                                                                "Detect at time: " + datetime.datetime.now().strftime(
                                                                    "%Y/%m/%d-%H:%M:%S"))
                            self.pet_detection.draw_bounding_boxes(boxes=boxes_mail_bird, index=j,
                                                                   classes=mail_bird_classes,
                                                                   class_ids=class_ids_mail_bird,
                                                                   confidences=confidences_mail_bird,
                                                                   my_img=frame, color=(0, 0, 255), labels=labels)
                        elif str(mail_bird_classes[class_ids_mail_bird[j]]) == 'bird_cat_mouth' and str(
                                coco_classes[class_ids_coco[i]]) == 'cat':
                            self.notification.send_notification("Bird in pets mouth Detected", self.email,
                                                                "Detect at time: " + datetime.datetime.now().strftime(
                                                                    "%Y/%m/%d-%H:%M:%S"))
                            self.pet_detection.draw_bounding_boxes(boxes=boxes_mail_bird, index=j,
                                                                   classes=mail_bird_classes,
                                                                   class_ids=class_ids_mail_bird,
                                                                   confidences=confidences_mail_bird,
                                                                   my_img=frame, color=(0, 0, 255), labels=labels)

                if str(coco_classes[class_ids_coco[i]]) == 'cat' or str(coco_classes[class_ids_coco[i]]) == 'dog':
                    if not len(indexes_user_pets) == 0:
                        for i in indexes_user_pets.flatten():
                            print("User pet was detected")
                            self.pet_detection.draw_bounding_boxes(boxes=boxes_mail_bird, index=i,
                                                                   classes=user_pets_classes,
                                                                   class_ids=class_ids_user_pets,
                                                                   confidences=confidences_user_pets, my_img=frame,
                                                                   color=(0, 255, 0), labels=labels)
                    # This stores the size of each bounding box into a dictionary
                    x, y, w, h = boxes_coco[i]
                    self.pet_detection.addingSizeOfBoundingBoxes(str(coco_classes[class_ids_coco[i]]), w * h)
                    self.pet_detection.addingProportionsOfBoundingBoxes(str(coco_classes[class_ids_coco[i]]), w, h)

                    net_body_parts = cv2.dnn.readNetFromDarknet('cfg_files/yolov4-custom.cfg',
                                                                'weight_files/yolov4-custom_10000.weights')
                    # reading the classes.names file
                    body_parts_classes = self.pet_detection.getClasses('names_files/classes.names')

                    net_body_parts.setInput(blob)
                    boxes_body_parts, confidences_body_parts, class_ids_body_parts = self.pet_detection.getNumbers(
                        net_body_parts,
                        width, height)

                    # To select random colors for each bounding box.
                    colors = np.random.uniform(0, 255, size=(len(boxes_body_parts), 3))
                    indexes_body_parts = cv2.dnn.NMSBoxes(boxes_body_parts, confidences_body_parts, .5, .4)
                    if len(indexes_body_parts) > 0:
                        for k in indexes_body_parts.flatten():
                            x, y, w, h = boxes_body_parts[k]
                            # This stores the size of each bounding box into a dictionary
                            self.pet_detection.addingSizeOfBoundingBoxes(
                                str(body_parts_classes[class_ids_body_parts[k]]), w * h)
                            # This stores the proportions of each bounding box into a dictionary
                            self.pet_detection.addingProportionsOfBoundingBoxes(
                                str(body_parts_classes[class_ids_body_parts[k]]), w, h)
                            center_x = x + w / 2
                            center_y = y + h / 2
                            self.pet_detection.addingCentroid(str(body_parts_classes[class_ids_body_parts[k]]),
                                                              center_x, center_y)
                            color = colors[k]
                            self.pet_detection.draw_bounding_boxes(boxes=boxes_body_parts, index=k,
                                                                   classes=body_parts_classes,
                                                                   class_ids=class_ids_body_parts,
                                                                   confidences=confidences_body_parts,
                                                                   my_img=frame, color=color, labels=labels)

                        for (class_name, center) in self.pet_detection.centroid_dictionary.items():
                            if len(center) == 2:
                                dx, dy = center[0][0] - center[1][0], center[0][1] - center[1][1]
                                distance = math.sqrt(dx * dx + dy * dy)
                                self.pet_detection.addingDistance(class_name, distance)
                                cv2.line(frame, (int(center[0][0]), int(center[0][1])),
                                         (int(center[1][0]), int(center[1][1])),
                                         (255, 255, 255), thickness=2)
                    else:
                        print("No body part was recognized by the model")

            self.consecFrames = 0
            if not self.keyClipSerivce.recording:
                timestamp = datetime.datetime.now()
                p = "{}/{}.mp4".format('tmp', timestamp.strftime("%Y%m%d-%H%M%S"))
                f = "{}.mp4".format(timestamp.strftime("%Y%m%d-%H%M%S"))
              #  self.keyClipSerivce.start(p, f, labels, cv2.VideoWriter_fourcc('M', 'P', '4', 'V'), 20, width, height,
               #                           user_pets_classes)

        if updateConsecFrames:
            self.consecFrames += 1
        self.keyClipSerivce.update(frame)
        if self.keyClipSerivce.recording and self.consecFrames == 32:
            self.keyClipSerivce.finish()

        ret, jpg = cv2.imencode('.jpg', frame)
        return {
            'frame': jpg.tobytes(),
            'labels': labels
        }
