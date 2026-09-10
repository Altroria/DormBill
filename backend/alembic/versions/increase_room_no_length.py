"""increase room_no length to 50

Revision ID: increase_room_no_length
Revises: add_room_unit
Create Date: 2026-09-10

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'increase_room_no_length'
down_revision = 'add_room_unit'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 增加 room_no 字段长度从 20 到 50
    op.alter_column('rooms', 'room_no',
                    existing_type=sa.String(20),
                    type_=sa.String(50),
                    existing_nullable=False,
                    existing_comment='房号')


def downgrade() -> None:
    # 恢复 room_no 字段长度到 20
    op.alter_column('rooms', 'room_no',
                    existing_type=sa.String(50),
                    type_=sa.String(20),
                    existing_nullable=False,
                    existing_comment='房号')
