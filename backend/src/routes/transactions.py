from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime, date
from ..database.database import get_db
from ..schemas import schemas
from ..models import models
from ..utils.auth import get_current_user

router = APIRouter() 
# Создание транзакции
@router.post("/transactions/", response_model=schemas.Transaction) 
def create_transaction(
    transaction: schemas.TransactionCreate, # данные транзакции
    current_user: models.User = Depends(get_current_user), # текущий пользователь
    db: Session = Depends(get_db) # база данных
):
    """Создание новой транзакции"""
    
    # Проверяем существование категории
    db_category = db.query(models.Category).filter( # запрос на получение категории
        models.Category.id == transaction.category_id  # фильтр по ID категории
    ).first() # получаем первую категорию
    if not db_category: # если категория не найдена
        raise HTTPException( # вызываем исключение
            status_code=404, # статус код 404
            detail="Категория не найдена" # сообщение
        )
    
    # Проверяем соответствие типа транзакции и категории
    if transaction.type != db_category.type: # если тип транзакции не соответствует типу категории
        raise HTTPException( 
            status_code=400, 
            detail="Тип транзакции не соответствует типу категории" 
        )
    
    # Создаем транзакцию
    db_transaction = models.Transaction(
        **transaction.model_dump(), # распаковываем все поля из схемы
        user_id=current_user.id # добавляем ID пользователя
    )
    
    db.add(db_transaction) # добавляем в базу
    db.commit() # сохраняем изменения
    db.refresh(db_transaction) # обновляем объект из базы
    
    return db_transaction
# Получение транзакций
@router.get("/transactions/", response_model=List[schemas.Transaction]) 
def get_transactions(
    current_user: models.User = Depends(get_current_user), # текущий пользователь
    db: Session = Depends(get_db), # база данных
    skip: int = 0, # пропуск пагинации
    limit: int = 100, # лимит пагинации
    category_id: Optional[int] = None, # ID категории
    transaction_type: Optional[models.TransactionType] = None, # тип транзакции
    start_date: Optional[date] = None, # дата начала
    end_date: Optional[date] = None # дата конца
):
    """Получение списка транзакций с фильтрацией"""
    query = db.query(models.Transaction).filter(models.Transaction.user_id == current_user.id) # запрос на получение транзакций
    
    if category_id: # если ID категории
        query = query.filter(models.Transaction.category_id == category_id) # фильтр по ID категории
    if transaction_type: # если тип транзакции
        query = query.filter(models.Transaction.type == transaction_type) # фильтр по типу транзакции
    if start_date: # если дата начала
        query = query.filter(models.Transaction.date >= start_date) # фильтр по дате начала
    if end_date: # если дата конца
        query = query.filter(models.Transaction.date <= end_date) # фильтр по дате конца
    
    return query.order_by(models.Transaction.date.desc()).offset(skip).limit(limit).all() # возвращаем транзакции

# Получение сводки по доходам/расходам
@router.get("/transactions/summary") 
def get_transactions_summary(
    current_user: models.User = Depends(get_current_user), # текущий пользователь
    db: Session = Depends(get_db), # база данных
    start_date: Optional[date] = None, # дата начала
    end_date: Optional[date] = None # дата конца
):
    """Получение сводки по доходам/расходам"""
    query = db.query( # запрос на получение сводки по доходам/расходам
        models.Transaction.type, # тип транзакции
        func.sum(models.Transaction.amount).label("total") # сумма транзакций
    ).filter(models.Transaction.user_id == current_user.id) # фильтр по ID пользователя
    
    if start_date: # если дата начала
        query = query.filter(models.Transaction.date >= start_date) # фильтр по дате начала
    if end_date: # если дата конца
        query = query.filter(models.Transaction.date <= end_date) # фильтр по дате конца
    
    summary = query.group_by(models.Transaction.type).all() # группируем по типу транзакции
    
    result = { # результат
        "income": 0, # доходы
        "expense": 0, # расходы
        "balance": 0 # баланс
    }
    
    for type_, total in summary: # для каждого типа транзакции и суммы
        if type_ == models.TransactionType.INCOME: # если тип транзакции - доход
            result["income"] = float(total) # добавляем сумму дохода
        else: 
            result["expense"] = float(total) # добавляем сумму расхода
    
    result["balance"] = result["income"] - result["expense"] # считаем баланс
    return result

# Получение сводки по категориям
@router.get("/transactions/by_category") 
def get_transactions_by_category(
    current_user: models.User = Depends(get_current_user), # текущий пользователь
    db: Session = Depends(get_db), # база данных
    transaction_type: Optional[models.TransactionType] = None, # тип транзакции
    start_date: Optional[date] = None, # дата начала
    end_date: Optional[date] = None # дата конца
):
    """Получение сводки по категориям"""
    query = db.query( # запрос на получение сводки по категориям
        models.Category.name, # название категории
        models.Transaction.type, # тип транзакции
        func.sum(models.Transaction.amount).label("total") # сумма транзакций
    ).join(models.Category).filter(models.Transaction.user_id == current_user.id) # фильтр по ID пользователя
    
    if transaction_type: # если тип транзакции
        query = query.filter(models.Transaction.type == transaction_type) # фильтр по типу транзакции
    if start_date: # если дата начала
        query = query.filter(models.Transaction.date >= start_date) # фильтр по дате начала
    if end_date: # если дата конца
        query = query.filter(models.Transaction.date <= end_date) # фильтр по дате конца
    
    return query.group_by(models.Category.name, models.Transaction.type).all() # возвращаем сводку по категориям