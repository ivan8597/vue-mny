from pydantic import BaseModel
from app.models.category import TransactionType

class CategoryBase(BaseModel):
    name: str
    type: TransactionType

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True 