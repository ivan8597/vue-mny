from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SavingsGoalBase(BaseModel):
    name: str
    target_amount: float
    current_amount: float = 0.0
    deadline: Optional[datetime] = None

class SavingsGoalCreate(SavingsGoalBase):
    pass

class SavingsGoalUpdate(BaseModel):
    name: Optional[str] = None
    target_amount: Optional[float] = None
    current_amount: Optional[float] = None
    deadline: Optional[datetime] = None

class SavingsGoalResponse(SavingsGoalBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True 