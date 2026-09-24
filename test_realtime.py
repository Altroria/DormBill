import sys
sys.path.insert(0, 'backend')

from app.database import SessionLocal
from app.services.settlement_service import calculate_realtime_settlements
from datetime import date

db = SessionLocal()
try:
    result = calculate_realtime_settlements(db, date(2026, 9, 1), water_mode="double")
    print(f"返回结果数量: {len(result)}")
    if result:
        print(f"第一条字段: {result[0].keys()}")
        print(f"员工ID: {result[0]['employee_id']}")
        print(f"房租: {result[0]['rent_actual']}")
        print(f"普通电费: {result[0]['electricity_fee']}")
        print(f"空调电费: {result[0]['ac_electricity_fee']}")
        print(f"水费: {result[0]['water_fee']}")
        print(f"最终扣款: {result[0].get('total_amount', 'NOT_FOUND')}")
    else:
        print("返回空列表")
except Exception as e:
    import traceback
    print(f"错误: {e}")
    traceback.print_exc()
finally:
    db.close()
