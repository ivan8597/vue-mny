from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
import sys

# Определяем тестовое окружение на основе переменной окружения
TESTING = os.getenv("TESTING") == "1"

# При тестировании используем SQLite
if TESTING:
    DATABASE_URL = "sqlite:///:memory:"
    connect_args = {"check_same_thread": False}
    print(f"Using SQLite: {DATABASE_URL}")
else:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/finance_db")
    connect_args = {}
    print(f"Using PostgreSQL: {DATABASE_URL}")

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 