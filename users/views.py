from rest_framework import viewsets
from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema, extend_schema_view, inline_serializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.serializers import CharField, EmailField, Serializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

from users.models import User
from users.serializers import CustomTokenObtainPairSerializer, UserSerializer


class TokenRefreshRequestSerializer(Serializer):
    refresh = CharField()


class TokenRefreshResponseSerializer(Serializer):
    access = CharField()


@extend_schema_view(
    list=extend_schema(
        tags=["Auth"],
        summary="Список пользователей",
        description="Возвращает список зарегистрированных пользователей. Эндпоинт доступен только авторизованным пользователям.",
        responses={200: UserSerializer(many=True)},
    ),
    create=extend_schema(
        tags=["Auth"],
        summary="Регистрация пользователя",
        description="Создает нового пользователя и возвращает его базовые данные.",
        request=UserSerializer,
        responses={201: UserSerializer},
        examples=[
            OpenApiExample(
                "Пример регистрации",
                value={
                    "username": "ivan",
                    "email": "ivan@example.com",
                    "password": "SecurePass123!",
                },
                request_only=True,
            )
        ],
    ),
    retrieve=extend_schema(
        tags=["Auth"],
        summary="Детали пользователя",
        description="Возвращает данные конкретного пользователя.",
        responses={200: UserSerializer},
    ),
    update=extend_schema(tags=["Auth"], summary="Обновить пользователя"),
    partial_update=extend_schema(tags=["Auth"], summary="Частично обновить пользователя"),
    destroy=extend_schema(tags=["Auth"], summary="Удалить пользователя"),
)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "create":
            # Создание пользователя доступно всем (регистрация)
            self.permission_classes = [AllowAny]
        else:
            # Все остальные операции требуют авторизации
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()


@extend_schema(
    tags=["Auth"],
    summary="Получить JWT токены",
    description="Аутентификация по email и паролю. Возвращает access и refresh токены.",
    request=inline_serializer(
        name="TokenObtainRequest",
        fields={
            "email": EmailField(),
            "password": CharField(),
        },
    ),
    responses={
        200: inline_serializer(
            name="TokenObtainResponse",
            fields={
                "refresh": CharField(),
                "access": CharField(),
            },
        ),
        401: OpenApiResponse(description="Неверные учетные данные."),
    },
    examples=[
        OpenApiExample(
            "Пример логина",
            value={
                "email": "ivan@example.com",
                "password": "SecurePass123!",
            },
            request_only=True,
        )
    ],
)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@extend_schema(
    tags=["Auth"],
    summary="Обновить access token",
    description="Принимает refresh token и возвращает новый access token.",
    request=TokenRefreshRequestSerializer,
    responses={200: TokenRefreshResponseSerializer},
    examples=[
        OpenApiExample(
            "Пример refresh",
            value={
                "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            },
            request_only=True,
        )
    ],
)
class CustomTokenRefreshView(TokenRefreshView):
    pass

