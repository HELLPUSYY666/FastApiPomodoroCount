from celery import Celery
from celery.schedules import crontab

from app.settings import settings

celery = Celery(__name__)

celery.conf.broker_url = settings.CELERY_REDIS_URL
celery.conf.result_backend = settings.CELERY_REDIS_URL
print(settings.CELERY_REDIS_URL)

celery.conf.beat_schedule = {
    "generate-ai-plan-daily": {
        "task": "generate_ai_plan",
        "schedule": crontab(hour=0, minute=0),
    },
}
