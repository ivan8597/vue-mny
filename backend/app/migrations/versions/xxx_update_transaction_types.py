"""update transaction types

Revision ID: xxx
Revises: previous_revision
Create Date: 2024-02-28
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    # Обновляем значения в таблице на верхний регистр
    op.execute("UPDATE transactions SET type = UPPER(type)")
    
    # Пересоздаем enum тип
    op.execute("""
        DO $$ 
        BEGIN
            DROP TYPE IF EXISTS transactiontype CASCADE;
            CREATE TYPE transactiontype AS ENUM ('INCOME', 'EXPENSE');
        END $$;
    """)
    
    # Создаем новую колонку с правильным типом
    op.execute("""
        ALTER TABLE transactions 
        ALTER COLUMN type TYPE transactiontype 
        USING type::transactiontype
    """)

def downgrade():
    pass 