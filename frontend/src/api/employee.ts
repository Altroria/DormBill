/**
 * 员工 API
 */
import { get, post, put, del, uploadFile } from './index';
import type { Employee, ListResponse } from '@/types';

export const employeeApi = {
  list: (params?: {
    keyword?: string;
    company?: string;
    department?: string;
    status?: string;
    page?: number;
    page_size?: number;
  }) => get<ListResponse<Employee>>('/employees', params),

  get: (id: number) => get<Employee>(`/employees/${id}`),

  create: (data: Partial<Employee>) => post<Employee>('/employees', data),

  update: (id: number, data: Partial<Employee>) =>
    put<Employee>(`/employees/${id}`, data),

  delete: (id: number) => del<void>(`/employees/${id}`),

  import: (file: File) => {
    const fd = new FormData();
    fd.append('file', file);
    return uploadFile<{ message: string; total: number; created: number; errors: unknown[] }>(
      '/import/employees', fd
    );
  },
};
