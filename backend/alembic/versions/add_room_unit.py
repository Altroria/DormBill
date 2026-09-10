"""add room_unit field

Revision ID: add_room_unit
Revises: 
Create Date: 2026-09-10

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_room_unit'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('rooms', sa.Column('room_unit', sa.String(20), nullable=True, comment='室号'))


def downgrade() -> None:
    op.drop_column('rooms', 'room_unit')
