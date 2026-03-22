from datetime import time
from unittest.mock import Mock, patch

from django.contrib.auth import get_user_model
from django.test import override_settings
from django.test import TestCase

from habits.models import Habit
from habits.services import TelegramService
from habits.tasks import send_habit_reminders


User = get_user_model()


class HabitReminderTaskTests(TestCase):
    @patch("habits.tasks.TelegramService.send_habit_reminder")
    def test_send_habit_reminders_updates_last_reminded_at(self, mocked_send):
        mocked_send.return_value = True
        user = User.objects.create_user(
            username="ivan",
            email="ivan@example.com",
            password="SecurePass123!",
            telegram_chat_id=123456,
        )
        habit = Habit.objects.create(
            user=user,
            action="Прочитать книгу",
            place="Дом",
            time=time(12, 0),
            periodicity=1,
            duration=30,
        )

        with patch("habits.tasks.timezone.localtime") as mocked_localtime:
            from django.utils import timezone

            now = timezone.now().replace(hour=12, minute=0, second=0, microsecond=0)
            mocked_localtime.return_value = now
            result = send_habit_reminders()

        habit.refresh_from_db()
        self.assertEqual(result, 1)
        self.assertIsNotNone(habit.last_reminded_at)


class TelegramServiceTests(TestCase):
    @override_settings(TELEGRAM_BOT_TOKEN="test-bot-token")
    @patch("habits.services.telegram.notify")
    def test_send_message_uses_notifier_with_config_token(self, mocked_notify):
        mocked_notify.return_value = Mock(ok=True)

        result = TelegramService.send_message(chat_id=578672315, text="Текст уведомления")

        self.assertTrue(result)
        mocked_notify.assert_called_once_with(
            token="test-bot-token",
            chat_id=578672315,
            message="Текст уведомления",
        )

    @override_settings(TELEGRAM_BOT_TOKEN="test-bot-token")
    @patch("habits.services.telegram.notify")
    def test_send_message_returns_false_on_notifier_failure(self, mocked_notify):
        mocked_notify.return_value = Mock(ok=False, errors=["bad request"])

        result = TelegramService.send_message(chat_id=578672315, text="Текст уведомления")

        self.assertFalse(result)
