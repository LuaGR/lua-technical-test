#!/bin/sh
set -e

echo "Waiting for the database to be ready..."
until pg_isready -h db -p 5432 -U postgres; do
  sleep 1
done

echo "Database is ready, running Alembic migrations..."
cd /app
alembic upgrade head

echo "Starting FastAPI backend with Uvicorn..."
cd src
uvicorn main:app --host 0.0.0.0 --port 8000
