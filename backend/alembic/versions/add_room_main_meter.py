"""Add room_main_meter_records table

Revision ID: add_room_main_meter
Revises: a7f066b00d54
Create Date: 2026-09-13
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Numeric, BigInteger


# revision identifiers, used by Alembic.
revision = 'add_room_main_meter'
down_revision = 'a7f066b00d54'
branch_labels = None
depends_on = None


def upgrade():
    # 创建房号总电表记录表
    op.create_table(
        'room_main_meter_records',
        sa.Column('id', BigInteger, primary_key=True, autoincrement=True),
        sa.Column('building_id', BigInteger, sa.ForeignKey('buildings.id'), nullable=False),
        sa.Column('room_no', sa.String(50), nullable=False, comment='房号（如201、202）'),
        sa.Column('month', sa.Date, nullable=False, comment='结算月份（每月1号）'),
        sa.Column('meter_no', sa.String(50), nullable=True, comment='总电表编号'),
        
        sa.Column('previous_reading', Numeric(12, 2), server_default='0', comment='上月读数'),
        sa.Column('current_reading', Numeric(12, 2), server_default='0', comment='本月读数'),
        sa.Column('total_degree', Numeric(12, 2), server_default='0', comment='用电量'),
        
        sa.Column('electricity_price', Numeric(10, 4), server_default='0.4900', comment='电价'),
        sa.Column('total_fee', Numeric(12, 2), server_default='0', comment='电费'),
        
        sa.Column('status', sa.Enum('pending', 'recorded', 'calculated', name='main_meter_status'),
                  server_default='pending', comment='待录入/已录入/已计算'),
        sa.Column('remark', sa.String(500), nullable=True),
        
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()),
        
        comment='房号总电表记录'
    )
    
    # 创建唯一索引
    op.create_unique_constraint(
        'uk_building_room_month',
        'room_main_meter_records',
        ['building_id', 'room_no', 'month']
    )
    
    # 创建普通索引
    op.create_index('idx_main_meter_month', 'room_main_meter_records', ['month'])
    op.create_index('idx_main_meter_building_room', 'room_main_meter_records', ['building_id', 'room_no'])


def downgrade():
    # 删除索引
    op.drop_index('idx_main_meter_building_room', 'room_main_meter_records')
    op.drop_index('idx_main_meter_month', 'room_main_meter_records')
    
    # 删除唯一约束
    op.drop_constraint('uk_building_room_month', 'room_main_meter_records', type_='unique')
    
    # 删除表
    op.drop_table('room_main_meter_records')
    
    # 删除枚举类型
    op.execute('DROP TYPE IF EXISTS main_meter_status')
