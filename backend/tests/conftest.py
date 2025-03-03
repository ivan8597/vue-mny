import pytest
import os
import sys
from app.database import Base
from app.models import *  # Импортируем все модели перед созданием таблиц
from app.test_config import test_engine, TestSessionLocal
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.api.auth import create_access_token
from sqlalchemy import text

# Устанавливаем переменную окружения
os.environ["TESTING"] = "1"
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Создаем схему БД для тестов"""
    # Проверяем, какие таблицы будут созданы
    tables = Base.metadata.tables
    print(f"Available tables: {', '.join(tables.keys())}")
    print(f"Registered models: {', '.join(str(m) for m in Base.registry.mappers)}")
    
    Base.metadata.create_all(bind=test_engine)
    
    # Проверяем, что таблицы действительно созданы
    with test_engine.connect() as conn:
        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        print(f"Created tables in DB: {', '.join(row[0] for row in result)}")
    
    yield
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture
def test_db():
    """Создаем новую сессию для каждого теста"""
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.rollback()  # Откатываем изменения после каждого теста
        db.close()

@pytest.fixture
def test_user():
    return {
        "username": "testuser",
        "name": "Test User",
        "password": "testpass",
        "email": "test@example.com"
    }

@pytest.fixture
def auth_headers(client, test_user):
    # Регистрируем пользователя
    register_response = client.post("/api/auth/register", json=test_user)
    print(f"Register response: {register_response.status_code} - {register_response.json()}")
    
    # Получаем токен
    login_data = {
        "username": test_user["email"],
        "password": test_user["password"]
    }
    token_response = client.post("/api/auth/token", data=login_data)
    print(f"Token response: {token_response.status_code} - {token_response.json()}")
    token = token_response.json()["access_token"]
    
    # Возвращаем заголовки с токеном
    return {"Authorization": f"Bearer {token}"}

# @pytest.fixture(scope="session")
# def test_engine():
#     """Создаем движок SQLite для тестов"""
#     return create_engine(
#         TEST_DATABASE_URL,
#         connect_args={"check_same_thread": False},
#         echo=False
#     )

# @pytest.fixture(scope="session")
# def TestingSessionLocal(test_engine):
#     """Фабрика сессий для тестовой БД"""
#     return sessionmaker(
#         autocommit=False,
#         autoflush=False,
#         bind=test_engine
#     )

# Создаем временную PostgreSQL БД для тестов
# postgresql_proc = factories.postgresql_proc(port=None, dbname="test_db")
# postgresql = factories.postgresql("postgresql_proc")

# @pytest.fixture
# def app():
#     # Создаем тестовое приложение
#     return create_app("testing") 

@pytest.fixture(autouse=True)
def cleanup_db(test_db):
    yield
    # Очищаем таблицы после каждого теста
    test_db.query(Transaction).delete()
    test_db.query(Category).delete()
    test_db.commit() 