from sqlalchemy.orm import Session
from app.models.category import Category, TransactionType
from app.database import SessionLocal

def create_initial_categories():
    db = SessionLocal()
    try:
        # Проверяем, есть ли уже категории
        if db.query(Category).count() == 0:
            # Категории расходов
            expense_categories = [
                {"name": "Продукты", "type": TransactionType.EXPENSE},
                {"name": "Транспорт", "type": TransactionType.EXPENSE},
                {"name": "Развлечения", "type": TransactionType.EXPENSE},
                {"name": "Коммунальные платежи", "type": TransactionType.EXPENSE},
                {"name": "Здоровье", "type": TransactionType.EXPENSE}
            ]
            
            # Категории доходов
            income_categories = [
                {"name": "Зарплата", "type": TransactionType.INCOME},
                {"name": "Фриланс", "type": TransactionType.INCOME},
                {"name": "Инвестиции", "type": TransactionType.INCOME}
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