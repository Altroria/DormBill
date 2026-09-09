<template>
  <div class="building-list">
    <div class="page-header">
      <h2>楼栋管理</h2>
      <el-button type="primary" :icon="Plus" @click="showDialog()">新增楼栋</el-button>
    </div>

    <el-card shadow="never">
      <div class="toolbar">
        <el-input
          v-model="search"
          placeholder="搜索楼栋编号/名称"
          clearable
          style="width: 280px"
          :prefix-icon="Search"
          @input="loadData"
        />
        <el-select v-model="statusFilter" placeholder="状态筛选" clearable style="width: 150px" @change="loadData">
          <el-option label="使用中" value="active" />
          <el-option label="停用" value="inactive" />
        </el-select>
      </div>

      <el-table :data="list" v-loading="loading" stripe>
        <el-table-column prop="building_no" label="楼栋编号" width="120" />
        <el-table-column prop="name" label="楼栋名称" width="150" />
        <el-table-column prop="address" label="地址" min-width="200" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'info'">
              {{ row.status === 'active' ? '使用中' : '停用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="remark" label="备注" min-width="150" show-overflow-tooltip />
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button text type="primary" :icon="Edit" @click="showDialog(row)">编辑</el-button>
            <el-button text type="danger" :icon="Delete" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog
      v-model="dialogVisible"
      :title="form.id ? '编辑楼栋' : '新增楼栋'"
      width="500px"
      @close="resetForm"
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="楼栋编号" prop="building_no">
          <el-input v-model="form.building_no" placeholder="如: 247" />
        </el-form-item>
        <el-form-item label="楼栋名称" prop="name">
          <el-input v-model="form.name" placeholder="如: 247栋" />
        </el-form-item>
        <el-form-item label="地址" prop="address">
          <el-input v-model="form.address" placeholder="详细地址" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="form.status">
            <el-radio value="active">使用中</el-radio>
            <el-radio value="inactive">停用</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input v-model="form.remark" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus';
import { Plus, Search, Edit, Delete } from '@element-plus/icons-vue';
import { buildingApi } from '@/api/building';
import type { Building } from '@/types';

const search = ref('');
const statusFilter = ref('');
const loading = ref(false);
const list = ref<Building[]>([]);

const dialogVisible = ref(false);
const submitting = ref(false);
const formRef = ref<FormInstance>();
const form = reactive<Partial<Building>>({
  building_no: '',
  name: '',
  address: '',
  status: 'active',
  remark: '',
});

const rules: FormRules = {
  building_no: [{ required: true, message: '请输入楼栋编号', trigger: 'blur' }],
};

async function loadData() {
  loading.value = true;
  try {
    const res = await buildingApi.list({ keyword: search.value, status: statusFilter.value });
    list.value = res.items;
  } finally {
    loading.value = false;
  }
}

function showDialog(row?: Building) {
  if (row) {
    Object.assign(form, row);
  } else {
    resetForm();
  }
  dialogVisible.value = true;
}

function resetForm() {
  formRef.value?.resetFields();
  Object.assign(form, {
    id: undefined,
    building_no: '',
    name: '',
    address: '',
    status: 'active',
    remark: '',
  });
}

async function handleSubmit() {
  await formRef.value?.validate();
  submitting.value = true;
  try {
    if (form.id) {
      await buildingApi.update(form.id, form);
      ElMessage.success('更新成功');
    } else {
      await buildingApi.create(form);
      ElMessage.success('创建成功');
    }
    dialogVisible.value = false;
    loadData();
  } finally {
    submitting.value = false;
  }
}

async function handleDelete(row: Building) {
  await ElMessageBox.confirm('确认删除该楼栋？', '提示', { type: 'warning' });
  await buildingApi.delete(row.id);
  ElMessage.success('删除成功');
  loadData();
}

onMounted(loadData);
</script>

<style scoped lang="scss">
.building-list {
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    
    h2 {
      margin: 0;
      font-size: 1.5rem;
      font-weight: 600;
      color: #1E293B;
    }
  }

  .toolbar {
    display: flex;
    gap: 12px;
    margin-bottom: 16px;
  }
}
</style>
