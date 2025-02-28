"""update enum values to lowercase

Revision ID: xxx
Revises: b520e94c6136
Create Date: 2024-02-28
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    # Обновляем значения в таблице categories
    op.execute("UPDATE categories SET type = LOWER(type)")
    
    # Обновляем значения в таблице transactions
    op.execute("UPDATE transactions SET type = LOWER(type)")
    
    # Пересоздаем enum тип
    op.execute("""
        DO $$ 
        BEGIN
            DROP TYPE IF EXISTS transactiontype CASCADE;
            CREATE TYPE transactiontype AS ENUM ('income', 'expense');
        END $$;
    """)
    
    # Обновляем колонки с новым типом
    op.execute("""
        ALTER TABLE categories 
        ALTER COLUMN type TYPE transactiontype 
        USING type::transactiontype;
        
        ALTER TABLE transactions 
        ALTER COLUMN type TYPE transactiontype 
        USING type::transactiontype;
    """)

def downgrade():
    pass 