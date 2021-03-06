import smtplib
from email.message import EmailMessage
import time


class NotificationService:
    def __init__(self):
        self.notification = None
        self.start_time = None
        self.detected_objects = list()

    def send_notification(self, subject, receiver_email, content, detected_object):
        if self.timer(detected_object):
            self.notification = Sender()
            self.notification.log_in()
            self.notification.send(subject, receiver_email, content)
            self.notification.quit()
        else:
            print("Last email was sent less than a minute ago")

    def start_timer(self):
        self.start_time = time.perf_counter()

    def timer(self, detected_object):
        if self.start_time is None:
            self.start_timer()
            self.detected_objects.append(detected_object)
            return True
        elapsed_time = time.perf_counter() - self.start_time
        if detected_object not in self.detected_objects:
            self.detected_objects.append(detected_object)
            return True
        if elapsed_time >= 60:
            self.stop()
            return True
        return False

    def stop(self):
        self.start_time = None
        self.detected_objects.clear()


class Sender:
    def __init__(self):
        self.server = None
        self.msg = EmailMessage()

    def log_in(self):
        self.server = smtplib.SMTP("smtp.gmail.com", 587)
        self.server.starttls()
        self.server.login("abirshah28@gmail.com", "ubizixrpedoxlscu")

    def quit(self):
        self.server.quit()

    def send(self, subject, receiver_email, content):
        self.msg['Subject'] = subject
        self.msg['From'] = 'Automated Pet Door'
        self.msg['To'] = receiver_email
        self.msg.set_content(content)
        self.server.send_message(self.msg)
