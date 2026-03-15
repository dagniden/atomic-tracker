import logging
from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from habits.models import Habit
from telegram_integration.services import TelegramService


logger = logging.getLogger(__name__)


@shared_task
def send_habit_reminders():
    now = timezone.localtime()
    habits = Habit.objects.filter(
        time__hour=now.hour,
        time__minute=now.minute,
        user__telegram_chat_id__isnull=False,
    ).select_related("user", "related_habit")

    sent_count = 0
    for habit in habits:
        if habit.last_reminded_at and now < habit.last_reminded_at + timedelta(days=habit.periodicity):
            continue

        chat_id = habit.user.telegram_chat_id
        if not chat_id:
            continue

        if TelegramService.send_habit_reminder(habit, chat_id):
            habit.last_reminded_at = now
            habit.save(update_fields=["last_reminded_at"])
            sent_count += 1
        else:
            logger.warning("Reminder was not sent for habit_id=%s", habit.id)

    return sent_count
