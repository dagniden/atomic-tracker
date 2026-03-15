from django.core.management.base import BaseCommand, CommandError

from telegram_integration.bot import run_bot


class Command(BaseCommand):
    help = "Run Telegram bot in polling mode"

    def handle(self, *args, **options):
        try:
            run_bot()
        except RuntimeError as exc:
            raise CommandError(str(exc)) from exc
