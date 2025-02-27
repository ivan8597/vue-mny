from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TransactionBase(BaseModel):
    title: str
    amount: float
    type: str
    category_id: int
    description: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    id: int
    date: datetime
    user_id: int

    class Config:
        from_attributes = True 