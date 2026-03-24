from celery import shared_task
from datetime import timedelta
import logging

from django.utils import timezone

from habits.models import Habit
from habits.services import TelegramService


logger = logging.getLogger(__name__)


@shared_task
def send_habit_reminders():
    now = timezone.localtime()
    habits = Habit.objects.filter(
        user__telegram_chat_id__isnull=False,
        time__hour=now.hour,
        time__minute=now.minute,
    ).select_related("user", "related_habit")

    sent_count = 0
    for habit in habits:
        if habit.last_reminded_at and now < habit.last_reminded_at + timedelta(days=habit.periodicity):
            continue

        if TelegramService.send_habit_reminder(habit):
            habit.last_reminded_at = now
            habit.save(update_fields=["last_reminded_at"])
            sent_count += 1
        else:
            logger.warning("Failed to send reminder for habit %s", habit.pk)

    return sent_count
