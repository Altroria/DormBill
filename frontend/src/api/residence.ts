/**
 * 入住记录 API
 */
import { get, post, put, del } from './index';
import type { ResidenceRecord, ListResponse } from '@/types';

export const residenceApi = {
  list: (params?: {
    building_id?: number;
    room_id?: number;
    building_no?: string;
    room_no?: string;
    keyword?: string;
    status?: string;
    is_current?: boolean;
  }) => get<ListResponse<ResidenceRecord>>('/residences', params),

  get: (id: number) => get<ResidenceRecord>(`/residences/${id}`),

  create: (data: Partial<ResidenceRecord>) =>
    post<ResidenceRecord>('/residences', data),

  update: (id: number, data: Partial<ResidenceRecord>) =>
    put<ResidenceRecord>(`/residences/${id}`, data),

  delete: (id: number) => del<void>(`/residences/${id}`),

  batchMoveOut: (data: { residence_ids: number[]; check_out_date: string }) =>
    post<{ message: string; updated: number }>('/residences/batch-move-out', data),

  batchTransfer: (data: { items: { residence_id: number; target_room_id: number }[]; transfer_date: string }) =>
    post<{ message: string; transferred: number }>('/residences/batch-transfer', data),
};
