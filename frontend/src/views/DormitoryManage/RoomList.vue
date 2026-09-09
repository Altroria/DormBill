<template>
  <div class="room-list">
    <div class="toolbar">
      <el-select
        v-model="filters.buildingId"
        placeholder="选择楼栋"
        clearable
        style="width: 200px"
        @change="fetchRooms"
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
        placeholder="搜索房号或房间名称"
        clearable
        style="width: 240px"
        @keyup.enter="fetchRooms"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>

      <el-button type="primary" @click="handleAdd">
        <el-icon><Plus /></el-icon>
        新增房间
      </el-button>

      <el-button type="success" @click="showBatchDialog = true">
        <el-icon><DocumentAdd /></el-icon>
        批量新增
      </el-button>
    </div>

    <el-table
      v-loading="loading"
      :data="rooms"
      stripe
      border
      style="width: 100%"
    >
      <el-table-column prop="building_no" label="楼栋编号" width="120" />
      <el-table-column prop="room_no" label="房号" width="100" />
      <el-table-column prop="room_name" label="房间名称" min-width="150" />
      <el-table-column prop="meter_no" label="电表编号" width="120" />
      <el-table-column prop="ac_meter_no" label="空调电表编号" width="140" />
      <el-table-column label="默认电价" width="110" align="right">
        <template #default="{ row }">
          ¥{{ row.electricity_price.toFixed(2) }}
        </template>
      </el-table-column>
      <el-table-column label="房租标准" width="110" align="right">
        <template #default="{ row }">
          ¥{{ row.rent_standard.toFixed(2) }}
        </template>
      </el-table-column>
      <el-table-column label="状态" width="80" align="center">
        <template #default="{ row }">
          <el-tag :type="row.status === 'active' ? 'success' : 'info'">
            {{ row.status === 'active' ? '启用' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="150" fixed="right" align="center">
        <template #default="{ row }">
          <el-button link type="primary" @click="handleEdit(row)">编辑</el-button>
          <el-button link type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑房间' : '新增房间'"
      width="600px"
      @close="resetForm"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="120px"
      >
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

        <el-form-item label="房号" prop="room_no">
          <el-input v-model="form.room_no" placeholder="请输入房号" />
        </el-form-item>

        <el-form-item label="房间名称" prop="room_name">
          <el-input v-model="form.room_name" placeholder="请输入房间名称" />
        </el-form-item>

        <el-form-item label="电表编号">
          <el-input v-model="form.meter_no" placeholder="请输入电表编号" />
        </el-form-item>

        <el-form-item label="空调电表编号">
          <el-input v-model="form.ac_meter_no" placeholder="请输入空调电表编号" />
        </el-form-item>

        <el-form-item label="默认电价" prop="electricity_price">
          <el-input-number
            v-model="form.electricity_price"
            :precision="2"
            :step="0.01"
            :min="0"
            style="width: 100%"
          />
        </el-form-item>

        <el-form-item label="房租标准" prop="rent_standard">
          <el-input-number
            v-model="form.rent_standard"
            :precision="2"
            :step="10"
            :min="0"
            style="width: 100%"
          />
        </el-form-item>

        <el-form-item label="状态">
          <el-radio-group v-model="form.status">
            <el-radio value="active">启用</el-radio>
            <el-radio value="inactive">禁用</el-radio>
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

    <!-- 批量新增对话框 -->
    <el-dialog
      v-model="showBatchDialog"
      title="批量新增房间"
      width="800px"
      @close="resetBatchForm"
    >
      <el-form label-width="100px">
        <el-form-item label="选择楼栋" required>
          <el-select
            v-model="batchForm.building_id"
            placeholder="请选择楼栋"
            style="width: 300px"
          >
            <el-option
              v-for="building in buildings"
              :key="building.id"
              :label="building.name"
              :value="building.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="房间列表">
          <div style="width: 100%">
            <el-button
              type="primary"
              size="small"
              @click="addBatchRow"
              style="margin-bottom: 10px"
            >
              <el-icon><Plus /></el-icon>
              添加行
            </el-button>

            <el-table :data="batchForm.items" border style="width: 100%">
              <el-table-column label="房号" width="120">
                <template #default="{ row }">
                  <el-input v-model="row.room_no" placeholder="房号" />
                </template>
              </el-table-column>
              <el-table-column label="房间名称" width="180">
                <template #default="{ row }">
                  <el-input v-model="row.room_name" placeholder="房间名称" />
                </template>
              </el-table-column>
              <el-table-column label="房租" width="150">
                <template #default="{ row }">
                  <el-input-number
                    v-model="row.rent_standard"
                    :precision="2"
                    :step="10"
                    :min="0"
                    style="width: 100%"
                  />
                </template>
              </el-table-column>
              <el-table-column label="电价" width="150">
                <template #default="{ row }">
                  <el-input-number
                    v-model="row.electricity_price"
                    :precision="2"
                    :step="0.01"
                    :min="0"
                    style="width: 100%"
                  />
                </template>
              </el-table-column>
              <el-table-column label="操作" width="80" align="center">
                <template #default="{ $index }">
                  <el-button
                    link
                    type="danger"
                    @click="removeBatchRow($index)"
                  >
                    删除
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="showBatchDialog = false">取消</el-button>
        <el-button type="primary" :loading="batchSubmitting" @click="handleBatchSubmit">
          确定新增
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { Search, Plus, DocumentAdd } from '@element-plus/icons-vue'
import { roomApi } from '@/api/room'
import { buildingApi } from '@/api/building'
import type { Room, Building } from '@/types'

const loading = ref(false)
const submitting = ref(false)
const batchSubmitting = ref(false)
const dialogVisible = ref(false)
const showBatchDialog = ref(false)
const isEdit = ref(false)
const formRef = ref<FormInstance>()

const rooms = ref<Room[]>([])
const buildings = ref<Building[]>([])

const filters = reactive({
  buildingId: undefined as number | undefined,
  search: ''
})

const form = reactive({
  id: undefined as number | undefined,
  building_id: undefined as number | undefined,
  room_no: '',
  room_name: '',
  meter_no: '',
  ac_meter_no: '',
  electricity_price: 0.49,
  rent_standard: 0,
  status: 'active' as 'active' | 'inactive',
  remark: ''
})

const batchForm = reactive({
  building_id: undefined as number | undefined,
  items: [] as Array<{
    room_no: string
    room_name: string
    rent_standard: number
    electricity_price: number
  }>
})

const rules: FormRules = {
  building_id: [{ required: true, message: '请选择楼栋', trigger: 'change' }],
  room_no: [{ required: true, message: '请输入房号', trigger: 'blur' }],
  room_name: [{ required: true, message: '请输入房间名称', trigger: 'blur' }],
  electricity_price: [{ required: true, message: '请输入默认电价', trigger: 'blur' }],
  rent_standard: [{ required: true, message: '请输入房租标准', trigger: 'blur' }]
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
  loading.value = true
  try {
    const params: any = {}
    if (filters.buildingId) {
      params.building_id = filters.buildingId
    }
    if (filters.search) {
      params.search = filters.search
    }
    const res = await roomApi.list(params)
    rooms.value = res.items || res
  } catch (error) {
    ElMessage.error('获取房间列表失败')
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  isEdit.value = false
  dialogVisible.value = true
}

const handleEdit = (row: Room) => {
  isEdit.value = true
  Object.assign(form, {
    id: row.id,
    building_id: row.building_id,
    room_no: row.room_no,
    room_name: row.room_name,
    meter_no: row.meter_no || '',
    ac_meter_no: row.ac_meter_no || '',
    electricity_price: row.electricity_price,
    rent_standard: row.rent_standard,
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
          await roomApi.update(form.id, form)
          ElMessage.success('更新成功')
        } else {
          await roomApi.create(form)
          ElMessage.success('创建成功')
        }
        dialogVisible.value = false
        fetchRooms()
      } catch (error) {
        ElMessage.error(isEdit.value ? '更新失败' : '创建失败')
      } finally {
        submitting.value = false
      }
    }
  })
}

const handleDelete = async (row: Room) => {
  try {
    await ElMessageBox.confirm('确定要删除这个房间吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await roomApi.delete(row.id)
    ElMessage.success('删除成功')
    fetchRooms()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const addBatchRow = () => {
  batchForm.items.push({
    room_no: '',
    room_name: '',
    rent_standard: 0,
    electricity_price: 0.49
  })
}

const removeBatchRow = (index: number) => {
  batchForm.items.splice(index, 1)
}

const handleBatchSubmit = async () => {
  if (!batchForm.building_id) {
    ElMessage.warning('请选择楼栋')
    return
  }
  if (batchForm.items.length === 0) {
    ElMessage.warning('请至少添加一行房间数据')
    return
  }

  const invalid = batchForm.items.some(
    room => !room.room_no || !room.room_name
  )
  if (invalid) {
    ElMessage.warning('请填写完整的房号和房间名称')
    return
  }

  batchSubmitting.value = true
  try {
    if (!batchForm.building_id) {
      ElMessage.warning('请选择楼栋')
      return
    }
    await roomApi.batchCreate(batchForm as { building_id: number; items: Partial<Room>[] })
    ElMessage.success('批量新增成功')
    showBatchDialog.value = false
    fetchRooms()
  } catch (error) {
    ElMessage.error('批量新增失败')
  } finally {
    batchSubmitting.value = false
  }
}

const resetForm = () => {
  Object.assign(form, {
    id: undefined,
    building_id: undefined,
    room_no: '',
    room_name: '',
    meter_no: '',
    ac_meter_no: '',
    electricity_price: 0.49,
    rent_standard: 0,
    status: 'active',
    remark: ''
  })
  formRef.value?.resetFields()
}

const resetBatchForm = () => {
  batchForm.building_id = undefined
  batchForm.items = []
}

onMounted(() => {
  fetchBuildings()
  fetchRooms()
})
</script>

<style scoped>
.room-list {
  padding: 20px;
}

.toolbar {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}
</style>
