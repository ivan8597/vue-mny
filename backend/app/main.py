from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.initial_data import create_initial_categories
from app.api.auth import router as auth_router
from app.api.categories import router as categories_router
from app.api.transactions import router as transactions_router

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

# Создание начальных категорий при запуске
create_initial_categories()

# Подключаем роутеры
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(categories_router, prefix="/api/categories", tags=["categories"])
app.include_router(transactions_router, prefix="/api/transactions", tags=["transactions"])

@app.get("/")
def root():
    return {"message": "Welcome to Finance API"} 