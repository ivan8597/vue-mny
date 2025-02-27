from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware # cors
from .routes import transactions, categories, users # импорт роутов

app = FastAPI(title="Finance API") # приложение

# Настройка CORS для работы с frontend
app.add_middleware( # добавление middleware
    CORSMiddleware, # cors
    allow_origins=["http://localhost:5173"], # разрешение для frontend
    allow_credentials=True, # разрешение учетных данных
    allow_methods=["*"], # разрешение всех методов
    allow_headers=["*"], # разрешение всех заголовков
)

app.include_router(transactions.router, prefix="/api") # включение маршрутов
app.include_router(categories.router, prefix="/api") # включение маршрутов категорий
app.include_router(users.router, prefix="/api/auth") # включение маршрутов пользователей

@app.get("/") # корневой маршрут
async def root(): # корневой маршрут
    return {"message": "Добро пожаловать в API учета финансов"} 