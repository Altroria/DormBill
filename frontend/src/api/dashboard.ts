/**
 * 仪表盘 API
 */
import { get } from './index';
import type { DashboardData } from '@/types';

export const dashboardApi = {
  get: (month?: string) => get<DashboardData>('/dashboard', { month }),
};
