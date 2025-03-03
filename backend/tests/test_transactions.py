# Сначала импортируем фикстуры и тестовую конфигурацию
import os
os.environ["TESTING"] = "1"

import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta

from app.test_config import TestSessionLocal
from app.main import app
from app.database import get_db, Base
# from app.config import settings  # Временно комментируем

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
def client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

def test_create_transaction(client, auth_headers):
    # Сначала создаем категорию
    category_data = {
        "name": "Продукты",
        "type": "expense"
    }
    category_response = client.post("/api/categories/", json=category_data, headers=auth_headers)
    assert category_response.status_code == 201
    category_id = category_response.json()["id"]

    # Создаем транзакцию
    transaction_data = {
        "title": "Покупка продуктов",
        "amount": 1000,
        "type": "expense",
        "category_id": category_id,
        "date": datetime.now().strftime("%Y-%m-%d")
    }
    response = client.post("/api/transactions/", json=transaction_data, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == transaction_data["title"]
    assert data["amount"] == transaction_data["amount"]
    assert data["category_id"] == category_id

def test_get_transactions(client, auth_headers):
    # Создаем тестовые данные
    category_data = {"name": "Зарплата", "type": "income"}
    category_response = client.post("/api/categories/", json=category_data, headers=auth_headers)
    category_id = category_response.json()["id"]

    transactions = [
        {
            "title": f"Транзакция {i}",
            "amount": 1000 * i,
            "type": "income",
            "category_id": category_id,
            "date": (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        }
        for i in range(1, 4)
    ]

    for tx in transactions:
        client.post("/api/transactions/", json=tx, headers=auth_headers)

    # Получаем список транзакций
    response = client.get("/api/transactions/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3

def test_get_transaction_summary(client, auth_headers):
    # Создаем категории
    categories = [
        {"name": "Зарплата", "type": "income"},
        {"name": "Продукты", "type": "expense"}
    ]
    category_ids = []
    for cat in categories:
        response = client.post("/api/categories/", json=cat, headers=auth_headers)
        category_ids.append(response.json()["id"])

    # Создаем транзакции
    transactions = [
        {
            "title": "Зарплата",
            "amount": 50000,
            "type": "income",
            "category_id": category_ids[0],
            "date": datetime.now().strftime("%Y-%m-%d")
        },
        {
            "title": "Продукты",
            "amount": 10000,
            "type": "expense",
            "category_id": category_ids[1],
            "date": datetime.now().strftime("%Y-%m-%d")
        }
    ]

    for tx in transactions:
        client.post("/api/transactions/", json=tx, headers=auth_headers)

    # Получаем сводку по транзакциям
    response = client.get("/api/transactions/summary", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["income"] == 50000
    assert data["expense"] == 10000
    assert data["balance"] == 40000

def test_filter_transactions_by_date(client, auth_headers):
    # Создаем категорию
    category_data = {"name": "Тест", "type": "expense"}
    category_response = client.post("/api/categories/", json=category_data, headers=auth_headers)
    category_id = category_response.json()["id"]

    # Создаем транзакции за разные даты
    dates = [
        datetime.now() - timedelta(days=10),
        datetime.now() - timedelta(days=5),
        datetime.now()
    ]

    for i, date in enumerate(dates):
        transaction = {
            "title": f"Транзакция {i}",
            "amount": 1000,
            "type": "expense",
            "category_id": category_id,
            "date": date.strftime("%Y-%m-%d")
        }
        client.post("/api/transactions/", json=transaction, headers=auth_headers)

    # Фильтруем по дате
    start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    end_date = datetime.now().strftime("%Y-%m-%d")
    
    response = client.get(f"/api/transactions/?start_date={start_date}&end_date={end_date}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2  # Должны получить только 2 транзакции в указанном диапазоне 