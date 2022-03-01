import smtplib
from email.message import EmailMessage


class notification:
    def __init__(self):
        self.msg = EmailMessage()
        self.server = smtplib.SMTP("smtp.gmail.com", 587)

    def log_in(self):
        self.server.starttls()
        self.server.login("abirshah28@gmail.com", "ubizixrpedoxlscu")

    def quit(self):
        self.server.quit()

    def send_notification(self, subject, receiver_email, content):
        self.log_in()
        self.msg['Subject'] = subject
        self.msg['From'] = 'Automated Pet Door'
        self.msg['To'] = receiver_email
        self.msg.set_content(content)
        self.server.send_message(self.msg)
        self.quit()


if __name__ == "__main__":
    n = notication()
    n.login()
    n.send_notification(subject="Detected", receiver_email="deeppatel770@gmail.com", content="Testing email")
    n.quit()
