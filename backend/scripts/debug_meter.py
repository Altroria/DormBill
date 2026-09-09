"""
调试电表数据导入
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import openpyxl

def debug_meter_data():
    base_dir = Path(__file__).parent.parent.parent
    ac_file = base_dir / "7月空调各房间分摊费用.xlsx"
    
    wb = openpyxl.load_workbook(ac_file, data_only=True)  # data_only=True 获取计算后的值
    ws = wb.active
    
    print("前10行电表数据详情:")
    print("="*80)
    
    for row_idx in range(3, 13):
        row = list(ws.iter_rows(min_row=row_idx, max_row=row_idx, values_only=True))[0]
        
        seq = row[0]
        building_col = row[1]
        room_col = row[2]
        household = row[3]
        col4 = row[4]  # 空调度数公式
        col5 = row[5]  # 电费
        
        print(f"\n第{row_idx}行:")
        print(f"  序号: {seq}, 类型: {type(seq)}")
        print(f"  楼栋: {building_col}, 类型: {type(building_col)}")
        print(f"  房间: {room_col}, 类型: {type(room_col)}")
        print(f"  户主: {household}")
        print(f"  列4(空调度数): {col4}, 类型: {type(col4)}")
        print(f"  列5(电费): {col5}, 类型: {type(col5)}")
        
        # 解析
        if isinstance(seq, (int, float)) and building_col:
            building_str = str(int(float(building_col)))
            if len(building_str) >= 3:
                building_num = building_str[0]
                room_num = building_str[1:]
                print(f"  解析结果: {building_num}栋{room_num}室")

if __name__ == "__main__":
    debug_meter_data()
