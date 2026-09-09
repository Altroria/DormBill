<template>
  <div class="resident-list">
    <div class="toolbar">
      <el-select
        v-model="filters.buildingId"
        placeholder="选择楼栋"
        clearable
        style="width: 180px"
        @change="handleFilterChange"
      >
        <el-option
          v-for="building in buildings"
          :key="building.id"
          :label="building.name"
          :value="building.id"
        />
      </el-select>

      <el-select
        v-model="filters.roomId"
        placeholder="选择房间"
        clearable
        filterable
        style="width: 200px"
        @change="fetchResidents"
      >
        <el-option
          v-for="room in filteredRooms"
          :key="room.id"
          :label="`${room.room_no} - ${room.room_name}`"
          :value="room.id"
        />
      </el-select>

      <el-input
        v-model="filters.search"
        placeholder="搜索员工姓名"
        clearable
        style="width: 200px"
        @keyup.enter="fetchResidents"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>

      <div style="flex: 1"></div>

      <el-button type="primary" @click="handleAdd">
        <el-icon><Plus /></el-icon>
        新增入住
      </el-button>

      <el-button type="warning" @click="showBatchMoveOutDialog = true" :disabled="selectedRows.length === 0">
        <el-icon><SwitchButton /></el-icon>
        批量搬离
      </el-button>

      <el-button type="success" @click="showBatchTransferDialog = true" :disabled="selectedRows.length === 0">
        <el-icon><Position /></el-icon>
        批量换房
      </el-button>
    </div>

    <el-tabs v-model="filters.statusTab" @tab-change="fetchResidents">
      <el-tab-pane label="全部" name="all" />
      <el-tab-pane label="在住" name="valid" />
      <el-tab-pane label="出差" name="business_trip" />
      <el-tab-pane label="已搬离" name="leave" />
    </el-tabs>

    <el-table
      v-loading="loading"
      :data="residents"
      stripe
      border
      style="width: 100%"
      @selection-change="handleSelectionChange"
      :row-class-name="getRowClassName"
    >
      <el-table-column type="selection" width="55" />
      
      <el-table-column label="楼栋-房号-房间" min-width="200">
        <template #default="{ row }">
          {{ row.building_code }} - {{ row.room_number }} - {{ row.room_name }}
        </template>
      </el-table-column>

      <el-table-column label="员工姓名" width="120">
        <template #default="{ row }">
          <span>
            {{ row.employee_name }}
            <el-tag v-if="row.is_primary" type="danger" size="small" effect="dark">★</el-tag>
          </span>
        </template>
      </el-table-column>

      <el-table-column prop="employee_code" label="工号" width="120" />
      <el-table-column prop="organization" label="任职单位" min-width="150" />
      <el-table-column prop="department" label="一级部门" width="120" />
      <el-table-column prop="position" label="职务" width="120" />
      
      <el-table-column label="入住日期" width="110">
        <template #default="{ row }">
          {{ row.check_in_date }}
        </template>
      </el-table-column>

      <el-table-column label="搬离日期" width="110">
        <template #default="{ row }">
          {{ row.check_out_date || '-' }}
        </template>
      </el-table-column>

      <el-table-column label="试用期" width="80" align="center">
        <template #default="{ row }">
          {{ row.probation_months }}个月
        </template>
      </el-table-column>

      <el-table-column label="状态" width="90" align="center">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)">
            {{ getStatusLabel(row.status) }}
          </el-tag>
        </template>
      </el-table-column>

      <el-table-column prop="remark" label="备注" min-width="120" show-overflow-tooltip />

      <el-table-column label="操作" width="150" fixed="right" align="center">
        <template #default="{ row }">
          <el-button link type="primary" @click="handleEdit(row)">编辑</el-button>
          <el-button link type="warning" @click="handleMoveOut(row)" v-if="!row.check_out_date">
            搬离
          </el-button>
          <el-button link type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑入住信息' : '新增入住'"
      width="700px"
      @close="resetForm"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="120px"
      >
        <el-form-item label="员工" prop="employee_id">
          <el-select
            v-model="form.employee_id"
            placeholder="请选择员工"
            filterable
            remote
            :remote-method="searchEmployees"
            :loading="employeeSearching"
            style="width: 100%"
            @change="handleEmployeeChange"
          >
            <el-option
              v-for="emp in employees"
              :key="emp.id"
              :label="`${emp.name} (${emp.employee_no})`"
              :value="emp.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="楼栋" prop="building_id">
          <el-select
            v-model="form.building_id"
            placeholder="请选择楼栋"
            style="width: 100%"
            @change="handleBuildingChange"
          >
            <el-option
              v-for="building in buildings"
              :key="building.id"
              :label="building.name"
              :value="building.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="房间" prop="room_id">
          <el-select
            v-model="form.room_id"
            placeholder="请选择房间"
            filterable
            style="width: 100%"
          >
            <el-option
              v-for="room in availableRooms"
              :key="room.id"
              :label="`${room.room_no} - ${room.room_name}`"
              :value="room.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="入住日期" prop="check_in_date">
          <el-date-picker
            v-model="form.check_in_date"
            type="date"
            placeholder="选择入住日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>

        <el-form-item label="试用期">
          <el-select v-model="form.probation_months" style="width: 100%">
            <el-option label="无试用期" :value="0" />
            <el-option label="3个月" :value="3" />
            <el-option label="6个月" :value="6" />
          </el-select>
        </el-form-item>

        <el-form-item label="主要缴费人">
          <el-checkbox v-model="form.is_primary">设为主要缴费人</el-checkbox>
        </el-form-item>

        <el-form-item label="状态">
          <el-radio-group v-model="form.status">
            <el-radio value="valid">在住</el-radio>
            <el-radio value="business_trip">出差</el-radio>
            <el-radio value="leave">已搬离</el-radio>
          </el-radio-group>
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

    <!-- 批量搬离对话框 -->
    <el-dialog
      v-model="showBatchMoveOutDialog"
      title="批量搬离"
      width="600px"
    >
      <el-alert
        title="提示"
        :description="`已选择 ${selectedRows.length} 条记录`"
        type="info"
        show-icon
        :closable="false"
        style="margin-bottom: 20px"
      />

      <el-form label-width="100px">
        <el-form-item label="搬离日期" required>
          <el-date-picker
            v-model="batchMoveOutDate"
            type="date"
            placeholder="选择搬离日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="showBatchMoveOutDialog = false">取消</el-button>
        <el-button type="primary" :loading="batchSubmitting" @click="handleBatchMoveOut">
          确定搬离
        </el-button>
      </template>
    </el-dialog>

    <!-- 批量换房对话框 -->
    <el-dialog
      v-model="showBatchTransferDialog"
      title="批量换房"
      width="600px"
    >
      <el-alert
        title="提示"
        :description="`已选择 ${selectedRows.length} 条记录`"
        type="info"
        show-icon
        :closable="false"
        style="margin-bottom: 20px"
      />

      <el-form label-width="100px">
        <el-form-item label="目标楼栋" required>
          <el-select
            v-model="batchTransferForm.building_id"
            placeholder="请选择目标楼栋"
            style="width: 100%"
            @change="handleTransferBuildingChange"
          >
            <el-option
              v-for="building in buildings"
              :key="building.id"
              :label="building.name"
              :value="building.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="目标房间" required>
          <el-select
            v-model="batchTransferForm.room_id"
            placeholder="请选择目标房间"
            filterable
            style="width: 100%"
          >
            <el-option
              v-for="room in transferAvailableRooms"
              :key="room.id"
              :label="`${room.room_no} - ${room.room_name}`"
              :value="room.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="换房日期" required>
          <el-date-picker
            v-model="batchTransferForm.transfer_date"
            type="date"
            placeholder="选择换房日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="showBatchTransferDialog = false">取消</el-button>
        <el-button type="primary" :loading="batchSubmitting" @click="handleBatchTransfer">
          确定换房
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, onActivated } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { Search, Plus, SwitchButton, Position } from '@element-plus/icons-vue'
import { residenceApi } from '@/api/residence'
import { buildingApi } from '@/api/building'
import { roomApi } from '@/api/room'
import { employeeApi } from '@/api/employee'
import type { ResidenceRecord, Building, Room, Employee } from '@/types'

const loading = ref(false)
const submitting = ref(false)
const batchSubmitting = ref(false)
const employeeSearching = ref(false)
const dialogVisible = ref(false)
const showBatchMoveOutDialog = ref(false)
const showBatchTransferDialog = ref(false)
const isEdit = ref(false)
const formRef = ref<FormInstance>()

const residents = ref<ResidenceRecord[]>([])
const buildings = ref<Building[]>([])
const rooms = ref<Room[]>([])
const employees = ref<Employee[]>([])
const selectedRows = ref<ResidenceRecord[]>([])
const availableRooms = ref<Room[]>([])
const transferAvailableRooms = ref<Room[]>([])

const filters = reactive({
  buildingId: undefined as number | undefined,
  roomId: undefined as number | undefined,
  search: '',
  statusTab: 'all'
})

const form = reactive({
  id: undefined as number | undefined,
  employee_id: undefined as number | undefined,
  building_id: undefined as number | undefined,
  room_id: undefined as number | undefined,
  check_in_date: '',
  probation_months: 0,
  is_primary: false,
  status: 'valid' as 'valid' | 'business_trip' | 'leave',
  remark: ''
})

const batchMoveOutDate = ref('')

const batchTransferForm = reactive({
  building_id: undefined as number | undefined,
  room_id: undefined as number | undefined,
  transfer_date: ''
})

const rules: FormRules = {
  employee_id: [{ required: true, message: '请选择员工', trigger: 'change' }],
  building_id: [{ required: true, message: '请选择楼栋', trigger: 'change' }],
  room_id: [{ required: true, message: '请选择房间', trigger: 'change' }],
  check_in_date: [{ required: true, message: '请选择入住日期', trigger: 'change' }]
}

const filteredRooms = computed(() => {
  if (!filters.buildingId) return rooms.value
  return rooms.value.filter(room => room.building_id === filters.buildingId)
})

const getStatusType = (status: string) => {
  const map: Record<string, any> = {
    valid: 'success',
    business_trip: 'warning',
    leave: 'info'
  }
  return map[status] || 'info'
}

const getStatusLabel = (status: string) => {
  const map: Record<string, string> = {
    valid: '在住',
    business_trip: '出差',
    leave: '已搬离'
  }
  return map[status] || status
}

const getRowClassName = ({ row }: { row: ResidenceRecord }) => {
  if (row.probation_months > 0 && !row.check_out_date) {
    return 'row-probation'
  }
  if (row.status === 'business_trip') {
    return 'row-business-trip'
  }
  if (row.check_out_date) {
    return 'row-leave'
  }
  return ''
}

const fetchBuildings = async () => {
  try {
    const res = await buildingApi.list()
    buildings.value = res.items || res
  } catch (error) {
    ElMessage.error('获取楼栋列表失败')
  }
}

const fetchRooms = async () => {
  try {
    const res = await roomApi.list()
    rooms.value = res.items || res
  } catch (error) {
    ElMessage.error('获取房间列表失败')
  }
}

const searchEmployees = async (query: string) => {
  if (!query) {
    employees.value = []
    return
  }
  employeeSearching.value = true
  try {
    const res = await employeeApi.list({ keyword: query })
    employees.value = res.items || res
  } catch (error) {
    ElMessage.error('搜索员工失败')
  } finally {
    employeeSearching.value = false
  }
}

const fetchResidents = async () => {
  loading.value = true
  try {
    const params: any = {}
    if (filters.buildingId) params.building_id = filters.buildingId
    if (filters.roomId) params.room_id = filters.roomId
    if (filters.search) params.search = filters.search
    if (filters.statusTab !== 'all') params.status = filters.statusTab
    
    const res = await residenceApi.list(params)
    residents.value = res.items || res
  } catch (error) {
    ElMessage.error('获取入住列表失败')
  } finally {
    loading.value = false
  }
}

const handleFilterChange = () => {
  filters.roomId = undefined
  fetchResidents()
}

const handleSelectionChange = (selection: ResidenceRecord[]) => {
  selectedRows.value = selection
}

const handleEmployeeChange = (employeeId: number) => {
  const employee = employees.value.find((e: Employee) => e.id === employeeId)
  if (employee) {
    // Auto-populate employee info if needed
  }
}

const handleBuildingChange = async (buildingId: number) => {
  form.room_id = undefined
  try {
    const res = await roomApi.list({ building_id: buildingId })
    availableRooms.value = res.items || res
  } catch (error) {
    ElMessage.error('获取房间列表失败')
  }
}

const handleTransferBuildingChange = async (buildingId: number) => {
  batchTransferForm.room_id = undefined
  try {
    const res = await roomApi.list({ building_id: buildingId })
    transferAvailableRooms.value = res.items || res
  } catch (error) {
    ElMessage.error('获取房间列表失败')
  }
}

const handleAdd = () => {
  isEdit.value = false
  dialogVisible.value = true
}

const handleEdit = async (row: ResidenceRecord) => {
  isEdit.value = true
  
  // Load employee for select
  try {
    const empData = await employeeApi.list({ keyword: row.employee_name })
    employees.value = empData.items || empData
  } catch (error) {
    // Ignore
  }

  // Load rooms for building
  if (row.building_id) {
    try {
      const roomData = await roomApi.list({ building_id: row.building_id })
      availableRooms.value = roomData.items || roomData
    } catch (error) {
      // Ignore
    }
  }

  Object.assign(form, {
    id: row.id,
    employee_id: row.employee_id,
    building_id: row.building_id,
    room_id: row.room_id,
    check_in_date: row.check_in_date,
    probation_months: row.probation_months,
    is_primary: row.is_primary_payer === 1,
    status: row.status,
    remark: row.remark || ''
  })
  
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        if (isEdit.value && form.id) {
          await residenceApi.update(form.id, form)
          ElMessage.success('更新成功')
        } else {
          await residenceApi.create(form)
          ElMessage.success('创建成功')
        }
        dialogVisible.value = false
        fetchResidents()
      } catch (error) {
        ElMessage.error(isEdit.value ? '更新失败' : '创建失败')
      } finally {
        submitting.value = false
      }
    }
  })
}

const handleMoveOut = async (row: ResidenceRecord) => {
  try {
    const { value: date } = await ElMessageBox.prompt('请输入搬离日期', '确认搬离', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      inputType: 'date',
      inputPattern: /^\d{4}-\d{2}-\d{2}$/,
      inputErrorMessage: '请输入正确的日期格式'
    })
    
    await residenceApi.update(row.id, { check_out_date: date })
    ElMessage.success('搬离成功')
    fetchResidents()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('搬离失败')
    }
  }
}

const handleDelete = async (row: ResidenceRecord) => {
  try {
    await ElMessageBox.confirm('确定要删除这条入住记录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await residenceApi.delete(row.id)
    ElMessage.success('删除成功')
    fetchResidents()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const handleBatchMoveOut = async () => {
  if (!batchMoveOutDate.value) {
    ElMessage.warning('请选择搬离日期')
    return
  }

  batchSubmitting.value = true
  try {
    await residenceApi.batchMoveOut({
      residence_ids: selectedRows.value.map((r: ResidenceRecord) => r.id),
      check_out_date: batchMoveOutDate.value
    })
    ElMessage.success('批量搬离成功')
    showBatchMoveOutDialog.value = false
    batchMoveOutDate.value = ''
    fetchResidents()
  } catch (error) {
    ElMessage.error('批量搬离失败')
  } finally {
    batchSubmitting.value = false
  }
}

const handleBatchTransfer = async () => {
  if (!batchTransferForm.building_id || !batchTransferForm.room_id || !batchTransferForm.transfer_date) {
    ElMessage.warning('请填写完整的换房信息')
    return
  }

  batchSubmitting.value = true
  try {
    await residenceApi.batchTransfer({
      items: selectedRows.value.map((r: ResidenceRecord) => ({
        residence_id: r.id,
        target_room_id: batchTransferForm.room_id!
      })),
      transfer_date: batchTransferForm.transfer_date
    })
    ElMessage.success('批量换房成功')
    showBatchTransferDialog.value = false
    Object.assign(batchTransferForm, {
      building_id: undefined,
      room_id: undefined,
      transfer_date: ''
    })
    fetchResidents()
  } catch (error) {
    ElMessage.error('批量换房失败')
  } finally {
    batchSubmitting.value = false
  }
}

const resetForm = () => {
  Object.assign(form, {
    id: undefined,
    employee_id: undefined,
    building_id: undefined,
    room_id: undefined,
    check_in_date: '',
    probation_months: 0,
    is_primary: false,
    status: 'valid',
    remark: ''
  })
  employees.value = []
  availableRooms.value = []
  formRef.value?.resetFields()
}

onMounted(() => {
  fetchBuildings()
  fetchRooms()
  fetchResidents()
})

onActivated(() => {
  fetchResidents()
})
</script>

<style scoped>
.resident-list {
  padding: 20px;
}

.toolbar {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

:deep(.row-probation) {
  background-color: #fef9e7 !important;
}

:deep(.row-business-trip) {
  background-color: #ebf5ff !important;
}

:deep(.row-leave) {
  background-color: #f5f5f5 !important;
  color: #999;
}
</style>
