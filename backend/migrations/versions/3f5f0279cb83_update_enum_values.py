"""update_enum_values

Revision ID: 3f5f0279cb83
Revises: f25d7f9f4515
Create Date: 2025-02-28 12:15:19.332387

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3f5f0279cb83'
down_revision: Union[str, None] = 'f25d7f9f4515'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
