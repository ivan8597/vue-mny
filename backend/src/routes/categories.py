from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database.database import get_db
from ..schemas import schemas
from ..models import models
from ..utils.auth import get_current_user

router = APIRouter() # роутер

@router.post("/categories/", response_model=schemas.Category) # создание категории
def create_category(
    category: schemas.CategoryCreate, # категория
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db) # база данных
):
    """Создание новой категории"""
    db_category = models.Category(**category.model_dump()) # создание категории
    db.add(db_category) # добавление категории
    db.commit() # сохранение категории
    db.refresh(db_category) # обновление категории
    return db_category

@router.get("/categories/", response_model=List[schemas.Category]) # получение категорий
def read_categories(
    skip: int = 0, # пропуск
    limit: int = 100, # лимит
    db: Session = Depends(get_db) # база данных
):
    return db.query(models.Category).offset(skip).limit(limit).all() 