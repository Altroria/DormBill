<template>
  <div class="water-meter-page">
    <!-- 顶部筛选和操作栏 -->
    <el-card class="filter-card" shadow="never">
      <el-form inline :model="filterForm">
        <el-form-item label="月份">
          <el-date-picker
            v-model="filterForm.month"
            type="month"
            placeholder="选择月份"
            value-format="YYYY-MM"
            style="width: 150px"
          />
        </el-form-item>
        
        <el-form-item label="楼栋">
          <el-select
            v-model="filterForm.buildingId"
            placeholder="选择楼栋"
            clearable
            style="width: 150px"
          >
            <el-option
              v-for="building in buildings"
              :key="building.id"
              :label="`${building.building_no}栋`"
              :value="building.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="房号">
          <el-input
            v-model="filterForm.roomNo"
            placeholder="模糊搜索"
            clearable
            style="width: 120px"
            @keyup.enter="loadData"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" :icon="Search" @click="loadData">
            查询
          </el-button>
          <el-button type="info" :loading="initializing" @click="initMonth">
            初始化月份
          </el-button>
          <el-button
            type="success"
            :icon="Check"
            :loading="saving"
            :disabled="!hasChanges"
            @click="batchSave"
          >
            批量保存{{ changedCount > 0 ? ` (${changedCount})` : '' }}
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 数据加载状态 -->
    <el-card v-loading="loading" class="content-card" shadow="never">
      <template v-if="!loading && waterMeterData.length === 0 && hasSearched">
        <el-empty description="暂无数据">
          <template #description>
            <div style="margin-bottom: 16px; color: #909399;">
              当前筛选条件下没有水费记录
            </div>
            <div style="margin-bottom: 16px; color: #606266;">
              如果是新月份，请先点击"初始化月份"按钮创建水费记录
            </div>
            <el-button type="primary" :loading="initializing" @click="initMonth">
              立即初始化
            </el-button>
          </template>
        </el-empty>
      </template>
      
      <template v-if="!loading && !hasSearched">
        <el-empty description="请选择月份和楼栋，然后点击查询按钮加载数据" />
      </template>

      <!-- 统计信息和表格 -->
      <template v-if="waterMeterData.length > 0">
        <!-- 水费数据表格 -->
        <el-table
          :data="waterMeterData"
          border
          stripe
          size="default"
          style="width: 100%"
          max-height="calc(100vh - 320px)"
          :header-cell-style="{ background: '#f5f7fa', color: '#606266', fontWeight: '600', fontSize: '13px' }"
          :cell-style="{ fontSize: '13px' }"
        >
        <el-table-column type="index" label="序号" width="70" align="center" fixed />
        
        <el-table-column label="楼栋" width="100" align="center" fixed>
          <template #default="{ row }">
            <el-tag type="info" size="small" effect="plain">
              {{ row.building_no }}栋
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column label="房号" width="120" align="center" fixed>
          <template #default="{ row }">
            <el-text style="font-weight: 600; font-size: 14px; color: #303133;">
              {{ row.room_no }}
            </el-text>
          </template>
        </el-table-column>

        <el-table-column label="入住人数" width="110" align="center">
          <template #default="{ row }">
            <el-tag 
              :type="row.occupants_count > 0 ? 'success' : 'info'" 
              size="small"
              effect="light"
            >
              {{ row.occupants_count }} 人
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column label="总水费" width="200" align="center">
          <template #default="{ row }">
            <div style="display: flex; align-items: center; justify-content: center; gap: 8px;">
              <el-input-number
                v-model="row.total_fee"
                :precision="2"
                :step="10"
                :min="0"
                size="small"
                controls-position="right"
                style="width: 150px"
                @change="onChange(row)"
              />
              <span style="color: #909399; font-size: 12px;">元</span>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="人均水费" width="140" align="center">
          <template #default="{ row }">
            <div style="display: flex; flex-direction: column; align-items: center; gap: 4px; padding: 4px 0;">
              <el-text 
                :type="row.occupants_count === 0 ? 'info' : 'danger'" 
                style="font-weight: 600; font-size: 16px;"
              >
                ¥{{ calculatePerPersonFee(row).toFixed(2) }}
              </el-text>
              <el-text v-if="row.occupants_count === 0" size="small" type="info">
                无人入住
              </el-text>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="操作" width="100" align="center" fixed="right">
          <template #default="{ row }">
            <el-tag 
              v-if="changesMap.has(getRowKey(row))" 
              type="warning" 
              size="small"
              effect="dark"
            >
              待保存
            </el-tag>
            <el-text v-else type="success" size="small">
              ✓ 已同步
            </el-text>
          </template>
        </el-table-column>
        </el-table>
      </template>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Check } from '@element-plus/icons-vue'
import { waterMeterV2Api, type WaterMeterItem } from '@/api/water_meter_v2'
import type { Building } from '@/types'
import { buildingApi } from '@/api/building'

// 数据状态
const loading = ref(false)
const saving = ref(false)
const initializing = ref(false)
const hasSearched = ref(false)
const buildings = ref<Building[]>([])
const waterMeterData = ref<WaterMeterItem[]>([])

// 筛选表单
const filterForm = reactive({
  month: '',
  buildingId: undefined as number | undefined,
  roomNo: '',
})

// 变更跟踪
const changesMap = ref(new Map<string, boolean>())

// 计算属性
const hasChanges = computed(() => changesMap.value.size > 0)
const changedCount = computed(() => changesMap.value.size)

// 加载楼栋列表
const loadBuildings = async () => {
  try {
    const response = await buildingApi.list()
    buildings.value = response.items
  } catch (error) {
    ElMessage.error('加载楼栋列表失败')
  }
}

// 初始化月份
const initMonth = async () => {
  if (!filterForm.month) {
    ElMessage.warning('请选择月份')
    return
  }

  try {
    await ElMessageBox.confirm(
      `确定要初始化 ${filterForm.month} 的水费记录吗？` +
      (filterForm.buildingId ? '（仅选中的楼栋）' : '（所有楼栋）') +
      '\n\n初始化后会自动创建所有房间的水费记录。',
      '确认初始化',
      { 
        type: 'info',
        confirmButtonText: '确定初始化',
        cancelButtonText: '取消'
      }
    )

    initializing.value = true

    const response = await waterMeterV2Api.initMonth({
      month: filterForm.month,
      building_id: filterForm.buildingId,
    })

    ElMessage.success(
      `初始化成功！创建了 ${response.water_meter_count} 个房间水费记录`
    )

    // 自动加载数据
    await loadData()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '初始化失败')
    }
  } finally {
    initializing.value = false
  }
}

// 加载水费数据
const loadData = async () => {
  if (!filterForm.month) {
    ElMessage.warning('请选择月份')
    return
  }

  loading.value = true
  hasSearched.value = true
  changesMap.value.clear()

  try {
    const response = await waterMeterV2Api.list({
      month: filterForm.month,
      building_id: filterForm.buildingId,
      room_no: filterForm.roomNo,
      skip: 0,
      limit: 500,
    })

    waterMeterData.value = response.items

    if (response.items.length === 0) {
      ElMessage.info('没有找到符合条件的数据')
    } else {
      ElMessage.success(`加载成功，共 ${response.items.length} 个房间`)
    }
  } catch (error: any) {
    ElMessage.error(error.message || '加载数据失败')
  } finally {
    loading.value = false
  }
}

// 获取行的唯一键
const getRowKey = (row: WaterMeterItem) => {
  return `${row.building_id}-${row.room_no}`
}

// 通用变更
const onChange = (row: WaterMeterItem) => {
  const key = getRowKey(row)
  changesMap.value.set(key, true)
}

// 计算人均水费
const calculatePerPersonFee = (row: WaterMeterItem) => {
  if (row.occupants_count > 0) {
    return row.total_fee / row.occupants_count
  }
  return 0
}

// 批量保存
const batchSave = async () => {
  if (!hasChanges.value) {
    ElMessage.warning('没有需要保存的变更')
    return
  }

  try {
    await ElMessageBox.confirm(
      `确定要保存 ${changedCount.value} 个房间的水费数据吗？`,
      '确认保存',
      { type: 'warning' }
    )

    saving.value = true

    // 构建批量更新数据
    const updates = waterMeterData.value
      .filter(row => changesMap.value.has(getRowKey(row)))
      .map(row => ({
        building_id: row.building_id,
        room_no: row.room_no,
        total_fee: row.total_fee,
      }))

    // 调用批量更新API
    const response = await waterMeterV2Api.batchUpdate({
      month: filterForm.month,
      updates,
    })

    ElMessage.success(response.message)
    changesMap.value.clear()

    // 重新加载数据
    await loadData()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '保存失败')
    }
  } finally {
    saving.value = false
  }
}

// 初始化
onMounted(() => {
  loadBuildings()
  
  // 设置默认月份为当前月份
  const now = new Date()
  filterForm.month = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`
})
</script>

<style scoped lang="scss">
.water-meter-page {
  padding: 20px;
  background: #f5f7fa;
  min-height: 100vh;
}

.filter-card {
  margin-bottom: 16px;
  border-radius: 8px;
  
  :deep(.el-card__body) {
    padding: 16px 20px;
  }
}

.content-card {
  border-radius: 8px;
  
  :deep(.el-card__body) {
    padding: 20px;
  }
}

:deep(.el-table) {
  .el-table__body-wrapper {
    .el-table__row:hover {
      background: #f0f9ff;
    }
  }
}
</style>
