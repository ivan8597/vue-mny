from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Импортируем наши модели
import sys
import os
sys.path.append('/app')  # Добавляем корневую директорию для поиска модуля app
sys.path.append('/app/app')
sys.path.append('/app/src')  # Добавляем путь к новым моделям
from database import Base, DATABASE_URL
from models.user import User
from models.transaction import Transaction
from models.category import Category


# это объект конфигурации Alembic, который обеспечивает
# доступ к значениям используемого .ini файла
config = context.config

# Интерпретация конфигурационного файла для логирования Python.
# Эта строка настраивает логгеры.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Указываем метаданные наших моделей
target_metadata = Base.metadata

#

config.set_main_option("sqlalchemy.url", DATABASE_URL)

def run_migrations_offline() -> None:
    """Запуск миграций в 'оффлайн' режиме.

    Это настраивает контекст только с URL
    без Engine, хотя Engine также допустим
    здесь. Пропуская создание Engine,
    нам даже не нужен доступный DBAPI.

    Вызовы context.execute() здесь выводят заданную строку
    в скрипт.
    """
    url = config.get_main_option("sqlalchemy.url") # получаем URL из конфигурации
    context.configure(
        url=url,
        target_metadata=target_metadata, # указываем метаданные наших моделей
        literal_binds=True, # используем прямое сопоставление параметров
        dialect_opts={"paramstyle": "named"}, # используем именованные параметры
    )

    with context.begin_transaction(): # начинаем транзакцию
        context.run_migrations() # запускаем миграции


def run_migrations_online() -> None: # запуск миграций в 'онлайн' режиме
    """Запуск миграций в 'онлайн' режиме.

    В этом сценарии нам нужно создать Engine
    и связать соединение с контекстом.
    """
    configuration = config.get_section(config.config_ini_section) # получаем секцию конфигурации
    connectable = engine_from_config(
        configuration,  # конфигурация движка
        prefix="sqlalchemy.", # префикс для конфигурации
        poolclass=pool.NullPool, # используем пустой пул
    )

    with connectable.connect() as connection: # создаем соединение
        context.configure(  # настраиваем контекст
            connection=connection, # связываем соединение с контекстом
            target_metadata=target_metadata # указываем метаданные наших моделей
        )

        with context.begin_transaction(): # начинаем транзакцию
            context.run_migrations() # запускаем миграции


if context.is_offline_mode(): # если режим офлайн
    run_migrations_offline() # запускаем миграции в офлайн режиме
else:
    run_migrations_online() # запускаем миграции в онлайн режиме
