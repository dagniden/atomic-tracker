# Atomic Tracker

Backend для учебного SPA-приложения "Трекер привычек" на Django REST Framework.

Проект предоставляет API для регистрации, авторизации, управления привычками, просмотра публичных привычек и отправки напоминаний через Celery и Telegram.

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
- контейнеризация через Docker Compose;
- CI/CD через GitHub Actions.

## Стек локального запуска

Локально проект поднимается одной командой через Docker Compose и включает:

- `web` - Django;
- `postgres` - база данных PostgreSQL;
- `redis` - брокер и backend для Celery;
- `celery_worker` - Celery worker;
- `celery_beat` - Celery beat;
- `nginx` - reverse proxy для Django и раздачи `static`/`media`.

## Требования

- Docker;
- Docker Compose;
- `act` для локальной проверки GitHub Actions.

## Быстрый старт

1. Скопируйте `.env.example` в `.env`.
2. При необходимости измените значения переменных окружения.
3. Запустите проект одной командой:

```bash
docker compose up -d
```

После первого запуска будут автоматически выполнены миграции и `collectstatic`.

## Локальные адреса

- приложение: `http://localhost:8080`
- OpenAPI schema: `http://localhost:8080/api/schema/`
- Swagger UI: `http://localhost:8080/api/schema/swagger-ui/`
- Redoc: `http://localhost:8080/api/schema/redoc/`

## Остановка проекта

```bash
docker compose down
```

Если нужно удалить и volumes:

```bash
docker compose down -v
```

## Переменные окружения

Основные переменные из `.env`:

- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `TIME_ZONE`
- `DB_ENGINE`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`
- `CORS_ALLOWED_ORIGINS`
- `CSRF_TRUSTED_ORIGINS`
- `CELERY_BROKER_URL`
- `CELERY_RESULT_BACKEND`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_BOT_USERNAME`

Для локального запуска через Docker Compose используются значения PostgreSQL и Redis из `docker-compose.yml`.

## Ручной запуск без Docker

Если нужен локальный запуск без контейнеров:

```bash
poetry install
poetry run python manage.py migrate
poetry run python manage.py runserver
```

Дополнительно для напоминаний отдельно запускаются:

```bash
poetry run celery -A config worker --loglevel=info
poetry run celery -A config beat --loglevel=info
```

## Проверки качества

Flake8:

```bash
poetry run flake8 . --exclude=.git,__pycache__,.venv,migrations
```

Тесты:

```bash
poetry run python manage.py test
```

Проверка Django-конфига:

```bash
poetry run python manage.py check
```

Сборка Docker-образов:

```bash
docker compose build
```

## GitHub Actions

В репозитории настроен workflow `.github/workflows/ci.yml`.

Он выполняет:

- тесты;
- линтинг через `flake8`;
- проверку миграций;
- сборку Docker-образов;
- деплой на сервер после успешных проверок для `push` в `main` или `master`.

Для deploy используются GitHub Secrets:

- `SSH_USER`
- `SERVER_IP`
- `DEPLOY_DIR`
- `SSH_KEY`

## Локальная проверка workflow через act

Для локального запуска workflow используются файлы:

- `.actrc`
- `.secrets`

Основная команда проверки:

```bash
act pull_request
```

Дополнительная проверка deploy-ветки без реального деплоя:

```bash
act push -j deploy
```

Важно: для `act` должны быть свободны локальные порты `5432` и `6379`, так как они используются сервисами PostgreSQL и Redis внутри workflow.

## Деплой

Workflow деплоя уже подготовлен и использует схему:

1. подключение по SSH;
2. копирование проекта на сервер через `rsync`;
3. запуск на сервере команды:

```bash
docker compose up -d --build --remove-orphans
```

Полноценная серверная часть зависит от конкретного окружения и может быть завершена отдельно.

## Эндпоинты API

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
