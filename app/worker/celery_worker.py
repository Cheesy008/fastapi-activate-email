import smtplib
import ssl
from email.mime.text import MIMEText

from .celery_app import app
from ..constants import SENDER_PASSWORD, SENDER_EMAIL, PORT, HOST


@app.task
def send_email_task(message, receiver_email):
    context = ssl.create_default_context()
    msg = MIMEText(message, 'html',  _charset="UTF-8")

    with smtplib.SMTP_SSL(HOST, PORT, context=context) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver_email, msg.as_bytes())



