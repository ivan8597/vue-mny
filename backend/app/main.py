from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.initial_data import create_initial_categories
from app.api.auth import router as auth_router
from app.api.categories import router as categories_router
from app.api.transactions import router as transactions_router
from app.database import SessionLocal

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Проверка подключения к базе данных
def init_db():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        print("Database connection successful")
        create_initial_categories()
    except Exception as e:
        print(f"Database connection failed: {e}")
        raise e

init_db()

# Подключаем роутеры
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(categories_router, prefix="/api/categories", tags=["categories"])
app.include_router(transactions_router, prefix="/api/transactions", tags=["transactions"])

@app.get("/")
def root():
    return {"message": "Welcome to Finance API"} 