from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="habits")
    action = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    time = models.TimeField()
    is_pleasant = models.BooleanField(default=False)
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="dependent_habits",
    )
    reward = models.CharField(max_length=255, blank=True)
    periodicity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(7)])
    duration = models.PositiveIntegerField(validators=[MaxValueValidator(120)])
    is_public = models.BooleanField(default=False)
    last_reminded_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("time", "id")

    def __str__(self) -> str:
        return self.action
