<template>
  <div class="data-table">
    <el-table
      :data="data"
      :loading="loading"
      v-bind="$attrs"
      stripe
      border
      highlight-current-row
    >
      <slot />
      
      <!-- 默认操作列 -->
      <el-table-column
        v-if="showActions"
        :label="actionsLabel"
        :width="actionsWidth"
        fixed="right"
        align="center"
      >
        <template #default="{ row }">
          <slot name="actions" :row="row">
            <el-button
              v-if="showEdit"
              type="primary"
              link
              size="small"
              :icon="Edit"
              @click="handleEdit(row)"
            >
              编辑
            </el-button>
            <el-button
              v-if="showDelete"
              type="danger"
              link
              size="small"
              :icon="Delete"
              @click="handleDelete(row)"
            >
              删除
            </el-button>
          </slot>
        </template>
      </el-table-column>
    </el-table>
    
    <!-- 分页 -->
    <div v-if="showPagination" class="pagination-wrapper">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        :total="total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts" generic="T extends Record<string, unknown>">
import { Edit, Delete } from '@element-plus/icons-vue';

interface Props {
  data: T[];
  loading?: boolean;
  showActions?: boolean;
  actionsLabel?: string;
  actionsWidth?: number | string;
  showEdit?: boolean;
  showDelete?: boolean;
  showPagination?: boolean;
  total?: number;
  currentPage?: number;
  pageSize?: number;
}

interface Emits {
  (e: 'edit', row: T): void;
  (e: 'delete', row: T): void;
  (e: 'page-change', page: number): void;
  (e: 'size-change', size: number): void;
  (e: 'update:currentPage', page: number): void;
  (e: 'update:pageSize', size: number): void;
}

const props = withDefaults(defineProps<Props>(), {
  loading: false,
  showActions: true,
  actionsLabel: '操作',
  actionsWidth: 160,
  showEdit: true,
  showDelete: true,
  showPagination: false,
  total: 0,
  currentPage: 1,
  pageSize: 10,
});

const emit = defineEmits<Emits>();

const currentPage = computed({
  get: () => props.currentPage,
  set: (val) => emit('update:currentPage', val),
});

const pageSize = computed({
  get: () => props.pageSize,
  set: (val) => emit('update:pageSize', val),
});

const handleEdit = (row: T) => {
  emit('edit', row);
};

const handleDelete = (row: T) => {
  emit('delete', row);
};

const handleSizeChange = (size: number) => {
  emit('size-change', size);
};

const handleCurrentChange = (page: number) => {
  emit('page-change', page);
};
</script>

<script lang="ts">
import { defineComponent, computed } from 'vue';
export default defineComponent({
  name: 'DataTable',
});
</script>

<style scoped lang="scss">
.data-table {
  background-color: #ffffff;
  border-radius: 8px;
  overflow: hidden;
}

.pagination-wrapper {
  display: flex;
  justify-content: flex-end;
  padding: 16px;
  border-top: 1px solid #E2E8F0;
}
</style>
