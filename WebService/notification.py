import smtplib
from email.message import EmailMessage

msg = EmailMessage()
msg['Subject'] = 'Detected'
msg['From'] = 'Automated Pet Door'
msg['To'] = 'abir_mtl@hotmail.com'
msg.set_content("Testing email")

server = smtplib.SMTP("smtp.gmail.com", 587)

server.starttls()

server.login("abirshah28@gmail.com", "ubizixrpedoxlscu")

server.send_message(msg)

server.quit()

