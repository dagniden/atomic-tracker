from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0005_telegramlinktoken"),
    ]

    operations = [
        migrations.DeleteModel(
            name="TelegramLinkToken",
        ),
    ]
