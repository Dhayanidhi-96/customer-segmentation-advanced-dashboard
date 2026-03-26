from __future__ import annotations

from celery import Celery
from celery.schedules import crontab

from config import settings


def _parse_cron(expr: str) -> crontab:
    parts = expr.split()
    if len(parts) != 5:
        return crontab(hour=0, minute=0)
    minute, hour, day_of_month, month_of_year, day_of_week = parts
    return crontab(
        minute=minute,
        hour=hour,
        day_of_month=day_of_month,
        month_of_year=month_of_year,
        day_of_week=day_of_week,
    )


celery_app = Celery("customer_segmentation", broker=settings.REDIS_URL, backend=settings.REDIS_URL)
celery_app.conf.update(
    timezone="UTC",
    enable_utc=True,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    beat_schedule={
        "nightly-email-campaign": {
            "task": "tasks.email_tasks.nightly_email_campaign",
            "schedule": _parse_cron(settings.EMAIL_CAMPAIGN_SCHEDULE),
        },
        "weekly-model-retrain": {
            "task": "tasks.retrain_tasks.weekly_model_retrain",
            "schedule": _parse_cron(settings.MODEL_RETRAIN_SCHEDULE),
        },
        "nightly-resegment": {
            "task": "tasks.segment_tasks.nightly_resegmentation",
            "schedule": crontab(hour=1, minute=30),
        },
    },
)

celery_app.autodiscover_tasks(["tasks"])
