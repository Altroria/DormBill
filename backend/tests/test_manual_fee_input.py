"""测试手动输入总电费功能"""
import pytest
from datetime import date
from decimal import Decimal
from sqlalchemy.orm import Session

from app.services.meter_v2_service import MeterV2Service
from app.models.room_main_meter import RoomMainMeterRecord
from app.models.meter import MeterRecord
from app.models.room import Room
from app.models.building import Building


def test_manual_fee_input_calculate_price(db_session: Session):
    """测试手动输入用电量和总电费，反算电价"""
    service = MeterV2Service(db_session)
    
    # 准备测试数据
    building = Building(
        building_no="1",
        building_name="1号楼",
        status="active"
    )
    db_session.add(building)
    db_session.flush()
    
    room = Room(
        building_id=building.id,
        room_no="101",
        room_unit="A",
        room_name="A套间",
        status="active"
    )
    db_session.add(room)
    db_session.flush()
    
    month = date(2024, 7, 1)
    
    # 手动输入用电量1000度，总电费550元
    # 期望电价 = 550 / 1000 = 0.55 元/度
    record = service.update_main_meter(
        building_id=building.id,
        room_no="101",
        month=month,
        current_reading=Decimal("2000.00"),
        total_degree=Decimal("1000.00"),
        total_fee=Decimal("550.00"),
    )
    
    assert record.total_degree == Decimal("1000.00")
    assert record.total_fee == Decimal("550.00")
    assert record.electricity_price == Decimal("0.55")
    assert record.status == "recorded"
    

def test_manual_fee_input_abnormal_price_warning(db_session: Session):
    """测试电价异常时的警告"""
    service = MeterV2Service(db_session)
    
    # 准备测试数据
    building = Building(
        building_no="2",
        building_name="2号楼",
        status="active"
    )
    db_session.add(building)
    db_session.flush()
    
    room = Room(
        building_id=building.id,
        room_no="201",
        room_unit="A",
        room_name="A套间",
        status="active"
    )
    db_session.add(room)
    db_session.flush()
    
    month = date(2024, 7, 1)
    
    # 输入异常电价：用电量1000度，总电费150元
    # 电价 = 150 / 1000 = 0.15 元/度（低于0.3的合理范围）
    record = service.update_main_meter(
        building_id=building.id,
        room_no="201",
        month=month,
        current_reading=Decimal("2000.00"),
        total_degree=Decimal("1000.00"),
        total_fee=Decimal("150.00"),
    )
    
    assert record.electricity_price == Decimal("0.15")
    assert "[警告] 电价异常" in record.remark
    assert "0.1500元/度" in record.remark


def test_cascade_update_ac_meters_price(db_session: Session):
    """测试总表电价变化时，级联更新空调表电价"""
    service = MeterV2Service(db_session)
    
    # 准备测试数据
    building = Building(
        building_no="3",
        building_name="3号楼",
        status="active"
    )
    db_session.add(building)
    db_session.flush()
    
    # 同一房号下有3个套间
    room1 = Room(
        building_id=building.id,
        room_no="301",
        room_unit="A",
        room_name="A套间",
        status="active"
    )
    room2 = Room(
        building_id=building.id,
        room_no="301",
        room_unit="B",
        room_name="B套间",
        status="active"
    )
    room3 = Room(
        building_id=building.id,
        room_no="301",
        room_unit="C",
        room_name="C套间",
        status="active"
    )
    db_session.add_all([room1, room2, room3])
    db_session.flush()
    
    month = date(2024, 7, 1)
    
    # 创建3个空调表记录，初始电价0.49
    for room in [room1, room2, room3]:
        ac_record = MeterRecord(
            room_id=room.id,
            building_id=building.id,
            month=month,
            ac_previous_reading=Decimal("0"),
            ac_current_reading=Decimal("100"),
            electricity_price=Decimal("0.49"),
            previous_reading=Decimal("0"),
            current_reading=Decimal("0"),
        )
        ac_record.ac_degree = Decimal("100")
        ac_record.ac_fee = Decimal("100") * Decimal("0.49")
        db_session.add(ac_record)
    
    db_session.flush()
    
    # 更新总表，手动输入用电量和总电费，反算电价为0.60
    main_record = service.update_main_meter(
        building_id=building.id,
        room_no="301",
        month=month,
        current_reading=Decimal("3000.00"),
        total_degree=Decimal("1000.00"),
        total_fee=Decimal("600.00"),
    )
    
    assert main_record.electricity_price == Decimal("0.60")
    
    # 检查所有空调表的电价和电费是否已更新
    ac_records = (
        db_session.query(MeterRecord)
        .filter(
            MeterRecord.building_id == building.id,
            MeterRecord.month == month
        )
        .all()
    )
    
    assert len(ac_records) == 3
    for ac_record in ac_records:
        assert ac_record.electricity_price == Decimal("0.60")
        # 空调用电100度 × 新电价0.60 = 60元
        assert ac_record.ac_fee == Decimal("60.00")


def test_only_input_total_degree(db_session: Session):
    """测试仅手动输入用电量，按现有电价计算费用"""
    service = MeterV2Service(db_session)
    
    building = Building(
        building_no="4",
        building_name="4号楼",
        status="active"
    )
    db_session.add(building)
    db_session.flush()
    
    room = Room(
        building_id=building.id,
        room_no="401",
        room_unit="A",
        room_name="A套间",
        status="active"
    )
    db_session.add(room)
    db_session.flush()
    
    month = date(2024, 7, 1)
    
    # 仅输入用电量，不输入总电费
    record = service.update_main_meter(
        building_id=building.id,
        room_no="401",
        month=month,
        current_reading=Decimal("2000.00"),
        total_degree=Decimal("1000.00"),
    )
    
    assert record.total_degree == Decimal("1000.00")
    # 应该按默认电价0.49计算
    assert record.total_fee == Decimal("1000.00") * Decimal("0.49")
    assert record.electricity_price == Decimal("0.49")


def test_only_input_total_fee(db_session: Session):
    """测试仅手动输入总电费，按读数计算用电量并反算电价"""
    service = MeterV2Service(db_session)
    
    building = Building(
        building_no="5",
        building_name="5号楼",
        status="active"
    )
    db_session.add(building)
    db_session.flush()
    
    room = Room(
        building_id=building.id,
        room_no="501",
        room_unit="A",
        room_name="A套间",
        status="active"
    )
    db_session.add(room)
    db_session.flush()
    
    month = date(2024, 7, 1)
    
    # 先创建一条记录
    record = service.update_main_meter(
        building_id=building.id,
        room_no="501",
        month=month,
        current_reading=Decimal("1000.00"),
    )
    record.previous_reading = Decimal("0.00")
    db_session.flush()
    
    # 仅输入总电费
    record = service.update_main_meter(
        building_id=building.id,
        room_no="501",
        month=month,
        total_fee=Decimal("600.00"),
    )
    
    # 用电量应该从读数自动计算：1000 - 0 = 1000
    assert record.total_degree == Decimal("1000.00")
    assert record.total_fee == Decimal("600.00")
    # 反算电价：600 / 1000 = 0.6
    assert record.electricity_price == Decimal("0.6")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
