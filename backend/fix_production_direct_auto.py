#!/usr/bin/env python3
"""
生产数据库直连修复脚本 - 自动执行版
数据库: 47.102.36.185:3306/dormbill
执行: python fix_production_direct_auto.py
"""
import sys
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# 生产数据库连接信息
PROD_DB_HOST = "47.102.36.185"
PROD_DB_PORT = 3306
PROD_DB_USER = "root"
PROD_DB_PASSWORD = "405649"
PROD_DB_NAME = "dormbill"

def main():
    print("=" * 100)
    print("生产数据库直连修复脚本 - 自动执行版")
    print("=" * 100)
    print(f"目标数据库: {PROD_DB_HOST}:{PROD_DB_PORT}/{PROD_DB_NAME}")
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 连接数据库
    print("🔌 正在连接生产数据库...")
    try:
        DATABASE_URL = f"mysql+pymysql://{PROD_DB_USER}:{PROD_DB_PASSWORD}@{PROD_DB_HOST}:{PROD_DB_PORT}/{PROD_DB_NAME}"
        engine = create_engine(DATABASE_URL, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()
        print("✓ 连接成功")
        print()
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        return 1
    
    try:
        # 1. 统计当前状态
        result = session.execute(text("""
            SELECT COUNT(*) as total,
                   SUM(CASE WHEN is_primary_payer = 1 THEN 1 ELSE 0 END) as primary_count,
                   SUM(CASE WHEN is_primary_payer != 1 THEN 1 ELSE 0 END) as non_primary_count
            FROM residence_records
            WHERE status != 'invalid'
        """))
        stats = result.fetchone()
        
        print(f"📊 修复前数据统计:")
        print(f"   有效入住记录总数: {stats[0]} 条")
        print(f"   主缴费人(is_primary_payer=1): {stats[1]} 条")
        print(f"   非主缴费人(is_primary_payer!=1): {stats[2]} 条")
        print()
        
        # 2. 执行修复 SQL
        print("🔄 正在执行修复...")
        print("修复逻辑: 默认设为1，只有备注中包含'配偶'或'夫妻间副'才设为0")
        print()
        
        # 先将所有记录设为 1（主缴费人）
        result = session.execute(text("""
            UPDATE residence_records 
            SET is_primary_payer = 1
            WHERE status != 'invalid'
        """))
        print(f"✓ 步骤1: 将所有有效记录设为主缴费人(1)")
        
        # 再将备注中包含"配偶"或"夫妻间副"的设为 0
        result = session.execute(text("""
            UPDATE residence_records 
            SET is_primary_payer = 0
            WHERE status != 'invalid' 
            AND (remark LIKE '%配偶%' OR remark LIKE '%夫妻间副%')
        """))
        spouse_count = result.rowcount
        print(f"✓ 步骤2: 将备注包含'配偶'或'夫妻间副'的记录设为0，共 {spouse_count} 条")
        
        session.commit()
        print()
        print("✅ 更新完成")
        print()
        
        # 3. 验证结果
        print("=" * 100)
        print("📊 修复后数据统计:")
        
        result = session.execute(text("""
            SELECT COUNT(*) as total,
                   SUM(CASE WHEN is_primary_payer = 1 THEN 1 ELSE 0 END) as primary_count,
                   SUM(CASE WHEN is_primary_payer != 1 THEN 1 ELSE 0 END) as non_primary_count
            FROM residence_records
            WHERE status != 'invalid'
        """))
        stats = result.fetchone()
        
        print(f"   有效入住记录总数: {stats[0]} 条")
        print(f"   主缴费人(is_primary_payer=1): {stats[1]} 条")
        print(f"   非主缴费人(is_primary_payer!=1): {stats[2]} 条")
        print()
        
        # 4. 显示配偶记录（验证）
        result = session.execute(text("""
            SELECT id, employee_id, remark
            FROM residence_records
            WHERE status != 'invalid' AND is_primary_payer = 0
            ORDER BY id
        """))
        spouse_records = result.fetchall()
        
        if spouse_records:
            print(f"✓ 非主缴费人记录（共{len(spouse_records)}条）:")
            for record_id, emp_id, remark in spouse_records:
                print(f"   ID={record_id}, 员工ID={emp_id}, 备注={remark}")
        else:
            print("✓ 没有非主缴费人记录（所有人都是主缴费人）")
        
        print()
        print("=" * 100)
        print("✅ 修复完成！")
        print()
        print("📝 修复总结:")
        print(f"   - 修复前非主缴费人: {stats[2]} 条")
        print(f"   - 修复后非主缴费人: {len(spouse_records)} 条")
        print(f"   - 修正记录数: {stats[2] - len(spouse_records)} 条")
        
        return 0
        
    except Exception as e:
        session.rollback()
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return 1
        
    finally:
        session.close()

if __name__ == "__main__":
    sys.exit(main())
