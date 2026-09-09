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
