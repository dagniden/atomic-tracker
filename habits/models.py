from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Habit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="habits",
        verbose_name="Пользователь",
        help_text="Владелец привычки",
    )
    action = models.CharField(
        max_length=255,
        verbose_name="Действие",
        help_text="Что именно нужно сделать",
    )
    place = models.CharField(
        max_length=255,
        verbose_name="Место",
        help_text="Где выполняется привычка",
    )
    time = models.TimeField(
        db_index=True,
        verbose_name="Время",
        help_text="Во сколько выполнять привычку",
    )
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name="Приятная привычка",
        help_text="Можно использовать как вознаграждение",
    )
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="dependent_habits",
        verbose_name="Связанная привычка",
        help_text="Связанная приятная привычка",
    )
    reward = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Вознаграждение",
        help_text="Текстовое вознаграждение",
    )
    periodicity = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        verbose_name="Периодичность",
        help_text="Периодичность в днях: от 1 до 7",
    )
    duration = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(120)],
        verbose_name="Длительность",
        help_text="Время выполнения в секундах, не более 120",
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name="Публичная привычка",
        help_text="Доступна для просмотра другим пользователям",
    )
    last_reminded_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Последнее напоминание",
        help_text="Дата и время последнего напоминания",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создана")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлена")

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ("time", "id")
        indexes = [
            models.Index(fields=["user", "time"]),
            models.Index(fields=["is_public"]),
        ]

    def __str__(self):
        return f"{self.action} ({self.time})"
