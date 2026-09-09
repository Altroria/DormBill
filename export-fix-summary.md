# Excel 导出功能修复总结

## 问题描述

导出 Excel 文件时出现 500 内部服务器错误:
```
UnicodeEncodeError: 'latin-1' codec can't encode characters in position 22-25: ordinal not in range(256)
```

**原因**: HTTP 响应头的 `Content-Disposition` 中的 filename 包含中文字符,但 HTTP header 默认只支持 latin-1 编码(ASCII 字符集),无法处理中文。

## 影响范围

所有导出功能都受到影响:
- `/api/export/settlement` - 导出员工扣款表
- `/api/export/meter-detail` - 导出房间电费明细
- `/api/export/water-detail` - 导出水费分摊明细

## 修复方案

### 修改文件: `backend/app/routers/export.py`

#### 1. 添加 URL 编码导入
```python
from urllib.parse import quote
```

#### 2. 修复所有导出接口的文件名处理

**修复前**:
```python
filename = f"扣款表_{month}.xlsx"
return StreamingResponse(
    BytesIO(bio),
    media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    headers={"Content-Disposition": f'attachment; filename="{filename}"'},
)
```

**修复后**:
```python
filename = f"扣款表_{month}.xlsx"
encoded_filename = quote(filename)
return StreamingResponse(
    BytesIO(bio),
    media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    headers={"Content-Disposition": f'attachment; filename*=UTF-8\'\'{encoded_filename}'},
)
```

### 关键改动

1. 使用 `urllib.parse.quote()` 对文件名进行 URL 编码
2. 使用 `filename*=UTF-8''` 格式代替 `filename=`(符合 RFC 2231 标准)
3. 适用于所有三个导出接口

## 技术说明

- `filename*` 是 RFC 2231 定义的扩展格式,支持非 ASCII 字符
- `UTF-8''` 表示使用 UTF-8 编码,没有语言标签
- `quote()` 函数将中文字符转换为 URL 编码格式(如 `%E6%89%A3%E6%AC%BE%E8%A1%A8`)

## 测试结果

✅ 所有导出接口现在可以正常工作
✅ 下载的文件名正确显示中文
✅ Excel 文件内容正常

## 修复时间

2026-09-09 20:05

## 相关文件

- `backend/app/routers/export.py` - 主修复文件
