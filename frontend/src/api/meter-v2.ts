/**
 * 电表管理V2 API（总表+空调表分离）
 */
import { get, post, put } from './index'

export interface AcMeter {
  room_id: number
  room_unit: string
  ac_meter_no?: string
  ac_previous_reading: number
  ac_current_reading: number
  ac_degree: number
  ac_fee: number
}

export interface CombinedMeterItem {
  building_id: number
  room_no: string
  month: string
  // 总表数据
  main_meter_no?: string
  main_previous_reading: number
  main_current_reading: number
  main_total_degree: number
  main_total_fee: number
  // 空调表数据
  ac_meters: AcMeter[]
  // 状态
  status: 'pending' | 'recorded' | 'calculated'
  remark?: string
}

export interface CombinedMeterListResponse {
  items: CombinedMeterItem[]
  total: number
  skip: number
  limit: number
}

export interface MainMeterUpdateRequest {
  current_reading?: number
  meter_no?: string
  remark?: string
}

export interface AcMeterUpdateRequest {
  ac_current_reading?: number
  ac_meter_no?: string
}

export interface MeterCalculateRequest {
  building_id?: number
  month?: string
}

/**
 * 获取组合电表列表
 */
export function getCombinedMeterList(params: {
  month: string
  building_id?: number
  room_no?: string
  skip?: number
  limit?: number
}) {
  return get<CombinedMeterListResponse>('/v1/meters-v2/combined', params)
}

/**
 * 更新房号总电表读数
 */
export function updateMainMeter(
  buildingId: number,
  roomNo: string,
  month: string,
  data: MainMeterUpdateRequest
) {
  return put(`/v1/meters-v2/main/${buildingId}/${roomNo}/${month}`, data)
}

/**
 * 更新空调电表读数
 */
export function updateAcMeter(
  roomId: number,
  month: string,
  data: AcMeterUpdateRequest
) {
  return put(`/v1/meters-v2/ac/${roomId}/${month}`, data)
}

/**
 * 批量计算电表费用
 */
export function calculateMeters(data: MeterCalculateRequest) {
  return post('/v1/meters-v2/calculate', data)
}
