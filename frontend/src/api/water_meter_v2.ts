/**
 * 水费管理 API（简化版）
 */
import { get, post, put } from './index'

export interface WaterMeterItem {
  id: number
  room_no: string
  building_id: number
  building_no: string
  room_name: string | null
  month: string
  total_fee: number
  remark: string | null
  occupants_count: number
}

export interface WaterMeterListResponse {
  items: WaterMeterItem[]
  total: number
}

export interface InitMonthRequest {
  month: string  // YYYY-MM
  building_id?: number
}

export interface InitMonthResponse {
  water_meter_count: number
  message: string
}

export interface WaterMeterUpdateRequest {
  total_fee?: number
  remark?: string
}

export interface BatchUpdateItem {
  building_id: number
  room_no: string
  total_fee?: number
  remark?: string
}

export interface BatchUpdateRequest {
  month: string
  updates: BatchUpdateItem[]
}

export interface BatchUpdateResponse {
  updated_count: number
  message: string
}

export const waterMeterV2Api = {
  /**
   * 初始化月度水费记录
   */
  initMonth(data: InitMonthRequest) {
    return post<InitMonthResponse>('/water-meters-v2/init-month', data)
  },

  /**
   * 获取水费列表
   */
  list(params: {
    month: string
    building_id?: number
    room_no?: string
    skip?: number
    limit?: number
  }) {
    return get<WaterMeterListResponse>('/water-meters-v2/list', params)
  },

  /**
   * 更新单个水费
   */
  update(buildingId: number, roomNo: string, month: string, data: WaterMeterUpdateRequest) {
    return put(`/water-meters-v2/${buildingId}/${roomNo}/${month}`, data)
  },

  /**
   * 批量更新水费
   */
  batchUpdate(data: BatchUpdateRequest) {
    return post<BatchUpdateResponse>('/water-meters-v2/batch-update', data)
  },
}
