#!/bin/sh
set -e

if [ "$DB_ENGINE" = "postgres" ]; then
  python - <<'PY'
import os
import socket
import time

host = os.environ.get("DB_HOST", "postgres")
port = int(os.environ.get("DB_PORT", "5432"))

for _ in range(60):
    try:
        with socket.create_connection((host, port), timeout=2):
            break
    except OSError:
        time.sleep(1)
else:
    raise SystemExit(f"Postgres is unavailable on {host}:{port}")
PY
fi

if [ "$1" = "python" ] && [ "$2" = "manage.py" ] && [ "$3" = "runserver" ]; then
  python manage.py migrate --noinput
  python manage.py collectstatic --noinput
fi

exec "$@"
