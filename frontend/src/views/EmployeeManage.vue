<template>
  <div class="employee-manage">
    <div class="toolbar">
      <el-input
        v-model="filters.search"
        placeholder="搜索工号或姓名"
        clearable
        style="width: 240px"
        @keyup.enter="fetchEmployees"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>

      <el-select
        v-model="filters.company"
        placeholder="任职单位"
        clearable
        style="width: 180px"
        @change="fetchEmployees"
      >
        <el-option
          v-for="org in organizations"
          :key="org"
          :label="org"
          :value="org"
        />
      </el-select>

      <el-select
        v-model="filters.department"
        placeholder="一级部门"
        clearable
        style="width: 180px"
        @change="fetchEmployees"
      >
        <el-option
          v-for="dept in departments"
          :key="dept"
          :label="dept"
          :value="dept"
        />
      </el-select>

      <el-select
        v-model="filters.status"
        placeholder="状态"
        clearable
        style="width: 120px"
        @change="fetchEmployees"
      >
        <el-option label="在职" value="active" />
        <el-option label="离职" value="inactive" />
      </el-select>

      <div style="flex: 1"></div>

      <el-button type="primary" @click="handleAdd">
        <el-icon><Plus /></el-icon>
        新增员工
      </el-button>

      <el-button type="success" @click="showImportDialog = true">
        <el-icon><Upload /></el-icon>
        导入Excel
      </el-button>
    </div>

    <el-table
      v-loading="loading"
      :data="employees"
      stripe
      border
      style="width: 100%"
    >
      <el-table-column prop="employee_no" label="工号" width="120" />
      <el-table-column prop="name" label="姓名" width="120" />
      <el-table-column prop="company" label="任职单位" min-width="180" />
      <el-table-column prop="department" label="一级部门" width="140" />
      <el-table-column prop="position" label="职务" width="140" />
      <el-table-column label="状态" width="80" align="center">
        <template #default="{ row }">
          <el-tag :type="row.status === 'active' ? 'success' : 'info'">
            {{ row.status === 'active' ? '在职' : '离职' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="remark" label="备注" min-width="150" show-overflow-tooltip />
      <el-table-column label="操作" width="150" fixed="right" align="center">
        <template #default="{ row }">
          <el-button link type="primary" @click="handleEdit(row)">编辑</el-button>
          <el-button link type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      v-model:current-page="pagination.page"
      v-model:page-size="pagination.pageSize"
      :total="pagination.total"
      :page-sizes="[10, 20, 50, 100]"
      layout="total, sizes, prev, pager, next, jumper"
      style="margin-top: 20px; justify-content: center"
      @size-change="fetchEmployees"
      @current-change="fetchEmployees"
    />

    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑员工' : '新增员工'"
      width="600px"
      @close="resetForm"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="工号" prop="employee_no">
          <el-input v-model="form.employee_no" placeholder="请输入工号" />
        </el-form-item>

        <el-form-item label="姓名" prop="name">
          <el-input v-model="form.name" placeholder="请输入姓名" />
        </el-form-item>

        <el-form-item label="任职单位" prop="company">
          <el-input v-model="form.company" placeholder="请输入任职单位" />
        </el-form-item>

        <el-form-item label="一级部门" prop="department">
          <el-input v-model="form.department" placeholder="请输入一级部门" />
        </el-form-item>

        <el-form-item label="职务">
          <el-input v-model="form.position" placeholder="请输入职务" />
        </el-form-item>

        <el-form-item label="状态">
          <el-radio-group v-model="form.status">
            <el-radio value="active">在职</el-radio>
            <el-radio value="inactive">离职</el-radio>
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

    <!-- 导入对话框 -->
    <el-dialog
      v-model="showImportDialog"
      title="导入员工Excel"
      width="700px"
      @close="resetImport"
    >
      <el-alert
        title="导入说明"
        type="info"
        :closable="false"
        style="margin-bottom: 20px"
      >
        <p>Excel 文件需包含以下列：工号、姓名、任职单位、一级部门、职务、状态、备注</p>
        <p>状态列填写：在职 或 离职</p>
      </el-alert>

      <el-upload
        ref="uploadRef"
        :auto-upload="false"
        :limit="1"
        accept=".xlsx,.xls"
        :on-change="handleFileChange"
        :on-exceed="handleExceed"
        drag
      >
        <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
        <div class="el-upload__text">
          拖拽文件到此处或 <em>点击上传</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            只支持 xlsx/xls 格式文件
          </div>
        </template>
      </el-upload>

      <div v-if="importPreview.length > 0" style="margin-top: 20px">
        <el-divider content-position="left">预览数据（前10条）</el-divider>
        <el-table :data="importPreview.slice(0, 10)" border max-height="300">
          <el-table-column prop="employee_no" label="工号" width="100" />
          <el-table-column prop="name" label="姓名" width="100" />
          <el-table-column prop="company" label="任职单位" min-width="150" />
          <el-table-column prop="department" label="一级部门" width="120" />
          <el-table-column prop="position" label="职务" width="120" />
          <el-table-column prop="status" label="状态" width="80" />
        </el-table>
        <div style="margin-top: 10px; color: #909399">
          共 {{ importPreview.length }} 条数据
        </div>
      </div>

      <template #footer>
        <el-button @click="showImportDialog = false">取消</el-button>
        <el-button 
          type="primary" 
          :loading="importing" 
          :disabled="!importFile"
          @click="handleImport"
        >
          确定导入
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules, type UploadInstance, type UploadFile } from 'element-plus'
import { Search, Plus, Upload, UploadFilled } from '@element-plus/icons-vue'
import { employeeApi } from '@/api/employee'
import type { Employee } from '@/types'

const loading = ref(false)
const submitting = ref(false)
const importing = ref(false)
const dialogVisible = ref(false)
const showImportDialog = ref(false)
const isEdit = ref(false)
const formRef = ref<FormInstance>()
const uploadRef = ref<UploadInstance>()

const employees = ref<Employee[]>([])
const organizations = ref<string[]>([])
const departments = ref<string[]>([])
const importFile = ref<File | null>(null)
const importPreview = ref<any[]>([])

const filters = reactive({
  search: '',
  company: '',
  department: '',
  status: ''
})

const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0
})

const form = reactive({
  id: undefined as number | undefined,
  employee_no: '',
  name: '',
  company: '',
  department: '',
  position: '',
  status: 'active' as 'active' | 'inactive',
  remark: ''
})

const rules: FormRules = {
  employee_no: [{ required: true, message: '请输入工号', trigger: 'blur' }],
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  company: [{ required: true, message: '请输入任职单位', trigger: 'blur' }],
  department: [{ required: true, message: '请输入一级部门', trigger: 'blur' }]
}

const fetchEmployees = async () => {
  loading.value = true
  try {
    const params: any = {
      page: pagination.page,
      page_size: pagination.pageSize
    }
    if (filters.search) params.search = filters.search
    if (filters.company) params.company = filters.company
    if (filters.department) params.department = filters.department
    if (filters.status) params.status = filters.status

    const response = await employeeApi.list(params)
    
    if (response.items) {
      employees.value = response.items
      pagination.total = response.total || 0
    } else {
      employees.value = []
      pagination.total = 0
    }

    // Extract unique organizations and departments
    const uniqueOrgs = new Set<string>()
    const uniqueDepts = new Set<string>()
    employees.value.forEach(emp => {
      if (emp.company) uniqueOrgs.add(emp.company)
      if (emp.department) uniqueDepts.add(emp.department)
    })
    organizations.value = Array.from(uniqueOrgs)
    departments.value = Array.from(uniqueDepts)
  } catch (error) {
    ElMessage.error('获取员工列表失败')
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  isEdit.value = false
  dialogVisible.value = true
}

const handleEdit = (row: Employee) => {
  isEdit.value = true
  Object.assign(form, {
    id: row.id,
    employee_no: row.employee_no,
    name: row.name,
    company: row.company,
    department: row.department,
    position: row.position || '',
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
          await employeeApi.update(form.id, form)
          ElMessage.success('更新成功')
        } else {
          await employeeApi.create(form)
          ElMessage.success('创建成功')
        }
        dialogVisible.value = false
        fetchEmployees()
      } catch (error) {
        ElMessage.error(isEdit.value ? '更新失败' : '创建失败')
      } finally {
        submitting.value = false
      }
    }
  })
}

const handleDelete = async (row: Employee) => {
  try {
    await ElMessageBox.confirm('确定要删除这个员工吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await employeeApi.delete(row.id)
    ElMessage.success('删除成功')
    fetchEmployees()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const handleFileChange = (uploadFile: UploadFile) => {
  if (uploadFile.raw) {
    importFile.value = uploadFile.raw
    parseExcelPreview(uploadFile.raw)
  }
}

const handleExceed = () => {
  ElMessage.warning('只能上传一个文件')
}

const parseExcelPreview = async (_file: File) => {
  try {
    // Simple preview - in production, you'd parse the Excel here
    // For now, we'll just set a placeholder
    importPreview.value = []
    ElMessage.info('文件已选择，点击"确定导入"开始导入')
  } catch (error) {
    ElMessage.error('文件解析失败')
  }
}

const handleImport = async () => {
  if (!importFile.value) {
    ElMessage.warning('请先选择文件')
    return
  }

  importing.value = true
  try {
    await employeeApi.import(importFile.value)
    ElMessage.success('导入成功')
    showImportDialog.value = false
    fetchEmployees()
  } catch (error) {
    ElMessage.error('导入失败')
  } finally {
    importing.value = false
  }
}

const resetForm = () => {
  Object.assign(form, {
    id: undefined,
    employee_no: '',
    name: '',
    company: '',
    department: '',
    position: '',
    status: 'active',
    remark: ''
  })
  formRef.value?.resetFields()
}

const resetImport = () => {
  importFile.value = null
  importPreview.value = []
  uploadRef.value?.clearFiles()
}

onMounted(() => {
  fetchEmployees()
})
</script>

<style scoped>
.employee-manage {
  padding: 20px;
}

.toolbar {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.el-icon--upload {
  font-size: 67px;
  color: #8c939d;
  margin-bottom: 16px;
}
</style>
