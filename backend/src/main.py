from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware # cors
from .routes import transactions # транзакции

app = FastAPI(title="Finance API") # приложение

# Настройка CORS для работы с frontend
app.add_middleware( # добавление middleware
    CORSMiddleware, # cors
    allow_origins=["http://localhost:5173"], # разрешение для frontend
    allow_credentials=True, # разрешение учетных данных
    allow_methods=["*"], # разрешение всех методов
    allow_headers=["*"], # разрешение всех заголовков
)

app.include_router(transactions.router, prefix="/api/v1") # включение маршрутов

@app.get("/") # корневой маршрут
async def root(): # корневой маршрут
    return {"message": "Добро пожаловать в API учета финансов"} 