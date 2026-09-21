"""直接测试 API 返回的数据"""
import sys
from pathlib import Path

# 先设置编码
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 再设置路径
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.services.settlement_service import calculate_realtime_settlements
from datetime import date

# 创建数据库连接
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

# 测试实时结算计算
month = date(2026, 9, 1)
settlements = calculate_realtime_settlements(db, month, "double")

print(f"=== 2026年9月实时结算数据 ===")
print(f"共 {len(settlements)} 条记录\n")

# 显示前5条有空调电费的记录
ac_records = [s for s in settlements if s.get('ac_electricity_fee', 0) > 0]
print(f"有空调电费的记录: {len(ac_records)} 条\n")

if ac_records:
    print("前5条有空调电费的记录:")
    for item in ac_records[:5]:
        print(f"\n员工: {item['employee_name']} ({item['employee_no']})")
        print(f"  房间: {item['building_no']}-{item['room_no']}")
        print(f"  普通电费: ¥{item['electricity_fee']:.2f}")
        print(f"  空调电费: ¥{item['ac_electricity_fee']:.2f}")
        print(f"  水费: ¥{item['water_fee']:.2f}")
        print(f"  房租: ¥{item['rent_actual']:.2f}")
        print(f"  总扣款: ¥{item['total_amount']:.2f}")

# 检查返回数据的键
print("\n=== 数据结构（第一条记录的键）===")
if settlements:
    print(sorted(settlements[0].keys()))

db.close()
