<template>
  <div class="water-manage">
    <div class="toolbar">
      <el-date-picker
        v-model="filters.period"
        type="month"
        placeholder="选择水费周期起始月"
        format="YYYY-MM"
        value-format="YYYY-MM-DD"
        style="width: 220px"
        @change="fetchWaterBills"
      />

      <el-select
        v-model="filters.buildingId"
        placeholder="选择楼栋"
        clearable
        style="width: 180px"
        @change="fetchWaterBills"
      >
        <el-option
          v-for="building in buildings"
          :key="building.id"
          :label="building.name"
          :value="building.id"
        />
      </el-select>

      <el-button type="primary" @click="handleAdd">
        <el-icon><Plus /></el-icon>
        新增水费账单
      </el-button>
    </div>

    <div v-loading="loading" class="water-bills">
      <el-empty v-if="waterBills.length === 0" description="暂无水费账单数据" />

      <el-card
        v-for="bill in waterBills"
        :key="bill.id"
        class="bill-card"
        shadow="hover"
      >
        <template #header>
          <div class="card-header">
            <div class="card-title">
              <el-tag type="primary" size="large">{{ bill.building_no }}</el-tag>
              <span class="period">
                {{ bill.period_start }} ~ {{ bill.period_end }}
              </span>
            </div>
            <div class="card-actions">
              <el-button link type="primary" @click="handleEdit(bill)">
                编辑
              </el-button>
              <el-button 
                link 
                type="success" 
                @click="handleAllocate(bill)"
                :disabled="bill.status === 'allocated'"
              >
                生成分摊
              </el-button>
              <el-button link type="warning" @click="handleExport(bill)">
                导出
              </el-button>
              <el-button link type="danger" @click="handleDelete(bill)">
                删除
              </el-button>
            </div>
          </div>
        </template>

        <div class="bill-info">
          <div class="info-item">
            <span class="label">水表起始：</span>
            <span class="value">{{ bill.meter_start?.toFixed(2) }}</span>
          </div>
          <div class="info-item">
            <span class="label">水表截止：</span>
            <span class="value">{{ bill.meter_end?.toFixed(2) }}</span>
          </div>
          <div class="info-item">
            <span class="label">用水量：</span>
            <span class="value">{{ ((bill.meter_end || 0) - (bill.meter_start || 0)).toFixed(2) }} 吨</span>
          </div>
          <div class="info-item">
            <span class="label">水费金额：</span>
            <span class="value amount">¥{{ bill.total_amount.toFixed(2) }}</span>
          </div>
          <div class="info-item">
            <span class="label">状态：</span>
            <el-tag :type="bill.status === 'allocated' ? 'success' : 'info'">
              {{ bill.status === 'allocated' ? '已分摊' : '待分摊' }}
            </el-tag>
          </div>
          <div v-if="bill.remark" class="info-item full-width">
            <span class="label">备注：</span>
            <span class="value">{{ bill.remark }}</span>
          </div>
        </div>

        <!-- 分摊明细 -->
        <div v-if="expandedBillId === bill.id && allocations.length > 0" class="allocations">
          <el-divider content-position="left">分摊明细</el-divider>
          <el-table
            :data="allocations"
            border
            size="small"
            max-height="400"
          >
            <el-table-column label="房号-房间" width="180">
              <template #default="{ row }">
                {{ row.room_number }} - {{ row.room_name }}
              </template>
            </el-table-column>
            <el-table-column prop="employee_name" label="员工" width="120" />
            <el-table-column label="第一月天数" width="100" align="center">
              <template #default="{ row }">
                {{ row.days_first_month }}
              </template>
            </el-table-column>
            <el-table-column label="第二月天数" width="100" align="center">
              <template #default="{ row }">
                {{ row.days_second_month }}
              </template>
            </el-table-column>
            <el-table-column label="是否有效" width="90" align="center">
              <template #default="{ row }">
                <el-tag :type="row.is_valid ? 'success' : 'info'" size="small">
                  {{ row.is_valid ? '有效' : '无效' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="分摊金额" width="120" align="right">
              <template #default="{ row }">
                <el-input-number
                  v-model="row.amount"
                  :precision="2"
                  :step="1"
                  :min="0"
                  size="small"
                  @change="handleUpdateAllocation(row)"
                />
              </template>
            </el-table-column>
            <el-table-column prop="remark" label="备注" min-width="150" show-overflow-tooltip />
          </el-table>
          <div class="allocation-summary">
            总计：¥{{ calculateTotalAllocation().toFixed(2) }}
          </div>
        </div>
      </el-card>
    </div>

    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑水费账单' : '新增水费账单'"
      width="600px"
      @close="resetForm"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="120px"
      >
        <el-form-item label="起始月份" prop="period_start">
          <el-date-picker
            v-model="form.period_start"
            type="month"
            placeholder="选择起始月份"
            format="YYYY-MM"
            value-format="YYYY-MM-DD"
            style="width: 100%"
            @change="handlePeriodChange"
          />
        </el-form-item>

        <el-form-item label="结束月份">
          <el-input :value="form.period_end?.substring(0, 7)" disabled />
          <div style="font-size: 12px; color: #909399; margin-top: 4px">
            自动设置为起始月份+1
          </div>
        </el-form-item>

        <el-form-item label="楼栋" prop="building_id">
          <el-select
            v-model="form.building_id"
            placeholder="请选择楼栋"
            style="width: 100%"
          >
            <el-option
              v-for="building in buildings"
              :key="building.id"
              :label="building.name"
              :value="building.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="水表起始" prop="meter_start">
          <el-input-number
            v-model="form.meter_start"
            :precision="2"
            :step="1"
            :min="0"
            style="width: 100%"
            placeholder="请输入水表起始读数"
          />
        </el-form-item>

        <el-form-item label="水表截止" prop="meter_end">
          <el-input-number
            v-model="form.meter_end"
            :precision="2"
            :step="1"
            :min="0"
            style="width: 100%"
            placeholder="请输入水表截止读数"
          />
        </el-form-item>

        <el-form-item label="用水量">
          <el-input
            :value="calculateWaterUsage()"
            disabled
            suffix-icon="吨"
          />
        </el-form-item>

        <el-form-item label="水费金额" prop="total_amount">
          <el-input-number
            v-model="form.total_amount"
            :precision="2"
            :step="10"
            :min="0"
            style="width: 100%"
            placeholder="请输入水费金额"
          />
        </el-form-item>

        <el-form-item label="备注">
          <el-input
            v-model="form.remark"
            type="textarea"
            :rows="3"
            placeholder="请输入备注"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { waterApi } from '@/api/water'
import { buildingApi } from '@/api/building'
import type { WaterExpense, WaterAllocation, Building } from '@/types'

const loading = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref<FormInstance>()
const expandedBillId = ref<number | null>(null)

const waterBills = ref<WaterExpense[]>([])
const buildings = ref<Building[]>([])
const allocations = ref<WaterAllocation[]>([])

const filters = reactive({
  period: new Date().toISOString().substring(0, 10),
  buildingId: undefined as number | undefined
})

const form = reactive({
  id: undefined as number | undefined,
  period_start: '',
  period_end: '',
  building_id: undefined as number | undefined,
  meter_start: undefined as number | undefined,
  meter_end: undefined as number | undefined,
  total_amount: undefined as number | undefined,
  remark: ''
})

const rules: FormRules = {
  period_start: [{ required: true, message: '请选择起始月份', trigger: 'change' }],
  building_id: [{ required: true, message: '请选择楼栋', trigger: 'change' }],
  meter_start: [{ required: true, message: '请输入水表起始读数', trigger: 'blur' }],
  meter_end: [{ required: true, message: '请输入水表截止读数', trigger: 'blur' }],
  total_amount: [{ required: true, message: '请输入水费金额', trigger: 'blur' }]
}

const handlePeriodChange = (val: string) => {
  if (val) {
    const date = new Date(val)
    date.setMonth(date.getMonth() + 1)
    form.period_end = date.toISOString().substring(0, 10)
  }
}

const calculateWaterUsage = () => {
  if (form.meter_start !== undefined && form.meter_end !== undefined) {
    const usage = form.meter_end - form.meter_start
    return usage >= 0 ? `${usage.toFixed(2)} 吨` : '0.00 吨'
  }
  return '-'
}

const calculateTotalAllocation = () => {
  return allocations.value.reduce((sum, item) => sum + (item.amount || 0), 0)
}

const fetchBuildings = async () => {
  try {
    const res = await buildingApi.list()
    buildings.value = res.items
  } catch (error) {
    ElMessage.error('获取楼栋列表失败')
  }
}

const fetchWaterBills = async () => {
  loading.value = true
  try {
    const params: any = {}
    if (filters.period) {
      params.period = filters.period.substring(0, 7)
    }
    if (filters.buildingId) {
      params.building_id = filters.buildingId
    }
    const res = await waterApi.list(params)
    waterBills.value = res.items
  } catch (error) {
    ElMessage.error('获取水费账单失败')
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  isEdit.value = false
  dialogVisible.value = true
}

const handleEdit = (bill: WaterExpense) => {
  isEdit.value = true
  Object.assign(form, {
    id: bill.id,
    period_start: bill.period_start,
    period_end: bill.period_end,
    building_id: bill.building_id,
    meter_start: bill.meter_start,
    meter_end: bill.meter_end,
    total_amount: bill.total_amount,
    remark: bill.remark || ''
  })
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      if (form.meter_end! <= form.meter_start!) {
        ElMessage.warning('水表截止读数必须大于起始读数')
        return
      }

      submitting.value = true
      try {
        if (isEdit.value && form.id) {
          await waterApi.update(form.id, form)
          ElMessage.success('更新成功')
        } else {
          await waterApi.create(form)
          ElMessage.success('创建成功')
        }
        dialogVisible.value = false
        fetchWaterBills()
      } catch (error) {
        ElMessage.error(isEdit.value ? '更新失败' : '创建失败')
      } finally {
        submitting.value = false
      }
    }
  })
}

const handleAllocate = async (bill: WaterExpense) => {
  try {
    await ElMessageBox.confirm(
      '确定要生成水费分摊吗？系统会根据入住天数自动计算各房间的分摊金额。',
      '确认生成分摊',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    loading.value = true
    const result = await waterApi.allocate(bill.id)
    allocations.value = result.allocations || []
    expandedBillId.value = bill.id
    ElMessage.success('分摊生成成功')
    fetchWaterBills()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('生成分摊失败')
    }
  } finally {
    loading.value = false
  }
}

const handleUpdateAllocation = async (allocation: WaterAllocation) => {
  try {
    await waterApi.updateSingleAllocation(allocation.id, allocation.amount)
    ElMessage.success('更新成功')
  } catch (error) {
    ElMessage.error('更新失败')
  }
}

const handleDelete = async (bill: WaterExpense) => {
  try {
    await ElMessageBox.confirm('确定要删除这个水费账单吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await waterApi.delete(bill.id)
    ElMessage.success('删除成功')
    fetchWaterBills()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const handleExport = (bill: WaterExpense) => {
  const period = bill.period_start.substring(0, 7)
  const url = `/api/export/water-detail?period=${period}&building_id=${bill.building_id}`
  
  const link = document.createElement('a')
  link.href = url
  link.download = `水费明细_${period}_${bill.building_no}.xlsx`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  
  ElMessage.success('导出任务已开始')
}

const resetForm = () => {
  Object.assign(form, {
    id: undefined,
    period_start: '',
    period_end: '',
    building_id: undefined,
    meter_start: undefined,
    meter_end: undefined,
    total_amount: undefined,
    remark: ''
  })
  formRef.value?.resetFields()
}

onMounted(() => {
  fetchBuildings()
  fetchWaterBills()
})
</script>

<style scoped>
.water-manage {
  padding: 20px;
}

.toolbar {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.water-bills {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.bill-card {
  transition: transform 0.2s;
}

.bill-card:hover {
  transform: translateY(-2px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.period {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.card-actions {
  display: flex;
  gap: 8px;
}

.bill-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.info-item.full-width {
  grid-column: 1 / -1;
}

.label {
  color: #909399;
  font-size: 14px;
}

.value {
  color: #303133;
  font-size: 14px;
  font-weight: 500;
}

.value.amount {
  color: #6366F1;
  font-size: 18px;
  font-weight: 700;
}

.allocations {
  margin-top: 20px;
}

.allocation-summary {
  margin-top: 12px;
  text-align: right;
  font-size: 16px;
  font-weight: 600;
  color: #6366F1;
}
</style>
