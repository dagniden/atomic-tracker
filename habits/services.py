import logging

from django.conf import settings
from notifiers import get_notifier


logger = logging.getLogger(__name__)
telegram = get_notifier("telegram")


class TelegramService:
    @classmethod
    def send_message(cls, chat_id, text):
        response = telegram.notify(
            token=settings.TELEGRAM_BOT_TOKEN,
            chat_id=chat_id,
            message=text,
        )
        if response.ok:
            return True

        logger.warning("Telegram sendMessage failed: %s", response.errors)
        return False

    @classmethod
    def send_habit_reminder(cls, habit):
        chat_id = habit.user.telegram_chat_id
        if not chat_id:
            return False
        return cls.send_message(chat_id=chat_id, text=cls.render_habit_reminder(habit))

    @staticmethod
    def render_habit_reminder(habit):
        lines = [
            "Напоминание!",
            "",
            f"Я буду {habit.action} в {habit.time.strftime('%H:%M')} в {habit.place}",
        ]
        if habit.related_habit:
            lines.append(f"После выполнения: {habit.related_habit.action}")
        elif habit.reward:
            lines.append(f"Вознаграждение: {habit.reward}")
        return "\n".join(lines)
