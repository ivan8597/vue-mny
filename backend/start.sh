#!/bin/sh

# Ждем готовности базы данных
./wait-for-db.sh db

# Применяем миграции
alembic upgrade head

# Запускаем сервер
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload 