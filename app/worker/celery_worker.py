import smtplib
import ssl

from .celery_app import app
from ..constants import SENDER_PASSWORD, SENDER_EMAIL, PORT, HOST


@app.task
def send_email_task(generated_code, receiver_email):
    message = f"""\
    Subject: Код активации

    Ваш код активации {generated_code}""".encode('utf-8').strip()

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(HOST, PORT, context=context) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver_email, message)



