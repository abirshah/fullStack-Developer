from collections import deque
from threading import Thread
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from queue import Queue
from Services.s3_service import S3Service
from Models.events import Events
import mysql.connector
import time
import cv2
DATABASE_CONNECTION_INFO = 'mysql://admin:abir1971@pet-project.cqlvbpbplnsv.us-east-2.rds.amazonaws.com/automated_pet_door'

class KeyClipService:
    def __init__(self, bufSize=64, timeout=1.0):
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


    def start(self, outputPath, outputFile, labels, fourcc, fps):
        self.recording = True
        self.outputPath = outputPath
        self.outputFile = outputFile
        self.labels = labels
        self.writer = cv2.VideoWriter(outputPath, fourcc, fps,
                                      (self.frames[0].shape[1], self.frames[0].shape[0]), True)
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
        if result:
            new_event = Events(classes=str(self.labels), video=self.outputFile, access_granted=False)
            db_session = self.DBSession
            db_session.add(new_event)
            db_session.commit()
