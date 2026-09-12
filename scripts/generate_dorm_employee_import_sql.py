"""
根据 房间和人员数据.xlsx 生成宿舍/员工/入住记录的导入 SQL

输出文件: scripts/import_dorm_employee_from_xlsx.sql

Excel 列含义(0-based):
  0  楼号            -- buildings.building_no
  1  房号            -- rooms.room_no
  4  室号            -- rooms.room_unit
  5  房间            -- rooms.room_name
  6  任职单位        -- employees.company
  7  一级部门        -- employees.department
  8  职务            -- employees.position
  9  姓名            -- employees.name
  10 转宿日期,备注   -- residence_records.check_in_date / remark
  11 房租            -- residence_records.remark (记录到 remark)

约束:
- 楼栋用 building_no 唯一标识(原值保留,如 247、248、249、250、99)
- 房间唯一键 (building_no, room_no, room_name),rent_standard 取首个非零房租
- 员工唯一键 (name, company, department, position)
- 同一员工在同一房间只生成一条入住记录(check_out_date 为空时去重)
"""

from openpyxl import load_workbook
from datetime import datetime
import os
import re
from collections import OrderedDict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XLSX_PATH = os.path.join(BASE_DIR, "房间和人员数据.xlsx")
SQL_OUT_PATH = os.path.join(BASE_DIR, "scripts", "import_dorm_employee_from_xlsx.sql")

CURRENT_YEAR = datetime.now().year


def clean(value):
    if value is None:
        return None
    if isinstance(value, str):
        v = value.strip()
        return v if v else None
    return value


def sql_escape(value):
    if value is None:
        return "NULL"
    s = str(value).replace("\\", "\\\\").replace("'", "\\'")
    return f"'{s}'"


def parse_date(text):
    """从『转宿日期，备注』文本里抽取第一个日期 (M/D 或 M-D) -> date 或 None"""
    if not text:
        return None
    m = re.search(r"(\d{1,2})[\/\-\.](\d{1,2})", text)
    if not m:
        return None
    month, day = int(m.group(1)), int(m.group(2))
    if not (1 <= month <= 12 and 1 <= day <= 31):
        return None
    try:
        return datetime(CURRENT_YEAR, month, day).date()
    except ValueError:
        return None


def detect_check_out(text):
    """备注里出现『离宿』『搬出』『转宿到』『搬离』等关键字,认为是搬离"""
    if not text:
        return None
    if re.search(r"(离宿|搬出|搬离|转宿到|退租)", text):
        return parse_date(text)
    return None


def parse_remark(text, rent, check_in_date):
    """把备注整理成 remark 字段(包含房租/入住/特殊说明)"""
    parts = []
    if text:
        # 排除已经被 check_in_date 解析过的部分,保留完整原文作为备注
        parts.append(text)
    if rent and rent > 0:
        parts.append(f"月租:{int(rent)}")
    if check_in_date:
        parts.append(f"入住:{check_in_date.isoformat()}")
    return "; ".join(parts) if parts else None


def collect_from_excel(xlsx_path):
    wb = load_workbook(xlsx_path, data_only=True)
    ws = wb.active

    # 收集楼栋 / 房间 / 员工 / 入住记录
    buildings = OrderedDict()           # building_no -> name
    rooms = OrderedDict()               # (building_no, room_no, room_name) -> dict
    employees = OrderedDict()           # (name, company, department, position) -> dict
    residences = OrderedDict()          # (employee_name, building_no, room_no, room_unit, room_name, check_in_date) -> dict

    last_building_no = None
    last_room_no = None

    for row_idx in range(3, ws.max_row + 1):
        row = ws[row_idx]
        building_no = clean(row[0].value)
        room_no = clean(row[1].value)
        room_unit = clean(row[4].value)
        room_name = clean(row[5].value)
        company = clean(row[6].value)
        department = clean(row[7].value)
        position = clean(row[8].value)
        name = clean(row[9].value)
        memo = clean(row[10].value)
        rent_raw = row[11].value

        # 合并单元格:沿用上一行
        if building_no:
            last_building_no = building_no
        else:
            building_no = last_building_no
        if room_no:
            last_room_no = room_no
        else:
            room_no = last_room_no

        # 跳过空行(无姓名、无房间) — 这些代表「房间占位」,也要建房间
        if not (building_no and room_no and room_name):
            continue

        building_no = str(building_no)
        room_no = str(int(room_no)) if isinstance(room_no, (int, float)) else str(room_no)
        room_unit = str(int(room_unit)) if isinstance(room_unit, (int, float)) else str(room_unit) if room_unit is not None else None

        rent = None
        if isinstance(rent_raw, (int, float)):
            rent = float(rent_raw)

        # 1) 楼栋
        if building_no not in buildings:
            buildings[building_no] = f"{building_no}栋"

        # 2) 房间
        room_key = (building_no, room_no, room_name)
        if room_key not in rooms:
            rooms[room_key] = {
                "building_no": building_no,
                "room_no": room_no,
                "room_unit": room_unit,
                "room_name": room_name,
                "rent_standard": rent if (rent is not None and rent > 0) else 0.0,
            }
        elif rooms[room_key]["rent_standard"] == 0 and rent and rent > 0:
            # 已有但房租为 0,补一个非零值
            rooms[room_key]["rent_standard"] = rent

        # 3) 员工(没有姓名就跳过 — 这表示空房间,不算员工)
        if not name:
            continue

        emp_key = (name, company, department, position)
        if emp_key not in employees:
            employees[emp_key] = {
                "name": name,
                "company": company or "未知",
                "department": department or None,
                "position": position or None,
            }

        # 4) 入住记录
        check_out_date = detect_check_out(memo)
        # 只有"非搬离"行,才把备注里的日期当作入住日;否则走默认值
        if not check_out_date:
            check_in_date = parse_date(memo) if memo else None
            if not check_in_date:
                # 默认本月1日
                check_in_date = datetime(CURRENT_YEAR, datetime.now().month, 1).date()
        else:
            # 搬离/转宿/离宿行:没有真实的入住日,默认当月1日
            check_in_date = datetime(CURRENT_YEAR, datetime.now().month, 1).date()

        remark = parse_remark(memo, rent, check_in_date if not check_out_date else None)

        # 去重 key:同一员工在同一房间(building+room_no+room_name)只保留一条
        res_key = (name, building_no, room_no, room_name)
        if res_key in residences:
            # 已存在,合并备注/房租
            old = residences[res_key]
            old_rent = old.get("rent", 0) or 0
            new_rent = rent or 0
            old["rent"] = max(old_rent, new_rent)
            if check_out_date and not old.get("check_out_date"):
                old["check_out_date"] = check_out_date
            if remark and remark not in (old.get("remark") or ""):
                old["remark"] = (old.get("remark") + " | " + remark) if old.get("remark") else remark
            continue

        residences[res_key] = {
            "name": name,
            "company": company,
            "department": department,
            "position": position,
            "building_no": building_no,
            "room_no": room_no,
            "room_unit": room_unit,
            "room_name": room_name,
            "rent": rent or 0,
            "check_in_date": check_in_date,
            "check_out_date": check_out_date,
            "remark": remark,
        }

    wb.close()
    return buildings, rooms, employees, residences


def generate_sql():
    if not os.path.exists(XLSX_PATH):
        raise FileNotFoundError(f"找不到 Excel: {XLSX_PATH}")

    buildings, rooms, employees, residences = collect_from_excel(XLSX_PATH)

    lines = []
    lines.append("-- ============================================================")
    lines.append("-- 宿舍 / 员工 / 入住记录 导入脚本(由 generate_dorm_employee_import_sql.py 生成)")
    lines.append(f"-- 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"-- 来源 Excel: 房间和人员数据.xlsx")
    lines.append("-- 导入前请先执行 scripts/clean_dorm_employee_data.sql 清空相关表")
    lines.append("-- ============================================================")
    lines.append("")
    lines.append("USE dormbill;")
    lines.append("SET NAMES utf8mb4;")
    lines.append("SET CHARACTER SET utf8mb4;")
    lines.append("SET FOREIGN_KEY_CHECKS = 0;")
    lines.append("")
    lines.append("START TRANSACTION;")
    lines.append("")

    # ============ 1) 楼栋 ============
    lines.append("-- ========================================")
    lines.append(f"-- 1) 楼栋 ({len(buildings)} 条)")
    lines.append("-- ========================================")
    for b_no, b_name in buildings.items():
        lines.append(
            f"INSERT INTO buildings (building_no, name, status, created_at, updated_at) "
            f"VALUES ({sql_escape(b_no)}, {sql_escape(b_name)}, 'active', NOW(), NOW());"
        )
    lines.append("")

    # 先建立 building_no -> id 的临时映射(在 SQL 里用子查询)
    # ============ 2) 房间 ============
    lines.append("-- ========================================")
    lines.append(f"-- 2) 房间 ({len(rooms)} 条)")
    lines.append("-- ========================================")
    for r_key, r in rooms.items():
        lines.append(
            f"INSERT INTO rooms (building_id, room_no, room_unit, room_name, rent_standard, status, created_at, updated_at) "
            f"SELECT b.id, {sql_escape(r['room_no'])}, {sql_escape(r['room_unit'])}, "
            f"{sql_escape(r['room_name'])}, {r['rent_standard']:.2f}, 'active', NOW(), NOW() "
            f"FROM buildings b WHERE b.building_no = {sql_escape(r['building_no'])};"
        )
    lines.append("")

    # ============ 3) 员工 ============
    lines.append("-- ========================================")
    lines.append(f"-- 3) 员工 ({len(employees)} 条)")
    lines.append("-- ========================================")
    for i, (emp_key, emp) in enumerate(employees.items(), 1):
        employee_no = f"E{i:05d}"
        lines.append(
            f"INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) "
            f"VALUES ({sql_escape(employee_no)}, {sql_escape(emp['name'])}, "
            f"{sql_escape(emp['company'])}, {sql_escape(emp['department'])}, "
            f"{sql_escape(emp['position'])}, 'active', NOW(), NOW());"
        )
    lines.append("")

    # ============ 4) 入住记录 ============
    lines.append("-- ========================================")
    lines.append(f"-- 4) 入住记录 ({len(residences)} 条)")
    lines.append("-- ========================================")
    for r in residences.values():
        check_in = r["check_in_date"].isoformat() if r["check_in_date"] else None
        check_out = r["check_out_date"].isoformat() if r["check_out_date"] else None
        # status: 有 check_out_date -> invalid, 备注里出现『离宿/转宿』 -> invalid
        status = "invalid" if check_out else "valid"
        is_primary = 1 if (r["remark"] and "夫妻间" in r["remark"]) else 0

        lines.append(
            f"INSERT INTO residence_records (employee_id, room_id, check_in_date, check_out_date, "
            f"is_primary_payer, status, remark, created_at, updated_at) "
            f"SELECT e.id, rm.id, "
            f"{sql_escape(check_in)}, {sql_escape(check_out)}, {is_primary}, "
            f"{sql_escape(status)}, {sql_escape(r['remark'])}, NOW(), NOW() "
            f"FROM employees e "
            f"JOIN rooms rm ON rm.building_id = (SELECT id FROM buildings WHERE building_no = {sql_escape(r['building_no'])}) "
            f"  AND rm.room_no = {sql_escape(r['room_no'])} "
            f"  AND rm.room_name = {sql_escape(r['room_name'])} "
            f"WHERE e.name = {sql_escape(r['name'])} "
            f"  AND e.company = {sql_escape(r['company'] or '未知')} "
            f"  AND (e.department = {sql_escape(r['department'])} OR (e.department IS NULL AND {sql_escape(r['department'])} IS NULL)) "
            f"  AND (e.position = {sql_escape(r['position'])} OR (e.position IS NULL AND {sql_escape(r['position'])} IS NULL));"
        )
    lines.append("")

    lines.append("COMMIT;")
    lines.append("SET FOREIGN_KEY_CHECKS = 1;")
    lines.append("")
    lines.append("-- ============================================================")
    lines.append("-- 校验统计")
    lines.append("-- ============================================================")
    lines.append("SELECT")
    lines.append("  (SELECT COUNT(*) FROM buildings)         AS buildings,")
    lines.append("  (SELECT COUNT(*) FROM rooms)             AS rooms,")
    lines.append("  (SELECT COUNT(*) FROM employees)         AS employees,")
    lines.append("  (SELECT COUNT(*) FROM residence_records) AS residences;")
    lines.append("")

    with open(SQL_OUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    # 打印统计
    print(f"✅ SQL 生成完成: {SQL_OUT_PATH}")
    print()
    print("统计信息:")
    print(f"  - 楼栋   : {len(buildings)} 个   -> {list(buildings.keys())}")
    print(f"  - 房间   : {len(rooms)} 个")
    print(f"  - 员工   : {len(employees)} 个")
    print(f"  - 入住记录: {len(residences)} 条")
    return buildings, rooms, employees, residences


if __name__ == "__main__":
    generate_sql()
