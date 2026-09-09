<template>
  <div class="dormitory-manage-index">
    <el-card class="page-card" shadow="never">
      <!-- 页面头部 -->
      <div class="page-header">
        <div>
          <h2 class="page-title">宿舍管理</h2>
          <p class="page-desc">管理楼栋、房间和入住信息</p>
        </div>
      </div>

      <!-- 统计卡片 -->
      <div class="stats-grid" v-loading="statsLoading">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" style="background-color: rgba(99, 102, 241, 0.1);">
              <el-icon :size="32" style="color: #6366F1;"><OfficeBuilding /></el-icon>
            </div>
            <div class="stat-info">
              <p class="stat-label">楼栋总数</p>
              <p class="stat-value">{{ stats.building_count }}</p>
            </div>
          </div>
        </el-card>

        <el-card shadow="hover" class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" style="background-color: rgba(16, 185, 129, 0.1);">
              <el-icon :size="32" style="color: #10B981;"><House /></el-icon>
            </div>
            <div class="stat-info">
              <p class="stat-label">房间总数</p>
              <p class="stat-value">{{ stats.room_count }}</p>
            </div>
          </div>
        </el-card>

        <el-card shadow="hover" class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" style="background-color: rgba(245, 158, 11, 0.1);">
              <el-icon :size="32" style="color: #F59E0B;"><User /></el-icon>
            </div>
            <div class="stat-info">
              <p class="stat-label">在住人数</p>
              <p class="stat-value">{{ stats.current_residents }}</p>
            </div>
          </div>
        </el-card>

        <el-card shadow="hover" class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" style="background-color: rgba(59, 130, 246, 0.1);">
              <el-icon :size="32" style="color: #3B82F6;"><Avatar /></el-icon>
            </div>
            <div class="stat-info">
              <p class="stat-label">员工总数</p>
              <p class="stat-value">{{ stats.employee_count }}</p>
            </div>
          </div>
        </el-card>
      </div>

      <!-- 功能导航卡片 -->
      <div class="nav-section">
        <h3 class="section-title">功能菜单</h3>
        <div class="nav-cards">
          <el-card shadow="hover" class="nav-card" @click="navigateTo('/dormitory/buildings')">
            <div class="nav-content">
              <div class="nav-icon" style="background-color: rgba(99, 102, 241, 0.1);">
                <el-icon :size="40" style="color: #6366F1;"><OfficeBuilding /></el-icon>
              </div>
              <div class="nav-info">
                <h4>楼栋管理</h4>
                <p>管理楼栋信息、地址和备注</p>
              </div>
              <el-icon class="nav-arrow" :size="20" style="color: #94a3b8;"><ArrowRight /></el-icon>
            </div>
          </el-card>

          <el-card shadow="hover" class="nav-card" @click="navigateTo('/dormitory/rooms')">
            <div class="nav-content">
              <div class="nav-icon" style="background-color: rgba(16, 185, 129, 0.1);">
                <el-icon :size="40" style="color: #10B981;"><House /></el-icon>
              </div>
              <div class="nav-info">
                <h4>房间管理</h4>
                <p>管理房间、电表编号、房租和电价</p>
              </div>
              <el-icon class="nav-arrow" :size="20" style="color: #94a3b8;"><ArrowRight /></el-icon>
            </div>
          </el-card>

          <el-card shadow="hover" class="nav-card" @click="navigateTo('/dormitory/residents')">
            <div class="nav-content">
              <div class="nav-icon" style="background-color: rgba(245, 158, 11, 0.1);">
                <el-icon :size="40" style="color: #F59E0B;"><User /></el-icon>
              </div>
              <div class="nav-info">
                <h4>入住管理</h4>
                <p>管理员工入住、试用期、搬离和换房</p>
              </div>
              <el-icon class="nav-arrow" :size="20" style="color: #94a3b8;"><ArrowRight /></el-icon>
            </div>
          </el-card>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { OfficeBuilding, House, User, Avatar, ArrowRight } from '@element-plus/icons-vue';
import { dashboardApi } from '@/api/dashboard';

const router = useRouter();

const statsLoading = ref(false);
const stats = ref({
  building_count: 0,
  room_count: 0,
  employee_count: 0,
  current_residents: 0,
});

const loadStats = async () => {
  statsLoading.value = true;
  try {
    const res = await dashboardApi.get();
    if (res.summary) {
      stats.value = {
        building_count: res.summary.building_count || 0,
        room_count: res.summary.room_count || 0,
        employee_count: res.summary.employee_count || 0,
        current_residents: res.summary.current_residents || 0,
      };
    }
  } catch {
    // 如果仪表盘 API 不可用，保持默认值 0
  } finally {
    statsLoading.value = false;
  }
};

const navigateTo = (path: string) => {
  router.push(path);
};

onMounted(() => {
  loadStats();
});
</script>

<style scoped lang="scss">
.dormitory-manage-index {
  padding: 0;
}

.page-card {
  border-radius: 8px;
}

.page-header {
  margin-bottom: 20px;

  .page-title {
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--text-primary, #1e293b);
    margin: 0 0 4px;
  }

  .page-desc {
    color: var(--text-secondary, #64748b);
    margin: 0;
    font-size: 0.875rem;
  }
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
  margin-bottom: 32px;

  .stat-card {
    cursor: default;
    border-radius: 8px;

    .stat-content {
      display: flex;
      align-items: center;
      gap: 16px;

      .stat-icon {
        width: 64px;
        height: 64px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
      }

      .stat-info {
        flex: 1;

        .stat-label {
          font-size: 0.875rem;
          color: var(--text-secondary, #64748b);
          margin: 0 0 4px;
        }

        .stat-value {
          font-size: 1.75rem;
          font-weight: 700;
          color: var(--text-primary, #1e293b);
          margin: 0;
        }
      }
    }
  }
}

.nav-section {
  .section-title {
    font-size: 1rem;
    font-weight: 600;
    color: var(--text-primary, #1e293b);
    margin: 0 0 16px;
  }
}

.nav-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 16px;

  .nav-card {
    cursor: pointer;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    border-radius: 8px;

    &:hover {
      transform: translateY(-4px);
    }

    .nav-content {
      display: flex;
      align-items: center;
      gap: 16px;

      .nav-icon {
        width: 72px;
        height: 72px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
      }

      .nav-info {
        flex: 1;

        h4 {
          font-size: 1.125rem;
          font-weight: 600;
          color: var(--text-primary, #1e293b);
          margin: 0 0 4px;
        }

        p {
          font-size: 0.875rem;
          color: var(--text-secondary, #64748b);
          margin: 0;
        }
      }

      .nav-arrow {
        flex-shrink: 0;
        transition: transform 0.2s ease;
      }
    }

    &:hover .nav-arrow {
      transform: translateX(4px);
    }
  }
}
</style>