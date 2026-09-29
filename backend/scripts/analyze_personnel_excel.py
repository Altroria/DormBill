"""
分析房间和人员Excel文件结构
"""
import openpyxl
from pathlib import Path


def analyze_excel():
    """分析Excel文件"""
    file_path = Path(__file__).parent.parent.parent / "data" / "房间和人员-最新.xls"
    
    print(f"分析文件: {file_path}")
    print("=" * 80)
    
    # 使用openpyxl读取（即使是.xls文件，尝试读取）
    try:
        wb = openpyxl.load_workbook(file_path, data_only=True)
    except Exception as e:
        print(f"openpyxl读取失败: {e}")
        print("\n尝试使用xlrd读取...")
        import xlrd
        wb = xlrd.open_workbook(file_path)
        ws = wb.sheet_by_index(0)
        
        print(f"\n工作表名称: {ws.name}")
        print(f"总行数: {ws.nrows}")
        print(f"总列数: {ws.ncols}")
        
        # 打印前10行
        print("\n前10行数据:")
        for row_idx in range(min(10, ws.nrows)):
            row_data = ws.row_values(row_idx)
            print(f"\n第{row_idx + 1}行:")
            for col_idx, value in enumerate(row_data):
                if value:
                    print(f"  列{col_idx + 1}: {value}")
        return
    
    ws = wb.active
    print(f"\n工作表名称: {ws.title}")
    print(f"总行数: {ws.max_row}")
    print(f"总列数: {ws.max_column}")
    
    # 打印前10行
    print("\n前10行数据:")
    for row_idx in range(1, min(11, ws.max_row + 1)):
        print(f"\n第{row_idx}行:")
        row_data = list(ws.iter_rows(min_row=row_idx, max_row=row_idx, values_only=True))[0]
        for col_idx, value in enumerate(row_data):
            if value:
                print(f"  列{col_idx + 1}: {value}")
    
    # 分析数据结构
    print("\n\n" + "=" * 80)
    print("数据结构分析:")
    print("=" * 80)
    
    # 假设第1行是表头
    headers = list(ws.iter_rows(min_row=1, max_row=1, values_only=True))[0]
    print("\n表头列名:")
    for idx, header in enumerate(headers):
        if header:
            print(f"  列{idx + 1}: {header}")
    
    # 统计数据 (xlrd版本)
    print("\n\n数据统计:")
    unique_buildings = set()
    unique_rooms = set()
    unique_employees = set()
    
    for row_idx in range(1, ws.nrows):
        row = ws.row_values(row_idx)
        if not any(row):
            continue
        if len(row) > 0 and row[0]:  # 楼栋
            unique_buildings.add(str(row[0]))
        if len(row) > 1 and row[1]:  # 房号
            unique_rooms.add(str(row[1]))
        if len(row) > 7 and row[7]:  # 姓名
            unique_employees.add(str(row[7]))
    
    print(f"  唯一楼栋数: {len(unique_buildings)}")
    print(f"  唯一房间数: {len(unique_rooms)}")
    print(f"  唯一员工数: {len(unique_employees)}")
    print(f"\n楼栋列表: {sorted(unique_buildings)}")
    
    # 查看几条完整记录
    print("\n\n完整记录示例 (前3条):")
    headers = ws.row_values(0)
    for row_idx in range(1, min(4, ws.nrows)):
        row = ws.row_values(row_idx)
        print(f"\n记录 {row_idx}:")
        for col_idx, value in enumerate(row):
            if col_idx < len(headers) and value:
                print(f"  {headers[col_idx]}: {value}")


if __name__ == "__main__":
    analyze_excel()
