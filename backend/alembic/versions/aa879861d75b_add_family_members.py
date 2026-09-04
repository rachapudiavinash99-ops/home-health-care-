"""Add family members

Revision ID: aa879861d75b
Revises: e5ce41f286f6
Create Date: 2026-09-04 11:55:52.026325

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aa879861d75b'
down_revision: Union[str, None] = 'e5ce41f286f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
