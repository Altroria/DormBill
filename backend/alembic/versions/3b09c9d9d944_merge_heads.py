"""merge_heads

Revision ID: 3b09c9d9d944
Revises: add_room_main_meter, split_main_and_ac_meters
Create Date: 2026-09-13 20:09:51.491307

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b09c9d9d944'
down_revision = ('add_room_main_meter', 'split_main_and_ac_meters')
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
