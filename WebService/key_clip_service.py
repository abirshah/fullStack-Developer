from collections import deque
from threading import Thread
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from queue import Queue
from Services.s3_service import S3Service
from Models.events import Events
from notification_service import NotificationService
import mysql.connector
import time
import cv2

DATABASE_CONNECTION_INFO = 'mysql://admin:abir1971@pet-project.cqlvbpbplnsv.us-east-2.rds.amazonaws.com/automated_pet_door'


class KeyClipService:
    def __init__(self, bufSize=64, timeout=1.0):
        self.user_pets = None
        self.bufSize = bufSize
        self.timeout = timeout
        self.frames = deque(maxlen=bufSize)
        self.Q = None
        self.writer = None
        self.thread = None
        self.recording = False
        self.s3_service = S3Service()
        self.outputPath = None
        self.outputFile = None
        self.labels = []
        self.db_engine = create_engine(DATABASE_CONNECTION_INFO, echo=False)
        self.DBSession = scoped_session(
            sessionmaker(
                autoflush=True,
                autocommit=False,
                bind=self.db_engine
            )
        )
        self.notification = NotificationService()
        self.email = "deeppatel770@gmail.com"

    def start(self, outputPath, outputFile, labels, fourcc, fps, width, height, user_pets):
        self.recording = True
        self.outputPath = outputPath
        self.outputFile = outputFile
        self.labels = labels
        self.user_pets = user_pets
        print(self.frames)
        self.writer = cv2.VideoWriter(outputPath, fourcc, fps,
                                      (width, height), True)
        self.Q = Queue()
        for i in range(len(self.frames), 0, -1):
            self.Q.put(self.frames[i - 1])
        self.thread = Thread(target=self.write, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self, frame):
        self.frames.appendleft(frame)
        if self.recording:
            self.Q.put(frame)

    def write(self):
        while True:
            if not self.recording:
                return
            if not self.Q.empty():
                frame = self.Q.get()
                self.writer.write(frame)
            else:
                time.sleep(self.timeout)

    def flush(self):
        while not self.Q.empty():
            frame = self.Q.get()
            self.writer.write(frame)

    def finish(self):
        self.recording = False
        self.thread.join()
        self.flush()
        self.writer.release()
        self.save_key_event_clip()
        self.outputPath = None
        self.outputFile = None
        self.labels = None

    def save_key_event_clip(self):
        result = self.s3_service.upload_file('video-snapshots', self.outputPath, self.outputFile)
        # Only grant access if a user_cat or user_dog has been detected and if there is not bird in their mouth
        if result:
            access_granted = False
            if any(self.user_pets) in self.labels: #or 'user_dog' in self.labels:
                if 'bird_in_cat_mouth' not in self.labels and 'bird_in_dog_mouth' not in self.labels:
                    access_granted = True
                    print("access_granted")
                    self.notification.send_notification("User Pet Detected", self.email,
                                                        "Detect at time: " + datetime.datetime.now().strftime(
                                                            "%Y/%m/%d-%H:%M:%S"))
            new_event = Events(classes=str(self.labels), video=self.outputFile, access_granted=access_granted)
            db_session = self.DBSession
            db_session.add(new_event)
            db_session.commit()
