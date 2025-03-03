def create_app(config=None):
    """Фабрика приложений для разных окружений"""
    from fastapi import FastAPI
    app = FastAPI()
    
    # Настраиваем БД на основе конфигурации
    if config == "testing":
        # Тестовая конфигурация с SQLite
        from .test_config import configure_app
    else:
        # Основная конфигурация с PostgreSQL
        from .config import configure_app
    
    # Настраиваем приложение
    configure_app(app)
    return app 