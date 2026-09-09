<template>
  <div class="search-bar">
    <el-input
      v-model="searchKeyword"
      :placeholder="placeholder"
      clearable
      @clear="handleClear"
      @keyup.enter="handleSearch"
    >
      <template #prefix>
        <el-icon><Search /></el-icon>
      </template>
    </el-input>
    <el-button type="primary" :icon="Search" @click="handleSearch">搜索</el-button>
    <el-button v-if="showAdd" type="primary" :icon="Plus" @click="handleAdd">
      {{ addText }}
    </el-button>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { Search, Plus } from '@element-plus/icons-vue';

interface Props {
  placeholder?: string;
  showAdd?: boolean;
  addText?: string;
  modelValue?: string;
}

interface Emits {
  (e: 'search', keyword: string): void;
  (e: 'clear'): void;
  (e: 'add'): void;
  (e: 'update:modelValue', value: string): void;
}

const props = withDefaults(defineProps<Props>(), {
  placeholder: '请输入关键词搜索',
  showAdd: false,
  addText: '新增',
  modelValue: '',
});

const emit = defineEmits<Emits>();

const searchKeyword = ref(props.modelValue);

watch(
  () => props.modelValue,
  (newVal) => {
    searchKeyword.value = newVal;
  }
);

watch(searchKeyword, (newVal) => {
  emit('update:modelValue', newVal);
});

const handleSearch = () => {
  emit('search', searchKeyword.value);
};

const handleClear = () => {
  emit('clear');
  emit('search', '');
};

const handleAdd = () => {
  emit('add');
};
</script>

<style scoped lang="scss">
.search-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background-color: #ffffff;
  border-radius: 8px;
  margin-bottom: 16px;
  
  .el-input {
    flex: 1;
    max-width: 400px;
  }
}
</style>
