from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from habits.models import Habit
from tasks.reminder_tasks import send_habit_reminders


User = get_user_model()


class ReminderTaskTests(TestCase):
    @patch("tasks.reminder_tasks.TelegramService.send_habit_reminder", return_value=True)
    def test_due_habit_is_sent_once(self, send_habit_reminder_mock):
        now = timezone.now().replace(second=0, microsecond=0)
        user = User.objects.create_user(
            username="reminder@example.com",
            email="reminder@example.com",
            password="SecurePass123!",
            telegram_chat_id=999,
        )
        habit = Habit.objects.create(
            user=user,
            action="Read",
            place="Home",
            time=now.time(),
            is_pleasant=False,
            periodicity=2,
            duration=30,
            last_reminded_at=now - timedelta(days=3),
        )

        with patch("tasks.reminder_tasks.timezone.localtime", return_value=now):
            result = send_habit_reminders()

        habit.refresh_from_db()
        self.assertEqual(result, 1)
        self.assertEqual(habit.last_reminded_at, now)
        send_habit_reminder_mock.assert_called_once_with(habit, 999)

    @patch("tasks.reminder_tasks.TelegramService.send_habit_reminder", return_value=True)
    def test_habit_is_skipped_when_periodicity_not_elapsed(self, send_habit_reminder_mock):
        now = timezone.now().replace(second=0, microsecond=0)
        user = User.objects.create_user(
            username="skip@example.com",
            email="skip@example.com",
            password="SecurePass123!",
            telegram_chat_id=999,
        )
        Habit.objects.create(
            user=user,
            action="Read",
            place="Home",
            time=now.time(),
            is_pleasant=False,
            periodicity=7,
            duration=30,
            last_reminded_at=now - timedelta(days=1),
        )

        with patch("tasks.reminder_tasks.timezone.localtime", return_value=now):
            result = send_habit_reminders()

        self.assertEqual(result, 0)
        send_habit_reminder_mock.assert_not_called()
