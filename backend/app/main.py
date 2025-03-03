from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.initial_data import create_initial_categories
from app.database import SessionLocal, TESTING, engine, Base
from app.api.auth import router as auth_router
from app.api.transactions import router as transactions_router
from app.api.categories import router as categories_router
from app.api.savings_goals import router as savings_goals_router
import os

# Создаем экземпляр приложения, но не инициализируем БД сразу
app = FastAPI()

# Настройка CORS до подключения роутеров
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене заменить на конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600
)

def init_db():
    try:
        # Не инициализируем БД при тестировании
        if TESTING:
            print("Running in test mode with SQLite in memory")
            return

        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        print("Database connection successful")
        if not TESTING:
            create_initial_categories()
    except Exception as e:
        print(f"Database connection failed: {e}")
        if not TESTING:
            raise e

# Выносим инициализацию БД в отдельную функцию
def startup_db():
    if not os.getenv("TESTING") == "1":
        init_db()

# Подключаем роутеры
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(categories_router, prefix="/api/categories", tags=["categories"])
app.include_router(transactions_router, prefix="/api/transactions", tags=["transactions"])
app.include_router(savings_goals_router, prefix="/api/savings-goals", tags=["savings-goals"])

@app.get("/")
def root():
    return {"message": "Welcome to Finance API"}

# Регистрируем событие запуска для инициализации БД
@app.on_event("startup")
def startup_event():
    startup_db() 