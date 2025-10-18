import apiClient from './api';

export interface RegisterData {
  email: string;
  password: string;
  password_confirm: string;
  first_name?: string;
  last_name?: string;
  gdpr_consent: boolean;
}

export interface LoginData {
  email: string;
  password: string;
}

export interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  role: 'BRAND' | 'INFLUENCER' | null;
  is_email_verified: boolean;
  gdpr_consent: boolean;
  created_at: string;
  updated_at: string;
}

export interface AuthResponse {
  status: string;
  data: {
    user: User;
    tokens: {
      access: string;
      refresh: string;
    };
  };
  errors: any[];
}

export interface ApiResponse<T> {
  status: string;
  data: T;
  errors: any[];
}

const authService = {
  /**
   * Register a new user
   */
  async register(data: RegisterData): Promise<AuthResponse> {
    const response = await apiClient.post<AuthResponse>('/api/v1/auth/register/', data);
    
    if (response.data.status === 'success') {
      // Store tokens and user data
      localStorage.setItem('accessToken', response.data.data.tokens.access);
      localStorage.setItem('refreshToken', response.data.data.tokens.refresh);
      localStorage.setItem('user', JSON.stringify(response.data.data.user));
    }
    
    return response.data;
  },

  /**
   * Login user
   */
  async login(data: LoginData): Promise<AuthResponse> {
    const response = await apiClient.post<AuthResponse>('/api/v1/auth/login/', data);
    
    if (response.data.status === 'success') {
      // Store tokens and user data
      localStorage.setItem('accessToken', response.data.data.tokens.access);
      localStorage.setItem('refreshToken', response.data.data.tokens.refresh);
      localStorage.setItem('user', JSON.stringify(response.data.data.user));
    }
    
    return response.data;
  },

  /**
   * Logout user
   */
  async logout(): Promise<void> {
    try {
      const refreshToken = localStorage.getItem('refreshToken');
      
      if (refreshToken) {
        await apiClient.post('/api/v1/auth/logout/', {
          refresh: refreshToken,
        });
      }
    } finally {
      // Clear local storage regardless of API call success
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      localStorage.removeItem('user');
    }
  },

  /**
   * Select user role (Brand or Influencer)
   */
  async selectRole(role: 'BRAND' | 'INFLUENCER'): Promise<ApiResponse<{ user: User; message: string }>> {
    const response = await apiClient.post<ApiResponse<{ user: User; message: string }>>(
      '/api/v1/auth/role/',
      { role }
    );
    
    if (response.data.status === 'success') {
      // Update stored user data
      localStorage.setItem('user', JSON.stringify(response.data.data.user));
    }
    
    return response.data;
  },

  /**
   * Get current user data
   */
  async getCurrentUser(): Promise<ApiResponse<{ user: User }>> {
    const response = await apiClient.get<ApiResponse<{ user: User }>>('/api/v1/auth/me/');
    
    if (response.data.status === 'success') {
      // Update stored user data
      localStorage.setItem('user', JSON.stringify(response.data.data.user));
    }
    
    return response.data;
  },

  /**
   * Request password reset
   */
  async requestPasswordReset(email: string): Promise<ApiResponse<{ message: string }>> {
    const response = await apiClient.post<ApiResponse<{ message: string }>>(
      '/api/v1/auth/password/reset/',
      { email }
    );
    return response.data;
  },

  /**
   * Confirm password reset with token
   */
  async confirmPasswordReset(
    uid: string,
    token: string,
    password: string,
    password_confirm: string
  ): Promise<ApiResponse<{ message: string }>> {
    const response = await apiClient.post<ApiResponse<{ message: string }>>(
      '/api/v1/auth/password/reset/confirm/',
      {
        uid,
        token,
        password,
        password_confirm,
      }
    );
    return response.data;
  },

  /**
   * Change password for authenticated user
   */
  async changePassword(
    old_password: string,
    new_password: string,
    new_password_confirm: string
  ): Promise<ApiResponse<{ message: string }>> {
    const response = await apiClient.post<ApiResponse<{ message: string }>>(
      '/api/v1/auth/password/change/',
      {
        old_password,
        new_password,
        new_password_confirm,
      }
    );
    return response.data;
  },

  /**
   * Delete user account (GDPR)
   */
  async deleteAccount(): Promise<ApiResponse<{ message: string }>> {
    const response = await apiClient.delete<ApiResponse<{ message: string }>>(
      '/api/v1/auth/delete/'
    );
    
    // Clear local storage after deletion
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('user');
    
    return response.data;
  },

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    return !!localStorage.getItem('accessToken');
  },

  /**
   * Get stored user data
   */
  getStoredUser(): User | null {
    const userStr = localStorage.getItem('user');
    if (userStr) {
      try {
        return JSON.parse(userStr);
      } catch {
        return null;
      }
    }
    return null;
  },
};

export default authService;
