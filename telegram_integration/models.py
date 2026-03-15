from datetime import timedelta
from secrets import token_urlsafe

from django.conf import settings
from django.db import models
from django.utils import timezone


class TelegramLinkToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="telegram_tokens")
    token = models.CharField(max_length=64, unique=True)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        ordering = ("-created_at",)

    @classmethod
    def issue_for_user(cls, user):
        return cls.objects.create(
            user=user,
            token=token_urlsafe(16),
            expires_at=timezone.now() + timedelta(minutes=15),
        )

    @property
    def is_expired(self) -> bool:
        return timezone.now() >= self.expires_at

    def __str__(self) -> str:
        return self.token
