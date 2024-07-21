"""add foreign key to vehicle table

Revision ID: 1090dc9a7e0f
Revises: 7b587267ec20
Create Date: 2024-07-21 10:56:47.769266

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1090dc9a7e0f'
down_revision: Union[str, None] = '7b587267ec20'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('vehicles', sa.Column(
        'owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('vehicles_users_fk', source_table='vehicles', referent_table='users', local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('vehicles_users_fk', table_name='vehicles')
    op.drop_column('vehicles', 'owner_id')
    pass
