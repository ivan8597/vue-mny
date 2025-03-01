"""add user_id to categories

Revision ID: 824e4867e179
Revises: 3f5f0279cb83
Create Date: 2024-02-28 21:20:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '824e4867e179'
down_revision = '3f5f0279cb83'
branch_labels = None
depends_on = None

def upgrade():
    # Добавляем колонку user_id
    op.add_column('categories', sa.Column('user_id', sa.Integer(), nullable=True))
    
    # Создаем foreign key
    op.create_foreign_key(
        'fk_categories_users',
        'categories', 'users',
        ['user_id'], ['id']
    )

def downgrade():
    # Удаляем foreign key и колонку
    op.drop_constraint('fk_categories_users', 'categories', type_='foreignkey')
    op.drop_column('categories', 'user_id') 