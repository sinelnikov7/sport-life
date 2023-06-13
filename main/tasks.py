import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import dotenv

from sport_life.celery import app

dotenv.load_dotenv()
EMAIL_SENDER = os.environ.get('EMAIL_SENDER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')


# @app.task(bind=True)
def send_confirm_email(*args, **kwargs):
    """Отправка кода подтверждения регистрации на email"""
    to_email = kwargs['to_email']
    send_code = kwargs['send_code']
    password = kwargs['password']
    email_sender = EMAIL_SENDER
    email_password = EMAIL_PASSWORD
    smtp_server = smtplib.SMTP('smtp.yandex.ru', 587)
    smtp_server.starttls()
    msg = MIMEMultipart()
    msg.attach(MIMEText(
        f"Здравствуйте!\nВаш логин - {to_email}\nПароль - {password}\nДля продолжения введите проверочный код регистрации на сайте sportlife - {str(send_code)}"))
    msg["From"] = email_sender
    msg["Subject"] = "Код подтверждения регистрации на сайте sportlife"
    smtp_server.set_debuglevel(1)
    smtp_server.login(email_sender, email_password)
    smtp_server.sendmail(email_sender, to_email, msg.as_string())
    smtp_server.quit()