"""直接测试API路由"""
import asyncio
import sys
from datetime import date

sys.path.insert(0, './backend')

from backend.app.database import AsyncSessionLocal
from backend.app.services.meter_v2_service import MeterV2Service


async def test_combined_meters():
    """测试获取组合电表列表"""
    async with AsyncSessionLocal() as db:
        service = MeterV2Service(db)
        
        try:
            result = await service.get_combined_meter_list(
                building_id=None,
                month=date(2026, 9, 1),
                room_no=None,
                skip=0,
                limit=5,
            )
            
            print("✓ Success!")
            print(f"Total: {result['total']}")
            print(f"Items count: {len(result['items'])}")
            
            if result['items']:
                print(f"\nFirst item:")
                item = result['items'][0]
                print(f"  Building ID: {item['building_id']}")
                print(f"  Room No: {item['room_no']}")
                print(f"  Month: {item['month']}")
                print(f"  Main Fee: {item['main_total_fee']}")
                print(f"  AC Meters: {len(item['ac_meters'])}")
            
        except Exception as e:
            print(f"✗ Error: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_combined_meters())
