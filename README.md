# Atomic Tracker

Backend для учебного SPA-приложения "Трекер привычек" на Django REST Framework.

Цель проекта - дать пользователю API для регистрации, авторизации, создания привычек, просмотра публичных привычек и отправки напоминаний через Celery и Telegram.

## Что реализовано

- регистрация пользователя и JWT-аутентификация;
- CRUD для личных привычек;
- список публичных привычек только для чтения;
- пагинация по 5 элементов;
- бизнес-валидаторы для привычек;
- периодическая Celery-задача для напоминаний;
- отправка уведомлений в Telegram по сохраненному `telegram_chat_id`;
- Swagger и Redoc документация;
- настройка через переменные окружения;
- CORS для подключения фронтенда.

## Установка

1. Склонируйте репозиторий.
2. Установите Poetry, если он еще не установлен.
3. Скопируйте файл `.env.example` в `.env`.
4. Заполните переменные окружения при необходимости.
5. Установите зависимости:

```bash
poetry install
```

6. Примените миграции:

```bash
poetry run python manage.py migrate
```

## Переменные окружения

Основные переменные из `.env`:

- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `TIME_ZONE`
- `CORS_ALLOWED_ORIGINS`
- `CELERY_BROKER_URL`
- `CELERY_RESULT_BACKEND`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_BOT_USERNAME`

## Запуск проекта

Запуск Django-сервера:

```bash
poetry run python manage.py runserver
```

Для работы напоминаний отдельно запустите Redis, Celery worker и Celery beat.

Celery worker:

```bash
poetry run celery -A config worker --loglevel=info
```

Celery beat:

```bash
poetry run celery -A config beat --loglevel=info
```

## Telegram

Напоминания отправляются через Telegram Bot API по полю `telegram_chat_id`, сохраненному у пользователя.

Для учебного проекта интеграция сделана в облегченном виде: сервис отправляет сообщения в Telegram, если у пользователя уже указан `telegram_chat_id` и задан `TELEGRAM_BOT_TOKEN`.

## Документация API

- Swagger UI: `http://127.0.0.1:8000/api/schema/swagger-ui/`
- Redoc: `http://127.0.0.1:8000/api/schema/redoc/`
- OpenAPI schema: `http://127.0.0.1:8000/api/schema/`

## Эндпоинты

Аутентификация:

- `POST /api/v1/users/register/` - регистрация пользователя;
- `POST /api/v1/users/login/` - получение JWT access/refresh токенов;
- `POST /api/v1/users/token/refresh/` - обновление access токена.

Привычки:

- `GET /api/v1/habits/` - список привычек текущего пользователя;
- `POST /api/v1/habits/` - создание привычки;
- `GET /api/v1/habits/<id>/` - просмотр своей привычки;
- `PATCH /api/v1/habits/<id>/` - частичное обновление привычки;
- `PUT /api/v1/habits/<id>/` - полное обновление привычки;
- `DELETE /api/v1/habits/<id>/` - удаление привычки;
- `GET /api/v1/habits/public/` - список публичных привычек.

## Проверки качества

Flake8:

```bash
poetry run flake8 . --exclude=.git,__pycache__,.venv,migrations
```

Тесты:

```bash
poetry run python manage.py test
```

Покрытие тестами:

```bash
poetry run coverage run --source='.' manage.py test
poetry run coverage report
```

Актуальный отчет сохранен в файле `coverage-report.txt`.

## Чек-лист требований

- [x] Настроили CORS.
- [x] Настроили интеграцию с Телеграмом.
- [x] Реализовали пагинацию по 5 привычек на страницу.
- [x] Использовали переменные окружения.
- [x] Все необходимые модели описаны или переопределены.
- [x] Все необходимые эндпоинты реализовали.
- [x] Настроили все необходимые валидаторы.
- [x] Описанные права доступа заложены.
- [x] Настроили отложенную задачу через Celery.
- [x] Проект покрыт тестами более чем на 80%.
- [x] Код оформлен в соответствии с лучшими практиками.
- [x] Имеется список зависимостей.
- [x] Результат проверки Flake8 равен 100% при исключении миграций.
- [x] Решение выложено на GitHub.
