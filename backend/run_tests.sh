#!/bin/bash
export TESTING=1
export DATABASE_URL=sqlite:///:memory:
export PYTHONPATH=/app

# Запуск самого простого теста для проверки
python -m pytest tests/test_simple.py -v

# Если успешно, запускаем остальные тесты
if [ $? -eq 0 ]; then
    python -m pytest tests/ -v
fi 