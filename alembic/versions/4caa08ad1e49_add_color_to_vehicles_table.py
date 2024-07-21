"""add color to vehicles table

Revision ID: 4caa08ad1e49
Revises: 6c64decdae2a
Create Date: 2024-07-21 10:36:00.640985

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4caa08ad1e49'
down_revision: Union[str, None] = '6c64decdae2a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('vehicles', sa.Column('color', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('vehicles', 'color')
    pass
