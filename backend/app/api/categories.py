from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryResponse
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/", response_model=List[CategoryResponse])
def read_categories(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Получить все категории"""
    categories = db.query(Category).all()
    return categories

@router.post("/", response_model=CategoryResponse)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Создать новую категорию"""
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category 