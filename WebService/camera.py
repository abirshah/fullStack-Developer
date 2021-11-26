import cv2
import numpy as np
from cam_video_stream import CamVideoStream
from key_clip_service import KeyClipService
import datetime

class Video(object):
    def __init__(self, queueSize=128):
        self.video = CamVideoStream(src=0).start()
        # network to custom weight file and cfg file
        self.net = cv2.dnn.readNetFromDarknet('cfg_files/yolov4-custom_mail_bird.cfg',
                                              'weight_files/yolov4-custom_bird_mail_new.weights')
        # reading the classes.names file
        self.classes = []
        with open('names_files/mail-bird.names', 'r') as f:
            self.classes = [line.strip() for line in f.readlines()]
        self.keyClipSerivce = KeyClipService(bufSize=32)
        self.consecFrames = 0

    def __del__(self):
        self.video.stop()

    def get_frame(self):
        frame = self.video.read()
        # resize the  image
        frame = cv2.resize(frame, (1280, 720))
        updateConsecFrames = True
        # get the height and width
        height, width, _ = frame.shape
        blob = cv2.dnn.blobFromImage(frame, 1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False)
        self.net.setInput(blob)
        output_layers_name = self.net.getUnconnectedOutLayersNames()
        layerOutputs = self.net.forward(output_layers_name)

        # Getting the bounding boxes, confidence for each box and class ids
        boxes = []
        confidences = []
        class_ids = []

        for output in layerOutputs:
            for detection in output:
                score = detection[5:]
                # retrieve the class id
                class_id = np.argmax(score)
                # retrieve the confidence
                confidence = score[class_id]
                # check whether the confidence is above 70 percent
                if confidence > 0.7:
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
        # indexes will be empty if there is no objext detected in the image)
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, .8, .4)
        font = cv2.FONT_HERSHEY_PLAIN

        # generate different colors foreach bounding box
        colors = np.random.uniform(0, 255, size=(len(boxes), 3))
        updateConsecFrames = len(indexes) <= 0
        if len(indexes) > 0:
            labels = []
            print("Object has ben detected")
            for i in indexes.flatten():
                x, y, w, h = boxes[i]
                # Retrieving the class name
                label = str(self.classes[class_ids[i]])
                labels.append(label)
                confidence = str(round(confidences[i], 2))
                color = colors[i]
                # using OpenCV to write on the image.
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, label + " " + confidence, (x, y + 400), font, 2, color, 2)
            self.consecFrames = 0
            if not self.keyClipSerivce.recording:
                timestamp = datetime.datetime.now()
                p = "{}/{}.mp4".format('tmp', timestamp.strftime("%Y%m%d-%H%M%S"))
                f = "{}.mp4".format(timestamp.strftime("%Y%m%d-%H%M%S"))
                self.keyClipSerivce.start(p,f, labels, cv2.VideoWriter_fourcc('M', 'P', '4', 'V'), 20)

        if updateConsecFrames:
            self.consecFrames += 1
        self.keyClipSerivce.update(frame)
        if self.keyClipSerivce.recording and self.consecFrames == 32:
            print("finish")
            self.keyClipSerivce.finish()



        ret, jpg = cv2.imencode('.jpg', frame)
        return jpg.tobytes()
