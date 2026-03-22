from unittest.mock import patch

from django.test import TestCase

from habits.services import TelegramService


class TelegramServiceTests(TestCase):
    @patch("habits.services.requests.post")
    def test_send_message(self, mocked_post):
        mocked_post.return_value.ok = True

        result = TelegramService.send_message(123456, "test")

        self.assertTrue(result)
        mocked_post.assert_called_once()
