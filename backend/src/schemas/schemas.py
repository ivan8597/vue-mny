from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional # тип
from src.models.models import TransactionType # тип транзакции

class UserBase(BaseModel): # пользователь
    email: EmailStr # email
    name: str # имя

class UserCreate(UserBase): # создание пользователя
    password: str # пароль

class User(UserBase): # пользователь
    id: int # id
    
    class Config: # конфигурация
        from_attributes = True # извлекать атрибуты

class CategoryBase(BaseModel): # категория
    name: str # имя
    type: TransactionType # тип

class CategoryCreate(CategoryBase): # создание категории
    pass

class Category(CategoryBase): # категория
    id: int # id
    
    class Config: # конфигурация
        from_attributes = True # извлекать атрибуты

class TransactionBase(BaseModel): # транзакция
    amount: float # сумма
    type: TransactionType # тип
    description: Optional[str] = None # описание
    category_id: int # id категории

class TransactionCreate(TransactionBase): # создание транзакции
    pass  # ничего не делать

class Transaction(TransactionBase): # транзакция
    id: int # id
    date: datetime # дата
    user_id: int # id пользователя
    
    class Config: # конфигурация
        from_attributes = True # извлекать атрибуты