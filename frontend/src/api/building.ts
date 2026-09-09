/**
 * 楼栋 API
 */
import { get, post, put, del } from './index';
import type { Building, ListResponse } from '@/types';

export const buildingApi = {
  list: (params?: { keyword?: string; status?: string }) =>
    get<ListResponse<Building>>('/buildings', params),

  get: (id: number) =>
    get<Building>(`/buildings/${id}`),

  create: (data: Partial<Building>) =>
    post<Building>('/buildings', data),

  update: (id: number, data: Partial<Building>) =>
    put<Building>(`/buildings/${id}`, data),

  delete: (id: number) =>
    del<void>(`/buildings/${id}`),
};
