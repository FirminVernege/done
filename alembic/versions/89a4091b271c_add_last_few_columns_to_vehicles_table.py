"""add last few columns to vehicles table

Revision ID: 89a4091b271c
Revises: 1090dc9a7e0f
Create Date: 2024-07-21 11:15:57.539370

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '89a4091b271c'
down_revision: Union[str, None] = '1090dc9a7e0f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('vehicles', sa.Column('rented', sa.Boolean,
                  nullable=False, server_default='False'), )
    op.add_column('vehicles', sa.Column('created_at', sa.TIMESTAMP(
        timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('vehicles', 'created_at')
    op.drop_column('vehicles', 'rented')
    pass
