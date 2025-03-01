from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from .transaction_type import TransactionType

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(Enum(TransactionType))
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="categories")
    transactions = relationship("Transaction", back_populates="category") 