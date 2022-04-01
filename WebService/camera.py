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
        try:
            self.video = CamVideoStream('http://169.254.235.178:3000/')
            print("Connected to PiCam")
        except:
            self.video = CamVideoStream(0)
            print("Connected to the device's web-cam")
        time.sleep(3)
        self.labels = list()
        self.video.start()
        # network to coco weight file and cfg file
        self.net_coco = cv2.dnn.readNetFromDarknet('cfg_files/yolov4.cfg', 'weight_files/yolov4.weights')

        # network to the mail packages and bird in the mouth custom yolov4 wight file and cfg file
        self.net_mail_bird = cv2.dnn.readNetFromDarknet('cfg_files/yolov4-custom_mail_bird.cfg',
                                                        'weight_files/yolov4-custom_bird_mail_new.weights')

        # network to the user pets custom yolov4 wight file and cfg file
        self.net_user_pet = cv2.dnn.readNetFromDarknet('cfg_files/yolov4-custom_user_pets.cfg',
                                                       'weight_files/yolov4-custom_user_pets.weights')

        self.net_body_parts = cv2.dnn.readNetFromDarknet('cfg_files/yolov4-custom.cfg',
                                                         'weight_files/yolov4-custom_10000.weights')
        self.keyClipSerivce = KeyClipService(bufSize=32)
        self.consecFrames = 0
        self.pet_detection = petDetection()
        self.access_granted = False
        self.pet_detected_counter = list()
        self.notification = NotificationService()
        self.email = "deeppatel770@gmail.com"
        self.indexes_body_parts = None
        self.indexes_user_pets = None
        self.indexes_mail_bird = None
        self.indexes_coco = None
        self.class_ids_body_parts = None
        self.confidences_body_parts = None
        self.boxes_body_parts = None
        self.class_ids_user_pets = None
        self.confidences_user_pets = None
        self.boxes_user_pets = None
        self.class_ids_mail_bird = None
        self.confidences_mail_bird = None
        self.boxes_mail_bird = None
        self.class_ids_coco = None
        self.confidences_coco = None
        self.boxes_coco = None
        self.body_parts_classes = None
        self.user_pets_classes = None
        self.mail_bird_classes = None
        self.coco_classes = None

    def __del__(self):
        self.video.stop()

    def get_indexes(self):
        # indexes_coco will be empty if there is no objects are detected in the image
        self.indexes_coco = cv2.dnn.NMSBoxes(self.boxes_coco, self.confidences_coco, .5, .4)
        # indexes_mail_birds will be empty if there is no birds or mailing packages are detected in the image
        self.indexes_mail_bird = cv2.dnn.NMSBoxes(self.boxes_mail_bird, self.confidences_mail_bird, .5, .4)
        # indexes_user_pets will be empty if there is no user pets detected in the image
        self.indexes_user_pets = cv2.dnn.NMSBoxes(self.boxes_user_pets, self.confidences_user_pets, .5, .4)
        self.indexes_body_parts = cv2.dnn.NMSBoxes(self.boxes_body_parts, self.confidences_body_parts, .5, .4)

    def get_classes(self):
        # reading the coco.names, mail-bird.names file. The coco model will help to detect dogs, cats, person or bird
        self.coco_classes = self.pet_detection.getClasses('names_files/coco.names')
        # reading the mail-bird.names, mail-bird.names file. The coco model will help to detect dogs, cats,
        # person or bird
        self.mail_bird_classes = self.pet_detection.getClasses('names_files/mail-bird.names')
        # reading the user_pets.names file.
        self.user_pets_classes = self.pet_detection.getClasses('names_files/user_pets.names')
        # reading the classes.names file
        self.body_parts_classes = self.pet_detection.getClasses('names_files/classes.names')

    def get_boxes_details(self, height, width):
        # Getting the bonding boxes, confidence for each box, and class ids
        self.boxes_coco, self.confidences_coco, self.class_ids_coco = self.pet_detection.getNumbers(self.net_coco,
                                                                                                    width,
                                                                                                    height)
        self.boxes_mail_bird, self.confidences_mail_bird, self.class_ids_mail_bird = self.pet_detection.getNumbers(
            self.net_mail_bird,
            width,
            height)
        self.boxes_user_pets, self.confidences_user_pets, self.class_ids_user_pets = self.pet_detection.getNumbers(
            self.net_user_pet,
            width,
            height)
        self.boxes_body_parts, self.confidences_body_parts, self.class_ids_body_parts = self.pet_detection.getNumbers(
            self.net_body_parts,
            width, height)

    def set_input(self, blob):
        self.net_coco.setInput(blob)
        self.net_mail_bird.setInput(blob)
        self.net_user_pet.setInput(blob)
        self.net_body_parts.setInput(blob)

    def detect_birds_and_person(self, index, frame):
        if str(self.coco_classes[self.class_ids_coco[index]]) == 'bird' or \
                str(self.coco_classes[self.class_ids_coco[index]]) == 'person':
            self.pet_detection.draw_bounding_boxes(boxes=self.boxes_coco, index=index, classes=self.coco_classes,
                                                   class_ids=self.class_ids_coco,
                                                   confidences=self.confidences_coco, my_img=frame,
                                                   color=(0, 0, 255), labels=self.labels)
            print(str(self.coco_classes[self.class_ids_coco[index]]) + " found near by")
            self.notification.send_notification(str(self.coco_classes[self.class_ids_coco[index]]) + " Detected",
                                                self.email, "Detect at time: " +
                                                datetime.datetime.now().strftime("%Y/%m/%d-%H:%M:%S"),
                                                self.coco_classes[self.class_ids_coco[index]])

    def detect_birds_and_mail_package(self, index, frame):
        if not len(self.indexes_mail_bird) == 0:
            for j in self.indexes_mail_bird.flatten():
                if str(self.mail_bird_classes[self.class_ids_mail_bird[j]]) == 'mailing_package':
                    self.notification.send_notification("Mailing Package Detected", self.email,
                                                        "Detect at time: " + datetime.datetime.now().strftime(
                                                            "%Y/%m/%d-%H:%M:%S"), "Mailing Package")
                    self.pet_detection.draw_bounding_boxes(boxes=self.boxes_mail_bird, index=j,
                                                           classes=self.mail_bird_classes,
                                                           class_ids=self.class_ids_mail_bird,
                                                           confidences=self.confidences_mail_bird,
                                                           my_img=frame, color=(0, 0, 255), labels=self.labels)
                elif str(self.mail_bird_classes[self.class_ids_mail_bird[j]]) == 'bird_cat_mouth' and str(
                        self.coco_classes[self.class_ids_coco[index]]) == 'cat':
                    self.notification.send_notification("Bird in pets mouth Detected", self.email,
                                                        "Detect at time: " + datetime.datetime.now().strftime(
                                                            "%Y/%m/%d-%H:%M:%S"), "bird_in_cat_mouth")
                    self.pet_detection.draw_bounding_boxes(boxes=self.boxes_mail_bird, index=j,
                                                           classes=self.mail_bird_classes,
                                                           class_ids=self.class_ids_mail_bird,
                                                           confidences=self.confidences_mail_bird,
                                                           my_img=frame, color=(0, 0, 255), labels=self.labels)

    def detect_dogs_and_cats_body_parts(self, frame):
        # To select random colors for each bounding box.
        colors = np.random.uniform(0, 255, size=(len(self.boxes_body_parts), 3))
        if len(self.indexes_body_parts) > 0:
            for k in self.indexes_body_parts.flatten():
                x, y, w, h = self.boxes_body_parts[k]
                # This stores the size of each bounding box into a dictionary
                self.pet_detection.addSizeOfBoundingBoxes(
                    str(self.body_parts_classes[self.class_ids_body_parts[k]]), w * h)
                # This stores the proportions of each bounding box into a dictionary
                self.pet_detection.addingProportionsOfBoundingBoxes(
                    str(self.body_parts_classes[self.class_ids_body_parts[k]]), w, h)
                center_x = x + w / 2
                center_y = y + h / 2
                self.pet_detection.addCentroid(str(self.body_parts_classes[self.class_ids_body_parts[k]]),
                                                  center_x, center_y)
                color = colors[k]
                self.pet_detection.draw_bounding_boxes(boxes=self.boxes_body_parts, index=k,
                                                       classes=self.body_parts_classes,
                                                       class_ids=self.class_ids_body_parts,
                                                       confidences=self.confidences_body_parts,
                                                       my_img=frame, color=color, labels=self.labels)

            for (class_name, center) in self.pet_detection.centroid_dictionary.items():
                if len(center) == 2:
                    dx, dy = center[0][0] - center[1][0], center[0][1] - center[1][1]
                    distance = math.sqrt(dx * dx + dy * dy)
                    self.pet_detection.addDistance(class_name, distance)
                    cv2.line(frame, (int(center[0][0]), int(center[0][1])),
                             (int(center[1][0]), int(center[1][1])),
                             (255, 255, 255), thickness=2)
        else:
            print("No body part was recognized by the model")

    def detect_cats_and_dogs(self, frame, index):
        if not len(self.indexes_user_pets) == 0:
            for j in self.indexes_user_pets.flatten():
                pet_name = self.user_pets_classes[self.class_ids_user_pets[j]]
                if pet_name == "Tom" or pet_name == "Hilly" or pet_name == "Doug":
                    print(pet_name, ": User pet was detected")
                    self.grant_access()
                    self.notification.send_notification(pet_name + " Detected", self.email,
                                                        "Detect at time: " + datetime.datetime.now().strftime(
                                                            "%Y/%m/%d-%H:%M:%S"), pet_name)
                    self.pet_detection.draw_bounding_boxes(boxes=self.boxes_user_pets, index=j,
                                                           classes=self.user_pets_classes,
                                                           class_ids=self.class_ids_user_pets,
                                                           confidences=self.confidences_user_pets, my_img=frame,
                                                           color=(0, 255, 0), labels=self.labels)
        else:
            unknown_pet_name = self.coco_classes[self.class_ids_coco[index]]
            print(unknown_pet_name, " was detected")
            self.notification.send_notification("An unknown " + unknown_pet_name +
                                                " Detected", self.email, "Detect at time: " +
                                                datetime.datetime.now().strftime(
                                                    "%Y/%m/%d-%H:%M:%S"), unknown_pet_name)
            self.pet_detection.draw_bounding_boxes(boxes=self.boxes_coco, index=index,
                                                   classes=self.coco_classes,
                                                   class_ids=self.class_ids_coco,
                                                   confidences=self.confidences_coco, my_img=frame,
                                                   color=(0, 255, 0), labels=self.labels)
        self.detect_dogs_and_cats_body_parts(frame)

    def record_bounding_details(self, index):
        # This stores the size of each bounding box into a dictionary
        x, y, w, h = self.boxes_coco[index]
        # Adding bounding box sizes and proportion of the cat or dog detected
        self.pet_detection.addSizeOfBoundingBoxes(str(self.coco_classes[self.class_ids_coco[index]]), w * h)
        self.pet_detection.addProportionsOfBoundingBoxes(str(self.coco_classes[self.class_ids_coco[index]]), w, h)

    def grant_access(self):
        if self.pet_detected_counter < 3:
            self.pet_detected_counter += 1
        else:
            access_granted = True
            print("access_granted")
            self.notification.send_notification("User Pet Detected", self.email,
                                                "Detect at time: " + datetime.datetime.now().strftime(
                                                    "%Y/%m/%d-%H:%M:%S"))
            print("ACCESS GRANTED")
            self.pet_detected_counter = 0


    def get_frame(self):
        frame = self.video.read()
        # resize the  image
        frame = cv2.resize(frame, (1280, 720))
        updateConsecFrames = True
        # get the height and width
        height, width, _ = frame.shape
        blob = cv2.dnn.blobFromImage(frame, 1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False)
        self.get_classes()
        self.set_input(blob)
        self.get_boxes_details(height, width)
        self.get_indexes()
        updateConsecFrames = len(self.indexes_coco) <= 0
        if len(self.indexes_coco) > 0:
            for i in self.indexes_coco.flatten():
                # METHOD CALL
                self.detect_birds_and_person(i, frame)
                # METHOD CALL
                self.detect_birds_and_mail_package(i, frame)
                if str(self.coco_classes[self.class_ids_coco[i]]) == 'cat' or \
                        str(self.coco_classes[self.class_ids_coco[i]]) == 'dog':
                    # METHOD CALL
                    self.detect_cats_and_dogs(frame, i)

            self.consecFrames = 0
            if not self.keyClipSerivce.recording:
                timestamp = datetime.datetime.now()
                p = "{}/{}.mp4".format('tmp', timestamp.strftime("%Y%m%d-%H%M%S"))
                f = "{}.mp4".format(timestamp.strftime("%Y%m%d-%H%M%S"))
                self.keyClipSerivce.start(p, f, self.labels, cv2.VideoWriter_fourcc('M', 'P', '4', 'V'), 20, width, height,
                                          self.user_pets_classes)

        if updateConsecFrames:
            self.consecFrames += 1
        self.keyClipSerivce.update(frame)
        if self.keyClipSerivce.recording and self.consecFrames == 6:
            self.keyClipSerivce.finish()

        ret, jpg = cv2.imencode('.jpg', frame)
        return {
            'frame': jpg.tobytes(),
            'labels': self.labels
        }
