<template>
  <el-dialog
    v-model="visible"
    :title="title"
    :width="width"
    :close-on-click-modal="false"
    @closed="handleClosed"
  >
    <slot />
    <template #footer>
      <slot name="footer">
        <el-button @click="handleCancel">{{ cancelText }}</el-button>
        <el-button type="primary" :loading="confirmLoading" @click="handleConfirm">
          {{ confirmText }}
        </el-button>
      </slot>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Props {
  modelValue: boolean;
  title?: string;
  width?: string | number;
  confirmText?: string;
  cancelText?: string;
  confirmLoading?: boolean;
}

interface Emits {
  (e: 'update:modelValue', value: boolean): void;
  (e: 'confirm'): void;
  (e: 'cancel'): void;
  (e: 'closed'): void;
}

const props = withDefaults(defineProps<Props>(), {
  title: '提示',
  width: '500px',
  confirmText: '确定',
  cancelText: '取消',
  confirmLoading: false,
});

const emit = defineEmits<Emits>();

const visible = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val),
});

const handleConfirm = () => {
  emit('confirm');
};

const handleCancel = () => {
  visible.value = false;
  emit('cancel');
};

const handleClosed = () => {
  emit('closed');
};
</script>

<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
  name: 'ConfirmDialog',
});
</script>

<style scoped lang="scss">
// 样式已在 Element Plus Dialog 覆盖中定义
</style>
