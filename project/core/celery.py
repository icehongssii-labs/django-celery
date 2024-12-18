import os

from celery import Celery
from celery.schedules import crontab, schedule
from tasks.sample_tasks import send_msm
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


CELERY_BEAT_SCHEDULE = {
    "sample_task": {
        "task": "tasks.sample_tasks.send_msm",
        "schedule": crontab(minute="*/1"),
    },
}
app.conf.beat_schedule = (CELERY_BEAT_SCHEDULE)