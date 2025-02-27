#!/bin/bash

# Ждем, пока PostgreSQL будет доступен
until PGPASSWORD=postgres psql -h db -U postgres -d finance_db -c '\q'; do
  echo "Postgres недоступен - ожидание"
  sleep 1
done

echo "Postgres готов!"

# Применяем миграции
alembic upgrade head

# Создаем начальные данные
python -m app.initial_data

# Запускаем приложение
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload 