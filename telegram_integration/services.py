import logging

import requests
from django.conf import settings


logger = logging.getLogger(__name__)


class TelegramService:
    @classmethod
    def _api_url(cls, method: str) -> str:
        return f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/{method}"

    @classmethod
    def send_message(cls, chat_id: int, text: str) -> bool:
        if not settings.TELEGRAM_BOT_TOKEN:
            logger.warning("Telegram bot token is not configured.")
            return False

        try:
            response = requests.post(
                cls._api_url("sendMessage"),
                json={"chat_id": chat_id, "text": text},
                timeout=10,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            logger.warning("Failed to send Telegram message: %s", exc)
            return False
        return True

    @classmethod
    def send_habit_reminder(cls, habit, chat_id: int) -> bool:
        text = [
            "⏰ Напоминание!",
            "",
            f"Я буду {habit.action.lower()} в {habit.time.strftime('%H:%M')} в {habit.place.lower()}",
        ]
        if habit.related_habit:
            text.append(f"После выполнения: {habit.related_habit.action.lower()}")
        elif habit.reward:
            text.append(f"Вознаграждение: {habit.reward.lower()}")
        return cls.send_message(chat_id=chat_id, text="\n".join(text))
