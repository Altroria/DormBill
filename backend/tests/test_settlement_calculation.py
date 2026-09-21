"""测试结算计算是否包含空调电费"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

# 设置控制台编码
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.services.settlement_service import calculate_realtime_settlements

# 创建数据库连接
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine)

def test_settlement_with_ac_fee():
    """测试结算是否包含空调电费"""
    db = SessionLocal()
    try:
        # 测试 2026年9月的结算
        target_month = date(2026, 9, 1)
        results = calculate_realtime_settlements(db, target_month)
        
        print(f"\n=== 2026年9月结算测试 ===")
        print(f"共 {len(results)} 条结算记录\n")
        
        for item in results[:5]:  # 只显示前5条
            print(f"员工: {item['employee_name']} ({item['employee_no']})")
            print(f"  房间: {item['building_no']}-{item['room_no']}")
            print(f"  公共电费: ¥{item['electricity_fee']:.2f}")
            print(f"  空调电费: ¥{item['ac_electricity_fee']:.2f}")
            print(f"  水费: ¥{item['water_fee']:.2f}")
            print(f"  房租: ¥{item['rent_actual']:.2f}")
            print(f"  总扣款: ¥{item['total_amount']:.2f}")
            print()
        
        # 统计有空调电费的记录
        with_ac_fee = [r for r in results if r['ac_electricity_fee'] > 0]
        print(f"有空调电费的记录: {len(with_ac_fee)} / {len(results)}")
        
        if with_ac_fee:
            print("\n有空调电费的员工:")
            for item in with_ac_fee[:10]:
                print(f"  {item['employee_name']}: 空调电费 ¥{item['ac_electricity_fee']:.2f}")
        
    finally:
        db.close()

if __name__ == "__main__":
    test_settlement_with_ac_fee()
