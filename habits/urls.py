from django.urls import include, path
from rest_framework.routers import DefaultRouter

from habits.views import HabitViewSet, PublicHabitViewSet

app_name = "habits"

router = DefaultRouter()
router.register(r"habits", HabitViewSet, basename="habits")
router.register(r"habits/public", PublicHabitViewSet, basename="public-habits")

urlpatterns = [
    path("", include(router.urls)),
]
