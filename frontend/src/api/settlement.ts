/**
 * 月度结算 API
 */
import { get, post, put } from './index';
import type { MonthlySettlement, ListResponse, PrecheckResponse } from '@/types';

export const settlementApi = {
  list: (params: {
    month: string;
    building_id?: number;
    keyword?: string;
    status?: string;
    water_mode?: 'single' | 'double';
    page?: number;
    page_size?: number;
  }) => get<ListResponse<MonthlySettlement>>('/settlements', params),

  precheck: (data: { month: string }) =>
    post<PrecheckResponse>('/settlements/precheck', data),

  generate: (data: { month: string; force?: boolean; water_mode?: string }) =>
    post<ListResponse<MonthlySettlement>>('/settlements/generate', data),

  recalculate: (data: { month: string; water_mode?: string }) =>
    post<ListResponse<MonthlySettlement>>('/settlements/recalculate', data),

  update: (id: number, data: Partial<MonthlySettlement>) =>
    put<MonthlySettlement>(`/settlements/${id}`, data),

  lock: (month: string) =>
    post<{ message: string; locked: number }>('/settlements/lock', { month }),

  unlock: (month: string) =>
    post<{ message: string; unlocked: number }>('/settlements/unlock', { month }),
};
