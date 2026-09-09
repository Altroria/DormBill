# 修复标签页切换不调用接口的问题

## 问题描述
在前端系统中切换标签页(tab)时,页面不会重新调用后端API接口,导致数据不刷新。

## 问题原因
Vue Router 的 `<router-view>` 组件默认会复用已经挂载过的组件实例。当用户在已访问过的页面之间切换时:
- 组件不会被重新创建
- `onMounted` 生命周期钩子不会再次触发
- 因此不会重新调用API接口

## 解决方案
使用 Vue 3 的 `<KeepAlive>` 组件配合 `onActivated` 生命周期钩子:

### 1. 在 App.vue 中添加 `<KeepAlive>`
```vue
<router-view v-slot="{ Component }">
  <transition name="fade" mode="out-in">
    <keep-alive>
      <component :is="Component" />
    </keep-alive>
  </transition>
</router-view>
```

### 2. 在各个页面组件中添加 `onActivated` 钩子
```typescript
import { onMounted, onActivated } from 'vue'

// 首次加载时调用
onMounted(() => {
  fetchBuildings()
  fetchData()
})

// 每次组件激活时调用(包括首次)
onActivated(() => {
  fetchData()
})
```

## 已修复的页面
✅ App.vue - 添加了 `<KeepAlive>` 包裹
✅ MeterManage.vue - 电表管理
✅ EmployeeManage.vue - 员工管理
✅ BuildingList.vue - 楼栋管理
✅ RoomList.vue - 房间管理
✅ ResidentList.vue - 入住管理
✅ WaterManage.vue - 水费管理
✅ Settlement.vue - 结算管理
✅ Dashboard.vue - 首页仪表板

## 效果
- ✅ 切换标签页时会重新调用API获取最新数据
- ✅ 组件状态和滚动位置会被保留
- ✅ 页面切换更加流畅
- ✅ 用户体验更好

## 注意事项
1. `onActivated` 只在使用 `<KeepAlive>` 时才会触发
2. `onActivated` 会在组件首次挂载和每次激活时都调用
3. 不需要在 `onActivated` 中重新获取静态数据(如下拉列表选项),只需刷新主要数据即可
