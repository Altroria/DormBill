"""add is_guest_room to rooms

Revision ID: add_is_guest_room
Revises: 3b09c9d9d944
Create Date: 2026-09-29 16:10:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_is_guest_room'
down_revision = '3b09c9d9d944'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add is_guest_room column to rooms table
    op.add_column('rooms', sa.Column('is_guest_room', sa.BigInteger(), nullable=True, comment='是否为客房（客房水电租全免）'))
    
    # Set default value for existing rows
    op.execute('UPDATE rooms SET is_guest_room = 0 WHERE is_guest_room IS NULL')
    
    # Make it NOT NULL with default
    op.alter_column('rooms', 'is_guest_room', nullable=False, server_default='0')


def downgrade() -> None:
    op.drop_column('rooms', 'is_guest_room')
