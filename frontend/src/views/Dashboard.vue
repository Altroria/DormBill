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

    <!-- 空闲房间列表 -->
    <el-card class="idle-rooms-card" shadow="never">
      <template #header>
        <div class="card-header">
          <span>空闲房间（{{ data?.idle_rooms?.length ?? 0 }}）</span>
          <el-button text type="primary" @click="$router.push('/dormitory/rooms')">
            进入房间管理 →
          </el-button>
        </div>
      </template>
      <div v-if="data?.idle_rooms?.length" class="idle-rooms-grid">
        <div
          v-for="room in data.idle_rooms"
          :key="room.id"
          class="idle-room-card"
        >
          <div class="room-header">
            <div class="room-info">
              <div class="room-name">{{ room.building_no }} - {{ room.room_no }}</div>
              <div class="room-full-name">{{ room.room_name }}</div>
            </div>
            <el-tag type="success" effect="light" size="small">空闲</el-tag>
          </div>
          <div class="room-rent">
            <span class="rent-label">房租标准</span>
            <span class="rent-value">¥{{ formatMoney(room.rent_standard) }}/月</span>
          </div>
          <el-button 
            type="primary" 
            size="small" 
            class="checkin-btn"
            @click="handleQuickCheckIn(room)"
          >
            快捷入住
          </el-button>
        </div>
      </div>
      <el-empty v-else description="暂无空闲房间" :image-size="80" />
    </el-card>

    <!-- 快捷入住对话框 -->
    <el-dialog
      v-model="checkInDialogVisible"
      title="快捷入住"
      width="600px"
      @close="resetCheckInForm"
    >
      <el-form
        ref="checkInFormRef"
        :model="checkInForm"
        :rules="checkInRules"
        label-width="100px"
      >
        <el-form-item label="房间信息">
          <el-input
            :value="`${selectedRoom?.building_no} - ${selectedRoom?.room_no} - ${selectedRoom?.room_name}`"
            disabled
          />
        </el-form-item>

        <el-form-item label="房租标准">
          <el-input
            :value="`¥${formatMoney(selectedRoom?.rent_standard)}/月`"
            disabled
          />
        </el-form-item>

        <el-form-item label="员工" prop="employee_id">
          <el-select
            v-model="checkInForm.employee_id"
            placeholder="请选择员工"
            filterable
            style="width: 100%"
            @focus="loadAllEmployees"
          >
            <el-option
              v-for="emp in employees"
              :key="emp.id"
              :label="`${emp.name} (${emp.employee_no})`"
              :value="emp.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="入住日期" prop="check_in_date">
          <el-date-picker
            v-model="checkInForm.check_in_date"
            type="date"
            placeholder="选择入住日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>

        <el-form-item label="前3月免租">
          <el-checkbox v-model="checkInForm.free_rent_enabled">
            勾选后前3个月免房租（严格按天计算）
          </el-checkbox>
        </el-form-item>

        <el-form-item label="主要缴费人">
          <el-checkbox v-model="checkInForm.is_primary">设为主要缴费人</el-checkbox>
        </el-form-item>

        <el-form-item label="备注">
          <el-input
            v-model="checkInForm.remark"
            type="textarea"
            :rows="3"
            placeholder="请输入备注"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="checkInDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleCheckInSubmit">
          确定入住
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onActivated } from 'vue';
import { ElMessage, type FormInstance, type FormRules } from 'element-plus';
import { WarningFilled } from '@element-plus/icons-vue';
import dayjs from 'dayjs';
import { dashboardApi } from '@/api/dashboard';
import { residenceApi } from '@/api/residence';
import { employeeApi } from '@/api/employee';
import type { DashboardData, Employee } from '@/types';

const selectedMonth = ref<string>(dayjs().format('YYYY-MM-DD'));
const data = ref<DashboardData | null>(null);
const checkInDialogVisible = ref(false);
const checkInFormRef = ref<FormInstance>();
const submitting = ref(false);
const employeeSearching = ref(false);
const selectedRoom = ref<any>(null);
const employees = ref<Employee[]>([]);

const checkInForm = ref({
  employee_id: undefined as number | undefined,
  room_id: undefined as number | undefined,
  check_in_date: dayjs().format('YYYY-MM-DD'),
  free_rent_enabled: false,
  is_primary: true,
  remark: ''
});

const checkInRules: FormRules = {
  employee_id: [{ required: true, message: '请选择员工', trigger: 'change' }],
  check_in_date: [{ required: true, message: '请选择入住日期', trigger: 'change' }]
};

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
  if (v === null || v === undefined) return '0.00'
  const num = typeof v === 'string' ? parseFloat(v) : v
  if (isNaN(num)) return '0.00'
  return num.toFixed(2)
}

function handleQuickCheckIn(room: any) {
  selectedRoom.value = room;
  checkInForm.value.room_id = room.id;
  checkInForm.value.check_in_date = dayjs().format('YYYY-MM-DD');
  loadAllEmployees();
  checkInDialogVisible.value = true;
}

async function loadAllEmployees() {
  if (employees.value.length > 0) return; // 已加载过就不重复加载
  employeeSearching.value = true;
  try {
    const res = await employeeApi.list({ page_size: 500 });
    employees.value = res.items || [];
  } catch (error) {
    ElMessage.error('加载员工列表失败');
  } finally {
    employeeSearching.value = false;
  }
}

async function searchEmployees(query: string) {
  if (!query) {
    loadAllEmployees();
    return;
  }
  employeeSearching.value = true;
  try {
    const res = await employeeApi.list({ keyword: query });
    employees.value = res.items || res;
  } catch (error) {
    ElMessage.error('搜索员工失败');
  } finally {
    employeeSearching.value = false;
  }
}

async function handleCheckInSubmit() {
  if (!checkInFormRef.value) return;
  await checkInFormRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true;
      try {
        const submitData = {
          employee_id: checkInForm.value.employee_id,
          room_id: checkInForm.value.room_id,
          check_in_date: checkInForm.value.check_in_date,
          check_out_date: null,
          probation_months: checkInForm.value.free_rent_enabled ? 3 : 0,
          is_primary_payer: checkInForm.value.is_primary ? 1 : 0,
          status: 'valid',
          remark: checkInForm.value.remark || ''
        };
        await residenceApi.create(submitData);
        ElMessage.success('入住成功');
        checkInDialogVisible.value = false;
        loadData(); // 刷新数据
      } catch (error) {
        ElMessage.error('入住失败');
      } finally {
        submitting.value = false;
      }
    }
  });
}

function resetCheckInForm() {
  checkInForm.value = {
    employee_id: undefined,
    room_id: undefined,
    check_in_date: dayjs().format('YYYY-MM-DD'),
    free_rent_enabled: false,
    is_primary: true,
    remark: ''
  };
  selectedRoom.value = null;
  checkInFormRef.value?.resetFields();
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
onActivated(loadData);
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

.idle-rooms-card {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: 600;
  }
}

.idle-rooms-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

.idle-room-card {
  border: 1px solid #E2E8F0;
  border-radius: 8px;
  padding: 16px;
  background: #F8FAFC;
  transition: all 0.2s;

  &:hover {
    border-color: #10B981;
    box-shadow: 0 2px 8px rgba(16, 185, 129, 0.15);
    transform: translateY(-2px);
  }

  .room-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 12px;
  }

  .room-info {
    flex: 1;

    .room-name {
      font-size: 1rem;
      font-weight: 600;
      color: #1E293B;
      margin-bottom: 4px;
    }

    .room-full-name {
      font-size: 0.875rem;
      color: #64748B;
    }
  }

  .room-rent {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 12px;
    background: #fff;
    border-radius: 6px;
    margin-bottom: 12px;

    .rent-label {
      font-size: 0.8125rem;
      color: #64748B;
    }

    .rent-value {
      font-size: 1rem;
      font-weight: 700;
      color: #10B981;
      font-family: 'DIN Alternate', monospace;
    }
  }

  .checkin-btn {
    width: 100%;
  }
}
</style>
