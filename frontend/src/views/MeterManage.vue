<template>
  <div class="meter-manage">
    <div class="toolbar">
      <el-date-picker
        v-model="filters.month"
        type="month"
        placeholder="选择月份"
        format="YYYY-MM"
        value-format="YYYY-MM-DD"
        style="width: 200px"
        @change="fetchMeters"
      />

      <el-select
        v-model="filters.buildingId"
        placeholder="选择楼栋"
        clearable
        style="width: 180px"
        @change="fetchMeters"
      >
        <el-option
          v-for="building in buildings"
          :key="building.id"
          :label="building.name"
          :value="building.id"
        />
      </el-select>

      <el-button type="primary" @click="handleInitMonth">
        <el-icon><DocumentAdd /></el-icon>
        初始化月度电表
      </el-button>

      <el-button type="success" @click="showCalculateDialog = true">
        <el-icon><CircleCheck /></el-icon>
        批量计算电费
      </el-button>

      <el-button type="warning" @click="handleExport">
        <el-icon><Download /></el-icon>
        导出明细
      </el-button>
    </div>

    <el-alert
      title="电表管理流程说明"
      type="info"
      :closable="false"
      style="margin-bottom: 20px"
    >
      <p>1. 每月初点击"初始化月度电表"按钮，系统会自动带出上月读数</p>
      <p>2. 逐房录入本月普通电表和空调电表读数</p>
      <p>3. 录入完成后点击"批量计算电费"，输入空调平均单价进行统一计算</p>
      <p>4. 计算完成后可导出明细表格</p>
    </el-alert>

    <el-table
      v-loading="loading"
      :data="meters"
      stripe
      border
      style="width: 100%"
    >
      <el-table-column label="楼栋-房号-房间" min-width="200" fixed="left">
        <template #default="{ row }">
          {{ row.building_no }} - {{ row.room_no }} - {{ row.room_name }}
        </template>
      </el-table-column>

      <el-table-column prop="meter_no" label="电表编号" width="120" />
      
      <el-table-column label="上月读数" width="100" align="right">
        <template #default="{ row }">
          {{ row.previous_reading?.toFixed(2) || '0.00' }}
        </template>
      </el-table-column>

      <el-table-column label="本月读数" width="100" align="right">
        <template #default="{ row }">
          {{ row.current_reading?.toFixed(2) || '-' }}
        </template>
      </el-table-column>

      <el-table-column label="用电量" width="100" align="right">
        <template #default="{ row }">
          {{ calculateUsage(row.current_reading, row.previous_reading) }}
        </template>
      </el-table-column>

      <el-table-column label="电价" width="90" align="right">
        <template #default="{ row }">
          ¥{{ row.electricity_price?.toFixed(2) || '0.00' }}
        </template>
      </el-table-column>

      <el-table-column label="普通电费" width="100" align="right">
        <template #default="{ row }">
          ¥{{ row.total_fee?.toFixed(2) || '0.00' }}
        </template>
      </el-table-column>

      <el-table-column label="上月空调" width="100" align="right">
        <template #default="{ row }">
          {{ row.ac_previous_reading?.toFixed(2) || '0.00' }}
        </template>
      </el-table-column>

      <el-table-column label="本月空调" width="100" align="right">
        <template #default="{ row }">
          {{ row.ac_current_reading?.toFixed(2) || '-' }}
        </template>
      </el-table-column>

      <el-table-column label="空调度数" width="100" align="right">
        <template #default="{ row }">
          {{ calculateUsage(row.ac_current_reading, row.ac_previous_reading) }}
        </template>
      </el-table-column>

      <el-table-column label="空调单价" width="100" align="right">
        <template #default="{ row }">
          ¥{{ row.ac_unit_price?.toFixed(2) || '0.00' }}
        </template>
      </el-table-column>

      <el-table-column label="空调电费" width="100" align="right">
        <template #default="{ row }">
          ¥{{ row.ac_fee?.toFixed(2) || '0.00' }}
        </template>
      </el-table-column>

      <el-table-column label="入住人数" width="90" align="center">
        <template #default="{ row }">
          {{ row.occupants_count || 0 }}
        </template>
      </el-table-column>

      <el-table-column label="状态" width="90" align="center">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)">
            {{ getStatusLabel(row.status) }}
          </el-tag>
        </template>
      </el-table-column>

      <el-table-column label="操作" width="100" fixed="right" align="center">
        <template #default="{ row }">
          <el-button link type="primary" @click="handleRecord(row)">
            录入
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 录入对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="录入电表读数"
      width="600px"
      @close="resetForm"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="140px"
      >
        <el-form-item label="房间信息">
          <el-input
            :value="`${currentMeter?.building_no} - ${currentMeter?.room_no} - ${currentMeter?.room_name}`"
            disabled
          />
        </el-form-item>

        <el-form-item label="上月普通读数">
          <el-input-number
            :value="currentMeter?.previous_reading"
            disabled
            style="width: 100%"
          />
        </el-form-item>

        <el-form-item label="本月普通读数" prop="current_reading">
          <el-input-number
            v-model="form.current_reading"
            :precision="2"
            :step="1"
            :min="0"
            style="width: 100%"
            placeholder="请输入本月普通电表读数"
          />
        </el-form-item>

        <el-divider />

        <el-form-item label="上月空调读数">
          <el-input-number
            :value="currentMeter?.ac_previous_reading"
            disabled
            style="width: 100%"
          />
        </el-form-item>

        <el-form-item label="本月空调读数" prop="ac_current_reading">
          <el-input-number
            v-model="form.ac_current_reading"
            :precision="2"
            :step="1"
            :min="0"
            style="width: 100%"
            placeholder="请输入本月空调电表读数"
          />
        </el-form-item>

        <el-form-item label="空调单价(可选)">
          <el-input-number
            v-model="form.ac_unit_price"
            :precision="2"
            :step="0.01"
            :min="0"
            style="width: 100%"
            placeholder="留空则使用批量计算时的单价"
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

    <!-- 批量计算对话框 -->
    <el-dialog
      v-model="showCalculateDialog"
      title="批量计算电费"
      width="500px"
    >
      <el-alert
        title="说明"
        type="info"
        :closable="false"
        style="margin-bottom: 20px"
      >
        将对所有已录入读数的房间统一计算电费，空调单价将应用到所有未单独设置单价的房间
      </el-alert>

      <el-form label-width="140px">
        <el-form-item label="计算月份">
          <el-input :value="filters.month?.substring(0, 7)" disabled />
        </el-form-item>

        <el-form-item label="空调平均单价" required>
          <el-input-number
            v-model="calculateForm.ac_unit_price"
            :precision="2"
            :step="0.01"
            :min="0"
            style="width: 100%"
            placeholder="请输入空调电费平均单价"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="showCalculateDialog = false">取消</el-button>
        <el-button type="primary" :loading="calculating" @click="handleCalculate">
          确定计算
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { DocumentAdd, CircleCheck, Download } from '@element-plus/icons-vue'
import { meterApi } from '@/api/meter'
import { buildingApi } from '@/api/building'
import type { MeterRecord, Building } from '@/types'

const loading = ref(false)
const submitting = ref(false)
const calculating = ref(false)
const dialogVisible = ref(false)
const showCalculateDialog = ref(false)
const formRef = ref<FormInstance>()

const meters = ref<MeterRecord[]>([])
const buildings = ref<Building[]>([])
const currentMeter = ref<MeterRecord | null>(null)

const filters = reactive({
  month: new Date().toISOString().substring(0, 10),
  buildingId: undefined as number | undefined
})

const form = reactive({
  current_reading: undefined as number | undefined,
  ac_current_reading: undefined as number | undefined,
  ac_unit_price: undefined as number | undefined,
  remark: ''
})

const calculateForm = reactive({
  ac_unit_price: undefined as number | undefined
})

const rules: FormRules = {
  current_reading: [
    { required: true, message: '请输入本月普通电表读数', trigger: 'blur' }
  ],
  ac_current_reading: [
    { required: true, message: '请输入本月空调电表读数', trigger: 'blur' }
  ]
}

const calculateUsage = (current: number | undefined, last: number | undefined) => {
  if (current === undefined || last === undefined) return '-'
  const usage = current - last
  return usage >= 0 ? usage.toFixed(2) : '0.00'
}

const getStatusType = (status: string) => {
  const map: Record<string, any> = {
    pending: 'info',
    recorded: 'warning',
    calculated: 'success'
  }
  return map[status] || 'info'
}

const getStatusLabel = (status: string) => {
  const map: Record<string, string> = {
    pending: '待录入',
    recorded: '已录入',
    calculated: '已计算'
  }
  return map[status] || status
}

const fetchBuildings = async () => {
  try {
    const res = await buildingApi.list()
    buildings.value = res.items
  } catch (error) {
    ElMessage.error('获取楼栋列表失败')
  }
}

const fetchMeters = async () => {
  if (!filters.month) {
    ElMessage.warning('请选择月份')
    return
  }

  loading.value = true
  try {
    const params: any = {
      month: filters.month.substring(0, 7)
    }
    if (filters.buildingId) {
      params.building_id = filters.buildingId
    }
    const res = await meterApi.list(params)
    meters.value = res.items || res
  } catch (error) {
    ElMessage.error('获取电表数据失败')
  } finally {
    loading.value = false
  }
}

const handleInitMonth = async () => {
  if (!filters.month) {
    ElMessage.warning('请选择月份')
    return
  }

  try {
    await ElMessageBox.confirm(
      `确定要初始化 ${filters.month.substring(0, 7)} 的电表数据吗？系统会自动带出上月读数。`,
      '确认初始化',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    loading.value = true
    const params: any = {
      month: filters.month.substring(0, 7)
    }
    if (filters.buildingId) {
      params.building_id = filters.buildingId
    }
    await meterApi.initMonth(params)
    ElMessage.success('初始化成功')
    fetchMeters()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('初始化失败')
    }
  } finally {
    loading.value = false
  }
}

const handleRecord = (row: MeterRecord) => {
  currentMeter.value = row
  form.current_reading = row.current_reading
  form.ac_current_reading = row.ac_current_reading
  form.ac_unit_price = row.ac_unit_price
  form.remark = row.remark || ''
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!formRef.value || !currentMeter.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      if (!currentMeter.value) return
      
      // Validate readings
      if (form.current_reading! < currentMeter.value.previous_reading) {
        ElMessage.warning('本月普通读数不能小于上月读数')
        return
      }
      if (form.ac_current_reading! < currentMeter.value.ac_previous_reading) {
        ElMessage.warning('本月空调读数不能小于上月读数')
        return
      }

      submitting.value = true
      try {
        await meterApi.update(currentMeter.value.room_id, filters.month.substring(0, 7), form)
        ElMessage.success('录入成功')
        dialogVisible.value = false
        fetchMeters()
      } catch (error) {
        ElMessage.error('录入失败')
      } finally {
        submitting.value = false
      }
    }
  })
}

const handleCalculate = async () => {
  if (!calculateForm.ac_unit_price || calculateForm.ac_unit_price <= 0) {
    ElMessage.warning('请输入有效的空调平均单价')
    return
  }

  calculating.value = true
  try {
    await meterApi.calculate({
      month: filters.month.substring(0, 7),
      ac_unit_price: calculateForm.ac_unit_price
    })
    ElMessage.success('计算成功')
    showCalculateDialog.value = false
    fetchMeters()
  } catch (error) {
    ElMessage.error('计算失败')
  } finally {
    calculating.value = false
  }
}

const handleExport = () => {
  if (!filters.month) {
    ElMessage.warning('请选择月份')
    return
  }

  const month = filters.month.substring(0, 7)
  const buildingParam = filters.buildingId ? `&building_id=${filters.buildingId}` : ''
  const url = `/api/export/meter-detail?month=${month}${buildingParam}`
  
  // Create download link
  const link = document.createElement('a')
  link.href = url
  link.download = `电费明细_${month}.xlsx`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  
  ElMessage.success('导出任务已开始')
}

const resetForm = () => {
  Object.assign(form, {
    current_reading: undefined,
    ac_current_reading: undefined,
    ac_unit_price: undefined,
    remark: ''
  })
  currentMeter.value = null
  formRef.value?.resetFields()
}

onMounted(() => {
  fetchBuildings()
  fetchMeters()
})
</script>

<style scoped>
.meter-manage {
  padding: 20px;
}

.toolbar {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.el-alert p {
  margin: 4px 0;
  line-height: 1.6;
}
</style>
