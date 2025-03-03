# Этот файл запускает тесты с правильными настройками окружения
import os
import sys
import pytest
import glob

# Установить переменные окружения ДО ЛЮБЫХ импортов
os.environ["TESTING"] = "1"
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

# Предварительно загружаем нашу тестовую конфигурацию
import app.test_config

# Выводим информацию для диагностики
print(f"TESTING={os.environ.get('TESTING')}")
print(f"DATABASE_URL={os.environ.get('DATABASE_URL')}")
print(f"Test files found: {glob.glob('tests/test_*.py')}")

# Запустить pytest с правильными аргументами
sys.exit(pytest.main(["-v", "tests/"])) 