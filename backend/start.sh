#!/bin/sh

# Ждем доступности базы данных
./wait-for-db.sh postgres

# Применяем миграции
alembic upgrade head

# Запускаем сервер
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload 