"""Final verification: check actual unique key (bno, room_no, room_name) duplicates"""
import re

with open(r'E:\cursor\DormBill\scripts\import_dorm_employee_from_xlsx.sql', encoding='utf-8') as f:
    content = f.read()

pattern = re.compile(r"SELECT b\.id, '([^']+)', '([^']+)', '([^']+)'.*?building_no = '([^']+)'", re.DOTALL)
rows = []
for m in pattern.finditer(content):
    rows.append((m.group(4), m.group(1), m.group(3)))  # bno, room_no, room_name

print(f'Total rooms: {len(rows)}')
print(f'Unique (bno, room_no, room_name): {len(set(rows))}')

from collections import Counter
c = Counter(rows)
dups = [(k, v) for k, v in c.items() if v > 1]
if dups:
    print('REAL DUPLICATES:')
    for k, v in dups:
        print(f'  {v}x {k}')
else:
    print('✓ No duplicates on unique key')

# Also count per-building rooms
bcount = Counter(r[0] for r in rows)
print()
print('Per-building room count:')
for b, cnt in sorted(bcount.items()):
    print(f'  {b}: {cnt}')