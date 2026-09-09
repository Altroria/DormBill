/**
 * 水费 API
 */
import { get, post, put, del } from './index';
import type { WaterExpense, ListResponse } from '@/types';

export const waterApi = {
  list: (params?: { building_id?: number; period?: string }) =>
    get<ListResponse<WaterExpense>>('/water-expenses', params),

  create: (data: Partial<WaterExpense>) =>
    post<WaterExpense>('/water-expenses', data),

  update: (id: number, data: Partial<WaterExpense>) =>
    put<WaterExpense>(`/water-expenses/${id}`, data),

  allocate: (id: number) =>
    post<WaterExpense>(`/water-expenses/${id}/allocate`),

  delete: (id: number) => del<void>(`/water-expenses/${id}`),

  batchUpdateAllocations: (items: { id: number; amount: number }[]) =>
    post<{ message: string }>('/water-expenses/allocate-batch', { items }),

  updateSingleAllocation: (id: number, amount: number, remark?: string) =>
    put(`/water-expenses/allocation/${id}`, null, {
      params: { amount, remark },
    }),
};
