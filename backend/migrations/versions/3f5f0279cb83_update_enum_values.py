"""update enum values

Revision ID: 3f5f0279cb83
Revises: b520e94c6136
Create Date: 2025-02-28 12:15:19.332387

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f5f0279cb83'
down_revision = 'b520e94c6136'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # В первой миграции уже создаются таблицы с правильными типами
    # Поэтому эта миграция не нужна
    pass


def downgrade() -> None:
    pass
