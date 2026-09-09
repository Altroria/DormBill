<template>
  <div class="app-header">
    <div class="header-left">
      <el-icon class="home-icon" :size="24">
        <HomeFilled />
      </el-icon>
      <h1 class="title">蓉蓉的收租小工具</h1>
    </div>
    <div class="header-right">
      <el-tag type="info" effect="plain">
        <el-icon :size="14"><Calendar /></el-icon>
        <span class="current-date">{{ currentMonth }}</span>
      </el-tag>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { HomeFilled, Calendar } from '@element-plus/icons-vue';
import dayjs from 'dayjs';

// 当前月份显示
const currentMonth = computed(() => {
  return dayjs().format('YYYY年MM月');
});
</script>

<style scoped lang="scss">
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 60px;
  padding: 0 24px;
  background-color: #ffffff;
  box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
  position: relative;
  
  &::after {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 4px;
    background: linear-gradient(180deg, #6366F1 0%, #818CF8 100%);
  }
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
  
  .home-icon {
    color: #6366F1;
  }
  
  .title {
    font-size: 1.25rem;
    font-weight: 600;
    color: #1E293B;
    margin: 0;
  }
}

.header-right {
  display: flex;
  align-items: center;
  
  .el-tag {
    padding: 6px 12px;
    font-size: 0.875rem;
    
    .el-icon {
      margin-right: 6px;
    }
    
    .current-date {
      font-weight: 500;
    }
  }
}
</style>
