import smtplib
from email.message import EmailMessage


class NotificationService:
    def __init__(self):
        self.n = None

    def send_notification(self, subject, receiver_email, content):
        self.n = Sender()
        self.n.log_in()
        self.n.msg['Subject'] = subject
        self.n.msg['From'] = 'Automated Pet Door'
        self.n.msg['To'] = receiver_email
        self.n.msg.set_content(content)
        self.n.server.send_message(self.n.msg)
        self.n.quit()


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
