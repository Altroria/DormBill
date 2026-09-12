#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
验证数据导入结果
检查数据完整性和关联关系
"""
import sys
import os

# 添加后端路径
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.insert(0, backend_path)

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.config import settings

def verify_import():
    """验证数据导入结果"""
    
    # 创建数据库连接
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    print("=" * 60)
    print("数据导入验证工具")
    print("=" * 60)
    print()
    
    try:
        # 1. 检查表记录数
        print("1️⃣  数据表记录统计")
        print("-" * 60)
        
        tables = {
            'buildings': '楼栋',
            'rooms': '房间',
            'employees': '员工',
            'residence_records': '入住记录'
        }
        
        for table, name in tables.items():
            result = session.execute(text(f"SELECT COUNT(*) FROM {table}"))
            count = result.scalar()
            print(f"  {name:12s}: {count:4d} 条")
        
        print()
        
        # 2. 检查楼栋信息
        print("2️⃣  楼栋信息")
        print("-" * 60)
        
        result = session.execute(text("""
            SELECT 
                building_no AS 楼号,
                name AS 名称,
                (SELECT COUNT(*) FROM rooms WHERE building_id = buildings.id) AS 房间数
            FROM buildings
            ORDER BY building_no
        """))
        
        for row in result:
            print(f"  {row[0]:6s} {row[1]:15s} - {row[2]:3d} 个房间")
        
        print()
        
        # 3. 检查公司分布
        print("3️⃣  员工公司分布")
        print("-" * 60)
        
        result = session.execute(text("""
            SELECT 
                company AS 公司,
                COUNT(*) AS 员工数
            FROM employees
            GROUP BY company
            ORDER BY 员工数 DESC
        """))
        
        for row in result:
            print(f"  {row[0]:15s}: {row[1]:3d} 人")
        
        print()
        
        # 4. 检查入住情况
        print("4️⃣  入住情况统计")
        print("-" * 60)
        
        # 按楼栋统计
        result = session.execute(text("""
            SELECT 
                b.building_no AS 楼号,
                COUNT(DISTINCT r.id) AS 总房间数,
                COUNT(DISTINCT rr.room_id) AS 已入住房间,
                COUNT(rr.id) AS 入住人数
            FROM buildings b
            LEFT JOIN rooms r ON r.building_id = b.id
            LEFT JOIN residence_records rr ON rr.room_id = r.id
            GROUP BY b.id, b.building_no
            ORDER BY b.building_no
        """))
        
        for row in result:
            occupancy_rate = (row[2] / row[1] * 100) if row[1] > 0 else 0
            print(f"  {row[0]:6s}: {row[1]:3d} 个房间，{row[2]:3d} 间已入住 ({occupancy_rate:5.1f}%)，{row[3]:3d} 人")
        
        print()
        
        # 5. 检查试用期员工
        print("5️⃣  试用期员工")
        print("-" * 60)
        
        result = session.execute(text("""
            SELECT 
                e.name AS 姓名,
                e.department AS 部门,
                rr.probation_months AS 试用期月数,
                rr.remark AS 备注
            FROM residence_records rr
            INNER JOIN employees e ON rr.employee_id = e.id
            WHERE rr.probation_months > 0
            ORDER BY e.name
        """))
        
        count = 0
        for row in result:
            print(f"  {row[0]:10s} ({row[1]:15s}) - {row[2]} 个月 - {row[3]}")
            count += 1
        
        if count == 0:
            print("  无试用期员工")
        
        print()
        
        # 6. 检查夫妻间
        print("6️⃣  夫妻间情况")
        print("-" * 60)
        
        result = session.execute(text("""
            SELECT 
                e.name AS 姓名,
                e.company AS 单位,
                rr.is_primary_payer AS 主缴费人,
                rr.remark AS 备注
            FROM residence_records rr
            INNER JOIN employees e ON rr.employee_id = e.id
            WHERE rr.remark LIKE '%夫妻%'
            ORDER BY rr.is_primary_payer DESC, e.name
        """))
        
        count = 0
        for row in result:
            payer_status = "主缴费人" if row[2] == 1 else "配偶"
            print(f"  {row[0]:10s} ({row[1]:10s}) - {payer_status:8s} - {row[3]}")
            count += 1
        
        if count == 0:
            print("  无夫妻间记录")
        
        print()
        
        # 7. 检查数据完整性
        print("7️⃣  数据完整性检查")
        print("-" * 60)
        
        # 检查孤立房间（没有楼栋）
        result = session.execute(text("""
            SELECT COUNT(*) FROM rooms 
            WHERE building_id NOT IN (SELECT id FROM buildings)
        """))
        orphan_rooms = result.scalar()
        
        # 检查孤立入住记录（没有员工）
        result = session.execute(text("""
            SELECT COUNT(*) FROM residence_records 
            WHERE employee_id NOT IN (SELECT id FROM employees)
        """))
        orphan_residences_emp = result.scalar()
        
        # 检查孤立入住记录（没有房间）
        result = session.execute(text("""
            SELECT COUNT(*) FROM residence_records 
            WHERE room_id NOT IN (SELECT id FROM rooms)
        """))
        orphan_residences_room = result.scalar()
        
        issues = []
        if orphan_rooms > 0:
            issues.append(f"发现 {orphan_rooms} 个孤立房间（没有关联楼栋）")
        if orphan_residences_emp > 0:
            issues.append(f"发现 {orphan_residences_emp} 条孤立入住记录（没有关联员工）")
        if orphan_residences_room > 0:
            issues.append(f"发现 {orphan_residences_room} 条孤立入住记录（没有关联房间）")
        
        if issues:
            print("  ⚠️  发现数据完整性问题:")
            for issue in issues:
                print(f"     - {issue}")
        else:
            print("  ✅ 数据完整性检查通过")
        
        print()
        
        # 8. 显示示例数据
        print("8️⃣  入住记录示例（前5条）")
        print("-" * 60)
        
        result = session.execute(text("""
            SELECT 
                b.building_no AS 楼号,
                r.room_no AS 房号,
                r.room_unit AS 室号,
                r.room_name AS 房间名称,
                e.name AS 姓名,
                e.department AS 部门,
                r.rent_standard AS 房租,
                rr.is_primary_payer AS 主缴费人
            FROM residence_records rr
            INNER JOIN employees e ON rr.employee_id = e.id
            INNER JOIN rooms r ON rr.room_id = r.id
            INNER JOIN buildings b ON r.building_id = b.id
            ORDER BY b.building_no, r.room_no, r.room_unit
            LIMIT 5
        """))
        
        for row in result:
            payer = "是" if row[7] == 1 else "否"
            print(f"  {row[0]:4s}-{row[1]:4s}-{row[2]:2s} {row[3]:15s} | {row[4]:10s} ({row[5]:12s}) | ¥{row[6]:6.2f} | 主缴:{payer}")
        
        print()
        print("=" * 60)
        print("✅ 验证完成")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 验证过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        session.close()
    
    return True

if __name__ == '__main__':
    try:
        success = verify_import()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ 程序异常: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
