# 前端错误修复总结

## 修复时间
2026-09-09 19:50

## 修复的问题

### 1. ✅ 标签页切换不调用接口
**问题**: 在已访问过的页面之间切换时,不会重新调用API获取最新数据

**解决方案**:
- 在 `App.vue` 中添加 `<KeepAlive>` 组件
- 在所有页面组件中添加 `onActivated` 生命周期钩子

**已修复文件**:
- App.vue
- MeterManage.vue
- EmployeeManage.vue
- BuildingList.vue
- RoomList.vue
- ResidentList.vue
- WaterManage.vue
- Settlement.vue
- Dashboard.vue

---

### 2. ✅ 类型错误: toFixed is not a function
**问题**: 后端返回的数字字段可能为 null 或字符串类型,直接调用 `.toFixed()` 方法会报错

**错误示例**:
```
TypeError: row.electricity_price.toFixed is not a function
```

**解决方案**: 添加空值检查和类型转换

**修复前**:
```vue
¥{{ row.electricity_price.toFixed(2) }}
```

**修复后**:
```vue
¥{{ row.electricity_price ? Number(row.electricity_price).toFixed(2) : '0.00' }}
```

或者:
```vue
¥{{ (row.electricity_price || 0).toFixed(2) }}
```

**已修复文件及字段**:

**RoomList.vue**:
- `electricity_price` - 默认电价
- `rent_standard` - 房租标准

**Settlement.vue**:
- `rent_should` - 应住房租
- `rent_actual` - 实扣房租
- `electricity_fee` - 普通电费
- `ac_electricity_fee` - 空调电费
- `water_fee` - 水费
- `deduction_minus` - 补扣-
- `deduction_plus` - 补扣+
- `total_amount` - 最终扣款

**WaterManage.vue**:
- `total_amount` - 水费金额

---

### 3. ✅ 路由导航守卫弃用警告
**问题**: Vue Router 提示使用了已弃用的 `next()` 回调方式

**警告信息**:
```
[VUE_ROUTER_R0025] The `next()` callback in navigation guards is deprecated.
```

**解决方案**: 移除 `next` 参数,直接返回布尔值

**修复前**:
```typescript
router.beforeEach((to, _from, next) => {
  const title = to.meta.title as string;
  if (title) {
    document.title = `${title} - 蓉蓉的收租小工具`;
  }
  next();
});
```

**修复后**:
```typescript
router.beforeEach((to, _from) => {
  const title = to.meta.title as string;
  if (title) {
    document.title = `${title} - 蓉蓉的收租小工具`;
  }
  return true;
});
```

**已修复文件**:
- `frontend/src/router/index.ts`

---

## 验证结果

✅ 前端服务已成功重启
✅ Vite 热更新已生效
✅ 所有修复已应用

## 注意事项

1. **数字类型处理**: 所有从后端接收的数字字段在使用 `.toFixed()` 前都应该做类型检查
2. **空值处理**: 使用 `|| 0` 或三元运算符确保有默认值
3. **类型转换**: 如果后端返回字符串数字,使用 `Number()` 转换

## 后续建议

1. 考虑在后端统一返回数字类型而不是字符串
2. 在前端使用 TypeScript 接口定义明确的数据类型
3. 添加全局的数字格式化辅助函数,统一处理这类场景
