"""
从 Excel 文件导入数据到数据库
读取 7月份的 Excel 数据，生成 SQL 插入脚本
"""
from openpyxl import load_workbook
from datetime import datetime
import os

def parse_excel_file(file_path):
    """解析 Excel 文件并显示结构"""
    print(f"\n{'='*60}")
    print(f"正在读取: {file_path}")
    print('='*60)
    
    wb = load_workbook(file_path, data_only=True)
    
    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        print(f"\n工作表: {sheet_name}")
        
        # 读取表头（第一行）
        headers = []
        for cell in ws[1]:
            headers.append(cell.value)
        print(f"列名: {headers}")
        
        # 读取前5行数据
        print(f"\n前5行数据:")
        max_row = min(6, ws.max_row)  # 最多显示5行数据
        for row_idx in range(1, max_row + 1):
            row_data = []
            for cell in ws[row_idx]:
                row_data.append(cell.value)
            print(f"第{row_idx}行: {row_data}")
        
        print(f"\n总行数: {ws.max_row}")
        print(f"总列数: {ws.max_column}")
    
    wb.close()

def main():
    """主函数"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Excel 文件路径
    files = [
        os.path.join(base_dir, "7月空调各房间分摊费用.xlsx"),
        os.path.join(base_dir, "7月宿舍员工 扣款.xlsx")
    ]
    
    for file_path in files:
        if os.path.exists(file_path):
            parse_excel_file(file_path)
        else:
            print(f"\n文件不存在: {file_path}")

if __name__ == "__main__":
    main()
