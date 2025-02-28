from sqlalchemy.orm import Session
from app.models.category import Category
from app.models.category import TransactionType
from app.database import SessionLocal

def create_initial_categories():
    db = SessionLocal()
    try:
        # Проверяем, есть ли уже категории
        if db.query(Category).count() == 0:
            # Категории расходов
            expense_categories = [
                {"name": "Продукты", "type": TransactionType.expense},
                {"name": "Транспорт", "type": TransactionType.expense},
                {"name": "Развлечения", "type": TransactionType.expense},
                {"name": "Коммунальные платежи", "type": TransactionType.expense},
                {"name": "Здоровье", "type": TransactionType.expense}
            ]
            
            # Категории доходов
            income_categories = [
                {"name": "Зарплата", "type": TransactionType.income},
                {"name": "Фриланс", "type": TransactionType.income},
                {"name": "Инвестиции", "type": TransactionType.income}
            ]
            
            # Добавляем все категории
            for category_data in expense_categories + income_categories:
                category = Category(**category_data)
                db.add(category)
            
            db.commit()
            print("Initial categories created successfully!")
    finally:
        db.close()

if __name__ == "__main__":
    create_initial_categories() 