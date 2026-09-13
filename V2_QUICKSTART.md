# 电表管理V2快速上手指南

## ✅ 已完成的更改

### 前端变化
- ✅ **删除**：旧版电表管理页面（`MeterManage.vue`）
- ✅ **合并路由**：`/meters` 现在直接指向V2版本
- ✅ **新增页面**：`/meter-input` 电表批量录入页面
- ✅ **保留页面**：`/meters` 电表查询管理（V2增强版）

### 后端变化
- ✅ **标记废弃**：`/api/v1/meters` 路由（保留兼容）
- ✅ **推荐使用**：`/api/v1/meters-v2` 路由
- ✅ **结算集成**：`use_v2=True` 默认使用V2计算逻辑

---

## 🎯 V2核心功能

### 业务架构
```
房号201（总表）
├── 套间201-1（空调表，2人）
├── 套间201-2（空调表，1人）
├── 套间201-3（空调表，2人）
└── 套间201-4（空调表，1人）

总用电 - 空调用电 = 公共用电
公共电费 ÷ 6人 = 人均公共电费
```

### 数据流程
```
1. 初始化月度电表
   ↓
2. 录入总表和空调表读数（批量录入页面）
   ↓
3. 批量保存（一次提交）
   ↓
4. 计算电费（自动计算公共用电）
   ↓
5. 查看结果（公共用电、人均费用）
   ↓
6. 生成结算（集成到月度扣款）
```

---

## 🚀 快速开始

### 第一次使用V2

#### 1. 数据库迁移
```bash
cd backend
alembic upgrade head
```

**验证迁移**：
```bash
python -c "
from app.database import engine
from sqlalchemy import inspect
inspector = inspect(engine)
cols = [c['name'] for c in inspector.get_columns('room_main_meter_records')]
print('✓ 迁移成功' if 'common_degree' in cols and 'common_fee' in cols else '✗ 迁移失败')
"
```

#### 2. 初始化本月电表
```bash
# 访问前端
http://localhost:5173/meter-input

# 或通过API
curl -X POST "http://localhost:8000/api/v1/meters-v2/init-month" \
  -H "Content-Type: application/json" \
  -d '{"month": "2026-09", "building_id": 1}'
```

#### 3. 录入电表读数

**方式1：前端录入（推荐）**
1. 访问 `/meter-input`
2. 选择月份和楼栋
3. 点击"加载数据"
4. 展开房号，录入总表和空调表读数
5. 点击"批量保存"
6. 点击"计算电费"

**方式2：API调用**
```bash
curl -X PUT "http://localhost:8000/api/v1/meters-v2/batch-update" \
  -H "Content-Type: application/json" \
  -d '{
    "month": "2026-09",
    "updates": [
      {
        "building_id": 1,
        "room_no": "201",
        "main_current_reading": 15000.5,
        "ac_meters": [
          {"room_id": 1, "ac_current_reading": 1200.0},
          {"room_id": 2, "ac_current_reading": 1350.0}
        ]
      }
    ]
  }'
```

#### 4. 计算电费
```bash
curl -X POST "http://localhost:8000/api/v1/meters-v2/calculate-enhanced" \
  -H "Content-Type: application/json" \
  -d '{
    "month": "2026-09",
    "building_id": 1,
    "calculate_distribution": true
  }'
```

#### 5. 查看结果
```bash
# 访问前端
http://localhost:5173/meters

# 或通过API
curl "http://localhost:8000/api/v1/meters-v2/list-enhanced?month=2026-09&building_id=1"
```

---

## 📋 常用操作

### 月度电表录入流程

```
月初（1-3号）
├── 1. 初始化月度电表
│   └── POST /api/v1/meters-v2/init-month
│
月中（15号左右）
├── 2. 批量录入读数
│   ├── 打开 /meter-input
│   ├── 选择月份和楼栋
│   ├── 逐个房号录入总表和空调表
│   └── 批量保存
│
├── 3. 计算电费
│   └── 点击"计算电费"按钮
│
├── 4. 检查结果
│   ├── 查看公共用电是否合理
│   ├── 检查人均费用
│   └── 导出明细（如需）
│
月末（28-30号）
└── 5. 生成结算
    └── 进入"结算管理"生成扣款
```

### 检查公共用电是否合理

**正常范围**：
- 公共用电占比：50%-80%总用电
- 人均公共电费：30-80元/人

**异常情况**：
```
❌ 公共用电为负值
   → 检查：总表读数是否小于空调表总和
   → 原因：录入错误或表计故障

❌ 公共用电占比 < 30%
   → 检查：空调表是否过高
   → 原因：空调使用过度或表计倍率问题

❌ 公共用电占比 > 90%
   → 检查：空调表是否未录入
   → 原因：数据缺失或表计故障
```

---

## 🆚 V1与V2对比

| 功能 | V1（已删除） | V2（当前版本） |
|-----|------------|--------------|
| **数据结构** | 每个套间一个电表 | 房号总表 + 套间空调表 |
| **录入方式** | 逐个套间录入 | 按房号批量录入 |
| **计算逻辑** | 按套间平均分摊 | 公共用电按房号分摊 |
| **电费组成** | 普通电费 + 空调电费 | 公共电费 + 空调电费 |
| **前端页面** | `/meters`（旧版） | `/meter-input` + `/meters` |
| **API路径** | `/api/v1/meters` | `/api/v1/meters-v2` |
| **状态** | ❌ 已废弃 | ✅ 当前使用 |

---

## 🔍 常见问题

### Q1: 旧版页面还能访问吗？
**A**: 前端旧版页面已删除，`/meters` 现在直接指向V2版本。后端API保留兼容，但标记为废弃。

### Q2: 历史数据会受影响吗？
**A**: 不会。旧数据完整保留在 `meter_records` 表中。V2只是新增了 `room_main_meter_records` 表。

### Q3: 如何回滚到V1？
**A**: 
```bash
# 前端
git checkout HEAD~3 frontend/src/router/index.ts
git checkout HEAD~3 frontend/src/views/MeterManage.vue

# 后端（修改结算调用）
use_v2=False  # settlement_service.py
```

### Q4: 公共用电为负值怎么办？
**A**: 
1. 检查总表读数是否正确
2. 检查空调表是否有重复录入
3. 检查表计是否故障或倍率设置错误

### Q5: V2比V1有什么优势？
**A**: 
- ✅ **符合实际业务**：总表-空调表架构更准确
- ✅ **录入更快**：批量录入减少50%点击
- ✅ **计算透明**：公共用电可见，易于验证
- ✅ **数据准确**：公共用电=总表-空调表，物理逻辑正确

### Q6: 需要重新培训吗？
**A**: 基本不需要。新页面更简单：
- 旧版：点击每个房间 → 录入 → 保存 → 重复
- 新版：展开房号 → 录入所有表 → 一次保存

---

## 📚 相关文档

- **完整设计方案**：[docs/V2_REFACTOR_GUIDE.md](docs/V2_REFACTOR_GUIDE.md)
- **迁移指南**：[MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)
- **项目README**：[README.md](README.md)

---

## 📞 技术支持

遇到问题？
1. 检查 `backend/logs/app.log`
2. 运行测试脚本：`python test_v2_refactor.py`
3. 查看API文档：http://localhost:8000/docs

---

**版本**：V2.0  
**更新时间**：2026-09-13  
**状态**：✅ 已部署，旧版已删除
