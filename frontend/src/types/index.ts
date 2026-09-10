/**
 * 宿舍房租水电费用管理系统 - TypeScript 类型定义
 * 与后端 FastAPI Pydantic Schema 对应
 */

/** 通用分页响应 */
export interface ListResponse<T> {
  items: T[];
  total: number;
}

/** 楼栋 */
export interface Building {
  id: number;
  building_no: string;
  name?: string;
  address?: string;
  status: 'active' | 'inactive';
  remark?: string;
  created_at?: string;
  updated_at?: string;
}

/** 房间 */
export interface Room {
  id: number;
  building_id: number;
  building_no?: string;
  building_name?: string;
  room_no: string;
  room_unit?: string;
  room_name: string;
  meter_no?: string;
  ac_meter_no?: string;
  electricity_price: number;
  rent_standard: number;
  status: 'active' | 'inactive';
  remark?: string;
  created_at?: string;
}

/** 员工 */
export interface Employee {
  id: number;
  employee_no: string;
  name: string;
  company?: string;
  department?: string;
  position?: string;
  status: 'active' | 'inactive';
  remark?: string;
  created_at?: string;
}

/** 入住记录 */
export interface ResidenceRecord {
  id: number;
  employee_id: number;
  room_id: number;
  check_in_date: string;
  check_out_date?: string;
  is_primary_payer: number;
  probation_months: number;
  status: 'valid' | 'invalid' | 'business_trip' | 'leave';
  remark?: string;
  created_at?: string;
  // 关联字段
  employee_name?: string;
  employee_no?: string;
  company?: string;
  department?: string;
  position?: string;
  room_no?: string;
  room_name?: string;
  building_id?: number;
  building_no?: string;
  building_name?: string;
  rent_standard?: number;
  electricity_price?: number;
}

/** 电表记录 */
export interface MeterRecord {
  id: number;
  room_id: number;
  month: string;
  previous_reading: number;
  current_reading: number;
  total_degree: number;
  ac_previous_reading: number;
  ac_current_reading: number;
  ac_degree: number;
  electricity_price: number;
  ac_unit_price: number;
  total_fee: number;
  ac_fee: number;
  status: 'normal' | 'abnormal' | 'manual';
  remark?: string;
  // 关联字段
  room_no?: string;
  room_name?: string;
  building_no?: string;
  meter_no?: string;
  ac_meter_no?: string;
  occupants_count?: number;
}

/** 水费账单 */
export interface WaterExpense {
  id: number;
  period_start: string;
  period_end: string;
  building_id: number;
  meter_start?: number;
  meter_end?: number;
  total_amount: number;
  status: 'pending' | 'allocated' | 'settled';
  remark?: string;
  created_at?: string;
  building_no?: string;
  building_name?: string;
  allocations?: WaterAllocation[];
}

/** 水费分摊 */
export interface WaterAllocation {
  id: number;
  water_expense_id: number;
  employee_id: number;
  room_id: number;
  amount: number;
  month1_days: number;
  month2_days: number;
  is_valid: number;
  remark?: string;
  employee_name?: string;
  employee_no?: string;
  room_no?: string;
  room_name?: string;
  building_no?: string;
}

/** 月度结算 */
export interface MonthlySettlement {
  id: number;
  month: string;
  employee_id: number;
  room_id: number;
  rent_should: number;
  rent_actual: number;
  stay_days: number;
  electricity_fee: number;
  ac_electricity_fee: number;
  water_fee: number;
  deduction_minus: number;
  deduction_plus: number;
  total_amount: number;
  status: 'draft' | 'generated' | 'locked';
  remark?: string;
  created_at?: string;
  // 关联字段
  employee_name?: string;
  employee_no?: string;
  company?: string;
  department?: string;
  position?: string;
  room_no?: string;
  room_name?: string;
  building_id?: number;
  building_no?: string;
}

/** 仪表盘数据 */
export interface DashboardData {
  current_month: string;
  summary: {
    building_count: number;
    room_count: number;
    employee_count: number;
    current_residents: number;
    meter_progress: string;
  };
  amounts: {
    rent_total: number;
    electricity_total: number;
    ac_electricity_total: number;
    water_total: number;
    settlement_total: number;
  };
  probation_expiring: Array<{
    residence_id: number;
    employee_id: number;
    probation_end: string;
    days_left: number;
  }>;
  recent_water: Array<{
    id: number;
    building_id: number;
    period_start: string;
    period_end: string;
    total_amount: number;
    status: string;
  }>;
}

/** 预检查结果 */
export interface PrecheckItem {
  type: string;
  message: string;
  ref_type?: string;
  ref_id?: number;
}

export interface PrecheckResponse {
  blocking: PrecheckItem[];
  warnings: PrecheckItem[];
}

/** 结算生成请求 */
export interface SettlementGenerateRequest {
  month: string;
  force?: boolean;
}
