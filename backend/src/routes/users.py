from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta
from ..database.database import get_db
from ..schemas import schemas
from ..models import models
from ..utils.auth import ( # импорт функций
    verify_password, # проверка пароля
    get_password_hash, # хеширование пароля
    create_access_token, # создание токена
    ACCESS_TOKEN_EXPIRE_MINUTES, # срок действия токена
    get_current_user # получение текущего пользователя
)

router = APIRouter()

# Регистрация пользователя
@router.post("/register", response_model=schemas.User) # регистрация пользователя
def register_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    """Регистрация нового пользователя"""
    # Проверяем, существует ли пользователь
    db_user = db.query(models.User).filter(models.User.email == user.email).first() # проверка на существование пользователя
    if db_user: # если пользователь существует
        raise HTTPException(   
            status_code=400, # статус код
            detail="Email уже зарегистрирован" # сообщение
        )
    
    # Создаем нового пользователя
    hashed_password = get_password_hash(user.password) # хеширование пароля
    db_user = models.User(
        email=user.email, # email
        name=user.name, # имя
        hashed_password=hashed_password # хеширование пароля
    )
    db.add(db_user) # добавление пользователя
    db.commit() # сохранение пользователя
    db.refresh(db_user) # обновление пользователя
    return db_user

# Авторизация пользователя
@router.post("/token") # авторизация пользователя
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), # форма запроса
    db: Session = Depends(get_db) # база данных
):
    """Аутентификация пользователя"""
    # Ищем пользователя
    user = db.query(models.User).filter(models.User.email == form_data.username).first() # поиск пользователя
    if not user or not verify_password(form_data.password, user.hashed_password): # если пользователь не найден или пароль не совпадает
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, # статус код
            detail="Неверный email или пароль", # сообщение
            headers={"WWW-Authenticate": "Bearer"}, # заголовок
        )
    
    # Создаем токен доступа
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) # срок действия токена
    access_token = create_access_token(
        data={"sub": user.email}, # данные токена
        expires_delta=access_token_expires # срок действия токена
    )
    return {"access_token": access_token, "token_type": "bearer"} # возвращаем токен

# Получение данных текущего пользователя
@router.get("/users/me", response_model=schemas.User) # получение данных текущего пользователя
def read_users_me(current_user: models.User = Depends(get_current_user)): # получение данных текущего пользователя
    """Получение данных текущего пользователя"""
    return current_user 