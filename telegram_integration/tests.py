from datetime import timedelta
from types import SimpleNamespace
from unittest.mock import AsyncMock

from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from telegram_integration.bot import start_command
from telegram_integration.models import TelegramLinkToken


User = get_user_model()


class TelegramApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user@example.com",
            email="user@example.com",
            password="SecurePass123!",
        )
        self.client.force_authenticate(self.user)

    def test_generate_link_token(self):
        response = self.client.get(reverse("telegram-link-token"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertTrue(TelegramLinkToken.objects.filter(user=self.user, token=response.data["token"]).exists())


class TelegramBotTests(TestCase):
    def test_start_command_links_telegram_account(self):
        user = User.objects.create_user(
            username="bot@example.com",
            email="bot@example.com",
            password="SecurePass123!",
        )
        token = TelegramLinkToken.objects.create(
            user=user,
            token="valid-token",
            expires_at=timezone.now() + timedelta(minutes=15),
        )
        reply_text = AsyncMock()
        update = SimpleNamespace(
            effective_message=SimpleNamespace(reply_text=reply_text),
            effective_chat=SimpleNamespace(id=321),
        )
        context = SimpleNamespace(args=["valid-token"])

        async_to_sync(start_command)(update, context)

        user.refresh_from_db()
        token.refresh_from_db()
        self.assertEqual(user.telegram_chat_id, 321)
        self.assertTrue(token.is_used)
        reply_text.assert_awaited_once()
