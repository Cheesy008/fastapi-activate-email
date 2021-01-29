import smtplib
import ssl
from email.mime.text import MIMEText
from jinja2 import Template

from .celery_app import app
from ..constants import SENDER_PASSWORD, SENDER_EMAIL, PORT, HOST


@app.task
def send_email_task(generated_code, receiver_email):
    context = ssl.create_default_context()

    with open('app/templates/email.html', 'r') as f:
        template_string = f.read()

    template = Template(template_string)
    rendered_template = template.render(generated_code=generated_code)

    message = MIMEText(rendered_template, 'html',  _charset="UTF-8")
    message['Subject'] = 'Активация аккаунта'
    message['From'] = SENDER_EMAIL

    with smtplib.SMTP_SSL(HOST, PORT, context=context) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver_email, message.as_string())



