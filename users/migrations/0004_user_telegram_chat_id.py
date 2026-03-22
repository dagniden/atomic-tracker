from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_remove_user_telegram_chat_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="telegram_chat_id",
            field=models.BigIntegerField(
                blank=True,
                help_text="ID чата пользователя в Telegram для отправки напоминаний",
                null=True,
                unique=True,
            ),
        ),
    ]
