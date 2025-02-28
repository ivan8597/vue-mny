from pydantic import BaseModel

class TransactionSummary(BaseModel):
    income: float
    expense: float
    balance: float 