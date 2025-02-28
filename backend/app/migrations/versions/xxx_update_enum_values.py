"""update enum values

Revision ID: xxx
Revises: previous_revision
Create Date: 2024-02-28
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    # Сначала обновляем значения в таблице на нижний регистр
    op.execute("UPDATE categories SET type = LOWER(type)")
    
    # Пересоздаем enum тип
    op.execute("""
        DO $$ 
        BEGIN
            DROP TYPE IF EXISTS transactiontype CASCADE;
            CREATE TYPE transactiontype AS ENUM ('income', 'expense');
        END $$;
    """)
    
    # Создаем новую колонку с правильным типом
    op.execute("""
        ALTER TABLE categories 
        ALTER COLUMN type TYPE transactiontype 
        USING type::transactiontype
    """)

def downgrade():
    pass 