<template>
  <div class="meter-input-page">
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
        
        <el-form-item>
          <el-button type="primary" :icon="Search" @click="loadData">
            加载数据
          </el-button>
          <el-button
            type="success"
            :icon="Check"
            :loading="saving"
            :disabled="!hasChanges"
            @click="batchSave"
          >
            批量保存 {{ changedCount > 0 ? `(${changedCount})` : '' }}
          </el-button>
          <el-button
            type="warning"
            :loading="calculating"
            @click="calculate"
          >
            计算电费
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 数据加载状态 -->
    <el-card v-loading="loading" class="content-card" shadow="never">
      <template v-if="!loading && meterData.length === 0">
        <el-empty description="暂无数据，请选择月份和楼栋后加载" />
      </template>

      <!-- 按房号分组的折叠面板 -->
      <el-collapse v-else v-model="activeRooms" accordion>
        <el-collapse-item
          v-for="room in meterData"
          :key="`${room.building_id}-${room.room_no}`"
          :name="`${room.building_id}-${room.room_no}`"
        >
          <!-- 房号标题 -->
          <template #title>
            <div class="room-header">
              <span class="room-no">{{ room.room_no }}号房</span>
              <el-tag size="small" type="info">{{ room.total_occupants }}人</el-tag>
              <el-tag
                v-if="room.status === 'calculated'"
                size="small"
                type="success"
              >
                已计算
              </el-tag>
              <el-tag
                v-if="room.status === 'recorded'"
                size="small"
                type="warning"
              >
                已录入
              </el-tag>
              <el-tag
                v-if="isRoomChanged(room)"
                size="small"
                type="danger"
              >
                待保存
              </el-tag>
            </div>
          </template>

          <!-- 总电表区域 -->
          <div class="main-meter-section">
            <h4 class="section-title">总电表</h4>
            <el-form label-width="100px" size="default">
              <el-row :gutter="20">
                <el-col :span="6">
                  <el-form-item label="上月读数">
                    <el-input
                      :value="room.main_previous_reading.toFixed(2)"
                      disabled
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="6">
                  <el-form-item label="本月读数">
                    <el-input-number
                      v-model="room.main_current_reading"
                      :precision="2"
                      :step="1"
                      :min="room.main_previous_reading"
                      style="width: 100%"
                      @change="onMainMeterChange(room)"
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="6">
                  <el-form-item label="用电量">
                    <el-input
                      :value="calculateMainDegree(room).toFixed(2)"
                      disabled
                      suffix-icon="Lightning"
                    >
                      <template #suffix>度</template>
                    </el-input>
                  </el-form-item>
                </el-col>
                <el-col :span="6">
                  <el-form-item label="总电费">
                    <el-input
                      :value="calculateMainFee(room).toFixed(2)"
                      disabled
                    >
                      <template #suffix>元</template>
                    </el-input>
                  </el-form-item>
                </el-col>
              </el-row>
            </el-form>
          </div>

          <!-- 空调表列表 -->
          <div class="ac-meters-section">
            <h4 class="section-title">空调电表（按套间）</h4>
            <el-table
              :data="room.ac_meters"
              size="default"
              border
              stripe
              style="width: 100%"
            >
              <el-table-column label="套间" width="80" align="center">
                <template #default="{ row }">
                  <el-tag size="small">{{ row.room_unit || '-' }}</el-tag>
                </template>
              </el-table-column>
              
              <el-table-column label="入住人数" width="100" align="center">
                <template #default="{ row }">
                  <el-text type="primary">{{ row.occupants || 0 }}人</el-text>
                </template>
              </el-table-column>
              
              <el-table-column label="上月读数" width="120" align="right">
                <template #default="{ row }">
                  {{ row.ac_previous_reading.toFixed(2) }}
                </template>
              </el-table-column>
              
              <el-table-column label="本月读数" width="180">
                <template #default="{ row }">
                  <el-input-number
                    v-model="row.ac_current_reading"
                    :precision="2"
                    :step="1"
                    :min="row.ac_previous_reading"
                    size="small"
                    controls-position="right"
                    style="width: 100%"
                    @change="onAcMeterChange(room)"
                  />
                </template>
              </el-table-column>
              
              <el-table-column label="空调用电" width="120" align="right">
                <template #default="{ row }">
                  {{ calculateAcDegree(row).toFixed(2) }} 度
                </template>
              </el-table-column>
              
              <el-table-column label="空调电费" width="120" align="right">
                <template #default="{ row }">
                  ¥{{ calculateAcFee(row).toFixed(2) }}
                </template>
              </el-table-column>
              
              <el-table-column label="人均空调费" align="right">
                <template #default="{ row }">
                  ¥{{ (row.occupants > 0 ? calculateAcFee(row) / row.occupants : 0).toFixed(2) }}
                </template>
              </el-table-column>
            </el-table>
          </div>

          <!-- 计算结果预览 -->
          <div v-if="room.status === 'calculated'" class="calculation-preview">
            <el-divider content-position="left">
              <el-icon><TrendCharts /></el-icon>
              电费分摊结果
            </el-divider>
            <el-descriptions :column="3" size="default" border>
              <el-descriptions-item label="总用电">
                <el-text type="primary" size="large">
                  {{ room.main_total_degree.toFixed(2) }} 度
                </el-text>
              </el-descriptions-item>
              <el-descriptions-item label="空调用电">
                <el-text type="warning" size="large">
                  {{ room.total_ac_degree.toFixed(2) }} 度
                </el-text>
              </el-descriptions-item>
              <el-descriptions-item label="公共用电">
                <el-text type="success" size="large">
                  {{ room.common_degree.toFixed(2) }} 度
                </el-text>
              </el-descriptions-item>
              <el-descriptions-item label="总电费">
                ¥{{ room.main_total_fee.toFixed(2) }}
              </el-descriptions-item>
              <el-descriptions-item label="空调电费">
                ¥{{ room.total_ac_fee.toFixed(2) }}
              </el-descriptions-item>
              <el-descriptions-item label="公共电费">
                ¥{{ room.common_fee.toFixed(2) }}
              </el-descriptions-item>
              <el-descriptions-item label="人均公共电费" :span="3">
                <el-text type="danger" size="large">
                  ¥{{ room.common_fee_per_person.toFixed(2) }} / 人
                </el-text>
              </el-descriptions-item>
            </el-descriptions>
          </div>
        </el-collapse-item>
      </el-collapse>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Check } from '@element-plus/icons-vue'
import { meterV2Api, type EnhancedMeterListItem, type RoomNoBatchUpdateItem } from '@/api/meter_v2'
import type { Building } from '@/types'
import { buildingApi } from '@/api/building'

// 数据状态
const loading = ref(false)
const saving = ref(false)
const calculating = ref(false)
const buildings = ref<Building[]>([])
const meterData = ref<EnhancedMeterListItem[]>([])
const activeRooms = ref<string[]>([])

// 筛选表单
const filterForm = reactive({
  month: '',
  buildingId: undefined as number | undefined,
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

// 加载电表数据
const loadData = async () => {
  if (!filterForm.month) {
    ElMessage.warning('请选择月份')
    return
  }

  loading.value = true
  changesMap.value.clear()

  try {
    const response = await meterV2Api.listEnhanced({
      month: filterForm.month,
      building_id: filterForm.buildingId,
      skip: 0,
      limit: 500,
    })

    meterData.value = response.items

    ElMessage.success(`加载成功，共 ${response.items.length} 个房号`)
  } catch (error: any) {
    ElMessage.error(error.message || '加载数据失败')
  } finally {
    loading.value = false
  }
}

// 计算总表用电量
const calculateMainDegree = (room: EnhancedMeterListItem) => {
  return Math.max(0, room.main_current_reading - room.main_previous_reading)
}

// 计算总表电费 (0.49元/度)
const calculateMainFee = (room: EnhancedMeterListItem) => {
  return calculateMainDegree(room) * 0.49
}

// 计算空调用电量
const calculateAcDegree = (acMeter: any) => {
  return Math.max(0, acMeter.ac_current_reading - acMeter.ac_previous_reading)
}

// 计算空调电费 (0.49元/度)
const calculateAcFee = (acMeter: any) => {
  return calculateAcDegree(acMeter) * 0.49
}

// 总表读数变更
const onMainMeterChange = (room: EnhancedMeterListItem) => {
  const key = `${room.building_id}-${room.room_no}`
  changesMap.value.set(key, true)
}

// 空调表读数变更
const onAcMeterChange = (room: EnhancedMeterListItem) => {
  const key = `${room.building_id}-${room.room_no}`
  changesMap.value.set(key, true)
}

// 判断房号是否有变更
const isRoomChanged = (room: EnhancedMeterListItem) => {
  const key = `${room.building_id}-${room.room_no}`
  return changesMap.value.has(key)
}

// 批量保存
const batchSave = async () => {
  if (!hasChanges.value) {
    ElMessage.warning('没有需要保存的变更')
    return
  }

  try {
    await ElMessageBox.confirm(
      `确定要保存 ${changedCount.value} 个房号的电表数据吗？`,
      '确认保存',
      { type: 'warning' }
    )

    saving.value = true

    // 构建批量更新数据
    const updates: RoomNoBatchUpdateItem[] = []

    for (const room of meterData.value) {
      const key = `${room.building_id}-${room.room_no}`
      if (changesMap.value.has(key)) {
        updates.push({
          building_id: room.building_id,
          room_no: room.room_no,
          main_current_reading: room.main_current_reading,
          main_meter_no: undefined,
          ac_meters: room.ac_meters.map(ac => ({
            room_id: ac.room_id,
            ac_current_reading: ac.ac_current_reading,
          })),
        })
      }
    }

    // 调用批量更新API
    const response = await meterV2Api.batchUpdate({
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

// 计算电费
const calculate = async () => {
  if (!filterForm.month) {
    ElMessage.warning('请选择月份')
    return
  }

  if (hasChanges.value) {
    ElMessage.warning('请先保存变更的数据，再进行计算')
    return
  }

  try {
    await ElMessageBox.confirm(
      '确定要计算电费吗？计算将自动完成公共用电分摊和个人费用分配。',
      '确认计算',
      { type: 'warning' }
    )

    calculating.value = true

    const response = await meterV2Api.calculateEnhanced({
      month: filterForm.month,
      building_id: filterForm.buildingId,
      calculate_distribution: true,
    })

    ElMessage.success(
      `计算完成！共计算 ${response.main_meters_calculated} 个房号，` +
      `生成 ${response.distributions_created} 条个人分摊记录`
    )

    // 重新加载数据
    await loadData()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '计算失败')
    }
  } finally {
    calculating.value = false
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
.meter-input-page {
  padding: 20px;
}

.filter-card {
  margin-bottom: 20px;
  
  :deep(.el-card__body) {
    padding: 16px 20px;
  }
}

.content-card {
  :deep(.el-card__body) {
    padding: 20px;
  }
}

.room-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 4px 0;
  font-size: 15px;
  
  .room-no {
    font-weight: 600;
    color: #1f2937;
    font-size: 16px;
  }
}

.main-meter-section,
.ac-meters-section {
  margin-bottom: 24px;
}

.section-title {
  margin: 0 0 16px 0;
  padding-left: 12px;
  border-left: 4px solid #38bdf8;
  font-size: 15px;
  font-weight: 600;
  color: #374151;
}

.calculation-preview {
  margin-top: 20px;
  padding: 16px;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}
</style>
