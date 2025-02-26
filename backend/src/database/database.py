# Импорт необходимых библиотек для работы с базой данных
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Загрузка переменных окружения из .env файла
load_dotenv()

# Получение URL базы данных из переменных окружения
DATABASE_URL = os.getenv("DATABASE_URL") 

# Создание движка базы данных
engine = create_engine(DATABASE_URL)

# Создание фабрики сессий
# autocommit=False: автоматическая фиксация транзакций выключена
# autoflush=False: автоматическая синхронизация с БД выключена
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание базового класса для всех моделей
Base = declarative_base()

# Функция для получения сессии базы данных
def get_db():
    # Создание новой сессии
    db = SessionLocal()
    try:
        # Возвращаем сессию
        yield db
    finally:
        # Гарантированное закрытие сессии после использования
        db.close() 