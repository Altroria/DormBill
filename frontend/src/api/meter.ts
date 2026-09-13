/**
 * 电表 API
 */
import { get, post, put } from './index';
import type { MeterRecord, ListResponse } from '@/types';

export const meterApi = {
  list: (params: { month: string; building_id?: number }) =>
    get<ListResponse<MeterRecord>>('/meters', params),

  update: (
    roomId: number,
    month: string,
    data: Partial<MeterRecord>,
  ) => put<MeterRecord>(`/meters/${roomId}/${month}`, data),

  calculate: (data: { month: string; ac_unit_price?: number }) =>
    post<{ message: string; count: number }>('/meters/calculate', data),

  initMonth: (params: { month: string; building_id?: number }) => {
    const queryParams: Record<string, string> = { month: params.month };
    if (params.building_id) {
      queryParams.building_id = String(params.building_id);
    }
    return post<{ message: string; count: number }>(`/meters/init-month?${new URLSearchParams(queryParams)}`);
  },
};

// V2 API - 组合电表接口
export interface AcMeterData {
  room_id: number;
  room_unit: string;
  ac_meter_no: string | null;
  ac_previous_reading: number;
  ac_current_reading: number;
  ac_degree: number;
  ac_fee: number;
}

export interface CombinedMeterItem {
  building_id: number;
  room_no: string;
  month: string;
  main_meter_no: string | null;
  main_previous_reading: number;
  main_current_reading: number;
  main_total_degree: number;
  main_total_fee: number;
  ac_meters: AcMeterData[];
  status: string;
  remark: string | null;
}

export interface CombinedMeterListResponse {
  items: CombinedMeterItem[];
  total: number;
  skip: number;
  limit: number;
}

export interface MainMeterUpdateRequest {
  current_reading: number;
  meter_no?: string;
  remark?: string;
}

export interface AcMeterUpdateRequest {
  room_id: number;
  current_reading: number;
  meter_no?: string;
}

/**
 * 获取组合电表列表
 */
export function getCombinedMeters(params: {
  month: string;
  building_id?: number;
  room_no?: string;
  skip: number;
  limit: number;
}) {
  return get<CombinedMeterListResponse>('/meters-v2/combined', params);
}

/**
 * 更新房号总表读数
 */
export function updateMainMeter(
  buildingId: number,
  roomNo: string,
  month: string,
  data: MainMeterUpdateRequest
) {
  return put(`/meters-v2/main/${buildingId}/${roomNo}/${month}`, data);
}

/**
 * 批量更新空调表读数
 */
export function batchUpdateAcMeters(
  month: string,
  data: AcMeterUpdateRequest[]
) {
  return put(`/meters-v2/ac-batch/${month}`, data);
}
