<template>
  <div class="data-import">
    <el-card class="page-card" shadow="never">
      <!-- 页面头部 -->
      <div class="page-header">
        <div>
          <h2 class="page-title">数据导入</h2>
          <p class="page-desc">批量导入楼栋、房间、员工和入住信息</p>
        </div>
      </div>

      <!-- 导入说明 -->
      <el-alert
        title="导入说明"
        type="info"
        :closable="false"
        style="margin-bottom: 20px;"
      >
        <template #default>
          <div style="line-height: 1.8;">
            <p><strong>Excel 文件格式要求：</strong></p>
            <ul style="margin: 10px 0; padding-left: 20px;">
              <li>第1行为表头，包含：楼号 | 房号 | 室号 | 房间 | 任职单位 | 一级部门 | 职务 | 姓名 | 转宿日期，备注</li>
              <li>从第2行开始为数据行</li>
              <li>支持 .xls 和 .xlsx 格式</li>
            </ul>
            <p><strong>导入模式说明：</strong></p>
            <ul style="margin: 10px 0; padding-left: 20px;">
              <li><strong>更新模式</strong>：已存在的数据会被更新，不存在的会新建（推荐）</li>
              <li><strong>覆盖模式</strong>：会先清空所有入住记录，再重新导入（谨慎使用）</li>
              <li><strong>仅添加模式</strong>：只添加新数据，跳过已存在的记录</li>
            </ul>
          </div>
        </template>
      </el-alert>

      <!-- 导入表单 -->
      <el-form :model="form" label-width="100px" style="max-width: 600px;">
        <el-form-item label="导入模式">
          <el-radio-group v-model="form.mode">
            <el-radio value="update">更新模式</el-radio>
            <el-radio value="add_only">仅添加模式</el-radio>
            <el-radio value="override">覆盖模式</el-radio>
          </el-radio-group>
          <div style="color: #909399; font-size: 12px; margin-top: 5px;">
            <template v-if="form.mode === 'update'">
              推荐使用，会智能更新已有数据
            </template>
            <template v-else-if="form.mode === 'add_only'">
              只新增数据，不更新已有记录
            </template>
            <template v-else-if="form.mode === 'override'">
              ⚠️ 警告：会先清空所有入住记录！
            </template>
          </div>
        </el-form-item>

        <el-form-item label="选择文件">
          <el-upload
            ref="uploadRef"
            :auto-upload="false"
            :limit="1"
            :on-change="handleFileChange"
            :on-exceed="handleExceed"
            accept=".xls,.xlsx"
            drag
          >
            <el-icon class="el-icon--upload"><upload-filled /></el-icon>
            <div class="el-upload__text">
              将文件拖到此处，或<em>点击上传</em>
            </div>
            <template #tip>
              <div class="el-upload__tip">
                只能上传 xls/xlsx 文件
              </div>
            </template>
          </el-upload>
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            :loading="importing"
            :disabled="!selectedFile"
            @click="handleImport"
          >
            <el-icon v-if="!importing"><Upload /></el-icon>
            {{ importing ? '导入中...' : '开始导入' }}
          </el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 导入结果 -->
      <el-card v-if="importResult" shadow="hover" style="margin-top: 20px;">
        <template #header>
          <div style="display: flex; align-items: center; gap: 8px;">
            <el-icon v-if="importResult.success" style="color: #67C23A;" :size="20">
              <CircleCheck />
            </el-icon>
            <el-icon v-else style="color: #F56C6C;" :size="20">
              <CircleClose />
            </el-icon>
            <span>导入结果</span>
          </div>
        </template>

        <div v-if="importResult.success && importResult.stats">
          <el-descriptions :column="2" border>
            <el-descriptions-item label="楼栋">
              新建 {{ importResult.stats.buildings_created || 0 }} 个，
              更新 {{ importResult.stats.buildings_updated || 0 }} 个
            </el-descriptions-item>
            <el-descriptions-item label="房间">
              新建 {{ importResult.stats.rooms_created || 0 }} 个，
              更新 {{ importResult.stats.rooms_updated || 0 }} 个
            </el-descriptions-item>
            <el-descriptions-item label="员工">
              新建 {{ importResult.stats.employees_created || 0 }} 人，
              更新 {{ importResult.stats.employees_updated || 0 }} 人
            </el-descriptions-item>
            <el-descriptions-item label="入住记录">
              新建 {{ importResult.stats.residences_created || 0 }} 条，
              更新 {{ importResult.stats.residences_updated || 0 }} 条，
              跳过 {{ importResult.stats.residences_skipped || 0 }} 条
            </el-descriptions-item>
          </el-descriptions>

          <!-- 错误列表 -->
          <div v-if="importResult.stats?.errors && importResult.stats.errors.length > 0" style="margin-top: 20px;">
            <el-divider content-position="left">
              <span style="color: #F56C6C;">错误信息（{{ importResult.stats.errors.length }} 条）</span>
            </el-divider>
            <el-scrollbar max-height="200px">
              <div v-for="(error, index) in importResult.stats.errors.slice(0, 20)" :key="index" 
                   style="padding: 5px 0; font-size: 13px; color: #606266;">
                <el-icon style="color: #F56C6C;"><WarningFilled /></el-icon>
                第 {{ error.row }} 行: {{ error.msg }}
              </div>
              <div v-if="importResult.stats.errors.length > 20" style="padding: 5px 0; color: #909399;">
                ... 还有 {{ importResult.stats.errors.length - 20 }} 条错误
              </div>
            </el-scrollbar>
          </div>
        </div>

        <el-alert v-else :title="importResult.message" type="error" :closable="false" />
      </el-card>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { ElMessage, ElMessageBox, type UploadInstance, type UploadFile, type UploadFiles } from 'element-plus';
import {
  UploadFilled,
  Upload,
  CircleCheck,
  CircleClose,
  WarningFilled,
} from '@element-plus/icons-vue';
import api from '@/api/index';

const uploadRef = ref<UploadInstance>();
const selectedFile = ref<File | null>(null);
const importing = ref(false);
const importResult = ref<any>(null);

const form = reactive({
  mode: 'update',
});

const handleFileChange = (file: UploadFile, files: UploadFiles) => {
  selectedFile.value = file.raw || null;
  importResult.value = null;
};

const handleExceed = () => {
  ElMessage.warning('只能上传一个文件');
};

const handleReset = () => {
  uploadRef.value?.clearFiles();
  selectedFile.value = null;
  importResult.value = null;
  form.mode = 'update';
};

const handleImport = async () => {
  if (!selectedFile.value) {
    ElMessage.warning('请先选择文件');
    return;
  }

  // 覆盖模式需要二次确认
  if (form.mode === 'override') {
    try {
      await ElMessageBox.confirm(
        '覆盖模式会先清空所有入住记录，再重新导入。此操作不可恢复，确定要继续吗？',
        '警告',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
        }
      );
    } catch {
      return;
    }
  }

  importing.value = true;
  importResult.value = null;

  try {
    const formData = new FormData();
    formData.append('file', selectedFile.value);

    const response = await api.post<any>(
      `/import/personnel?mode=${form.mode}`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );

    console.log('API 响应:', response);
    console.log('stats:', response.stats);

    importResult.value = {
      success: true,
      stats: response.stats,
      errors: response.stats?.errors || [],
    };

    ElMessage.success('导入成功！');
  } catch (error: any) {
    console.error('导入失败:', error);
    importResult.value = {
      success: false,
      message: error.response?.data?.detail || error.message || '导入失败',
    };
    ElMessage.error('导入失败：' + importResult.value.message);
  } finally {
    importing.value = false;
  }
};
</script>

<style scoped>
.data-import {
  padding: 20px;
}

.page-card {
  border-radius: 8px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 8px 0;
}

.page-desc {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
}

:deep(.el-upload-dragger) {
  padding: 40px;
}

:deep(.el-icon--upload) {
  font-size: 67px;
  color: #c0c4cc;
  margin-bottom: 16px;
}

:deep(.el-upload__text) {
  color: #606266;
  font-size: 14px;
}

:deep(.el-upload__text em) {
  color: #409eff;
  font-style: normal;
}
</style>
