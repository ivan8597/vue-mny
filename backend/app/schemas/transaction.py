from pydantic import BaseModel
from datetime import date
from app.models.transaction import TransactionType

class TransactionBase(BaseModel):
    title: str
    amount: float
    type: TransactionType
    category_id: int
    date: date
    description: str | None = None

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    id: int

    class Config:
        from_attributes = True 