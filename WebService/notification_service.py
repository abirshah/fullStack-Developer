import smtplib
from email.message import EmailMessage
import time


class NotificationService:
    def __init__(self):
        self.notification = None
        self.start_time = None

    def send_notification(self, subject, receiver_email, content):
        if self.timer():
            self.notification = Sender()
            self.notification.log_in()
            self.notification.msg['Subject'] = subject
            self.notification.msg['From'] = 'Automated Pet Door'
            self.notification.msg['To'] = receiver_email
            self.notification.msg.set_content(content)
            self.notification.server.send_message(self.notification.msg)
            self.notification.quit()
        else:
            print("Last email was sent less than a minute ago")

    def start_timer(self):
        self.start_time = time.perf_counter()

    def timer(self):
        if self.start_time is None:
            self.start_timer()
            return True
        elapsed_time = time.perf_counter() - self.start_time
        if elapsed_time == 60:
            self.stop()
            return True
        return False

    def stop(self):
        self.start_time = None


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
