# Atomic Tracker

Backend for a habit tracker with JWT auth, public/private habits, Telegram account linking, and Celery reminders.

## Stack

- Django + Django REST Framework
- Simple JWT
- Celery + Redis
- Telegram Bot API
- drf-spectacular

## Quick Start

1. Copy `.env.example` to `.env` and fill values.
2. Install dependencies:

```bash
poetry install
```

3. Apply migrations:

```bash
poetry run python manage.py migrate
```

4. Run services:

```bash
poetry run python manage.py runserver
poetry run celery -A config worker -l info
poetry run celery -A config beat -l info
poetry run python manage.py run_telegram_bot
```

## API

- `POST /api/register`
- `POST /api/token`
- `POST /api/token/refresh`
- `GET/POST /api/habits`
- `GET/PUT/PATCH/DELETE /api/habits/{id}`
- `GET /api/habits/public`
- `GET /api/habits/public/{id}`
- `GET /api/telegram/link-token`
- `GET /api/schema/swagger-ui/`

## Tests

```bash
poetry run python manage.py test
poetry run flake8 .
```
