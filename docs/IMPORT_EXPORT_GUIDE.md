# 电费水费导入导出功能使用指南

## 功能概述

系统提供了电费和水费的Excel导入导出功能，方便批量录入表计数据。

### 主要功能
1. **导出模板**：导出包含现有房间信息的Excel模板
2. **填写数据**：在Excel中填写表计读数或费用
3. **导入系统**：将填写完的Excel文件导入系统

---

## 电费管理

### 1. 导出电费导入模板

**API接口**
```
GET /api/meters-v2/export-template?month=YYYY-MM&building_id=1
```

**参数说明**
- `month`: 必填，月份（格式：YYYY-MM，例如：2024-09）
- `building_id`: 可选，楼栋ID（不传则导出所有楼栋）

**返回结果**
- Excel文件（.xlsx格式）
- 文件名：`电费导入模板_YYYY-MM.xlsx`

**模板内容**
| 列名 | 说明 | 是否必填 |
|------|------|----------|
| 楼栋ID | 楼栋编号（系统自动填充） | 是 |
| 楼栋 | 楼栋名称 | 否 |
| 房号 | 房间号码（系统自动填充） | 是 |
| 总表表号 | 总电表编号 | 否 |
| 总表上月读数 | 上月抄表数（系统自动填充） | 否 |
| **总表当前读数** | **本月抄表数（需要填写）** | **是** |
| 房间ID | 套间编号（系统自动填充） | 是 |
| 室号 | 套间编号 | 否 |
| 房间名称 | 套间名称 | 否 |
| 空调表号 | 空调电表编号 | 否 |
| 空调上月读数 | 上月空调表读数（系统自动填充） | 否 |
| **空调当前读数** | **本月空调表读数（需要填写）** | **是** |
| 备注 | 其他说明 | 否 |

### 2. 填写电费数据

1. 打开下载的Excel模板
2. 找到"总表当前读数"列，填写本月总电表读数
3. 找到"空调当前读数"列，填写本月空调表读数
4. 如需添加备注，在"备注"列填写
5. 保存文件

**注意事项**
- ⚠️ 不要修改楼栋ID、房号、房间ID等系统填充的列
- ⚠️ 当前读数必须大于或等于上月读数
- ⚠️ 如果某个房间没有空调表，空调当前读数列留空即可
- 📝 一个房号可能包含多个套间，每个套间有自己的空调表

### 3. 导入电费数据

**API接口**
```
POST /api/meters-v2/import-excel?month=YYYY-MM
Content-Type: multipart/form-data

file: <Excel文件>
```

**参数说明**
- `month`: 必填，月份（格式：YYYY-MM）
- `file`: 必填，填写好的Excel文件

**返回示例**
```json
{
  "message": "导入完成：总表 15 条，空调表 45 条",
  "main_meters_imported": 15,
  "ac_meters_imported": 45,
  "parse_errors": [],
  "import_errors": []
}
```

**错误处理**
- `parse_errors`: Excel解析错误（格式不正确）
- `import_errors`: 数据导入错误（如房间不存在、读数异常等）

---

## 水费管理

### 1. 导出水费导入模板

**API接口**
```
GET /api/water-meters-v2/export-template?month=YYYY-MM&building_id=1
```

**参数说明**
- `month`: 必填，月份（格式：YYYY-MM）
- `building_id`: 可选，楼栋ID

**返回结果**
- Excel文件（.xlsx格式）
- 文件名：`水费导入模板_YYYY-MM.xlsx`

**模板内容**
| 列名 | 说明 | 是否必填 |
|------|------|----------|
| 楼栋ID | 楼栋编号（系统自动填充） | 是 |
| 楼栋 | 楼栋名称 | 否 |
| 房号 | 房间号码（系统自动填充） | 是 |
| 房间名称 | 房间名称 | 否 |
| **水费金额** | **本月水费（需要填写）** | **是** |
| 备注 | 其他说明 | 否 |

### 2. 填写水费数据

1. 打开下载的Excel模板
2. 找到"水费金额"列，填写本月水费金额（单位：元）
3. 如需添加备注，在"备注"列填写
4. 保存文件

**注意事项**
- ⚠️ 不要修改楼栋ID、房号等系统填充的列
- 💰 水费金额为数字，保留两位小数
- 📝 水费按房号收取（一个房号包含多个套间）

### 3. 导入水费数据

**API接口**
```
POST /api/water-meters-v2/import-excel?month=YYYY-MM
Content-Type: multipart/form-data

file: <Excel文件>
```

**参数说明**
- `month`: 必填，月份（格式：YYYY-MM）
- `file`: 必填，填写好的Excel文件

**返回示例**
```json
{
  "message": "导入完成：成功 15 条",
  "imported": 15,
  "parse_errors": [],
  "import_errors": []
}
```

---

## 前端集成示例

### 电费导入导出

```typescript
import { meterV2Api } from '@/api/meter_v2'

// 导出模板
const exportElectricityTemplate = () => {
  const url = meterV2Api.exportTemplate({
    month: '2024-09',
    building_id: 1
  })
  window.open(url, '_blank')
}

// 导入数据
const importElectricityData = async (file: File) => {
  try {
    const result = await meterV2Api.importExcel('2024-09', file)
    console.log('导入成功', result)
    
    if (result.parse_errors.length > 0) {
      console.warn('解析错误', result.parse_errors)
    }
    
    if (result.import_errors.length > 0) {
      console.warn('导入错误', result.import_errors)
    }
  } catch (error) {
    console.error('导入失败', error)
  }
}
```

### 水费导入导出

```typescript
import { waterMeterV2Api } from '@/api/water_meter_v2'

// 导出模板
const exportWaterTemplate = () => {
  const url = waterMeterV2Api.exportTemplate({
    month: '2024-09',
    building_id: 1
  })
  window.open(url, '_blank')
}

// 导入数据
const importWaterData = async (file: File) => {
  try {
    const result = await waterMeterV2Api.importExcel('2024-09', file)
    console.log('导入成功', result)
    
    if (result.parse_errors.length > 0) {
      console.warn('解析错误', result.parse_errors)
    }
    
    if (result.import_errors.length > 0) {
      console.warn('导入错误', result.import_errors)
    }
  } catch (error) {
    console.error('导入失败', error)
  }
}
```

---

## 常见问题

### Q1: 导出的模板是空的？
**A:** 请确保已经初始化了该月份的电表/水表记录。使用 `POST /meters-v2/init-month` 或 `POST /water-meters-v2/init-month` 接口初始化。

### Q2: 导入时提示"房间不存在"？
**A:** 请不要修改模板中的楼栋ID、房号、房间ID等关键字段，这些字段用于定位数据。

### Q3: 导入后数据没有变化？
**A:** 检查返回的错误信息，可能是数据格式不正确或读数异常（如当前读数小于上月读数）。

### Q4: 能否只填写部分房间的数据？
**A:** 可以。未填写的行将被跳过，不会影响其他数据。

### Q5: 导入会覆盖已有数据吗？
**A:** 会。导入的数据会更新对应房间的表计读数。

---

## 数据流程图

```
┌─────────────┐
│  初始化月份   │
│ init-month  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  导出模板     │
│export-template│
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  填写Excel   │
│  (人工操作)  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  导入数据     │
│import-excel │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  计算费用     │
│  calculate  │
└─────────────┘
```

---

## 技术实现

### 后端技术栈
- **Excel处理**: openpyxl
- **数据验证**: Pydantic
- **文件上传**: FastAPI UploadFile
- **流式下载**: StreamingResponse

### 模板样式
- 表头：蓝色背景 (#6366F1)，白色文字，加粗
- 边框：浅灰色细线 (#E2E8F0)
- 列宽：自动调整（10-30字符）
- 字体：Microsoft YaHei

### 数据校验
- 楼栋ID、房号、房间ID必填
- 当前读数必须为数字
- 电费读数不能小于上月读数
- 水费金额必须为正数

---

## 更新日志

### v1.0.0 (2024-09)
- ✨ 新增电费导入导出功能
- ✨ 新增水费导入导出功能
- 📝 提供包含现有房间信息的模板
- 🔍 支持按楼栋筛选导出
- ⚡ 批量导入优化
