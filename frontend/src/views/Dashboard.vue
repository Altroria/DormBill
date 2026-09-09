<template>
  <div class="dashboard">
    <div class="page-header">
      <h2 class="page-title">数据概览</h2>
      <el-date-picker
        v-model="selectedMonth"
        type="month"
        placeholder="选择月份"
        format="YYYY-MM"
        value-format="YYYY-MM-DD"
        @change="loadData"
        style="width: 160px"
      />
    </div>

    <!-- 顶部统计卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <div class="stat-card stat-primary">
          <div class="stat-label">当前月份</div>
          <div class="stat-value">{{ formatMonth(data?.current_month) }}</div>
          <div class="stat-extra">月度结算</div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card stat-success">
          <div class="stat-label">入住人数 / 房间数</div>
          <div class="stat-value">
            {{ data?.summary.current_residents ?? 0 }}
            <span class="divider">/</span>
            {{ data?.summary.room_count ?? 0 }}
          </div>
          <div class="stat-extra">{{ data?.summary.building_count ?? 0 }} 个楼栋</div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card stat-warning">
          <div class="stat-label">本月最终扣款</div>
          <div class="stat-value">¥{{ formatMoney(data?.amounts.settlement_total) }}</div>
          <div class="stat-extra">房租+水电+补扣</div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card stat-info">
          <div class="stat-label">电表录入进度</div>
          <div class="stat-value">{{ data?.summary.meter_progress ?? '0/0' }}</div>
          <el-progress
            :percentage="meterProgressPercent"
            :stroke-width="6"
            :show-text="false"
            color="#6366F1"
            style="margin-top: 8px"
          />
        </div>
      </el-col>
    </el-row>

    <!-- 金额分布卡片 -->
    <el-row :gutter="20" class="amounts-row">
      <el-col :span="6">
        <div class="amount-card">
          <div class="amount-icon" style="background: #EEF2FF; color: #6366F1;">¥</div>
          <div class="amount-info">
            <div class="amount-label">本月房租合计</div>
            <div class="amount-value">¥{{ formatMoney(data?.amounts.rent_total) }}</div>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="amount-card">
          <div class="amount-icon" style="background: #ECFDF5; color: #10B981;">⚡</div>
          <div class="amount-info">
            <div class="amount-label">本月普通电费</div>
            <div class="amount-value">¥{{ formatMoney(data?.amounts.electricity_total) }}</div>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="amount-card">
          <div class="amount-icon" style="background: #FFFBEB; color: #F59E0B;">❄</div>
          <div class="amount-info">
            <div class="amount-label">本月空调电费</div>
            <div class="amount-value">¥{{ formatMoney(data?.amounts.ac_electricity_total) }}</div>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="amount-card">
          <div class="amount-icon" style="background: #EFF6FF; color: #3B82F6;">💧</div>
          <div class="amount-info">
            <div class="amount-label">本月水费合计</div>
            <div class="amount-value">¥{{ formatMoney(data?.amounts.water_total) }}</div>
          </div>
        </div>
      </el-col>
    </el-row>

    <!-- 试用期到期提醒 -->
    <el-card v-if="data?.probation_expiring?.length" class="alert-card" shadow="never">
      <template #header>
        <div class="alert-header">
          <el-icon class="alert-icon"><WarningFilled /></el-icon>
          <span>试用期到期提醒（{{ data.probation_expiring.length }} 人）</span>
        </div>
      </template>
      <div class="alert-list">
        <div
          v-for="item in data.probation_expiring"
          :key="item.residence_id"
          class="alert-item"
        >
          <el-tag type="danger" effect="light">还剩 {{ item.days_left }} 天</el-tag>
          <span class="alert-text">
            员工 #{{ item.employee_id }} 的试用期将于
            <strong>{{ item.probation_end }}</strong> 到期
          </span>
        </div>
      </div>
    </el-card>

    <!-- 最近水费周期 -->
    <el-card class="recent-water" shadow="never">
      <template #header>
        <div class="card-header">
          <span>最近水费周期</span>
          <el-button text type="primary" @click="$router.push('/water')">
            进入水费管理 →
          </el-button>
        </div>
      </template>
      <el-table :data="data?.recent_water ?? []" empty-text="暂无水费记录">
        <el-table-column label="楼栋" width="100">
          <template #default="{ row }">
            楼栋 #{{ row.building_id }}
          </template>
        </el-table-column>
        <el-table-column label="水费周期" min-width="200">
          <template #default="{ row }">
            {{ row.period_start }} ~ {{ row.period_end }}
          </template>
        </el-table-column>
        <el-table-column label="金额" width="120" align="right">
          <template #default="{ row }">
            ¥{{ formatMoney(row.total_amount) }}
          </template>
        </el-table-column>
        <el-table-column label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="waterStatusType(row.status)" effect="light">
              {{ waterStatusLabel(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { WarningFilled } from '@element-plus/icons-vue';
import dayjs from 'dayjs';
import { dashboardApi } from '@/api/dashboard';
import type { DashboardData } from '@/types';

const selectedMonth = ref<string>(dayjs().format('YYYY-MM-DD'));
const data = ref<DashboardData | null>(null);

const meterProgressPercent = computed(() => {
  if (!data.value?.summary.meter_progress) return 0;
  const [done, total] = data.value.summary.meter_progress.split('/').map(Number);
  if (!total || total === 0) return 0;
  return Math.round((done / total) * 100);
});

function formatMonth(s?: string) {
  if (!s) return '-';
  return s.replace('-', '年') + '月';
}

function formatMoney(v?: number) {
  return (v ?? 0).toFixed(2);
}

function waterStatusType(s: string): 'success' | 'warning' | 'info' {
  if (s === 'settled') return 'success';
  if (s === 'allocated') return 'warning';
  return 'info';
}

function waterStatusLabel(s: string) {
  return { pending: '未录入', allocated: '已分摊', settled: '已结算' }[s] || s;
}

async function loadData() {
  const month = selectedMonth.value?.slice(0, 7);
  try {
    data.value = await dashboardApi.get(month);
  } catch {
    // 错误已由拦截器处理
  }
}

onMounted(loadData);
</script>

<style scoped lang="scss">
.dashboard {
  max-width: 1400px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1E293B;
  margin: 0;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border: 1px solid #E2E8F0;
  height: 130px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.stat-label {
  font-size: 0.875rem;
  color: #64748B;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1E293B;
  font-family: 'DIN Alternate', monospace;

  .divider {
    color: #CBD5E1;
    margin: 0 4px;
    font-size: 1.25rem;
  }
}

.stat-extra {
  font-size: 0.8125rem;
  color: #94A3B8;
  margin-top: 4px;
}

.stat-primary { border-top: 3px solid #6366F1; }
.stat-success { border-top: 3px solid #10B981; }
.stat-warning { border-top: 3px solid #F59E0B; }
.stat-info    { border-top: 3px solid #3B82F6; }

.amounts-row {
  margin-bottom: 20px;
}

.amount-card {
  background: #fff;
  border-radius: 12px;
  padding: 16px 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  border: 1px solid #E2E8F0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.amount-icon {
  width: 48px;
  height: 48px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: bold;
}

.amount-info {
  flex: 1;

  .amount-label {
    font-size: 0.8125rem;
    color: #64748B;
  }
  .amount-value {
    font-size: 1.25rem;
    font-weight: 700;
    color: #1E293B;
    font-family: 'DIN Alternate', monospace;
    margin-top: 2px;
  }
}

.alert-card {
  margin-bottom: 20px;
  border-color: #F59E0B;

  .alert-header {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 600;
    color: #F59E0B;
  }

  .alert-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .alert-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px 12px;
    background: #FFFBEB;
    border-radius: 6px;
  }
}

.recent-water {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: 600;
  }
}
</style>
