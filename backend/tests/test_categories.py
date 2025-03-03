# Сначала импортируем фикстуры и тестовую конфигурацию
import os
os.environ["TESTING"] = "1"

import pytest
from fastapi.testclient import TestClient
from app.test_config import TestSessionLocal

from app.database import get_db
from app.main import app

@pytest.fixture
def client(test_db):
    """Создаем тестовый клиент с переопределенной БД"""
    app.dependency_overrides[get_db] = lambda: test_db
    yield TestClient(app)
    app.dependency_overrides.clear()

def test_create_category(client, auth_headers):
    category_data = {
        "name": "Продукты",
        "type": "expense"
    }
    response = client.post("/api/categories/", json=category_data, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == category_data["name"]
    assert data["type"] == category_data["type"]
    assert "id" in data

def test_get_categories(client, auth_headers):
    # Создаем несколько категорий
    categories = [
        {"name": "Продукты", "type": "expense"},
        {"name": "Зарплата", "type": "income"},
        {"name": "Транспорт", "type": "expense"}
    ]
    
    for category in categories:
        client.post("/api/categories/", json=category, headers=auth_headers)
    
    response = client.get("/api/categories/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3

def test_get_categories_by_type(client, auth_headers):
    # Создаем категории разных типов
    categories = [
        {"name": "Продукты", "type": "expense"},
        {"name": "Зарплата", "type": "income"},
        {"name": "Транспорт", "type": "expense"}
    ]
    
    for category in categories:
        client.post("/api/categories/", json=category, headers=auth_headers)
    
    # Проверяем фильтрацию по типу expense
    response = client.get("/api/categories/", params={"type": "expense"}, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(cat["type"] == "expense" for cat in data)

    # Проверяем фильтрацию по типу income
    response = client.get("/api/categories/", params={"type": "income"}, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["type"] == "income"

def test_create_duplicate_category(client, auth_headers):
    category_data = {
        "name": "Продукты",
        "type": "expense"
    }
    # Создаем первую категорию
    response = client.post("/api/categories/", json=category_data, headers=auth_headers)
    assert response.status_code == 201

    # Пытаемся создать дубликат
    response = client.post("/api/categories/", json=category_data, headers=auth_headers)
    assert response.status_code == 400 