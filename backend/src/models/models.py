from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum # колонки
from sqlalchemy.orm import relationship # отношения
from datetime import datetime # дата и время
import enum # перечисление
from ..database.database import Base # база данных

class TransactionType(enum.Enum): # тип транзакции
    income = "income" # доход
    expense = "expense" # расход

class User(Base): # пользователь
    __tablename__ = "users" # имя таблицы

    id = Column(Integer, primary_key=True, index=True) # id
    email = Column(String, unique=True, index=True) # email
    hashed_password = Column(String) # хэшированный пароль
    name = Column(String) # имя
    transactions = relationship("Transaction", back_populates="user") # транзакции

class Category(Base): # категория
    __tablename__ = "categories" # имя таблицы

    id = Column(Integer, primary_key=True, index=True) # id
    name = Column(String, unique=True) # имя
    type = Column(Enum(TransactionType)) # тип
    transactions = relationship("Transaction", back_populates="category") # транзакции

class Transaction(Base): # транзакция
    __tablename__ = "transactions" # имя таблицы

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)  # название транзакции
    amount = Column(Float, nullable=False)  # сумма
    type = Column(Enum(TransactionType), nullable=False)  # тип
    description = Column(String)  # описание
    date = Column(DateTime, default=datetime.utcnow)  # дата
    category_id = Column(Integer, ForeignKey("categories.id"))  # id категории
    user_id = Column(Integer, ForeignKey("users.id"))  # id пользователя

    # Связи с другими таблицами
    category = relationship("Category", back_populates="transactions")
    user = relationship("User", back_populates="transactions")