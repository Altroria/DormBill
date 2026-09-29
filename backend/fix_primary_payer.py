"""修复 is_primary_payer 错误数据
将所有非主缴费人改为主缴费人，除非备注中明确标注为配偶
"""
from app.database import SessionLocal
from app.models.residence import ResidenceRecord
from sqlalchemy import and_

db = SessionLocal()

try:
    # 查询所有有效入住记录
    all_residences = db.query(ResidenceRecord).filter(
        ResidenceRecord.status != "invalid"
    ).all()
    
    print(f"共找到 {len(all_residences)} 条有效入住记录")
    print("=" * 100)
    
    updated_count = 0
    spouse_count = 0
    
    for res in all_residences:
        old_value = res.is_primary_payer
        remark = res.remark or ""
        
        # 新逻辑：默认所有人都是主缴费人(1)，只有明确标注"配偶"或"夫妻间副"才设为0
        new_value = 0 if ('配偶' in remark or '夫妻间副' in remark) else 1
        
        if old_value != new_value:
            res.is_primary_payer = new_value
            updated_count += 1
            
            status = "配偶 → 主缴费人" if new_value == 1 else "主缴费人 → 配偶"
            print(f"更新: ID={res.id}, 员工ID={res.employee_id}, {status}, 备注=\"{remark}\"")
        
        if new_value == 0:
            spouse_count += 1
    
    print("=" * 100)
    print(f"需要更新的记录: {updated_count} 条")
    print(f"配偶记录数: {spouse_count} 条")
    print(f"主缴费人记录数: {len(all_residences) - spouse_count} 条")
    
    # 确认是否提交
    if updated_count > 0:
        confirm = input(f"\n确认更新 {updated_count} 条记录？(yes/no): ")
        if confirm.lower() == 'yes':
            db.commit()
            print("✓ 数据已更新")
        else:
            db.rollback()
            print("✗ 已取消更新")
    else:
        print("没有需要更新的记录")
        
except Exception as e:
    db.rollback()
    print(f"错误: {e}")
    raise
finally:
    db.close()
