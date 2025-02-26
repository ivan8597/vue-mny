from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional 
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..models.models import User

# Настройки JWT
SECRET_KEY = "ваш_секретный_ключ"  # секретный ключ
ALGORITHM = "HS256" 
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # срок действия токена

# Настройка хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # хеширование паролей

# Схема OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token") # схема OAuth2

def verify_password(plain_password: str, hashed_password: str) -> bool: 
    """Проверка пароля"""
    return pwd_context.verify(plain_password, hashed_password) # проверка пароля

def get_password_hash(password: str) -> str: # хеширование пароля
    """Хеширование пароля"""
    return pwd_context.hash(password) # хеширование пароля

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Создание JWT токена"""
    to_encode = data.copy() # копирование данных
    if expires_delta: # если срок действия токена
        expire = datetime.utcnow() + expires_delta # срок действия токена
    else:
        expire = datetime.utcnow() + timedelta(minutes=15) # срок действия токена
    to_encode.update({"exp": expire}) # обновление данных
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # кодирование JWT
    return encoded_jwt  

async def get_current_user( # получение текущего пользователя
    token: str = Depends(oauth2_scheme), # токен
    db: Session = Depends(get_db) # база данных
) -> User:
    """Получение текущего пользователя"""
    credentials_exception = HTTPException( 
        status_code=status.HTTP_401_UNAUTHORIZED, # статус код
        detail="Неверные учетные данные", # сообщение
        headers={"WWW-Authenticate": "Bearer"}, # заголовок
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # декодирование JWT
        email: str = payload.get("sub") # email
        if email is None: # если email не найден
            raise credentials_exception # вызов исключения
    except JWTError: # исключение
        raise credentials_exception # вызов исключения
    
    user = db.query(User).filter(User.email == email).first() # поиск пользователя
    if user is None: # если пользователь не найден
        raise credentials_exception # вызов исключения
    return user 