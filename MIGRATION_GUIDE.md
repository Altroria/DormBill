# 从V1迁移到V2电表管理系统指南

## 概述

本文档说明如何从旧版电表管理系统（V1）迁移到新版（V2）。

## 主要变化

### 业务架构
- **V1**：每个套间一个电表，按套间分摊
- **V2**：每个房号一个总表 + 每个套间一个空调表，公共用电按房号总人数分摊

### 数据模型
- **新增表**：`room_main_meter_records` - 房号总表记录
- **扩展字段**：`common_degree`（公共用电量）、`common_fee`（公共电费）

### 前端页面
- **删除**：`/meters`（旧版电表管理）
- **保留**：`/meter-input`（电表录入）、`/meters`（现在指向V2版本）

## 迁移步骤

### 1. 数据库迁移

```bash
cd backend

# 执行迁移
alembic upgrade head

# 验证
python -c "
from app.database import engine
from sqlalchemy import inspect
inspector = inspect(engine)
print('✓ 迁移成功' if 'room_main_meter_records' in inspector.get_table_names() else '✗ 迁移失败')
"
```

### 2. 初始化历史数据（可选）

如果需要将V1的历史数据转换为V2格式：

```python
# 脚本：scripts/migrate_v1_to_v2.py
from app.database import SessionLocal
from app.models import MeterRecord, Room
from app.models.room_main_meter import RoomMainMeterRecord
from sqlalchemy import and_
from datetime import date

db = SessionLocal()

# 按房号聚合V1电表数据
months = db.query(MeterRecord.month).distinct().all()

for (month,) in months:
    # 查询该月所有电表
    meters = db.query(MeterRecord).filter(MeterRecord.month == month).all()
    
    # 按房号分组
    room_groups = {}
    for meter in meters:
        room = db.query(Room).filter(Room.id == meter.room_id).first()
        if not room:
            continue
        
        key = (room.building_id, room.room_no)
        if key not in room_groups:
            room_groups[key] = []
        room_groups[key].append(meter)
    
    # 为每个房号创建总表记录
    for (building_id, room_no), meters_in_room in room_groups.items():
        # 计算总用电（假设V1时期总表=各套间之和）
        total_degree = sum(float(m.total_degree) for m in meters_in_room)
        total_fee = sum(float(m.electricity_fee + m.ac_electricity_fee) for m in meters_in_room)
        
        # 创建总表记录
        main_meter = RoomMainMeterRecord(
            building_id=building_id,
            room_no=room_no,
            month=month,
            meter_no=f"M-{room_no}",
            previous_reading=0,  # 历史数据可能无法追溯
            current_reading=total_degree,
            total_degree=total_degree,
            total_fee=total_fee,
            common_degree=0,  # 历史数据无公共用电概念
            common_fee=0,
            status="migrated",
            remark="从V1迁移"
        )
        db.add(main_meter)

db.commit()
print("✓ V1数据迁移完成")
```

### 3. 更新前端依赖

```bash
cd frontend

# 清理旧的构建缓存
rm -rf node_modules/.vite

# 重新构建
npm run build
```

### 4. 测试新系统

```bash
# 运行测试脚本
python test_v2_refactor.py

# 预期输出：
# ✓ 通过 - 初始化月度电表
# ✓ 通过 - 批量更新电表
# ✓ 通过 - 增强计算
# ✓ 通过 - 查询增强列表
# ✓ 通过 - 生成结算
```

### 5. 切换结算服务到V2

在 `backend/app/routers/settlements.py` 中：

```python
# 旧版调用
result = generate_settlement(db, month, use_v2=False)

# 新版调用（推荐）
result = generate_settlement(db, month, use_v2=True)
```

### 6. 前端访问新页面

- **电表录入**：http://localhost:5173/meter-input
- **电表查询**：http://localhost:5173/meters（现在指向V2）

## V1与V2对比

| 功能 | V1（旧版） | V2（新版） |
|-----|----------|----------|
| 数据结构 | 单表（meter_records） | 双表（总表+空调表） |
| 录入方式 | 逐个套间录入 | 按房号批量录入 |
| 计算逻辑 | 按套间分摊 | 公共用电按房号分摊 |
| 电费组成 | 普通电费 + 空调电费 | 公共电费 + 空调电费 |
| 前端页面 | MeterManage.vue | MeterInput.vue + MeterManageV2.vue |
| API前缀 | /meters | /meters-v2 |

## 兼容性说明

### 保留的V1组件
- ✅ `backend/app/routers/meters.py` - 标记为废弃，保留API兼容
- ✅ `backend/app/services/electricity_service.py` - 保留V1计算逻辑
- ✅ 结算服务的 `use_v2` 参数 - 支持切换V1/V2

### 删除的V1组件
- ❌ `frontend/src/views/MeterManage.vue` - 旧版前端页面
- ❌ 路由 `/meters-v2` - 合并到 `/meters`

### 如何回滚到V1

如果发现V2有问题，可以临时回滚：

```python
# backend/app/routers/settlements.py
def generate(month: str, db: Session = Depends(get_db)):
    # 临时回滚到V1
    result = generate_settlement(db, parse_month(month), use_v2=False)
    return result
```

前端回滚：
```bash
git checkout HEAD~1 frontend/src/router/index.ts
git checkout HEAD~1 frontend/src/views/MeterManage.vue
```

## 常见问题

### Q: 历史数据会丢失吗？
**A**: 不会。V1的 `meter_records` 表完整保留，V2只是新增了 `room_main_meter_records` 表。

### Q: 已经生成的结算会受影响吗？
**A**: 不会。已锁定的结算记录不会被重新计算。

### Q: 可以同时使用V1和V2吗？
**A**: 可以。通过 `use_v2` 参数控制，但建议统一使用V2。

### Q: 什么时候可以完全删除V1代码？
**A**: 建议V2稳定运行3-6个月后，再彻底清理V1代码。

### Q: V2的公共用电为负值怎么办？
**A**: 说明总表读数小于空调表总和，需要检查：
1. 总表读数是否录入错误
2. 空调表是否有重复录入
3. 表计是否故障

## 技术支持

如遇到迁移问题，请：
1. 查看 `docs/V2_REFACTOR_GUIDE.md` 了解详细设计
2. 运行 `test_v2_refactor.py` 进行诊断
3. 检查后端日志 `backend/logs/app.log`

---

**迁移状态**：✅ V2已部署，V1标记为废弃  
**更新时间**：2026-09-13  
**负责人**：开发团队
