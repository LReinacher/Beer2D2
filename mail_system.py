import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import settings


def send_mail(subject, message, to):
    fromaddr = "Beer2D2.code@gmail.com"
    toaddr = to
    msg = MIMEMultipart()
    msg['From'] = settings.name + " <Beer2D2.code@gmail.com>"
    msg['To'] = toaddr
    msg['Subject'] = subject

    body = message
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "Beer2D2Beer2D2")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()