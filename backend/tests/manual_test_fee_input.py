"""手动测试总电费输入功能（直接连接数据库）"""
import sys
import os
sys.path.insert(0, "E:/Cursor/DormBill/backend")

# 设置UTF-8编码
if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"

from datetime import date
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.services.meter_v2_service import MeterV2Service
from app.models.room_main_meter import RoomMainMeterRecord
from app.models.meter import MeterRecord
from app.config import settings

# 创建数据库引擎
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine)


def test_manual_fee_input():
    """测试手动输入用电量和总电费"""
    db = SessionLocal()
    service = MeterV2Service(db)
    
    try:
        month = date(2024, 7, 1)
        building_id = 1  # 使用已存在的楼栋ID
        room_no = "201"  # 使用已存在的房号
        
        print("=" * 60)
        print("测试1: 手动输入用电量和总电费，反算电价")
        print("=" * 60)
        
        # 手动输入：用电量1000度，总电费550元
        # 期望电价 = 550 / 1000 = 0.55元/度
        record = service.update_main_meter(
            building_id=building_id,
            room_no=room_no,
            month=month,
            current_reading=Decimal("2000.00"),
            total_degree=Decimal("1000.00"),
            total_fee=Decimal("550.00"),
        )
        
        print(f"楼栋ID: {record.building_id}")
        print(f"房号: {record.room_no}")
        print(f"月份: {record.month}")
        print(f"上月读数: {record.previous_reading}")
        print(f"本月读数: {record.current_reading}")
        print(f"用电量: {record.total_degree} 度")
        print(f"总电费: {record.total_fee} 元")
        print(f"计算电价: {record.electricity_price} 元/度")
        print(f"状态: {record.status}")
        
        assert record.total_degree == Decimal("1000.00"), "用电量应为1000度"
        assert record.total_fee == Decimal("550.00"), "总电费应为550元"
        assert record.electricity_price == Decimal("0.55"), "电价应为0.55元/度"
        
        print("[PASS] 测试1通过：电价计算正确")
        print()
        
        # 测试2: 异常电价警告
        print("=" * 60)
        print("测试2: 电价异常时应有警告")
        print("=" * 60)
        
        record = service.update_main_meter(
            building_id=building_id,
            room_no=room_no,
            month=month,
            total_degree=Decimal("1000.00"),
            total_fee=Decimal("150.00"),  # 电价0.15，低于合理范围
        )
        
        print(f"用电量: {record.total_degree} 度")
        print(f"总电费: {record.total_fee} 元")
        print(f"计算电价: {record.electricity_price} 元/度")
        print(f"备注: {record.remark}")
        
        assert record.electricity_price == Decimal("0.15"), "电价应为0.15元/度"
        assert record.remark and "[警告]" in record.remark, "应有电价异常警告"
        
        print("[PASS] 测试2通过：异常电价警告正常")
        print()
        
        # 测试3: 检查空调表电价是否级联更新
        print("=" * 60)
        print("测试3: 检查空调表电价级联更新")
        print("=" * 60)
        
        # 更新总表为正常电价
        record = service.update_main_meter(
            building_id=building_id,
            room_no=room_no,
            month=month,
            total_degree=Decimal("1000.00"),
            total_fee=Decimal("600.00"),  # 电价0.60
        )
        
        print(f"总表电价: {record.electricity_price} 元/度")
        
        # 查询该房号下的所有空调表
        ac_records = (
            db.query(MeterRecord)
            .join(MeterRecord.room)
            .filter(
                MeterRecord.building_id == building_id,
                MeterRecord.month == month,
                MeterRecord.room.has(room_no=room_no)
            )
            .all()
        )
        
        print(f"找到 {len(ac_records)} 个空调表记录")
        
        for ac_record in ac_records:
            print(f"  - 房间ID {ac_record.room_id}: 电价 {ac_record.electricity_price} 元/度, "
                  f"空调用电 {ac_record.ac_degree} 度, 空调电费 {ac_record.ac_fee} 元")
            assert ac_record.electricity_price == Decimal("0.60"), \
                f"空调表电价应为0.60元/度，实际为 {ac_record.electricity_price}"
        
        print("[PASS] 测试3通过：空调表电价级联更新正常")
        print()
        
        print("=" * 60)
        print("所有测试通过！[SUCCESS]")
        print("=" * 60)
        
    except Exception as e:
        print(f"[FAIL] 测试失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.rollback()  # 回滚以不影响实际数据
        db.close()


if __name__ == "__main__":
    test_manual_fee_input()
