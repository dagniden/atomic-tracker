# Atomic Tracker

Backend для курсового проекта "Трекер привычек" на Django REST Framework.

## Что реализовано

- регистрация и JWT-аутентификация;
- CRUD личных привычек;
- список публичных привычек;
- пагинация по 5 элементов;
- бизнес-валидаторы для привычек;
- Celery-задача для отправки напоминаний в Telegram;
- Swagger и Redoc документация;
- CORS и настройка через переменные окружения.

## Запуск проекта

1. Скопируйте `.env.example` в `.env`.
2. Установите зависимости:

```bash
poetry install
```

3. Примените миграции:

```bash
poetry run python manage.py migrate
```

4. Запустите сервер:

```bash
poetry run python manage.py runserver
```

## Celery

Для напоминаний нужен Redis и два процесса:

```bash
poetry run celery -A config worker --loglevel=info
poetry run celery -A config beat --loglevel=info
```

## Документация API

- `http://127.0.0.1:8000/api/schema/swagger-ui/`
- `http://127.0.0.1:8000/api/schema/redoc/`

## Основные эндпоинты

- `POST /api/v1/users/register/`
- `POST /api/v1/users/login/`
- `POST /api/v1/users/token/refresh/`
- `GET|POST /api/v1/habits/`
- `GET|PATCH|PUT|DELETE /api/v1/habits/<id>/`
- `GET /api/v1/habits/public/`

## Проверки

```bash
poetry run flake8 . --exclude=.git,__pycache__,.venv,migrations
poetry run python manage.py test
```
