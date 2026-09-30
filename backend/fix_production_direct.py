#!/usr/bin/env python3
"""
直接连接生产数据库修复脚本
数据库: 47.102.36.185:3306/dormbill
执行: python fix_production_direct.py
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
    print("生产数据库直连修复脚本")
    print("=" * 100)
    print(f"目标数据库: {PROD_DB_HOST}:{PROD_DB_PORT}/{PROD_DB_NAME}")
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 安全提示
    print("⚠️  警告：此脚本将直接修改生产数据库")
    print("修复内容：修正 residence_records 表中的 is_primary_payer 字段")
    print("修复逻辑：默认所有人都是主缴费人(1)，只有备注明确标注'配偶'或'夫妻间副'才设为0")
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
        
        print(f"📊 当前数据统计:")
        print(f"   有效入住记录总数: {stats[0]} 条")
        print(f"   主缴费人(is_primary_payer=1): {stats[1]} 条")
        print(f"   非主缴费人(is_primary_payer!=1): {stats[2]} 条")
        print()
        
        # 2. 预览需要更新的记录
        print("🔍 分析需要更新的记录...")
        print("-" * 100)
        
        # 查询所有有效记录
        result = session.execute(text("""
            SELECT id, employee_id, is_primary_payer, remark
            FROM residence_records
            WHERE status != 'invalid'
            ORDER BY id
        """))
        
        all_records = result.fetchall()
        updates = []
        
        for record in all_records:
            record_id, employee_id, old_value, remark = record
            remark = remark or ""
            
            # 新逻辑：只有备注中有"配偶"或"夫妻间副"才设为0，其他都是1
            new_value = 0 if ('配偶' in remark or '夫妻间副' in remark) else 1
            
            if old_value != new_value:
                updates.append({
                    'id': record_id,
                    'employee_id': employee_id,
                    'old': old_value,
                    'new': new_value,
                    'remark': remark
                })
        
        if not updates:
            print("✓ 没有需要更新的记录，数据已经正确")
            session.close()
            return 0
        
        print(f"发现 {len(updates)} 条需要更新的记录:")
        print()
        
        # 显示前 30 条
        for i, u in enumerate(updates[:30]):
            status = "0→1 (配偶改为主缴费人)" if u['new'] == 1 else "1→0 (主缴费人改为配偶)"
            print(f"{i+1}. ID={u['id']}, 员工ID={u['employee_id']}, {status}")
            if u['remark']:
                print(f"   备注: {u['remark']}")
        
        if len(updates) > 30:
            print(f"... 还有 {len(updates) - 30} 条记录")
        
        print()
        print("=" * 100)
        
        # 3. 二次确认
        print(f"⚠️  即将更新生产数据库 {PROD_DB_HOST}:{PROD_DB_PORT}/{PROD_DB_NAME}")
        print(f"将更新 {len(updates)} 条记录")
        print()
        confirm1 = input("请输入 'YES' 确认继续（其他任何输入将取消）: ")
        
        if confirm1 != 'YES':
            print("❌ 已取消更新")
            session.close()
            return 1
        
        print()
        print("⚠️  最后确认：此操作不可撤销")
        confirm2 = input("再次输入 'CONFIRM' 最终确认: ")
        
        if confirm2 != 'CONFIRM':
            print("❌ 已取消更新")
            session.close()
            return 1
        
        # 4. 执行更新
        print()
        print("🔄 正在更新...")
        
        updated_count = 0
        for u in updates:
            session.execute(text("""
                UPDATE residence_records 
                SET is_primary_payer = :new_value
                WHERE id = :record_id
            """), {'new_value': u['new'], 'record_id': u['id']})
            updated_count += 1
            
            if updated_count % 10 == 0:
                print(f"   已更新 {updated_count}/{len(updates)} 条...")
        
        session.commit()
        
        print(f"✅ 更新完成，共更新 {updated_count} 条记录")
        print()
        
        # 5. 验证结果
        print("=" * 100)
        print("📊 更新后统计:")
        
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
        
        # 6. 显示配偶记录（验证）
        result = session.execute(text("""
            SELECT employee_id, remark
            FROM residence_records
            WHERE status != 'invalid' AND is_primary_payer = 0
            LIMIT 10
        """))
        spouse_records = result.fetchall()
        
        if spouse_records:
            print("✓ 非主缴费人记录（前10条）:")
            for emp_id, remark in spouse_records:
                print(f"   员工ID={emp_id}, 备注={remark}")
        else:
            print("✓ 没有非主缴费人记录（所有人都是主缴费人）")
        
        print()
        print("=" * 100)
        print("✅ 修复完成！")
        
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
