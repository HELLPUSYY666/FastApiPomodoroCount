import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict

from celery import Celery
from celery.contrib.abortable import AbortableTask

from app.settings import settings

celery = Celery(__name__)

celery.conf.broker_url = settings.CELERY_REDIS_URL
celery.conf.result_backend = settings.CELERY_REDIS_URL
print(settings.CELERY_REDIS_URL)


@celery.task(name="send_email_task")
def send_email_task(subject: str, text: str, to: str):
    msg = _build_message(subject=subject, text=text, to=to)
    _send_message(msg=msg)


def _build_message(subject: str, text: str, to: str) -> MIMEMultipart:
    msg = MIMEMultipart()

    msg["From"] = settings.from_email
    msg["To"] = to
    msg["Subject"] = subject
    msg.attach(MIMEText(text, "plain"))
    return msg


def _send_message(msg: MIMEMultipart) -> None:
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT, context=context)
    server.login(settings.from_email, settings.SMTP_PASSWORD)
    server.send_message(msg=msg)
    server.quit()


@celery.task(name="generate_ai_plan", bind=True, base=AbortableTask)
def generate_ai_plan_task(requirements: str, progress_data: Dict[int]) -> None:
    pass
