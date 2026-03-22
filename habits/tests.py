from datetime import time
from unittest.mock import Mock, patch

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from habits.services import TelegramService
from habits.tasks import send_habit_reminders


User = get_user_model()


class HabitAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="owner",
            email="owner@example.com",
            password="SecurePass123!",
        )
        self.other_user = User.objects.create_user(
            username="other",
            email="other@example.com",
            password="SecurePass123!",
        )
        self.client.force_authenticate(self.user)

    def create_habit(self, user, **kwargs):
        payload = {
            "action": "Прочитать книгу",
            "place": "Дом",
            "time": time(21, 0),
            "periodicity": 1,
            "duration": 60,
            "is_public": False,
        }
        payload.update(kwargs)
        return Habit.objects.create(user=user, **payload)

    def test_list_returns_only_current_user_habits(self):
        own_habit = self.create_habit(self.user, action="Своя привычка")
        self.create_habit(self.other_user, action="Чужая привычка")

        response = self.client.get(reverse("habits:habits-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["id"], own_habit.id)

    def test_public_habits_endpoint_returns_only_public_habits(self):
        public_habit = self.create_habit(self.other_user, is_public=True)
        self.create_habit(self.other_user, action="Скрытая", is_public=False)

        response = self.client.get(reverse("habits:public-habits-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["id"], public_habit.id)

    def test_pagination_returns_five_items_per_page(self):
        for index in range(6):
            self.create_habit(self.user, action=f"Привычка {index}")

        response = self.client.get(reverse("habits:habits-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 5)
        self.assertIsNotNone(response.data["next"])

    def test_create_habit_assigns_current_user(self):
        response = self.client.post(
            reverse("habits:habits-list"),
            {
                "action": "Сделать зарядку",
                "place": "Дом",
                "time": "08:00:00",
                "periodicity": 1,
                "duration": 90,
                "is_public": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.get(pk=response.data["id"]).user, self.user)

    def test_create_habit_rejects_reward_and_related_habit_together(self):
        related_habit = self.create_habit(self.user, is_pleasant=True)

        response = self.client.post(
            reverse("habits:habits-list"),
            {
                "action": "Сделать зарядку",
                "place": "Дом",
                "time": "08:00:00",
                "periodicity": 1,
                "duration": 90,
                "reward": "Кофе",
                "related_habit": related_habit.id,
                "is_public": False,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Нельзя одновременно", str(response.data))

    def test_create_habit_rejects_non_pleasant_related_habit(self):
        related_habit = self.create_habit(self.user, is_pleasant=False)

        response = self.client.post(
            reverse("habits:habits-list"),
            {
                "action": "Сделать зарядку",
                "place": "Дом",
                "time": "08:00:00",
                "periodicity": 1,
                "duration": 90,
                "related_habit": related_habit.id,
                "is_public": False,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Связанная привычка должна быть приятной", str(response.data))

    def test_create_habit_rejects_pleasant_habit_with_reward(self):
        response = self.client.post(
            reverse("habits:habits-list"),
            {
                "action": "Послушать музыку",
                "place": "Дом",
                "time": "20:00:00",
                "periodicity": 1,
                "duration": 60,
                "reward": "Шоколад",
                "is_pleasant": True,
                "is_public": False,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Приятная привычка не может иметь текстовое вознаграждение", str(response.data))

    def test_create_habit_rejects_duration_more_than_120_seconds(self):
        response = self.client.post(
            reverse("habits:habits-list"),
            {
                "action": "Сделать зарядку",
                "place": "Дом",
                "time": "08:00:00",
                "periodicity": 1,
                "duration": 121,
                "is_public": False,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Ensure this value is less than or equal to 120", str(response.data))

    def test_create_habit_rejects_periodicity_more_than_7_days(self):
        response = self.client.post(
            reverse("habits:habits-list"),
            {
                "action": "Сделать зарядку",
                "place": "Дом",
                "time": "08:00:00",
                "periodicity": 8,
                "duration": 90,
                "is_public": False,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Ensure this value is less than or equal to 7", str(response.data))

    def test_patch_habit_keeps_validation_rules(self):
        related_habit = self.create_habit(self.user, action="Ванна", is_pleasant=True)
        habit = self.create_habit(self.user, related_habit=related_habit)

        response = self.client.patch(
            reverse("habits:habits-detail", args=[habit.pk]),
            {"reward": "Кофе"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Нельзя одновременно", str(response.data))

    def test_cannot_update_foreign_habit(self):
        foreign_habit = self.create_habit(self.other_user)

        response = self.client.patch(
            reverse("habits:habits-detail", args=[foreign_habit.pk]),
            {"action": "Новая привычка"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


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
