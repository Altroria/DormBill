<template>
  <div class="settlement">
    <div class="toolbar">
      <el-date-picker
        v-model="filters.month"
        type="month"
        placeholder="选择月份"
        format="YYYY-MM"
        value-format="YYYY-MM-DD"
        style="width: 200px"
        @change="fetchSettlements"
      />

      <el-select
        v-model="filters.buildingId"
        placeholder="选择楼栋"
        clearable
        style="width: 180px"
        @change="fetchSettlements"
      >
        <el-option
          v-for="building in buildings"
          :key="building.id"
          :label="building.name"
          :value="building.id"
        />
      </el-select>

      <!-- 水费周期选择 -->
      <el-select
        v-model="filters.waterMode"
        placeholder="水费周期"
        style="width: 160px"
        @change="fetchSettlements"
      >
        <el-option label="双月水费" value="double" />
        <el-option label="单月水费" value="single" />
        <el-option label="不计算水费" value="none" />
      </el-select>

      <el-input
        v-model="filters.search"
        placeholder="搜索员工姓名"
        clearable
        style="width: 200px"
        @clear="fetchSettlements"
        @keyup.enter="fetchSettlements"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>

      <el-button type="primary" @click="fetchSettlements">
        <el-icon><Search /></el-icon>
        查询
      </el-button>

      <div style="flex: 1"></div>

      <el-button type="success" @click="handleExport">
        <el-icon><Download /></el-icon>
        导出Excel
      </el-button>

      <el-button 
        v-if="!isMonthLocked" 
        type="warning" 
        @click="handleLock"
      >
        <el-icon><Lock /></el-icon>
        锁定月份
      </el-button>
      
      <el-button 
        v-else 
        type="info" 
        @click="handleUnlock"
      >
        <el-icon><Unlock /></el-icon>
        解锁月份
      </el-button>
    </div>

    <el-alert
      v-if="filters.waterMode === 'double'"
      title="💡 实时查询 - 双月水费模式"
      type="info"
      :closable="false"
      show-icon
      style="margin-bottom: 16px"
    >
      <div>
        水费按双月计算:上月+本月(例如:10月结算 = 9月水费 + 10月水费)
      </div>
    </el-alert>
    
    <el-alert
      v-if="filters.waterMode === 'single'"
      title="💡 实时查询 - 单月水费模式"
      type="warning"
      :closable="false"
      show-icon
      style="margin-bottom: 16px"
    >
      <div>
        水费仅计算当月(例如:10月结算 = 10月水费)
      </div>
      <div style="margin-top: 8px; font-size: 12px; color: #606266;">
        💡 切换水费模式或筛选条件后,点击"查询"按钮刷新数据
      </div>
    </el-alert>

    <el-alert
      v-if="filters.waterMode === 'none'"
      title="💡 实时查询 - 不计算水费"
      type="success"
      :closable="false"
      show-icon
      style="margin-bottom: 16px"
    >
      <div>
        本次结算不包含水费,仅计算房租和电费
      </div>
    </el-alert>

    <el-alert
      v-if="isMonthLocked"
      title="当前月份已锁定"
      type="success"
      :closable="false"
      show-icon
      style="margin-bottom: 20px"
    >
      该月份的结算数据已锁定，无法修改。如需修改请先解锁。
    </el-alert>

    <el-table
      v-loading="loading"
      :data="settlements"
      stripe
      border
      style="width: 100%"
      show-summary
      :summary-method="getSummaries"
    >
      <el-table-column label="楼栋-房号-房间" min-width="200" fixed="left">
        <template #default="{ row }">
          {{ row.building_no }} - {{ row.room_no }} - {{ row.room_name }}
        </template>
      </el-table-column>

      <el-table-column label="姓名" width="120">
        <template #default="{ row }">
          {{ row.employee_name }}
        </template>
      </el-table-column>

      <el-table-column prop="company" label="任职单位" min-width="150" />
      <el-table-column prop="department" label="一级部门" width="120" />

      <el-table-column label="应住房租" width="110" align="right">
        <template #default="{ row }">
          ¥{{ formatNumber(row.rent_should) }}
        </template>
      </el-table-column>

      <el-table-column label="实扣房租" width="110" align="right">
        <template #default="{ row }">
          <span :class="{ 'edited-value': row.rent_actual !== row.rent_should }">
            ¥{{ formatNumber(row.rent_actual) }}
          </span>
        </template>
      </el-table-column>

      <el-table-column label="入住天数" width="90" align="center">
        <template #default="{ row }">
          {{ row.stay_days }}
        </template>
      </el-table-column>

      <el-table-column label="分摊电费" width="110" align="right">
        <template #default="{ row }">
          ¥{{ formatNumber(row.electricity_fee) }}
        </template>
      </el-table-column>

      <el-table-column label="空调电费" width="110" align="right">
        <template #default="{ row }">
          ¥{{ formatNumber(row.ac_electricity_fee) }}
        </template>
      </el-table-column>

      <el-table-column label="水费" width="110" align="right">
        <template #default="{ row }">
          ¥{{ formatNumber(row.water_fee) }}
        </template>
      </el-table-column>

      <el-table-column label="补扣-" width="110" align="right">
        <template #default="{ row }">
          <span class="deduction-minus">
            ¥{{ formatNumber(row.deduction_minus) }}
          </span>
        </template>
      </el-table-column>

      <el-table-column label="补扣+" width="110" align="right">
        <template #default="{ row }">
          <span class="deduction-plus">
            ¥{{ formatNumber(row.deduction_plus) }}
          </span>
        </template>
      </el-table-column>

      <el-table-column label="最终扣款" width="120" align="right" fixed="right">
        <template #default="{ row }">
          <span class="final-amount">
            ¥{{ formatNumber(row.total_amount) }}
          </span>
        </template>
      </el-table-column>

    </el-table>

    <el-empty 
      v-if="!loading && settlements.length === 0" 
      description="暂无数据"
      style="margin: 40px 0"
    />

    <div v-if="total > 0" style="margin-top: 20px; display: flex; justify-content: flex-end;">
      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.pageSize"
        :page-sizes="[10, 20, 50, 100, 200]"
        :total="total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handlePageChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onActivated } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Lock, Unlock, Download } from '@element-plus/icons-vue'
import { settlementApi } from '@/api/settlement'
import { buildingApi } from '@/api/building'
import type { MonthlySettlement, Building } from '@/types'

const loading = ref(false)
const isMonthLocked = ref(false)
const total = ref(0)

const settlements = ref<MonthlySettlement[]>([])
const buildings = ref<Building[]>([])

const filters = reactive({
  month: new Date().toISOString().substring(0, 10),
  buildingId: undefined as number | undefined,
  search: '',
  waterMode: 'double' as 'single' | 'double' | 'none'
})

const pagination = reactive({
  page: 1,
  pageSize: 10
})


// 安全格式化数字
const formatNumber = (value: any, decimals: number = 2, defaultValue: string = '0.00'): string => {
  if (value === null || value === undefined || value === '') return defaultValue
  const num = typeof value === 'string' ? parseFloat(value) : value
  if (isNaN(num)) return defaultValue
  return num.toFixed(decimals)
}

const getSummaries = (param: any) => {
  const { columns, data } = param
  const sums: any[] = []
  
  columns.forEach((column: any, index: number) => {
    if (index === 0) {
      sums[index] = '合计'
      return
    }
    
    const values = data.map((item: any) => {
      switch (column.property) {
        case 'rent_should':
        case 'rent_actual':
        case 'electricity_fee':
        case 'ac_electricity_fee':
        case 'water_fee':
        case 'deduction_minus':
        case 'deduction_plus':
        case 'total_amount':
          return Number(item[column.property])
        default:
          return 0
      }
    })
    
    if (!values.every((value: any) => Number.isNaN(value))) {
      const sum = values.reduce((prev: number, curr: number) => {
        const value = Number(curr)
        if (!Number.isNaN(value)) {
          return prev + curr
        } else {
          return prev
        }
      }, 0)
      
      if (['rent_should', 'rent_actual', 'electricity_fee', 'ac_electricity_fee', 'water_fee', 
           'deduction_minus', 'deduction_plus', 'total_amount'].includes(column.property)) {
        sums[index] = `¥${formatNumber(sum)}`
      } else {
        sums[index] = ''
      }
    } else {
      sums[index] = ''
    }
  })
  
  return sums
}

const fetchBuildings = async () => {
  try {
    const res = await buildingApi.list()
    buildings.value = res.items
  } catch (error) {
    ElMessage.error('获取楼栋列表失败')
  }
}

const fetchSettlements = async () => {
  if (!filters.month) {
    ElMessage.warning('请选择月份')
    return
  }

  loading.value = true
  try {
    const params: any = {
      month: filters.month.substring(0, 7),
      water_mode: filters.waterMode,
      page: pagination.page,
      page_size: pagination.pageSize,
    }
    if (filters.buildingId) params.building_id = filters.buildingId
    if (filters.search) params.keyword = filters.search

    const response = await settlementApi.list(params)
    settlements.value = response.items || []
    total.value = response.total || 0
    
    // Check if month is locked
    isMonthLocked.value = settlements.value.some((s: MonthlySettlement) => s.status === 'locked')
  } catch (error) {
    ElMessage.error('获取结算数据失败')
  } finally {
    loading.value = false
  }
}

const handlePageChange = (page: number) => {
  pagination.page = page
  fetchSettlements()
}

const handleSizeChange = (size: number) => {
  pagination.pageSize = size
  pagination.page = 1
  fetchSettlements()
}

const checkMonthLockStatus = async () => {
  await fetchSettlements()
}

const handleLock = async () => {
  if (!filters.month) {
    ElMessage.warning('请选择月份')
    return
  }

  try {
    await ElMessageBox.confirm(
      '确定要锁定当前月份吗？\n\n锁定后该月份数据将固化，作为最终版本。',
      '确认锁定',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await settlementApi.lock(filters.month.substring(0, 7))
    ElMessage.success('锁定成功')
    checkMonthLockStatus()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('锁定失败')
    }
  }
}

const handleUnlock = async () => {
  if (!filters.month) {
    ElMessage.warning('请选择月份')
    return
  }

  try {
    await ElMessageBox.confirm(
      '确定要解锁当前月份吗？',
      '确认解锁',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await settlementApi.unlock(filters.month.substring(0, 7))
    ElMessage.success('解锁成功')
    checkMonthLockStatus()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('解锁失败')
    }
  }
}

const handleExport = async () => {
  if (!filters.month) {
    ElMessage.warning('请选择月份')
    return
  }

  const month = filters.month.substring(0, 7)
  const buildingParam = filters.buildingId ? `&building_id=${filters.buildingId}` : ''
  const waterModeParam = `&water_mode=${filters.waterMode}`
  const url = `/api/export/settlement?month=${month}${buildingParam}${waterModeParam}`
  
  try {
    const response = await fetch(url)
    if (!response.ok) {
      throw new Error('导出失败')
    }
    
    const blob = await response.blob()
    const downloadUrl = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = downloadUrl
    
    let waterSuffix = '双月'
    if (filters.waterMode === 'single') {
      waterSuffix = '单月'
    } else if (filters.waterMode === 'none') {
      waterSuffix = '不含水费'
    }
    link.download = `扣款表_${month}_${waterSuffix}.xlsx`
    
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(downloadUrl)
    
    ElMessage.success('导出成功')
  } catch (error) {
    console.error('导出失败:', error)
    ElMessage.error('导出失败，请检查网络连接')
  }
}

onMounted(() => {
  fetchBuildings()
  fetchSettlements()
})

onActivated(() => {
  fetchSettlements()
})
</script>

<style scoped>
.settlement {
  padding: 20px;
}

.toolbar {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.edited-value {
  color: #E6A23C;
  font-weight: 600;
}

.deduction-minus {
  color: #67C23A;
}

.deduction-plus {
  color: #F56C6C;
}

.final-amount {
  color: #6366F1;
  font-size: 16px;
  font-weight: 700;
}

:deep(.el-alert ul) {
  margin: 8px 0;
  padding-left: 20px;
}

:deep(.el-alert li) {
  margin: 4px 0;
  line-height: 1.6;
}
</style>
