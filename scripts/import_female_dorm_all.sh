#!/bin/bash
# 女生宿舍数据完整导入脚本
# 执行顺序：员工 -> 入住记录

set -e  # 遇到错误立即退出

echo "=================================="
echo "女生宿舍数据导入"
echo "=================================="

DB_CMD="docker compose -f docker-compose.prod.yml exec -T mysql mysql -uroot -p405649 dormbill"

echo ""
echo "步骤 1/3: 导入44名女生宿舍员工..."
$DB_CMD < scripts/import_female_dorm_employees.sql
echo "✅ 员工导入完成"

echo ""
echo "步骤 2/3: 导入44条入住记录..."
$DB_CMD < scripts/import_female_dorm_records_fixed.sql
echo "✅ 入住记录导入完成"

echo ""
echo "步骤 3/3: 验证结果..."
echo ""
echo "总入住记录数："
docker compose -f docker-compose.prod.yml exec mysql mysql -uroot -p405649 dormbill -e "SELECT COUNT(*) as total FROM residence_records;"

echo ""
echo "按公司统计："
docker compose -f docker-compose.prod.yml exec mysql mysql -uroot -p405649 dormbill -e "
SELECT 
    e.company,
    COUNT(*) as count
FROM residence_records rr
JOIN employees e ON rr.employee_id = e.id
GROUP BY e.company
ORDER BY COUNT(*) DESC;
"

echo ""
echo "按楼栋统计："
docker compose -f docker-compose.prod.yml exec mysql mysql -uroot -p405649 dormbill -e "
SELECT 
    b.building_no,
    COUNT(*) as count
FROM residence_records rr
JOIN rooms r ON rr.room_id = r.id
JOIN buildings b ON r.building_id = b.id
GROUP BY b.building_no
ORDER BY b.building_no;
"

echo ""
echo "=================================="
echo "✅ 全部完成！"
echo "=================================="
