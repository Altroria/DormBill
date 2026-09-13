"""add common electricity fields to room_main_meter_records

Revision ID: c1d2e3f4a5b6
Revises: 78137bb36331
Create Date: 2026-09-13 21:05:00.000000

"""
from alembic import op
import sqlalchemy as sa
from decimal import Decimal


# revision identifiers, used by Alembic.
revision = 'c1d2e3f4a5b6'
down_revision = '78137bb36331'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """添加公共用电量和公共电费字段"""
    # 添加 common_degree 字段（公共用电量）
    op.add_column(
        'room_main_meter_records',
        sa.Column('common_degree', sa.Numeric(12, 2), 
                  server_default='0.00', 
                  nullable=False,
                  comment='公共用电量（总表-空调表）')
    )
    
    # 添加 common_fee 字段（公共电费）
    op.add_column(
        'room_main_meter_records',
        sa.Column('common_fee', sa.Numeric(12, 2), 
                  server_default='0.00', 
                  nullable=False,
                  comment='公共电费（总表电费-空调电费）')
    )


def downgrade() -> None:
    """回滚：删除公共用电字段"""
    op.drop_column('room_main_meter_records', 'common_fee')
    op.drop_column('room_main_meter_records', 'common_degree')
