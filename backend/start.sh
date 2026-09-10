#!/bin/bash
set -e

echo "Waiting for MySQL to be ready..."
# 等待MySQL准备就绪
sleep 5

echo "Running database migrations..."
python -m alembic upgrade head

echo "Starting FastAPI application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
