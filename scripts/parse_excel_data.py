#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
解析房间和人员数据.xlsx，生成数据库导入SQL
"""
import pandas as pd
from pathlib import Path
from datetime import datetime
import sys

# 设置输出编码
sys.stdout.reconfigure(encoding='utf-8')

def parse_excel_to_sql():
    """解析Excel文件并生成SQL导入语句"""
    
    # 读取Excel文件
    excel_path = Path(__file__).parent.parent / 'data' / '房间和人员数据.xlsx'
    
    print(f"正在读取文件: {excel_path}")
    
    # 读取所有sheet
    excel_file = pd.ExcelFile(excel_path)
    print(f"\n发现以下工作表: {excel_file.sheet_names}")
    
    # 读取每个sheet
    for sheet_name in excel_file.sheet_names:
        df = pd.read_excel(excel_path, sheet_name=sheet_name)
        print(f"\n{'='*60}")
        print(f"工作表: {sheet_name}")
        print(f"{'='*60}")
        print(f"行数: {len(df)}, 列数: {len(df.columns)}")
        print(f"\n列名: {list(df.columns)}")
        print(f"\n前10行数据:")
        print(df.head(10))
        print(f"\n数据类型:")
        print(df.dtypes)
        
        # 显示唯一值统计
        print(f"\n楼号唯一值: {df['楼号'].dropna().unique()}")
        print(f"\n房号唯一值: {sorted(df['房号'].dropna().unique())}")

if __name__ == '__main__':
    parse_excel_to_sql()
