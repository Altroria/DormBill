import sys
sys.path.insert(0, 'backend')

from app.database import get_db
from datetime import date
from sqlalchemy.orm import Session

db = next(get_db())

try:
    from sqlalchemy import and_, func as sql_func
    from app.models.room_main_meter import RoomMainMeterRecord
    from app.models.meter import MeterRecord
    from app.models.room import Room
    from app.models.building import Building
    from app.models.residence import ResidenceRecord
    from app.utils.date_utils import month_start, stay_days_in_month
    
    month = "2026-09"
    month_date = date.fromisoformat(f"{month}-01")
    
    # 查询总表记录
    query = db.query(RoomMainMeterRecord).filter(
        RoomMainMeterRecord.month == month_date
    )
    
    total = query.count()
    print(f"Total records: {total}")
    
    main_meters = query.limit(10).all()
    print(f"First 10 records: {len(main_meters)}")
    
    if main_meters:
        main_meter = main_meters[0]
        print(f"\nProcessing record: building_id={main_meter.building_id}, room_no={main_meter.room_no}")
        
        # 批量预加载数据
        building_ids = list(set(m.building_id for m in main_meters))
        print(f"Building IDs: {building_ids}")
        
        buildings_dict = {
            b.id: b for b in db.query(Building).filter(Building.id.in_(building_ids)).all()
        } if building_ids else {}
        print(f"Buildings: {list(buildings_dict.keys())}")
        
        # 查询空调表
        ac_meters = (
            db.query(MeterRecord)
            .join(Room, Room.id == MeterRecord.room_id)
            .filter(
                and_(
                    MeterRecord.building_id == main_meter.building_id,
                    Room.room_no == main_meter.room_no,
                    MeterRecord.month == month_date,
                )
            )
            .all()
        )
        print(f"AC meters: {len(ac_meters)}")
        
        # 查询房间
        rooms = (
            db.query(Room)
            .filter(
                and_(
                    Room.building_id == main_meter.building_id,
                    Room.room_no == main_meter.room_no,
                    Room.status == "active",
                )
            )
            .all()
        )
        print(f"Rooms: {len(rooms)}")
        
        room_ids = [r.id for r in rooms]
        print(f"Room IDs: {room_ids}")
        
        # 查询入住记录
        if room_ids:
            all_records = (
                db.query(ResidenceRecord)
                .filter(
                    and_(
                        ResidenceRecord.room_id.in_(room_ids),
                        ResidenceRecord.status.in_(["valid", "business_trip"]),
                    )
                )
                .all()
            )
            print(f"Residence records: {len(all_records)}")
            
            # 统计入住人数
            total_occupants = 0
            for room_id in room_ids:
                records = [r for r in all_records if r.room_id == room_id]
                for r in records:
                    days = stay_days_in_month(r.check_in_date, r.check_out_date, month_date)
                    print(f"  Record {r.id}: room_id={r.room_id}, days={days}")
                    if days > 0:
                        total_occupants += 1
            
            print(f"Total occupants: {total_occupants}")
        
        print("\n✓ All queries executed successfully")
        
except Exception as e:
    import traceback
    print(f"\n✗ Error: {e}")
    traceback.print_exc()
