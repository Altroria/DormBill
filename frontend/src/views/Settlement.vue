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

      <el-input
        v-model="filters.search"
        placeholder="搜索员工姓名"
        clearable
        style="width: 200px"
        @keyup.enter="fetchSettlements"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>

      <el-select
        v-model="filters.status"
        placeholder="状态"
        clearable
        style="width: 120px"
        @change="fetchSettlements"
      >
        <el-option label="草稿" value="draft" />
        <el-option label="已生成" value="generated" />
        <el-option label="已锁定" value="locked" />
      </el-select>

      <div style="flex: 1"></div>

      <el-button type="primary" @click="handleGenerate">
        <el-icon><DocumentAdd /></el-icon>
        生成结算
      </el-button>

      <el-button type="success" @click="handleRecalculate">
        <el-icon><Refresh /></el-icon>
        重新计算
      </el-button>

      <el-button 
        type="warning" 
        @click="handleLock"
        :disabled="isMonthLocked"
      >
        <el-icon><Lock /></el-icon>
        锁定月份
      </el-button>

      <el-button 
        type="info" 
        @click="handleUnlock"
        :disabled="!isMonthLocked"
      >
        <el-icon><Unlock /></el-icon>
        解锁
      </el-button>

      <el-button type="warning" @click="handleExport">
        <el-icon><Download /></el-icon>
        导出Excel
      </el-button>
    </div>

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

      <el-table-column label="工号-姓名" width="150">
        <template #default="{ row }">
          {{ row.employee_no }} - {{ row.employee_name }}
        </template>
      </el-table-column>

      <el-table-column prop="company" label="任职单位" min-width="150" />
      <el-table-column prop="department" label="一级部门" width="120" />

      <el-table-column label="应住房租" width="110" align="right">
        <template #default="{ row }">
          ¥{{ row.rent_should.toFixed(2) }}
        </template>
      </el-table-column>

      <el-table-column label="实扣房租" width="110" align="right">
        <template #default="{ row }">
          <span :class="{ 'edited-value': row.rent_actual !== row.rent_should }">
            ¥{{ row.rent_actual.toFixed(2) }}
          </span>
        </template>
      </el-table-column>

      <el-table-column label="入住天数" width="90" align="center">
        <template #default="{ row }">
          {{ row.stay_days }}
        </template>
      </el-table-column>

      <el-table-column label="普通电费" width="110" align="right">
        <template #default="{ row }">
          ¥{{ row.electricity_fee.toFixed(2) }}
        </template>
      </el-table-column>

      <el-table-column label="空调电费" width="110" align="right">
        <template #default="{ row }">
          ¥{{ row.ac_electricity_fee.toFixed(2) }}
        </template>
      </el-table-column>

      <el-table-column label="水费" width="110" align="right">
        <template #default="{ row }">
          ¥{{ row.water_fee.toFixed(2) }}
        </template>
      </el-table-column>

      <el-table-column label="补扣-" width="110" align="right">
        <template #default="{ row }">
          <span class="deduction-minus">
            ¥{{ row.deduction_minus.toFixed(2) }}
          </span>
        </template>
      </el-table-column>

      <el-table-column label="补扣+" width="110" align="right">
        <template #default="{ row }">
          <span class="deduction-plus">
            ¥{{ row.deduction_plus.toFixed(2) }}
          </span>
        </template>
      </el-table-column>

      <el-table-column label="最终扣款" width="120" align="right" fixed="right">
        <template #default="{ row }">
          <span class="final-amount">
            ¥{{ row.total_amount.toFixed(2) }}
          </span>
        </template>
      </el-table-column>

      <el-table-column label="状态" width="90" align="center" fixed="right">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)">
            {{ getStatusLabel(row.status) }}
          </el-tag>
        </template>
      </el-table-column>

      <el-table-column label="操作" width="100" fixed="right" align="center">
        <template #default="{ row }">
          <el-button 
            link 
            type="primary" 
            @click="handleAdjust(row)"
            :disabled="isMonthLocked"
          >
            调整
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 预检查对话框 -->
    <el-dialog
      v-model="showPrecheckDialog"
      title="结算预检查"
      width="700px"
    >
      <el-alert
        v-if="precheckResult.blocking_issues?.length > 0"
        title="阻断项"
        type="error"
        :closable="false"
        style="margin-bottom: 16px"
      >
        <ul>
          <li v-for="(issue, index) in precheckResult.blocking_issues" :key="index">
            {{ issue }}
          </li>
        </ul>
      </el-alert>

      <el-alert
        v-if="precheckResult.warnings?.length > 0"
        title="警告项"
        type="warning"
        :closable="false"
        style="margin-bottom: 16px"
      >
        <ul>
          <li v-for="(warning, index) in precheckResult.warnings" :key="index">
            {{ warning }}
          </li>
        </ul>
      </el-alert>

      <el-alert
        v-if="!precheckResult.blocking_issues?.length && !precheckResult.warnings?.length"
        title="检查通过"
        type="success"
        :closable="false"
      >
        所有检查项通过，可以生成结算数据。
      </el-alert>

      <template #footer>
        <el-button @click="showPrecheckDialog = false">取消</el-button>
        <el-button 
          type="primary" 
          :loading="generating"
          :disabled="precheckResult.blocking_issues?.length > 0"
          @click="confirmGenerate"
        >
          确认生成
        </el-button>
      </template>
    </el-dialog>

    <!-- 调整对话框 -->
    <el-dialog
      v-model="showAdjustDialog"
      title="调整结算数据"
      width="600px"
      @close="resetAdjustForm"
    >
      <el-form
        ref="adjustFormRef"
        :model="adjustForm"
        label-width="120px"
      >
        <el-form-item label="员工信息">
          <el-input
            :value="`${currentSettlement?.employee_no} - ${currentSettlement?.employee_name}`"
            disabled
          />
        </el-form-item>

        <el-form-item label="房间信息">
          <el-input
            :value="`${currentSettlement?.building_no} - ${currentSettlement?.room_no} - ${currentSettlement?.room_name}`"
            disabled
          />
        </el-form-item>

        <el-divider />

        <el-form-item label="应住房租">
          <el-input-number
            :value="currentSettlement?.rent_should"
            disabled
            :precision="2"
            style="width: 100%"
          />
        </el-form-item>

        <el-form-item label="实扣房租">
          <el-input-number
            v-model="adjustForm.rent_actual"
            :precision="2"
            :step="10"
            :min="0"
            style="width: 100%"
          />
          <div style="font-size: 12px; color: #909399; margin-top: 4px">
            可以根据实际情况调整实际扣款的房租金额
          </div>
        </el-form-item>

        <el-divider />

        <el-form-item label="补扣-">
          <el-input-number
            v-model="adjustForm.deduction_minus"
            :precision="2"
            :step="10"
            :min="0"
            style="width: 100%"
          />
          <div style="font-size: 12px; color: #909399; margin-top: 4px">
            需要减免的金额（如优惠、补偿等）
          </div>
        </el-form-item>

        <el-form-item label="补扣+">
          <el-input-number
            v-model="adjustForm.deduction_plus"
            :precision="2"
            :step="10"
            :min="0"
            style="width: 100%"
          />
          <div style="font-size: 12px; color: #909399; margin-top: 4px">
            需要额外扣除的金额（如罚款、补缴等）
          </div>
        </el-form-item>

        <el-divider />

        <el-form-item label="预计最终扣款">
          <el-input
            :value="`¥${calculateAdjustedAmount().toFixed(2)}`"
            disabled
          />
        </el-form-item>

        <el-form-item label="备注">
          <el-input
            v-model="adjustForm.remark"
            type="textarea"
            :rows="3"
            placeholder="请输入调整原因"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="showAdjustDialog = false">取消</el-button>
        <el-button type="primary" :loading="adjusting" @click="handleSubmitAdjust">
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, DocumentAdd, Refresh, Lock, Unlock, Download } from '@element-plus/icons-vue'
import { settlementApi } from '@/api/settlement'
import { buildingApi } from '@/api/building'
import type { MonthlySettlement, Building } from '@/types'

const loading = ref(false)
const generating = ref(false)
const adjusting = ref(false)
const showPrecheckDialog = ref(false)
const showAdjustDialog = ref(false)
const isMonthLocked = ref(false)

const settlements = ref<MonthlySettlement[]>([])
const buildings = ref<Building[]>([])
const currentSettlement = ref<MonthlySettlement | null>(null)

const filters = reactive({
  month: new Date().toISOString().substring(0, 10),
  buildingId: undefined as number | undefined,
  search: '',
  status: ''
})

const precheckResult = reactive<{
  blocking_issues: string[]
  warnings: string[]
}>({
  blocking_issues: [],
  warnings: []
})

const adjustForm = reactive({
  rent_actual: 0,
  deduction_minus: 0,
  deduction_plus: 0,
  remark: ''
})

const getStatusType = (status: string) => {
  const map: Record<string, any> = {
    draft: 'info',
    generated: 'primary',
    locked: 'success'
  }
  return map[status] || 'info'
}

const getStatusLabel = (status: string) => {
  const map: Record<string, string> = {
    draft: '草稿',
    generated: '已生成',
    locked: '已锁定'
  }
  return map[status] || status
}

const calculateAdjustedAmount = () => {
  if (!currentSettlement.value) return 0
  
  const base = adjustForm.rent_actual +
    currentSettlement.value.electricity_fee +
    currentSettlement.value.ac_electricity_fee +
    currentSettlement.value.water_fee
  
  return base - adjustForm.deduction_minus + adjustForm.deduction_plus
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
        sums[index] = `¥${sum.toFixed(2)}`
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
      month: filters.month.substring(0, 7)
    }
    if (filters.buildingId) params.building_id = filters.buildingId
    if (filters.search) params.search = filters.search
    if (filters.status) params.status = filters.status

    const response = await settlementApi.list(params)
    settlements.value = response.items || []
    
    // Check if month is locked
    isMonthLocked.value = settlements.value.some((s: MonthlySettlement) => s.status === 'locked')
  } catch (error) {
    ElMessage.error('获取结算数据失败')
  } finally {
    loading.value = false
  }
}

const handleGenerate = async () => {
  if (!filters.month) {
    ElMessage.warning('请选择月份')
    return
  }

  // Run precheck first
  try {
    const result = await settlementApi.precheck({ month: filters.month.substring(0, 7) })
    precheckResult.blocking_issues = result.blocking.map((item: any) => item.message)
    precheckResult.warnings = result.warnings.map((item: any) => item.message)
    showPrecheckDialog.value = true
  } catch (error) {
    ElMessage.error('预检查失败')
  }
}

const confirmGenerate = async () => {
  generating.value = true
  try {
    await settlementApi.generate({
      month: filters.month.substring(0, 7),
      force: false
    })
    ElMessage.success('结算生成成功')
    showPrecheckDialog.value = false
    fetchSettlements()
  } catch (error) {
    ElMessage.error('结算生成失败')
  } finally {
    generating.value = false
  }
}

const handleRecalculate = async () => {
  if (!filters.month) {
    ElMessage.warning('请选择月份')
    return
  }

  try {
    await ElMessageBox.confirm(
      '确定要重新计算当前月份的结算数据吗？这将覆盖未锁定的结算记录。',
      '确认重新计算',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    loading.value = true
    await settlementApi.recalculate({
      month: filters.month.substring(0, 7)
    })
    ElMessage.success('重新计算成功')
    fetchSettlements()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('重新计算失败')
    }
  } finally {
    loading.value = false
  }
}

const handleLock = async () => {
  if (!filters.month) {
    ElMessage.warning('请选择月份')
    return
  }

  try {
    await ElMessageBox.confirm(
      '锁定后将无法修改该月份的结算数据，确定要锁定吗？',
      '确认锁定',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await settlementApi.lock(filters.month.substring(0, 7))
    ElMessage.success('锁定成功')
    fetchSettlements()
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
      '解锁后可以修改该月份的结算数据，确定要解锁吗？',
      '确认解锁',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await settlementApi.unlock(filters.month.substring(0, 7))
    ElMessage.success('解锁成功')
    fetchSettlements()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('解锁失败')
    }
  }
}

const handleAdjust = (row: MonthlySettlement) => {
  currentSettlement.value = row
  adjustForm.rent_actual = row.rent_actual
  adjustForm.deduction_minus = row.deduction_minus
  adjustForm.deduction_plus = row.deduction_plus
  adjustForm.remark = row.remark || ''
  showAdjustDialog.value = true
}

const handleSubmitAdjust = async () => {
  if (!currentSettlement.value) return

  adjusting.value = true
  try {
    await settlementApi.update(currentSettlement.value.id, adjustForm)
    ElMessage.success('调整成功')
    showAdjustDialog.value = false
    fetchSettlements()
  } catch (error) {
    ElMessage.error('调整失败')
  } finally {
    adjusting.value = false
  }
}

const handleExport = () => {
  if (!filters.month) {
    ElMessage.warning('请选择月份')
    return
  }

  const month = filters.month.substring(0, 7)
  const buildingParam = filters.buildingId ? `&building_id=${filters.buildingId}` : ''
  const url = `/api/export/settlement?month=${month}${buildingParam}`
  
  const link = document.createElement('a')
  link.href = url
  link.download = `扣款表_${month}.xlsx`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  
  ElMessage.success('导出任务已开始')
}

const resetAdjustForm = () => {
  adjustForm.rent_actual = 0
  adjustForm.deduction_minus = 0
  adjustForm.deduction_plus = 0
  adjustForm.remark = ''
  currentSettlement.value = null
}

onMounted(() => {
  fetchBuildings()
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
