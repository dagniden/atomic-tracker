import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("atomic_tracker")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.imports = ("tasks.reminder_tasks",)
app.conf.beat_schedule = {
    "send-habit-reminders": {
        "task": "tasks.reminder_tasks.send_habit_reminders",
        "schedule": crontab(minute="*"),
    }
}
