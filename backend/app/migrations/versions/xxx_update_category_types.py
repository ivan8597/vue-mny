"""update category types

Revision ID: xxx
Revises: previous_revision
Create Date: 2024-02-28

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import String
from sqlalchemy.sql import table, column

# revision identifiers, used by Alembic.
revision = 'xxx'
down_revision = 'previous_revision'
branch_labels = None
depends_on = None

def upgrade():
    # Создаем временную таблицу для хранения данных
    categories_table = table('categories',
        column('id', sa.Integer),
        column('name', String),
        column('type', String),
    )
    
    # Обновляем все значения type в нижний регистр
    op.execute(
        categories_table.update().values(
            type=sa.func.lower(categories_table.c.type)
        )
    )

def downgrade():
    pass 