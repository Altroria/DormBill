"""
添加房间空闲状态的数据库迁移脚本
执行方式: python backend/migrations/migrate_room_idle_status.py
"""
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy import text
from app.database import engine

def migrate():
    """执行迁移"""
    print("开始迁移：为房间表添加 'idle' 状态...")
    
    with engine.connect() as conn:
        # 开始事务
        trans = conn.begin()
        try:
            # 1. 先将 status 改为 VARCHAR（临时）
            print("步骤 1: 将状态字段改为 VARCHAR...")
            conn.execute(text(
                "ALTER TABLE rooms MODIFY COLUMN status VARCHAR(20) NOT NULL DEFAULT 'active'"
            ))
            
            # 2. 重新创建 ENUM 类型（包含新的 idle 状态）
            print("步骤 2: 重新创建 ENUM 类型...")
            conn.execute(text(
                "ALTER TABLE rooms MODIFY COLUMN status ENUM('active', 'inactive', 'idle') NOT NULL DEFAULT 'active'"
            ))
            
            trans.commit()
            print("✅ 迁移成功完成！")
            print("房间状态现在支持: active(启用), inactive(禁用), idle(空闲)")
            
        except Exception as e:
            trans.rollback()
            print(f"❌ 迁移失败: {e}")
            raise

if __name__ == "__main__":
    migrate()
