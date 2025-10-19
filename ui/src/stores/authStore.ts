import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import authService from '../services/authService';
import type { User, RegisterData, LoginData } from '../models/auth';

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<User | null>(null);
  const isAuthenticated = ref(false);
  const loading = ref(false);
  const error = ref<string | null>(null);

  // Computed
  const userRole = computed(() => user.value?.role);
  const hasRole = computed(() => !!user.value?.role);
  const isEmailVerified = computed(() => user.value?.is_email_verified || false);

  // Actions
  
  /**
   * Initialize store from localStorage
   */
  function initializeAuth() {
    const storedUser = authService.getStoredUser();
    const authenticated = authService.isAuthenticated();
    
    if (storedUser && authenticated) {
      user.value = storedUser;
      isAuthenticated.value = true;
    }
  }

  /**
   * Register new user
   */
  async function register(data: RegisterData) {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await authService.register(data);
      user.value = response.data.user;
      isAuthenticated.value = true;
      return response;
    } catch (err: any) {
      error.value = err.response?.data?.errors || err.message || 'Registration failed';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  /**
   * Login user
   */
  async function login(data: LoginData) {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await authService.login(data);
      user.value = response.data.user;
      isAuthenticated.value = true;
      return response;
    } catch (err: any) {
      error.value = err.response?.data?.errors || err.message || 'Login failed';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  /**
   * Logout user
   */
  async function logout() {
    loading.value = true;
    error.value = null;
    
    try {
      await authService.logout();
    } catch (err: any) {
      console.error('Logout error:', err);
    } finally {
      user.value = null;
      isAuthenticated.value = false;
      loading.value = false;
    }
  }

  /**
   * Select user role
   */
  async function selectRole(role: 'BRAND' | 'INFLUENCER') {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await authService.selectRole(role);
      user.value = response.data.user;
      return response;
    } catch (err: any) {
      error.value = err.response?.data?.errors || err.message || 'Role selection failed';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  /**
   * Fetch current user data
   */
  async function fetchCurrentUser() {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await authService.getCurrentUser();
      user.value = response.data.user;
      isAuthenticated.value = true;
      return response;
    } catch (err: any) {
      error.value = err.response?.data?.errors || err.message || 'Failed to fetch user';
      // If fetch fails, clear auth state
      user.value = null;
      isAuthenticated.value = false;
      throw err;
    } finally {
      loading.value = false;
    }
  }

  /**
   * Request password reset
   */
  async function requestPasswordReset(email: string) {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await authService.requestPasswordReset(email);
      return response;
    } catch (err: any) {
      error.value = err.response?.data?.errors || err.message || 'Password reset request failed';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  /**
   * Confirm password reset
   */
  async function confirmPasswordReset(
    uid: string,
    token: string,
    password: string,
    password_confirm: string
  ) {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await authService.confirmPasswordReset(uid, token, password, password_confirm);
      return response;
    } catch (err: any) {
      error.value = err.response?.data?.errors || err.message || 'Password reset failed';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  /**
   * Change password
   */
  async function changePassword(
    old_password: string,
    new_password: string,
    new_password_confirm: string
  ) {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await authService.changePassword(old_password, new_password, new_password_confirm);
      return response;
    } catch (err: any) {
      error.value = err.response?.data?.errors || err.message || 'Password change failed';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  /**
   * Delete user account
   */
  async function deleteAccount() {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await authService.deleteAccount();
      user.value = null;
      isAuthenticated.value = false;
      return response;
    } catch (err: any) {
      error.value = err.response?.data?.errors || err.message || 'Account deletion failed';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  /**
   * Clear error
   */
  function clearError() {
    error.value = null;
  }

  return {
    // State
    user,
    isAuthenticated,
    loading,
    error,
    // Computed
    userRole,
    hasRole,
    isEmailVerified,
    // Actions
    initializeAuth,
    register,
    login,
    logout,
    selectRole,
    fetchCurrentUser,
    requestPasswordReset,
    confirmPasswordReset,
    changePassword,
    deleteAccount,
    clearError,
  };
});
