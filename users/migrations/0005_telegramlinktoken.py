import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_user_telegram_chat_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="TelegramLinkToken",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("token", models.CharField(max_length=64, unique=True, verbose_name="Токен")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Создан")),
                ("expires_at", models.DateTimeField(verbose_name="Истекает")),
                ("is_used", models.BooleanField(default=False, verbose_name="Использован")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="telegram_link_tokens",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Токен привязки Telegram",
                "verbose_name_plural": "Токены привязки Telegram",
                "ordering": ("-created_at",),
            },
        ),
    ]
