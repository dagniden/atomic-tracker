FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=2.2.1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl libpq-dev \
    && pip install --no-cache-dir "poetry==$POETRY_VERSION" \
    && apt-get purge -y --auto-remove curl \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./

RUN poetry install --only main --no-root

COPY . .

RUN chmod +x /app/docker/app/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/docker/app/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
