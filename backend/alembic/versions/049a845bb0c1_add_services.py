"""Add services

Revision ID: 049a845bb0c1
Revises: aa879861d75b
Create Date: 2026-09-04 11:57:15.365587

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '049a845bb0c1'
down_revision: Union[str, None] = 'aa879861d75b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
