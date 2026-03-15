from django.urls import path

from telegram_integration.views import generate_link_token


urlpatterns = [
    path("link-token", generate_link_token, name="telegram-link-token"),
]
