from backend.app.database import get_db
from backend.app.models.room_main_meter import RoomMainMeterRecord

db = next(get_db())
record = db.query(RoomMainMeterRecord).first()

if record:
    print(f"Record ID: {record.id}")
    print(f"Has common_fee: {hasattr(record, 'common_fee')}")
    print(f"common_fee value: {record.common_fee}")
    print(f"Has common_degree: {hasattr(record, 'common_degree')}")
    print(f"common_degree value: {record.common_degree}")
else:
    print("No records found")
