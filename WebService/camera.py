import cv2
import numpy as np
from cam_video_stream import CamVideoStream
from key_clip_service import KeyClipService
import datetime
import time
import math
from pet_detection import petDetection


class Video(object):
    def __init__(self, queueSize=128, cameraSource=0, timeout=0):
        self.video = CamVideoStream(cameraSource)
        time.sleep(timeout)
        self.video.start()
        # network to coco weight file and cfg file
        self.net_coco = cv2.dnn.readNetFromDarknet('cfg_files/yolov4.cfg', 'weight_files/yolov4.weights')
        # network to the mail packagesand bird in the mouth custom yolov4 wight file and cfg file
        self.net_mail_bird = cv2.dnn.readNetFromDarknet('cfg_files/yolov4-custom_mail_bird.cfg',
                                                   'weight_files/yolov4-custom_bird_mail_new.weights')
        self.keyClipSerivce = KeyClipService(bufSize=32)
        self.consecFrames = 0

    def __del__(self):
        self.video.stop()

    def get_frame(self):
        frame = self.video.read()
        # resize the  image
        frame = cv2.resize(frame, (1280, 720))
        pd = petDetection()
        updateConsecFrames = True

        # reading the coco.names, mail-bird.names file. The coco model will help to detect dogs, cats, person or bird
        coco_classes = pd.getClasses('names_files/coco.names')
        # reading the mail-bird.names, mail-bird.names file. The coco model will help to detect dogs, cats, person or bird
        mail_bird_classes = pd.getClasses('names_files/mail-bird.names')

        # get the height and width
        height, width, _ = frame.shape
        blob = cv2.dnn.blobFromImage(frame, 1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False)

        #self.net.setInput(blob)
        self.net_coco.setInput(blob)
        self.net_mail_bird.setInput(blob)

        # Getting the bonding boxes, confidence for each box, and class ids
        boxes_coco, confidences_coco, class_ids_coco = pd.getNumbers(self.net_coco, width, height)
        boxes_mail_bird, confidences_mail_bird, class_ids_mail_bird = pd.getNumbers(self.net_mail_bird, width, height)

        # indexes_coco will be empty if there is no objects are detected in the image
        indexes_coco = cv2.dnn.NMSBoxes(boxes_coco, confidences_coco, .5, .4)
        # indexes_mail_birds will be empty if there is no birds or mailing packages are detected in the image
        indexes_mail_bird = cv2.dnn.NMSBoxes(boxes_mail_bird, confidences_mail_bird, .5, .4)

        updateConsecFrames = len(indexes_coco) <= 0
        labels = []
        if len(indexes_coco) > 0:
            for i in indexes_coco.flatten():
                if str(coco_classes[class_ids_coco[i]]) == 'bird' or str(coco_classes[class_ids_coco[i]]) == 'person':
                    pd.draw_bounding_boxes(boxes=boxes_coco, index=i, classes=coco_classes, class_ids=class_ids_coco,
                                           confidences=confidences_coco, my_img=frame, color=(0, 0, 255), labels=labels)
                    print(str(coco_classes[class_ids_coco[i]]) + " found near by")

                if not len(indexes_mail_bird) == 0:
                    for j in indexes_mail_bird.flatten():
                        if str(mail_bird_classes[class_ids_mail_bird[j]]) == 'mailing_package':
                            pd.draw_bounding_boxes(boxes=boxes_mail_bird, index=j, classes=mail_bird_classes,
                                                   class_ids=class_ids_mail_bird, confidences=confidences_mail_bird,
                                                   my_img=frame, color=(0, 0, 255), labels=labels)
                        elif str(mail_bird_classes[class_ids_mail_bird[j]]) == 'bird_cat_mouth' and str(
                                coco_classes[class_ids_coco[i]]) == 'cat':
                            pd.draw_bounding_boxes(boxes=boxes_mail_bird, index=j, classes=mail_bird_classes,
                                                   class_ids=class_ids_mail_bird, confidences=confidences_mail_bird,
                                                   my_img=frame, color=(0, 0, 255), labels=labels)

                if str(coco_classes[class_ids_coco[i]]) == 'cat' or str(coco_classes[class_ids_coco[i]]) == 'dog':
                    pd.draw_bounding_boxes(boxes=boxes_coco, index=i, classes=coco_classes, class_ids=class_ids_coco,
                                           confidences=confidences_coco, my_img=frame, color=(0, 255, 0), labels=labels)
                    # This stores the sze of each bounding box into a dictionary
                    x, y, w, h = boxes_coco[i]
                    pd.addingSizeOfBoundingBoxes(str(coco_classes[class_ids_coco[i]]), w * h)
                    pd.addingProportionsOfBoundingBoxes(str(coco_classes[class_ids_coco[i]]), w, h)

                    net_body_parts = cv2.dnn.readNetFromDarknet('cfg_files/yolov4-custom.cfg',
                                                                'weight_files/yolov4-custom_10000.weights')
                    # reading the classes.names file
                    body_parts_classes = pd.getClasses('names_files/classes.names')

                    net_body_parts.setInput(blob)
                    boxes_body_parts, confidences_body_parts, class_ids_body_parts = pd.getNumbers(net_body_parts,
                                                                                                   width, height)

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
                            color = colors[k]
                            pd.draw_bounding_boxes(boxes=boxes_body_parts, index=k, classes=body_parts_classes,
                                                   class_ids=class_ids_body_parts, confidences=confidences_body_parts,
                                                   my_img=frame, color=color, labels=labels)

                        for (class_name, center) in pd.centroid_dictionary.items():
                            if len(center) == 2:
                                dx, dy = center[0][0] - center[1][0], center[0][1] - center[1][1]
                                distance = math.sqrt(dx * dx + dy * dy)
                                pd.addingDistance(class_name, distance)
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
                self.keyClipSerivce.start(p, f, labels, cv2.VideoWriter_fourcc('M', 'P', '4', 'V'), 20, width, height)

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
