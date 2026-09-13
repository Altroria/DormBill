"""拆分总电表和空调电表

Revision ID: split_main_and_ac_meters
Revises: a7f066b00d54
Create Date: 2026-09-13 20:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'split_main_and_ac_meters'
down_revision: Union[str, None] = 'a7f066b00d54'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 创建房号总电表记录表
    op.create_table(
        'room_main_meter_records',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('building_id', sa.BigInteger(), nullable=False),
        sa.Column('room_no', sa.String(length=50), nullable=False, comment='房号（如201、202）'),
        sa.Column('month', sa.Date(), nullable=False, comment='结算月份（每月1号）'),
        sa.Column('meter_no', sa.String(length=50), nullable=True, comment='总电表编号'),
        sa.Column('previous_reading', sa.Numeric(precision=12, scale=2), server_default='0', comment='上月读数'),
        sa.Column('current_reading', sa.Numeric(precision=12, scale=2), server_default='0', comment='本月读数'),
        sa.Column('total_degree', sa.Numeric(precision=12, scale=2), server_default='0', comment='用电量'),
        sa.Column('electricity_price', sa.Numeric(precision=10, scale=4), server_default='0.4900', comment='电价'),
        sa.Column('total_fee', sa.Numeric(precision=12, scale=2), server_default='0', comment='电费'),
        sa.Column('status', sa.Enum('pending', 'recorded', 'calculated', name='main_meter_status'), 
                  server_default='pending', comment='待录入/已录入/已计算'),
        sa.Column('remark', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), 
                  server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['building_id'], ['buildings.id'], name='fk_main_meter_building'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('building_id', 'room_no', 'month', name='uk_building_room_month'),
        mysql_comment='房号总电表记录'
    )
    
    # 创建索引
    op.create_index('idx_main_meter_month', 'room_main_meter_records', ['month'])
    op.create_index('idx_main_meter_building_room', 'room_main_meter_records', ['building_id', 'room_no'])
    
    # 修改现有 meter_records 表的状态枚举（如果需要的话）
    # 保持现有表结构不变，后续只用它记录空调电表


def downgrade() -> None:
    op.drop_index('idx_main_meter_building_room', table_name='room_main_meter_records')
    op.drop_index('idx_main_meter_month', table_name='room_main_meter_records')
    op.drop_table('room_main_meter_records')
