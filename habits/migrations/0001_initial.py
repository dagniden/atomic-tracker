import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Habit",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "action",
                    models.CharField(
                        help_text="Что именно нужно сделать, например: Прочитать 20 страниц книги",
                        max_length=255,
                        verbose_name="Действие",
                    ),
                ),
                (
                    "place",
                    models.CharField(
                        help_text="Где выполняется привычка",
                        max_length=255,
                        verbose_name="Место",
                    ),
                ),
                (
                    "time",
                    models.TimeField(db_index=True, help_text="Во сколько выполнять привычку", verbose_name="Время"),
                ),
                (
                    "is_pleasant",
                    models.BooleanField(
                        default=False,
                        help_text="Можно использовать как вознаграждение для другой привычки",
                        verbose_name="Приятная привычка",
                    ),
                ),
                (
                    "reward",
                    models.CharField(
                        blank=True,
                        help_text="Текстовое описание награды после выполнения привычки",
                        max_length=255,
                        null=True,
                        verbose_name="Вознаграждение",
                    ),
                ),
                (
                    "periodicity",
                    models.PositiveSmallIntegerField(
                        default=1,
                        help_text="Периодичность выполнения в днях, от 1 до 7",
                        validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(7)],
                        verbose_name="Периодичность",
                    ),
                ),
                (
                    "duration",
                    models.PositiveSmallIntegerField(
                        help_text="Время выполнения привычки в секундах, не более 120",
                        validators=[django.core.validators.MaxValueValidator(120)],
                        verbose_name="Длительность",
                    ),
                ),
                (
                    "is_public",
                    models.BooleanField(
                        default=False,
                        help_text="Доступна для просмотра другим пользователям",
                        verbose_name="Публичная привычка",
                    ),
                ),
                (
                    "last_reminded_at",
                    models.DateTimeField(
                        blank=True,
                        help_text="Дата и время последней успешной отправки напоминания",
                        null=True,
                        verbose_name="Последнее напоминание",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Создана")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Обновлена")),
                (
                    "related_habit",
                    models.ForeignKey(
                        blank=True,
                        help_text="Приятная привычка, которая выступает вознаграждением",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="dependent_habits",
                        to="habits.habit",
                        verbose_name="Связанная привычка",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        help_text="Владелец привычки",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="habits",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Привычка",
                "verbose_name_plural": "Привычки",
                "ordering": ("time", "id"),
            },
        ),
        migrations.AddIndex(
            model_name="habit",
            index=models.Index(fields=["user", "time"], name="habits_habi_user_id_1cfbea_idx"),
        ),
        migrations.AddIndex(
            model_name="habit",
            index=models.Index(fields=["is_public"], name="habits_habi_is_publ_420eb9_idx"),
        ),
    ]
