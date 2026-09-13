"""add_meter_v2_fields

Revision ID: 78137bb36331
Revises: 3b09c9d9d944
Create Date: 2026-09-13 20:18:51.462425

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78137bb36331'
down_revision = '3b09c9d9d944'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 添加 building_id 字段到 meter_records 表
    op.add_column('meter_records', sa.Column('building_id', sa.BigInteger(), nullable=True, comment='楼栋ID（冗余字段）'))
    op.create_foreign_key('fk_meter_records_building_id', 'meter_records', 'buildings', ['building_id'], ['id'])
    
    # 添加 ac_meter_no 字段到 meter_records 表
    op.add_column('meter_records', sa.Column('ac_meter_no', sa.String(50), nullable=True, comment='空调电表编号'))
    
    # 创建索引
    op.create_index('idx_building_month', 'meter_records', ['building_id', 'month'])
    
    # 从 rooms 表同步 building_id 数据
    op.execute("""
        UPDATE meter_records mr
        JOIN rooms r ON mr.room_id = r.id
        SET mr.building_id = r.building_id
    """)


def downgrade() -> None:
    # 删除索引
    op.drop_index('idx_building_month', table_name='meter_records')
    
    # 删除外键
    op.drop_constraint('fk_meter_records_building_id', 'meter_records', type_='foreignkey')
    
    # 删除字段
    op.drop_column('meter_records', 'ac_meter_no')
    op.drop_column('meter_records', 'building_id')
