from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/", response_model=List[TransactionResponse])
def read_transactions(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    print(f"Getting transactions for user {current_user.id}")
    transactions = db.query(Transaction).filter(Transaction.user_id == current_user.id).all()
    print(f"Found {len(transactions)} transactions")
    return transactions

@router.get("/summary")
def get_summary(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # TODO: Реализовать получение сводки
    return {
        "income": 0,
        "expense": 0,
        "balance": 0
    } 