from asgiref.sync import sync_to_async
from django.conf import settings
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from telegram_integration.models import TelegramLinkToken


@sync_to_async
def get_unused_token(token_value: str):
    return TelegramLinkToken.objects.select_related("user").get(token=token_value, is_used=False)


@sync_to_async
def link_chat_to_user(token: TelegramLinkToken, chat_id: int):
    user = token.user
    user.telegram_chat_id = chat_id
    user.save(update_fields=["telegram_chat_id"])
    token.is_used = True
    token.save(update_fields=["is_used"])


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    chat = update.effective_chat
    args = context.args

    if not message or not chat:
        return

    if not args:
        await message.reply_text("Передайте токен в формате /start <token>.")
        return

    token_value = args[0]
    try:
        token = await get_unused_token(token_value)
    except TelegramLinkToken.DoesNotExist:
        await message.reply_text("Токен не найден или уже использован.")
        return

    if token.is_expired:
        await message.reply_text("Срок действия токена истек. Сгенерируйте новый токен в приложении.")
        return

    await link_chat_to_user(token, chat.id)

    await message.reply_text("Аккаунт Telegram успешно привязан.")


def build_application() -> Application:
    if not settings.TELEGRAM_BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not configured.")
    return Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()


def run_bot() -> None:
    application = build_application()
    application.add_handler(CommandHandler("start", start_command))
    application.run_polling()
