from django.urls import path

from habits.views import HabitViewSet, PublicHabitViewSet


urlpatterns = [
    path("habits", HabitViewSet.as_view({"get": "list", "post": "create"}), name="habit-list"),
    path(
        "habits/<int:pk>",
        HabitViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}),
        name="habit-detail",
    ),
    path("habits/public", PublicHabitViewSet.as_view({"get": "list"}), name="public-habit-list"),
    path("habits/public/<int:pk>", PublicHabitViewSet.as_view({"get": "retrieve"}), name="public-habit-detail"),
]
