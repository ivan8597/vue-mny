from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from fastapi.responses import JSONResponse

from app.database import get_db
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryResponse
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/", response_model=List[CategoryResponse])
def read_categories(
    db: Session = Depends(get_db),
    type: str | None = Query(None),
    _current_user = Depends(get_current_user)
):
    """Получить все категории"""
    try:
        print("Getting categories...")
        query = db.query(Category)
        if type:
            query = query.filter(Category.type == type)
        categories = query.all()
        print(f"Found {len(categories)} categories")
        if not categories:
            print("No categories found, creating initial categories...")
            from app.initial_data import create_initial_categories
            create_initial_categories()
            categories = db.query(Category).all()
            print(f"Created {len(categories)} initial categories")
        return categories
    except Exception as e:
        print(f"Error getting categories: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.post("/", response_model=CategoryResponse)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Создать новую категорию"""
    # Проверяем существование категории с таким же именем
    existing = db.query(Category).filter(Category.name == category.name).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Category with this name already exists"
        )
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return JSONResponse(
        status_code=201,
        content={"id": db_category.id, "name": db_category.name, "type": db_category.type}
    )

@router.get("/debug", response_model=List[dict])
def debug_categories(
    db: Session = Depends(get_db),
    _current_user = Depends(get_current_user)
):
    """Отладочный эндпоинт для проверки категорий"""
    categories = db.query(Category).all()
    return [{"id": c.id, "name": c.name, "type": c.type} for c in categories] 