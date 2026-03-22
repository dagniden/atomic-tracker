from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.pagination import HabitPagination
from habits.permissions import IsOwner
from habits.serializers import HabitSerializer


@extend_schema_view(
    list=extend_schema(
        tags=["Habits"],
        summary="Список привычек пользователя",
        description="Возвращает только привычки текущего авторизованного пользователя с пагинацией по 5 элементов.",
        responses={200: HabitSerializer(many=True)},
    ),
    create=extend_schema(
        tags=["Habits"],
        summary="Создать привычку",
        description=(
            "Создает полезную или приятную привычку. Нельзя одновременно передавать `reward` и `related_habit`. "
            "Приятная привычка не может иметь `reward` или `related_habit`, а связанная привычка должна быть приятной."
        ),
        request=HabitSerializer,
        responses={201: HabitSerializer, 400: OpenApiResponse(description="Ошибка бизнес-валидации.")},
        examples=[
            OpenApiExample(
                "Полезная привычка с наградой",
                value={
                    "action": "Прочитать 20 страниц книги",
                    "place": "Диван в гостиной",
                    "time": "21:00:00",
                    "is_pleasant": False,
                    "reward": "Выпить чашку горячего шоколада",
                    "periodicity": 1,
                    "duration": 30,
                    "is_public": False,
                },
                request_only=True,
            ),
            OpenApiExample(
                "Полезная привычка со связанной приятной",
                value={
                    "action": "Пробежать 3 км",
                    "place": "Городской парк",
                    "time": "07:00:00",
                    "is_pleasant": False,
                    "related_habit": 5,
                    "periodicity": 1,
                    "duration": 30,
                    "is_public": True,
                },
                request_only=True,
            ),
        ],
    ),
    retrieve=extend_schema(
        tags=["Habits"],
        summary="Детали привычки",
        description="Возвращает одну привычку текущего пользователя.",
        responses={200: HabitSerializer},
    ),
    update=extend_schema(tags=["Habits"], summary="Обновить привычку", request=HabitSerializer, responses={200: HabitSerializer}),
    partial_update=extend_schema(tags=["Habits"], summary="Частично обновить привычку", request=HabitSerializer, responses={200: HabitSerializer}),
    destroy=extend_schema(tags=["Habits"], summary="Удалить привычку", responses={204: OpenApiResponse(description="Привычка удалена.")}),
)
class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = HabitPagination

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user).select_related(
            "user", "related_habit"
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema_view(
    list=extend_schema(
        tags=["Public Habits"],
        summary="Список публичных привычек",
        description="Возвращает публичные привычки всех пользователей в режиме только для чтения.",
        responses={200: HabitSerializer(many=True)},
    ),
    retrieve=extend_schema(
        tags=["Public Habits"],
        summary="Детали публичной привычки",
        description="Возвращает одну публичную привычку.",
        responses={200: HabitSerializer},
    ),
)
class PublicHabitViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HabitPagination

    def get_queryset(self):
        return Habit.objects.filter(is_public=True).select_related(
            "user", "related_habit"
        )
