"""add username to users

Revision ID: add_username_rev
Revises: savings_goals_rev
Create Date: 2024-03-15 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_username_rev'
down_revision = 'savings_goals_rev'
branch_labels = None
depends_on = None

def upgrade():
    # Добавляем колонку username
    op.add_column('users', sa.Column('username', sa.String(), nullable=True))
    # Создаем уникальный индекс
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)

def downgrade():
    # Удаляем индекс и колонку
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_column('users', 'username') 