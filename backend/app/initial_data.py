from sqlalchemy.orm import Session
from app.models.category import Category
from app.database import SessionLocal

def create_initial_categories():
    db = SessionLocal()
    try:
        # Проверяем, есть ли уже категории
        if db.query(Category).count() == 0:
            # Категории расходов
            expense_categories = [
                {"name": "Продукты", "type": "expense"},
                {"name": "Транспорт", "type": "expense"},
                {"name": "Развлечения", "type": "expense"},
                {"name": "Коммунальные платежи", "type": "expense"},
                {"name": "Здоровье", "type": "expense"}
            ]
            
            # Категории доходов
            income_categories = [
                {"name": "Зарплата", "type": "income"},
                {"name": "Фриланс", "type": "income"},
                {"name": "Инвестиции", "type": "income"}
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