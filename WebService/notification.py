import smtplib
from email.message import EmailMessage


class notification:
    def __init__(self):
        self.server = None
        self.msg = EmailMessage()

    def log_in(self):
        self.server = smtplib.SMTP("smtp.gmail.com", 587)
        self.server.starttls()
        self.server.login("abirshah28@gmail.com", "ubizixrpedoxlscu")

    def quit(self):
        self.server.quit()

    def send_notification(self, subject, receiver_email, content):
        n = notification()
        n.log_in()
        n.msg['Subject'] = subject
        n.msg['From'] = 'Automated Pet Door'
        n.msg['To'] = receiver_email
        n.msg.set_content(content)
        n.server.send_message(n.msg)
        n.quit()
