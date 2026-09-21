import { get, post, put } from './index'

// 类型定义
export interface AcMeterResponse {
  id: number
  room_id: number
  month: string
  ac_previous_reading: number
  ac_current_reading: number
  ac_degree: number
  ac_unit_price: number
  ac_fee: number
  status: string
  remark?: string
  created_at?: string
  // 关联字段
  building_no?: string
  room_no?: string
  room_name?: string
  ac_meter_no?: string
  occupants_count?: number
}

export interface CombinedMeterResponse {
  // 房号信息
  building_id: number
  building_no: string
  room_no: string
  month: string
  
  // 总电表
  main_meter_id?: number
  main_meter_no?: string
  main_previous_reading: number
  main_current_reading: number
  main_total_degree: number
  main_electricity_price: number
  main_total_fee: number
  main_status: string
  
  // 空调电表列表
  ac_meters: AcMeterResponse[]
  
  // 汇总
  total_ac_fee: number
  grand_total: number
}

export interface CombinedMeterListResponse {
  items: CombinedMeterResponse[]
  total: number
}

export interface InitMonthResponse {
  main_meter_count: number
  ac_meter_count: number
}

export interface RoomMainMeterUpdateRequest {
  previous_reading?: number
  current_reading?: number
  total_degree?: number  // 新增：手动输入用电量
  total_fee?: number     // 新增：手动输入总电费
  electricity_price?: number
  meter_no?: string
  remark?: string
}

export interface AcMeterUpdateRequest {
  ac_previous_reading?: number
  ac_current_reading?: number
  ac_unit_price?: number
  remark?: string
}

// 批量更新相关类型
export interface AcMeterBatchUpdateItem {
  room_id: number
  ac_current_reading: number
}

export interface RoomNoBatchUpdateItem {
  building_id: number
  room_no: string
  main_current_reading: number
  main_total_degree?: number   // 新增：手动输入用电量
  main_total_fee?: number      // 新增：手动输入总电费
  main_meter_no?: string
  ac_meters: AcMeterBatchUpdateItem[]
}

export interface BatchUpdateRequest {
  month: string
  updates: RoomNoBatchUpdateItem[]
}

export interface BatchUpdateResponse {
  main_meters_updated: number
  ac_meters_updated: number
  message: string
}

// 增强计算相关类型
export interface EnhancedCalculateRequest {
  month: string
  building_id?: number
  calculate_distribution?: boolean
}

export interface EnhancedCalculateResponse {
  main_meters_calculated: number
  distributions_created: number
  total_common_fee: number
  total_ac_fee: number
  total_fee: number
}

// 增强列表相关类型
export interface AcMeterInfo {
  room_id: number
  room_unit?: string
  room_name?: string
  ac_meter_no?: string
  ac_previous_reading: number
  ac_current_reading: number
  ac_degree: number
  ac_fee: number
  occupants?: number
}

export interface EnhancedMeterListItem {
  building_id: number
  building_no?: string
  room_no: string
  month: string
  // 总表数据
  main_previous_reading: number
  main_current_reading: number
  main_total_degree: number
  main_total_fee: number
  common_degree: number
  common_fee: number
  // 空调汇总
  total_ac_degree: number
  total_ac_fee: number
  // 套间明细
  ac_meters: AcMeterInfo[]
  // 统计
  total_occupants: number
  common_fee_per_person: number
  status: string
}

export interface EnhancedMeterListResponse {
  items: EnhancedMeterListItem[]
  total: number
}

export const meterV2Api = {
  // 获取组合电表列表（总表+空调表）
  listCombined(params: {
    month: string
    building_id?: number
  }): Promise<CombinedMeterListResponse> {
    return get('/meters-v2/combined', params)
  },

  // 初始化月度电表
  initMonth(params: {
    month: string
    building_id?: number
  }): Promise<InitMonthResponse> {
    return post('/meters-v2/init-month', params)
  },

  // 更新房号总电表
  updateMainMeter(
    buildingId: number,
    roomNo: string,
    month: string,
    data: RoomMainMeterUpdateRequest
  ): Promise<any> {
    return put(
      `/meters-v2/main/${buildingId}/${roomNo}/${month}`,
      data
    )
  },

  // 更新空调电表
  updateAcMeter(
    roomId: number,
    month: string,
    data: AcMeterUpdateRequest
  ): Promise<any> {
    return put(
      `/meters-v2/ac/${roomId}/${month}`,
      data
    )
  },

  // 批量更新电表（总表+空调表）
  batchUpdate(data: BatchUpdateRequest): Promise<BatchUpdateResponse> {
    return put('/meters-v2/batch-update', data)
  },

  // 增强的电表计算（包含公共用电计算和个人分摊）
  calculateEnhanced(data: EnhancedCalculateRequest): Promise<EnhancedCalculateResponse> {
    return post('/meters-v2/calculate-enhanced', data)
  },

  // 获取增强的电表列表（包含统计信息）
  listEnhanced(params: {
    month: string
    building_id?: number
    room_no?: string
    skip?: number
    limit?: number
  }): Promise<EnhancedMeterListResponse> {
    return get('/meters-v2/list-enhanced', params)
  }
}
