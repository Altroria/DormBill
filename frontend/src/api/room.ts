/**
 * 房间 API
 */
import { get, post, put, del } from './index';
import type { Room, ListResponse } from '@/types';

export const roomApi = {
  list: (params?: { building_id?: number; keyword?: string; status?: string }) =>
    get<ListResponse<Room>>('/rooms', params),

  get: (id: number) =>
    get<Room>(`/rooms/${id}`),

  create: (data: Partial<Room>) =>
    post<Room>('/rooms', data),

  batchCreate: (data: { building_id: number; items: Partial<Room>[] }) =>
    post<ListResponse<Room>>('/rooms/batch', data),

  update: (id: number, data: Partial<Room>) =>
    put<Room>(`/rooms/${id}`, data),

  delete: (id: number) =>
    del<void>(`/rooms/${id}`),
};
