"""update_transaction_types

Revision ID: 6d545ae4ba95
Revises: 3f5f0279cb83
Create Date: 2025-02-28 13:21:37.958239

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6d545ae4ba95'
down_revision: Union[str, None] = '3f5f0279cb83'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
