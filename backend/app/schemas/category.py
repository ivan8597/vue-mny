from pydantic import BaseModel
from typing import Literal

class CategoryBase(BaseModel):
    name: str
    type: Literal['income', 'expense']

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True 