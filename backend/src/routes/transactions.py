from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database.database import get_db
from ..schemas import schemas
from ..models import models

router = APIRouter() # роутер

@router.post("/transactions/", response_model=schemas.Transaction) # создание транзакции
def create_transaction(
    transaction: schemas.TransactionCreate, # транзакция
    user_id: int, # id пользователя
    db: Session = Depends(get_db) # база данных
):
    db_transaction = models.Transaction(
        **transaction.model_dump(), # преобразуем транзакцию в словарь
        user_id=user_id # id пользователя
    )
    db.add(db_transaction) # добавляем транзакцию в базу данных
    db.commit() # сохраняем транзакцию
    db.refresh(db_transaction) # обновляем транзакцию
    return db_transaction

@router.get("/transactions/", response_model=List[schemas.Transaction]) # получение транзакций
def read_transactions( # получение транзакций
    skip: int = 0, # пропуск
    limit: int = 100, # лимит
    user_id: int = None, # id пользователя
    db: Session = Depends(get_db) # база данных
):
    transactions = db.query(models.Transaction) # запрос на транзакции
    if user_id: # если id пользователя
        transactions = transactions.filter(models.Transaction.user_id == user_id) # фильтрация транзакций по id пользователя
    return transactions.offset(skip).limit(limit).all() # возвращаем транзакции