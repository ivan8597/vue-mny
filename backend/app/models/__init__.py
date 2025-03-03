# Явно импортируем все модели, чтобы они зарегистрировались в Base.metadata
from .user import User
from .category import Category
from .transaction import Transaction
from .transaction_type import TransactionType
from .savings_goal import SavingsGoal

# Это позволит импортировать все модели одной строкой
__all__ = ['User', 'Category', 'Transaction', 'SavingsGoal']
