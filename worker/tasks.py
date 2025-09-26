import asyncio
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.repository.task import TaskRepository
from app.repository.user import UserRepository
from app.service.ai_task import AIService
from app.settings import settings
from worker.celery import celery


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
    try:
        server = smtplib.SMTP_SSL(
            settings.SMTP_HOST, settings.SMTP_PORT, context=context
        )
        server.login(settings.from_email, settings.SMTP_PASSWORD)
        server.send_message(msg=msg)
    except Exception as e:
        print(f"Email send failed: {e}")
    finally:
        server.quit()


@celery.task(name="generate_ai_plan")
def generate_ai_plan_task() -> None:
    user_repo = UserRepository()
    task_repo = TaskRepository()
    ai_service = AIService(user_repo=user_repo, task_repo=task_repo)

    async def main():
        users = await user_repo.get_all_users()
        for user in users:
            print(f"Generating plan for user {user.id}")
        coros = [ai_service.generate_task_plan(user=user) for user in users]
        await asyncio.gather(*coros)

    asyncio.run(main())
    return None
