<!-- 电表管理V2 - 总表+空调表分离录入 -->
<template>
  <div class="meter-manage-v2">
    <!-- 查询条件 -->
    <el-card class="filter-card">
      <el-form :inline="true" :model="filterForm">
        <el-form-item label="月份">
          <el-date-picker
            v-model="filterForm.month"
            type="month"
            placeholder="选择月份"
            format="YYYY-MM"
            value-format="YYYY-MM"
            @change="handleQuery"
          />
        </el-form-item>
        <el-form-item label="楼栋">
          <el-select
            v-model="filterForm.building_id"
            placeholder="全部楼栋"
            clearable
            @change="handleQuery"
          >
            <el-option
              v-for="building in buildings"
              :key="building.id"
              :label="building.name"
              :value="building.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="房号">
          <el-input
            v-model="filterForm.room_no"
            placeholder="房号模糊查询"
            clearable
            @keyup.enter="handleQuery"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleQuery">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 操作按钮 -->
    <el-card class="action-card">
      <el-button 
        type="success" 
        :disabled="!hasUnsavedChanges"
        @click="handleBatchSave"
      >
        批量保存 ({{ changedCount }})
      </el-button>
      <el-button @click="handleCancelChanges" :disabled="!hasUnsavedChanges">
        取消修改
      </el-button>
      <span class="tips">提示: 修改后点击"批量保存"统一提交</span>
    </el-card>

    <!-- 电表数据列表 -->
    <el-card class="data-card">
      <div v-loading="loading" class="meter-list">
        <div v-if="meterData.length === 0" class="empty-data">
          <el-empty description="暂无数据" />
        </div>
        
        <div 
          v-for="item in meterData" 
          :key="`${item.building_id}-${item.room_no}`"
          class="room-meter-card"
        >
          <!-- 房号标题 -->
          <div class="room-header">
            <h3>{{ item.room_no }}号房</h3>
            <el-tag>{{ getBuildingName(item.building_id) }}</el-tag>
          </div>

          <!-- 总表部分 -->
          <div class="main-meter-section">
            <h4 class="section-title">总表</h4>
            <el-form :inline="true" size="default">
              <el-form-item label="表号">
                <el-input
                  v-model="item.main_meter_no"
                  placeholder="选填"
                  style="width: 150px"
                  @input="markAsChanged()"
                />
              </el-form-item>
              <el-form-item label="上月读数">
                <el-input
                  :value="item.main_previous_reading"
                  disabled
                  style="width: 120px"
                />
              </el-form-item>
              <el-form-item label="本月读数">
                <el-input-number
                  v-model="item.main_current_reading"
                  :precision="2"
                  :step="1"
                  :min="0"
                  style="width: 150px"
                  @change="markAsChanged()"
                />
              </el-form-item>
              <el-form-item label="用电量">
                <el-input
                  :value="item.main_total_degree.toFixed(2)"
                  disabled
                  style="width: 120px"
                />
              </el-form-item>
              <el-form-item label="电费">
                <el-input
                  :value="item.main_total_fee.toFixed(2)"
                  disabled
                  style="width: 120px"
                />
              </el-form-item>
            </el-form>
          </div>

          <!-- 空调表部分 -->
          <div class="ac-meter-section">
            <h4 class="section-title">空调表 (按套间)</h4>
            <div class="ac-meter-list">
              <div
                v-for="acMeter in item.ac_meters"
                :key="acMeter.room_id"
                class="ac-meter-item"
                :class="{ 'has-changes': isAcMeterChanged(acMeter.room_id) }"
              >
                <span class="unit-label">{{ acMeter.room_unit }}号套间</span>
                <el-form :inline="true" size="small">
                  <el-form-item label="表号">
                    <el-input
                      v-model="acMeter.ac_meter_no"
                      placeholder="选填"
                      style="width: 130px"
                      @input="markAcMeterChanged(acMeter)"
                    />
                  </el-form-item>
                  <el-form-item label="上月">
                    <el-input
                      :value="acMeter.ac_previous_reading"
                      disabled
                      style="width: 100px"
                    />
                  </el-form-item>
                  <el-form-item label="本月">
                    <el-input-number
                      v-model="acMeter.ac_current_reading"
                      :precision="2"
                      :step="1"
                      :min="0"
                      style="width: 130px"
                      @change="markAcMeterChanged(acMeter)"
                    />
                  </el-form-item>
                  <el-form-item label="用量">
                    <el-input
                      :value="acMeter.ac_degree.toFixed(2)"
                      disabled
                      style="width: 100px"
                    />
                  </el-form-item>
                  <el-form-item label="电费">
                    <el-input
                      :value="acMeter.ac_fee.toFixed(2)"
                      disabled
                      style="width: 100px"
                    />
                  </el-form-item>
                </el-form>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :total="pagination.total"
          :page-sizes="[20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleQuery"
          @current-change="handleQuery"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { buildingApi } from '@/api/building';
import { 
  meterV2Api,
  type CombinedMeterResponse,
  type AcMeterResponse,
  type AcMeterUpdateRequest 
} from '@/api/meter_v2';

// 类型别名，便于理解
type CombinedMeterItem = CombinedMeterResponse;
type AcMeterData = AcMeterResponse;

// 楼栋列表
const buildings = ref<any[]>([]);

// 查询条件
const filterForm = reactive({
  month: new Date().toISOString().slice(0, 7), // YYYY-MM
  building_id: undefined as number | undefined,
  room_no: ''
});

// 分页
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0
});

// 数据
const meterData = ref<CombinedMeterItem[]>([]);
const loading = ref(false);

// 变更跟踪
const changedAcMeters = ref<Map<number, AcMeterUpdateRequest>>(new Map());

// 计算变更数量
const changedCount = computed(() => changedAcMeters.value.size);
const hasUnsavedChanges = computed(() => changedCount.value > 0);

// 获取楼栋名称
const getBuildingName = (buildingId: number) => {
  const building = buildings.value.find(b => b.id === buildingId);
  return building ? building.name : buildingId;
};

// 标记空调表已变更
const markAcMeterChanged = (acMeter: AcMeterData) => {
  // 计算用量和电费
  const degree = acMeter.ac_current_reading - acMeter.ac_previous_reading;
  const fee = degree * 0.49; // 假设电价0.49
  
  acMeter.ac_degree = degree;
  acMeter.ac_fee = fee;
  
  changedAcMeters.value.set(acMeter.room_id, {
    room_id: acMeter.room_id,
    current_reading: acMeter.ac_current_reading,
    meter_no: acMeter.ac_meter_no || undefined
  });
};

// 检查空调表是否已变更
const isAcMeterChanged = (roomId: number) => {
  return changedAcMeters.value.has(roomId);
};

// 标记主表变更（暂时不实现）
const markAsChanged = () => {
  // 主表更新暂不实现，等需要时再加
};

// 加载楼栋列表
const loadBuildings = async () => {
  try {
    const response = await buildingApi.list();
    buildings.value = response.items;
  } catch (error) {
    ElMessage.error('加载楼栋列表失败');
  }
};

// 加载电表数据
const loadMeterData = async () => {
  if (!filterForm.month) {
    ElMessage.warning('请选择月份');
    return;
  }

  loading.value = true;
  try {
    const response = await meterV2Api.listCombined({
      month: filterForm.month,
      building_id: filterForm.building_id
    });

    // 如果有房号筛选，前端过滤
    let items = response.items;
    if (filterForm.room_no) {
      items = items.filter(item => 
        item.room_no.includes(filterForm.room_no)
      );
    }

    meterData.value = items;
    pagination.total = items.length;
  } catch (error: any) {
    ElMessage.error(error.message || '加载数据失败');
  } finally {
    loading.value = false;
  }
};

// 查询
const handleQuery = () => {
  pagination.page = 1;
  changedAcMeters.value.clear(); // 清空变更
  loadMeterData();
};

// 重置
const handleReset = () => {
  filterForm.building_id = undefined;
  filterForm.room_no = '';
  handleQuery();
};

// 批量保存
const handleBatchSave = async () => {
  if (changedAcMeters.value.size === 0) {
    ElMessage.warning('没有需要保存的变更');
    return;
  }

  try {
    await ElMessageBox.confirm(
      `确认保存 ${changedAcMeters.value.size} 条空调表记录？`,
      '确认保存',
      { type: 'warning' }
    );

    loading.value = true;
    
    // 构造批量更新请求，按房号分组
    const roomUpdates = new Map<string, any>();
    
    for (const [roomId, update] of changedAcMeters.value) {
      // 查找对应的meter数据
      const meterItem = meterData.value.find(m => 
        m.ac_meters.some(ac => ac.room_id === roomId)
      );
      
      if (meterItem) {
        const key = `${meterItem.building_id}-${meterItem.room_no}`;
        if (!roomUpdates.has(key)) {
          roomUpdates.set(key, {
            building_id: meterItem.building_id,
            room_no: meterItem.room_no,
            main_current_reading: meterItem.main_current_reading,
            ac_meters: []
          });
        }
        
        roomUpdates.get(key).ac_meters.push({
          room_id: roomId,
          ac_current_reading: update.ac_current_reading || 0
        });
      }
    }
    
    await meterV2Api.batchUpdate({
      month: filterForm.month,
      updates: Array.from(roomUpdates.values())
    });
    
    ElMessage.success('保存成功');
    changedAcMeters.value.clear();
    await loadMeterData(); // 重新加载数据
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '保存失败');
    }
  } finally {
    loading.value = false;
  }
};

// 取消修改
const handleCancelChanges = () => {
  changedAcMeters.value.clear();
  loadMeterData(); // 重新加载原始数据
};

// 初始化
onMounted(() => {
  loadBuildings();
  loadMeterData();
});
</script>

<style scoped lang="scss">
.meter-manage-v2 {
  .filter-card,
  .action-card,
  .data-card {
    margin-bottom: 16px;
  }

  .action-card {
    .tips {
      margin-left: 16px;
      color: #909399;
      font-size: 14px;
    }
  }

  .meter-list {
    min-height: 400px;
  }

  .room-meter-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;

    &:last-child {
      margin-bottom: 0;
    }
  }

  .room-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
    padding-bottom: 12px;
    border-bottom: 2px solid #cbd5e1;

    h3 {
      margin: 0;
      font-size: 18px;
      font-weight: 600;
      color: #1e293b;
    }
  }

  .section-title {
    margin: 0 0 12px 0;
    font-size: 15px;
    font-weight: 600;
    color: #475569;
  }

  .main-meter-section {
    background: white;
    border-radius: 6px;
    padding: 16px;
    margin-bottom: 16px;
  }

  .ac-meter-section {
    background: white;
    border-radius: 6px;
    padding: 16px;
  }

  .ac-meter-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .ac-meter-item {
    display: flex;
    align-items: center;
    background: #f1f5f9;
    border-radius: 4px;
    padding: 12px;
    transition: all 0.2s;

    &.has-changes {
      background: #fef3c7;
      border-left: 3px solid #f59e0b;
    }

    .unit-label {
      font-weight: 600;
      color: #334155;
      min-width: 80px;
      margin-right: 16px;
    }

    .el-form {
      flex: 1;
    }
  }

  .pagination {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
  }

  .empty-data {
    padding: 60px 0;
  }
}
</style>
