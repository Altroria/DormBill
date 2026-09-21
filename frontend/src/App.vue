<template>
  <el-container class="app-container">
    <app-header />
    <el-container class="main-container">
      <el-aside width="220px" class="sidebar">
        <el-menu
          :default-active="activeMenu"
          :router="true"
          class="sidebar-menu"
        >
          <el-menu-item index="/dashboard">
            <el-icon><House /></el-icon>
            <span>首页</span>
          </el-menu-item>
          
          <el-sub-menu index="/dormitory">
            <template #title>
              <el-icon><OfficeBuilding /></el-icon>
              <span>宿舍管理</span>
            </template>
            <el-menu-item index="/dormitory/buildings">
              <el-icon><Grid /></el-icon>
              <span>楼栋管理</span>
            </el-menu-item>
            <el-menu-item index="/dormitory/rooms">
              <el-icon><Key /></el-icon>
              <span>房间管理</span>
            </el-menu-item>
            <el-menu-item index="/dormitory/residents">
              <el-icon><User /></el-icon>
              <span>入住管理</span>
            </el-menu-item>
          </el-sub-menu>
          
          <el-menu-item index="/employees">
            <el-icon><User /></el-icon>
            <span>员工管理</span>
          </el-menu-item>
          
          <el-menu-item index="/meters">
            <el-icon><Histogram /></el-icon>
            <span>电表管理</span>
          </el-menu-item>
          
          <el-menu-item index="/water">
            <el-icon><Drizzling /></el-icon>
            <span>水费管理</span>
          </el-menu-item>
          
          <el-menu-item index="/settlements">
            <el-icon><Coin /></el-icon>
            <span>结算管理</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      
      <el-main class="main-content">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <keep-alive>
              <component :is="Component" />
            </keep-alive>
          </transition>
        </router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import AppHeader from '@/components/AppHeader.vue';

const route = useRoute();

const activeMenu = computed(() => {
  return route.path;
});
</script>

<style scoped lang="scss">
.app-container {
  height: 100vh;
  flex-direction: column;
}

.main-container {
  flex: 1;
  overflow: hidden;
}

.sidebar {
  background-color: #ffffff;
  border-right: 1px solid #E2E8F0;
  overflow-y: auto;
  
  .sidebar-menu {
    height: 100%;
    padding: 12px 0;
    
    .el-menu-item,
    :deep(.el-sub-menu__title) {
      height: 48px;
      line-height: 48px;
      padding-left: 20px !important;
      
      .el-icon {
        margin-right: 10px;
        font-size: 18px;
      }
    }
    
    .el-sub-menu {
      .el-menu-item {
        padding-left: 48px !important;
        min-width: 0;
      }
    }
  }
}

.main-content {
  background-color: #F8FAFC;
  padding: 20px;
  overflow-y: auto;
}

// 路由过渡动画
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
