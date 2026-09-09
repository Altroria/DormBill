import axios, { type AxiosInstance, type AxiosRequestConfig, type AxiosResponse, type InternalAxiosRequestConfig } from 'axios';
import { ElMessage } from 'element-plus';

/**
 * 创建 axios 实例
 */
const api: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * 请求拦截器
 */
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    return config;
  },
  (error) => Promise.reject(error)
);

/**
 * 响应拦截器
 */
api.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error) => {
    const { response } = error;
    if (response) {
      ElMessage.error(response.data?.detail || `请求失败 (${response.status})`);
    } else if (error.request) {
      ElMessage.error('网络连接失败，请检查后端服务是否启动');
    } else {
      ElMessage.error('请求配置错误');
    }
    return Promise.reject(error);
  }
);

export function get<T>(url: string, params?: Record<string, unknown>, config?: AxiosRequestConfig): Promise<T> {
  return api.get(url, { params, ...config }).then((res) => res.data);
}

export function post<T>(url: string, data?: unknown, config?: AxiosRequestConfig): Promise<T> {
  return api.post(url, data, config).then((res) => res.data);
}

export function put<T>(url: string, data?: unknown, config?: AxiosRequestConfig): Promise<T> {
  return api.put(url, data, config).then((res) => res.data);
}

export function del<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
  return api.delete(url, config).then((res) => res.data);
}

export function uploadFile<T>(url: string, formData: FormData): Promise<T> {
  return api.post(url, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }).then((res) => res.data);
}

export function downloadFile(url: string, filename: string) {
  return api.get(url, { responseType: 'blob' }).then((res) => {
    const blob = new Blob([res.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
    const link = document.createElement('a');
    link.href = window.URL.createObjectURL(blob);
    link.download = filename;
    link.click();
    window.URL.revokeObjectURL(link.href);
  });
}

export default api;
