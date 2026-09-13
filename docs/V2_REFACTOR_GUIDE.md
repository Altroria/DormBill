# 电表管理V2重构使用指南

## 📋 概述

本次重构优化了电表管理系统，实现了**总表与空调表分离**的业务架构，并提供了**公共用电自动计算**和**一键批量录入**功能。

### 核心改进

1. **数据结构优化**
   - 新增 `common_degree` 和 `common_fee` 字段到总表
   - 清晰区分房号总表和套间空调表

2. **计算逻辑重构**
   - 公共用电 = 总表用电 - 空调用电（自动计算）
   - 公共电费按房号总人数分摊
   - 空调电费按套间人数分摊

3. **UI交互优化**
   - 折叠面板布局，按房号组织
   - 批量保存，减少网络请求
   - 实时计算预览

4. **API增强**
   - 批量更新接口
   - 增强计算接口
   - 增强查询接口（含统计信息）

---

## 🏗️ 架构说明

### 数据流

```
总表录入 → 空调表录入 → 批量保存 → 增强计算 → 生成结算
   ↓           ↓            ↓           ↓           ↓
房号级别    套间级别    API请求    公共用电     个人扣款
```

### 核心公式

```
公共用电量 = 总表用电量 - Σ(所有套间空调用电量)
公共电费 = 总表电费 - Σ(所有套间空调电费)

个人总电费 = 公共电费分摊 + 空调电费分摊

其中：
  公共电费分摊 = 公共电费 ÷ 房号内总人数
  空调电费分摊 = 套间空调电费 ÷ 套间内人数
```

### 示例计算

**201房号**：4个套间，6人入住

```
总表：1000度，490元

空调表：
  - 201-1：100度，49元（2人）
  - 201-2：150度，73.5元（1人）
  - 201-3：120度，58.8元（2人）
  - 201-4：80度，39.2元（1人）

计算过程：
1. 总空调用电 = 100+150+120+80 = 450度
2. 公共用电 = 1000-450 = 550度
3. 公共电费 = 490-(49+73.5+58.8+39.2) = 269.5元
4. 公共电费分摊 = 269.5÷6 = 44.92元/人（尾差处理）
5. 空调费分摊：
   - 201-1：49÷2 = 24.5元/人
   - 201-2：73.5÷1 = 73.5元/人
   - 201-3：58.8÷2 = 29.4元/人
   - 201-4：39.2÷1 = 39.2元/人

个人总电费 = 公共电费分摊 + 空调费分摊
```

---

## 🔧 数据库迁移

### 执行迁移

```bash
cd backend

# 查看待执行的迁移
alembic history

# 执行迁移（添加公共用电字段）
alembic upgrade head

# 验证字段是否添加成功
python -c "
from app.database import engine
from sqlalchemy import inspect
inspector = inspect(engine)
columns = [c['name'] for c in inspector.get_columns('room_main_meter_records')]
print('✓ common_degree' if 'common_degree' in columns else '✗ common_degree 缺失')
print('✓ common_fee' if 'common_fee' in columns else '✗ common_fee 缺失')
"
```

### 迁移内容

文件：`backend/alembic/versions/add_common_electricity_fields.py`

```python
# 添加字段
- common_degree: Numeric(12, 2) - 公共用电量
- common_fee: Numeric(12, 2) - 公共电费
```

---

## 🚀 API使用说明

### 1. 初始化月度电表

**端点**：`POST /api/v1/meters-v2/init-month`

```json
{
  "month": "2026-09",
  "building_id": 1
}
```

**响应**：
```json
{
  "main_meters_created": 20,
  "ac_meters_created": 80,
  "message": "初始化成功"
}
```

### 2. 批量更新电表（推荐）

**端点**：`PUT /api/v1/meters-v2/batch-update`

```json
{
  "month": "2026-09",
  "updates": [
    {
      "building_id": 1,
      "room_no": "201",
      "main_current_reading": 15000.5,
      "main_meter_no": "M-201",
      "ac_meters": [
        { "room_id": 1, "ac_current_reading": 1200.0 },
        { "room_id": 2, "ac_current_reading": 1350.0 }
      ]
    }
  ]
}
```

**响应**：
```json
{
  "main_meters_updated": 1,
  "ac_meters_updated": 2,
  "message": "成功更新 1 个房号总表和 2 个空调表"
}
```

### 3. 增强计算（包含公共用电和个人分摊）

**端点**：`POST /api/v1/meters-v2/calculate-enhanced`

```json
{
  "month": "2026-09",
  "building_id": 1,
  "calculate_distribution": true
}
```

**响应**：
```json
{
  "main_meters_calculated": 20,
  "ac_meters_calculated": 80,
  "distributions_created": 120,
  "total_common_fee": 5400.50,
  "total_ac_fee": 3200.00,
  "warnings": []
}
```

### 4. 查询增强列表

**端点**：`GET /api/v1/meters-v2/list-enhanced?month=2026-09&building_id=1`

**响应**：
```json
{
  "items": [
    {
      "building_id": 1,
      "building_no": "247",
      "room_no": "201",
      "month": "2026-09-01",
      "main_total_degree": 1000.0,
      "main_total_fee": 490.0,
      "common_degree": 550.0,
      "common_fee": 269.5,
      "total_ac_degree": 450.0,
      "total_ac_fee": 220.5,
      "ac_meters": [
        {
          "room_id": 1,
          "room_unit": "1",
          "ac_degree": 100.0,
          "ac_fee": 49.0,
          "occupants": 2
        }
      ],
      "total_occupants": 6,
      "common_fee_per_person": 44.92,
      "status": "calculated"
    }
  ],
  "total": 20
}
```

---

## 💻 前端使用指南

### 电表录入页面

路由：`/meter-input`

#### 功能特点

1. **按房号折叠面板**
   - 一个房号展示总表 + 所有空调表
   - 默认展开有变更的房号

2. **实时计算**
   - 输入本月读数后自动计算用电量
   - 自动计算电费（按0.49元/度）

3. **批量保存**
   - 一次性提交所有变更
   - 减少网络请求，提升效率

4. **计算结果预览**
   - 显示公共用电和公共电费
   - 显示人均公共电费
   - 显示套间空调费用

#### 操作流程

```
1. 选择月份和楼栋 → 加载数据
   ↓
2. 展开房号折叠面板
   ↓
3. 录入总表本月读数（自动计算用电量和费用）
   ↓
4. 录入各套间空调表读数（自动计算）
   ↓
5. 点击"批量保存"（保存所有变更）
   ↓
6. 点击"计算电费"（执行增强计算）
   ↓
7. 查看公共用电和分摊结果
```

### 电表查询页面

路由：`/meters-v2`

#### 功能特点

1. **增强查询**
   - 显示公共用电统计
   - 显示人均费用
   - 显示套间详情

2. **数据导出**
   - 导出完整电费明细
   - 包含公共用电和空调用电

---

## 🔄 与结算服务集成

### 结算生成

```python
# backend/app/services/settlement_service.py

def generate_settlement(db, target_month, use_v2=True):
    """
    生成月度结算
    
    Args:
        use_v2: True - 使用V2架构（总表-空调表分离）
                False - 使用V1架构（旧逻辑）
    """
    if use_v2:
        # 从ElectricityCalculationService获取分摊结果
        calc_service = ElectricityCalculationService(db)
        distributions = calc_service.calculate_room_electricity(...)
        
        # 公共电费作为普通电费
        electricity_fee = distribution['common_electricity_fee']
        # 空调费单独
        ac_electricity_fee = distribution['ac_electricity_fee']
    else:
        # 使用旧的distribute_electricity_fee
        ...
```

### 调用方式

```bash
# API调用
POST /api/v1/settlements/generate
{
  "month": "2026-09",
  "use_v2": true
}
```

---

## 🧪 测试

### 运行单元测试

```bash
cd backend

# 测试电费计算逻辑
pytest tests/test_electricity_calculation.py -v

# 测试完整工作流
python ../test_v2_refactor.py
```

### 测试覆盖

- ✅ 公共用电计算
- ✅ 公共电费计算
- ✅ 尾差处理
- ✅ 个人分摊
- ✅ 异常情况（公共用电为负值）
- ✅ 边界情况（单人、零费用、大量人数）

---

## 📊 性能优化

### 批量操作

- 使用 `batch-update` 一次性提交多个房号
- 使用 `calculate-enhanced` 一次性计算所有电费
- 减少数据库查询次数

### 查询优化

- 使用联表查询减少往返次数
- 增加索引：`(building_id, room_no, month)`
- 分页查询避免大数据量

---

## ⚠️ 注意事项

### 数据一致性

1. **总表与空调表关系**
   - 确保房号下所有套间的空调表都已录入
   - 公共用电不应为负值

2. **入住人数同步**
   - 计算前确保入住记录已更新
   - 出差/搬离状态及时维护

3. **月度锁定**
   - 已锁定月份不允许修改电表
   - 需先解锁才能重新计算

### 异常处理

```python
# 检测公共用电异常
if common_degree < 0:
    warnings.append({
        "room_no": room_no,
        "issue": "公共用电为负值",
        "common_degree": common_degree,
        "suggestion": "请检查总表或空调表读数是否录入错误"
    })
```

### 兼容性

- V1和V2可以并存
- 结算生成时通过 `use_v2` 参数选择
- 建议逐步迁移到V2架构

---

## 🎯 最佳实践

### 录入顺序

1. 先录入总表
2. 再录入所有空调表
3. 批量保存
4. 执行计算
5. 检查异常

### 数据校验

```python
# 录入后校验
1. 总表用电量 > 空调表用电量总和
2. 公共用电量在合理范围（50%-80%总用电）
3. 人均公共电费在合理范围
```

### 定期维护

- 每月初执行 `init-month`
- 月中完成电表录入
- 月末执行计算和结算
- 月底前锁定

---

## 📞 问题排查

### 问题1：公共用电为负值

**原因**：空调表用电大于总表用电

**解决**：
1. 检查总表读数是否录入错误
2. 检查空调表是否有重复录入
3. 检查表计是否故障

### 问题2：人均费用异常高

**原因**：入住人数统计错误

**解决**：
1. 检查入住记录状态
2. 确认搬离日期是否正确
3. 检查是否有未关闭的试用期

### 问题3：批量保存失败

**原因**：数据验证失败或网络超时

**解决**：
1. 检查必填字段是否完整
2. 分批次提交（每次10个房号）
3. 检查后端日志

---

## 📈 未来规划

- [ ] 电费趋势分析图表
- [ ] 房号级别用电对比
- [ ] 异常用电预警
- [ ] 移动端录入支持
- [ ] 语音录入功能

---

## 📚 相关文档

- [README.md](../README.md) - 项目整体说明
- [API文档](../backend/README.md) - 完整API参考
- [数据库设计](./DATABASE_SCHEMA.md) - 数据库表结构

---

**版本**：V2.0  
**更新时间**：2026-09-13  
**维护者**：开发团队
