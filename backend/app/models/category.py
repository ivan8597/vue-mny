from sqlalchemy import Column, Integer, String, Enum
from app.database import Base
from .transaction_type import TransactionType

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(Enum(TransactionType)) 