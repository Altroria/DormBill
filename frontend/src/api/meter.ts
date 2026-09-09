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

  initMonth: (month: string, building_id?: number) =>
    post<{ message: string; count: number }>(`/meters/init-month`, { month, building_id }),
};
