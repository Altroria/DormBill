import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router';

// 路由配置
const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/dashboard',
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue'),
    meta: {
      title: '首页',
      icon: 'House',
    },
  },
  {
    path: '/dormitory',
    name: 'Dormitory',
    redirect: '/dormitory/buildings',
    meta: {
      title: '宿舍管理',
      icon: 'OfficeBuilding',
    },
    children: [
      {
        path: 'buildings',
        name: 'Buildings',
        component: () => import('@/views/DormitoryManage/BuildingList.vue'),
        meta: {
          title: '楼栋管理',
          icon: 'OfficeBuilding',
        },
      },
      {
        path: 'rooms',
        name: 'Rooms',
        component: () => import('@/views/DormitoryManage/RoomList.vue'),
        meta: {
          title: '房间管理',
          icon: 'Door',
        },
      },
      {
        path: 'residents',
        name: 'Residents',
        component: () => import('@/views/DormitoryManage/ResidentList.vue'),
        meta: {
          title: '入住管理',
          icon: 'User',
        },
      },
    ],
  },
  {
    path: '/employees',
    name: 'Employees',
    component: () => import('@/views/EmployeeManage.vue'),
    meta: {
      title: '员工管理',
      icon: 'User',
    },
  },
  {
    path: '/meters',
    name: 'Meters',
    component: () => import('@/views/MeterManage.vue'),
    meta: {
      title: '电表管理',
      icon: 'Histogram',
    },
  },
  {
    path: '/water',
    name: 'Water',
    component: () => import('@/views/WaterManage.vue'),
    meta: {
      title: '水费管理',
      icon: 'Watermeloner',
    },
  },
  {
    path: '/settlements',
    name: 'Settlements',
    component: () => import('@/views/Settlement.vue'),
    meta: {
      title: '结算管理',
      icon: 'Coin',
    },
  },
];

// 创建路由实例
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

// 路由守卫 - 动态更新页面标题
router.beforeEach((to, _from, next) => {
  const title = to.meta.title as string;
  if (title) {
    document.title = `${title} - 蓉蓉的收租小工具`;
  }
  next();
});

export default router;
