import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import dayjs from 'dayjs';

interface UserInfo {
  id: number;
  name: string;
  phone?: string;
  role?: string;
}

export const useAppStore = defineStore('app', () => {
  // State
  const userInfo = ref<UserInfo | null>(null);
  const isLoggedIn = ref(false);
  const sidebarCollapsed = ref(false);
  const currentMonth = ref(dayjs().format('YYYY-MM'));
  const loading = ref(false);
  
  // Getters
  const userName = computed(() => userInfo.value?.name || '未登录');
  const isAdmin = computed(() => userInfo.value?.role === 'admin');
  
  // Actions
  const setUserInfo = (info: UserInfo | null) => {
    userInfo.value = info;
    isLoggedIn.value = !!info;
    if (info) {
      localStorage.setItem('user_info', JSON.stringify(info));
    } else {
      localStorage.removeItem('user_info');
    }
  };
  
  const setLoading = (value: boolean) => {
    loading.value = value;
  };
  
  const toggleSidebar = () => {
    sidebarCollapsed.value = !sidebarCollapsed.value;
  };
  
  const setCurrentMonth = (month: string) => {
    currentMonth.value = month;
  };
  
  const logout = () => {
    setUserInfo(null);
    localStorage.removeItem('auth_token');
  };
  
  // 初始化
  const init = () => {
    const storedUserInfo = localStorage.getItem('user_info');
    if (storedUserInfo) {
      try {
        userInfo.value = JSON.parse(storedUserInfo);
        isLoggedIn.value = true;
      } catch {
        localStorage.removeItem('user_info');
      }
    }
  };
  
  // 执行初始化
  init();
  
  return {
    // State
    userInfo,
    isLoggedIn,
    sidebarCollapsed,
    currentMonth,
    loading,
    // Getters
    userName,
    isAdmin,
    // Actions
    setUserInfo,
    setLoading,
    toggleSidebar,
    setCurrentMonth,
    logout,
  };
});
