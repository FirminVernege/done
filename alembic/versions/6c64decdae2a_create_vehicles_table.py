"""create vehicles table

Revision ID: 6c64decdae2a
Revises: 
Create Date: 2024-07-21 10:26:15.120141

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6c64decdae2a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('vehicles', sa.Column('id', sa.Integer(), nullable=False,
                    primary_key=True), sa.Column('numberplate', sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('vehicles')
    pass
