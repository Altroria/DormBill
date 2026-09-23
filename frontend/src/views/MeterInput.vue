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
          <el-button
            type="warning"
            :loading="calculating"
            @click="calculate"
          >
            计算电费
          </el-button>
          <el-button 
            :icon="Download"
            color="#0ea5e9"
            style="color: white; font-weight: 500; margin-left: 12px;"
            @click="exportTemplate"
          >
            导出模板
          </el-button>
          <el-upload
            ref="uploadRef"
            :auto-upload="false"
            :show-file-list="false"
            :on-change="handleFileChange"
            accept=".xlsx,.xls"
            style="display: inline-block; margin-left: 0;"
          >
            <el-button 
              :icon="Upload"
              :loading="importing"
              color="#06b6d4"
              style="color: white; font-weight: 500;"
            >
              导入数据
            </el-button>
          </el-upload>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 数据加载状态 -->
    <el-card v-loading="loading" class="content-card" shadow="never">
      <template v-if="!loading && meterData.length === 0 && hasSearched">
        <el-empty description="暂无数据">
          <template #description>
            <div style="margin-bottom: 16px; color: #909399;">
              当前筛选条件下没有电表记录
            </div>
            <div style="margin-bottom: 16px; color: #606266;">
              如果是新月份，请先点击"初始化月份"按钮创建电表记录
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
                      @change="onMainReadingChange(room)"
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="6">
                  <el-form-item label="用电量">
                    <el-input-number
                      v-model="room.main_total_degree"
                      :precision="2"
                      :step="1"
                      :min="0"
                      style="width: 100%"
                      @change="onMainDegreeChange(room)"
                    />
                    <el-text size="small" type="info">度（可修改）</el-text>
                  </el-form-item>
                </el-col>
                <el-col :span="6">
                  <el-form-item label="总电费">
                    <el-input-number
                      v-model="room.main_total_fee"
                      :precision="2"
                      :step="1"
                      :min="0"
                      style="width: 100%"
                      @change="onMainFeeChange(room)"
                    />
                    <el-text size="small" type="info">元（必填）</el-text>
                  </el-form-item>
                </el-col>
              </el-row>
              
              <!-- 电价显示 -->
              <el-row :gutter="20">
                <el-col :span="6" :offset="12">
                  <el-form-item label="计算电价">
                    <el-input 
                      :value="calculatePrice(room).toFixed(4)" 
                      disabled
                    >
                      <template #suffix>元/度</template>
                    </el-input>
                    <el-text 
                      v-if="isPriceAbnormal(room)" 
                      size="small" 
                      type="warning"
                    >
                      ⚠️ 电价异常，请检查（合理范围: 0.3-1.0元/度）
                    </el-text>
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

              <el-table-column label="房间名" width="120" align="center">
                <template #default="{ row }">
                  <el-text size="small" style="font-weight: 500;">{{ row.room_name || '-' }}</el-text>
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
                  ¥{{ calculateAcFee(row, room).toFixed(2) }}
                </template>
              </el-table-column>
              
              <el-table-column label="人均空调费" align="right">
                <template #default="{ row }">
                  ¥{{ (row.occupants > 0 ? calculateAcFee(row, room) / row.occupants : 0).toFixed(2) }}
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
import { Search, Check, Download, Upload } from '@element-plus/icons-vue'
import { meterV2Api, type EnhancedMeterListItem, type RoomNoBatchUpdateItem } from '@/api/meter_v2'
import type { Building } from '@/types'
import { buildingApi } from '@/api/building'

// 数据状态
const loading = ref(false)
const saving = ref(false)
const calculating = ref(false)
const initializing = ref(false)
const importing = ref(false)
const hasSearched = ref(false)
const buildings = ref<Building[]>([])
const meterData = ref<EnhancedMeterListItem[]>([])
const activeRooms = ref<string[]>([])
const uploadRef = ref()

// 筛选表单
const filterForm = reactive({
  month: '',
  buildingId: undefined as number | undefined,
  roomNo: '',
})

// 变更跟踪
const changesMap = ref(new Map<string, boolean>())
// 手动输入字段追踪 - 追踪哪些字段是用户手动输入的
const manualInputMap = ref(new Map<string, Set<string>>())

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
      `确定要初始化 ${filterForm.month} 的电表记录吗？` +
      (filterForm.buildingId ? '（仅选中的楼栋）' : '（所有楼栋）') +
      '\n\n初始化后会自动创建所有房号的电表记录，并带出上月读数。',
      '确认初始化',
      { 
        type: 'info',
        confirmButtonText: '确定初始化',
        cancelButtonText: '取消'
      }
    )

    initializing.value = true

    const response = await meterV2Api.initMonth({
      month: filterForm.month,
      building_id: filterForm.buildingId,
    })

    ElMessage.success(
      `初始化成功！创建了 ${response.main_meter_count} 个房号总表和 ${response.ac_meter_count} 个空调表记录`
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

// 加载电表数据
const loadData = async () => {
  if (!filterForm.month) {
    ElMessage.warning('请选择月份')
    return
  }

  loading.value = true
  hasSearched.value = true
  changesMap.value.clear()

  try {
    const response = await meterV2Api.listEnhanced({
      month: filterForm.month,
      building_id: filterForm.buildingId,
      skip: 0,
      limit: 500,
    })

    // 前端房号过滤
    let items = response.items
    if (filterForm.roomNo) {
      items = items.filter(item => item.room_no.includes(filterForm.roomNo))
    }

    meterData.value = items

    if (items.length === 0) {
      ElMessage.info('没有找到符合条件的数据')
    } else {
      ElMessage.success(`加载成功，共 ${items.length} 个房号`)
    }
  } catch (error: any) {
    ElMessage.error(error.message || '加载数据失败')
  } finally {
    loading.value = false
  }
}

// 计算电价
const calculatePrice = (room: EnhancedMeterListItem) => {
  if (room.main_total_degree > 0) {
    return room.main_total_fee / room.main_total_degree
  }
  return 0.49 // 默认值
}

// 判断电价是否异常
const isPriceAbnormal = (room: EnhancedMeterListItem) => {
  const price = calculatePrice(room)
  return price < 0.3 || price > 1.0
}

// 本月读数变更（自动计算用电量）
const onMainReadingChange = (room: EnhancedMeterListItem) => {
  room.main_total_degree = Math.max(0, room.main_current_reading - room.main_previous_reading)
  const key = `${room.building_id}-${room.room_no}`
  changesMap.value.set(key, true)
  // 本月读数变更时，清除用电量和总电费的手动输入标记（因为是自动计算的）
  const manualFields = manualInputMap.value.get(key)
  if (manualFields) {
    manualFields.delete('main_total_degree')
    manualFields.delete('main_total_fee')
  }
}

// 用电量手动变更
const onMainDegreeChange = (room: EnhancedMeterListItem) => {
  const key = `${room.building_id}-${room.room_no}`
  changesMap.value.set(key, true)
  // 标记用电量为手动输入
  if (!manualInputMap.value.has(key)) {
    manualInputMap.value.set(key, new Set())
  }
  manualInputMap.value.get(key)!.add('main_total_degree')
}

// 总电费变更
const onMainFeeChange = (room: EnhancedMeterListItem) => {
  const key = `${room.building_id}-${room.room_no}`
  changesMap.value.set(key, true)
  // 标记总电费为手动输入
  if (!manualInputMap.value.has(key)) {
    manualInputMap.value.set(key, new Set())
  }
  manualInputMap.value.get(key)!.add('main_total_fee')
}

// 计算空调用电量
const calculateAcDegree = (acMeter: any) => {
  return Math.max(0, acMeter.ac_current_reading - acMeter.ac_previous_reading)
}

// 计算空调电费（使用房号的实际电价）
const calculateAcFee = (acMeter: any, room?: EnhancedMeterListItem) => {
  const degree = calculateAcDegree(acMeter)
  // 使用房号的实际电价（从总表用电量和总电费反算）
  const price = room ? calculatePrice(room) : 0.49
  return degree * price
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
        // 获取该房号的手动输入字段
        const manualFields = manualInputMap.value.get(key) || new Set()
        
        updates.push({
          building_id: room.building_id,
          room_no: room.room_no,
          main_current_reading: room.main_current_reading,
          // 只有手动输入时才发送，否则发送 undefined（会被序列化为 null）
          main_total_degree: manualFields.has('main_total_degree') ? room.main_total_degree : undefined,
          main_total_fee: manualFields.has('main_total_fee') ? room.main_total_fee : undefined,
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
    manualInputMap.value.clear()

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

// 导出模板
const exportTemplate = () => {
  if (!filterForm.month) {
    ElMessage.warning('请选择月份')
    return
  }

  const url = meterV2Api.exportTemplate({
    month: filterForm.month,
    building_id: filterForm.buildingId,
  })
  
  // 创建隐藏的下载链接
  const link = document.createElement('a')
  link.href = url
  link.download = `电费导入模板_${filterForm.month}.xlsx`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  
  ElMessage.success('模板下载成功')
}

// 处理文件选择
const handleFileChange = async (file: any) => {
  if (!filterForm.month) {
    ElMessage.warning('请先选择月份')
    return
  }

  try {
    importing.value = true
    
    const result = await meterV2Api.importExcel(filterForm.month, file.raw)
    
    // 显示导入结果
    const errorMessages = []
    
    if (result.parse_errors && result.parse_errors.length > 0) {
      errorMessages.push(`解析错误 ${result.parse_errors.length} 条`)
    }
    
    if (result.import_errors && result.import_errors.length > 0) {
      errorMessages.push(`导入错误 ${result.import_errors.length} 条`)
    }
    
    if (errorMessages.length > 0) {
      ElMessageBox.alert(
        `${result.message}\n\n错误详情：\n${errorMessages.join('\n')}`,
        '导入完成（有错误）',
        { type: 'warning' }
      )
    } else {
      ElMessage.success(result.message)
    }
    
    // 重新加载数据
    await loadData()
  } catch (error: any) {
    ElMessage.error(error.message || '导入失败')
  } finally {
    importing.value = false
    // 清空文件选择
    if (uploadRef.value) {
      uploadRef.value.clearFiles()
    }
  }
}

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
