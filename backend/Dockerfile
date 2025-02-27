# Используем официальный образ Python 3.11 slim версии
FROM python:3.11-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Установка зависимостей для psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл с зависимостями
COPY requirements.txt .

# Устанавливаем зависимости
# --no-cache-dir: не сохраняем кэш pip, чтобы уменьшить размер образа
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY . .

# Устанавливаем рабочую директорию для скриптов
WORKDIR /app

# Даем права на выполнение скриптам
RUN chmod +x *.sh

EXPOSE 8000 