from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import func
from fastapi.responses import JSONResponse
from datetime import datetime

from app.database import get_db
from app.models.transaction import Transaction
from app.models.user import User
from app.models.transaction import TransactionType
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/", response_model=List[TransactionResponse])
def read_transactions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    start_date: str | None = Query(None),
    end_date: str | None = Query(None)
):
    print(f"Getting transactions for user {current_user.id}")
    query = db.query(Transaction).filter(Transaction.user_id == current_user.id)

    if start_date:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        query = query.filter(Transaction.date >= start)

    if end_date:
        end = datetime.strptime(end_date, "%Y-%m-%d")
        query = query.filter(Transaction.date <= end)

    transactions = query.all()
    print(f"Found {len(transactions)} transactions")
    return transactions

@router.get("/summary")
def get_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(
        Transaction.type,
        func.sum(Transaction.amount).label('total')
    ).filter(
        Transaction.user_id == current_user.id
    ).group_by(Transaction.type)
    
    result = {
        "income": 0,
        "expense": 0,
        "balance": 0
    }

    for type_, amount in query.all():
        if type_ == TransactionType.income:
            result["income"] = float(amount)
        elif type_ == TransactionType.expense:
            result["expense"] = float(amount)

    result["balance"] = result["income"] - result["expense"]
    return result

@router.post("/", response_model=TransactionResponse, status_code=201)
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_transaction = Transaction(**transaction.dict(), user_id=current_user.id)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_transactions_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(
        Transaction.type,
        func.sum(Transaction.amount)
    ).filter(
        Transaction.user_id == current_user.id
    ).group_by(Transaction.type)
    
    result = {
        "income": 0,
        "expense": 0
    }

    for type, amount in query.all():
        if type == TransactionType.income:
            result["income"] = amount
        elif type == TransactionType.expense:
            result["expense"] = amount

    return result 