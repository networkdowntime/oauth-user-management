/**
 * Real API service for communicating with the auth backend
 * Replaces the mock API with actual HTTP calls
 */

import axios, { AxiosResponse } from 'axios';

import type {
  User,
  Role,
  ServiceAccount,
  Scope,
  ScopeAppliesTo,
  AuditLog,
  CreateUserRequest,
  UpdateUserRequest,
  CreateServiceAccountRequest,
  UpdateServiceAccountRequest,
  CreateRoleRequest,
  UpdateRoleRequest,
  CreateScopeRequest,
  UpdateScopeRequest
} from './mockApi';

// Re-export for compatibility
export type {
  User,
  Role,
  ServiceAccount,
  Scope,
  ScopeAppliesTo,
  AuditLog,
  CreateUserRequest,
  UpdateUserRequest,
  CreateServiceAccountRequest,
  UpdateServiceAccountRequest,
  CreateRoleRequest,
  UpdateRoleRequest,
  CreateScopeRequest,
  UpdateScopeRequest
} from './mockApi';

// API Client Configuration
const API_BASE_URL = process.env.REACT_APP_AUTH_BACKEND_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for authentication
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access - redirect to login
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Type definitions for API responses (matching backend schemas)
// Backend API interfaces
interface UserResponse {
  id: string;
  email: string;
  display_name?: string;
  is_active: boolean;
  last_login_at?: string;
  failed_login_attempts: number;
  locked_until?: string;
  social_provider?: string;
  created_at: string;
  updated_at: string;
  roles: {
    id: string;
    name: string;
    description?: string;
    created_at: string;
    updated_at: string;
  }[];
}

// Paginated response interface for list endpoints
interface PaginatedResponse<T> {
  items: T[];
  total: number;
  skip: number;
  limit: number;
}

interface ServiceAccountResponse {
  id: string;
  client_id: string;
  client_name: string;
  description?: string;
  account_type: string;
  grant_types: string[];
  scopes: {
    id: string;
    name: string;
    description?: string;
  }[];
  token_endpoint_auth_method: string;
  audience?: string[];
  owner?: string;
  client_metadata?: Record<string, any>;
  redirect_uris?: string[];
  skip_consent: boolean;
  is_active: boolean;
  client_secret?: string;
  response_types: string[];
  last_used_at?: string;
  created_by: string;
  created_at: string;
  updated_at: string;
  roles: {
    id: string;
    name: string;
    description?: string;
    created_at: string;
    updated_at: string;
  }[];
}interface RoleResponse {
  id: string;
  name: string;
  description?: string;
  created_at: string;
  updated_at: string;
  user_count?: number;
}

interface AuditLogResponse {
  id: string;
  action: string;
  resource_type: string;
  resource_id?: string;
  details?: Record<string, any>;
  performed_by: string;
  ip_address?: string;
  user_agent?: string;
  timestamp: string;
}

interface SuccessResponse {
  success: boolean;
  message: string;
}

// Transform functions to match frontend interface
const transformUser = (backendUser: UserResponse): import('./mockApi').User => ({
  id: backendUser.id,
  email: backendUser.email,
  displayName: backendUser.display_name,
  isActive: backendUser.is_active,
  lastLoginAt: backendUser.last_login_at,
  failedLoginAttempts: backendUser.failed_login_attempts,
  lockedUntil: backendUser.locked_until,
  socialProvider: backendUser.social_provider,
  createdAt: backendUser.created_at,
  updatedAt: backendUser.updated_at,
  roles: backendUser.roles.map(role => ({
    id: role.id,
    name: role.name,
    description: role.description,
    createdAt: backendUser.created_at, // Placeholder - roles don't have these in the nested response
    updatedAt: backendUser.updated_at,
  })),
});

const transformServiceAccount = (backendServiceAccount: ServiceAccountResponse): import('./mockApi').ServiceAccount => ({
  id: backendServiceAccount.id,
  clientId: backendServiceAccount.client_id,
  clientName: backendServiceAccount.client_name,
  description: backendServiceAccount.description,
  accountType: backendServiceAccount.account_type as 'Service-to-service' | 'Browser',
  grantTypes: backendServiceAccount.grant_types,
  scopes: (backendServiceAccount.scopes || []).map(scope => ({
    id: scope.id,
    name: scope.name,
    description: scope.description || '',
    appliesTo: [], // This would need to be populated by a separate API call if needed
    isActive: true, // Default value - would need to be populated by backend
    serviceAccountCount: 0, // Default value - would need to be populated by backend
    createdAt: '', // Default value - would need to be populated by backend
    updatedAt: '', // Default value - would need to be populated by backend
  })),
  tokenEndpointAuthMethod: backendServiceAccount.token_endpoint_auth_method,
  audience: backendServiceAccount.audience,
  owner: backendServiceAccount.owner,
  clientMetadata: backendServiceAccount.client_metadata,
  redirectUris: backendServiceAccount.redirect_uris,
  skipConsent: backendServiceAccount.skip_consent,
  isActive: backendServiceAccount.is_active,
  clientSecret: backendServiceAccount.client_secret,
  responseTypes: backendServiceAccount.response_types,
  lastUsedAt: backendServiceAccount.last_used_at,
  createdBy: backendServiceAccount.created_by,
  createdAt: backendServiceAccount.created_at,
  updatedAt: backendServiceAccount.updated_at,
  roles: backendServiceAccount.roles.map(role => ({
    id: role.id,
    name: role.name,
    description: role.description,
    createdAt: role.created_at,
    updatedAt: role.updated_at,
  })),
});

const transformRole = (backendRole: RoleResponse): import('./mockApi').Role => ({
  id: backendRole.id,
  name: backendRole.name,
  description: backendRole.description,
  createdAt: backendRole.created_at,
  updatedAt: backendRole.updated_at,
  userCount: backendRole.user_count,
});

const transformAuditLog = (backendLog: AuditLogResponse): import('./mockApi').AuditLog => ({
  id: backendLog.id,
  action: backendLog.action,
  resourceType: backendLog.resource_type,
  resourceId: backendLog.resource_id,
  details: backendLog.details,
  performedBy: backendLog.performed_by,
  ipAddress: backendLog.ip_address,
  userAgent: backendLog.user_agent,
  timestamp: backendLog.timestamp,
});

// Transform frontend requests to backend format
const transformCreateUserRequest = (frontendRequest: import('./mockApi').CreateUserRequest) => ({
  email: frontendRequest.email,
  display_name: frontendRequest.displayName,
  password: frontendRequest.password,
});

const transformUpdateUserRequest = (frontendRequest: import('./mockApi').UpdateUserRequest) => ({
  display_name: frontendRequest.displayName,
  is_active: frontendRequest.isActive,
  role_ids: frontendRequest.roleIds,
});

const transformCreateRoleRequest = (frontendRequest: import('./mockApi').CreateRoleRequest) => ({
  name: frontendRequest.name,
  description: frontendRequest.description,
});

const transformUpdateRoleRequest = (frontendRequest: import('./mockApi').UpdateRoleRequest) => ({
  name: frontendRequest.name,
  description: frontendRequest.description,
});

const transformCreateServiceAccountRequest = (frontendRequest: import('./mockApi').CreateServiceAccountRequest) => ({
  client_id: frontendRequest.clientId,
  client_name: frontendRequest.clientName,
  description: frontendRequest.description,
  account_type: frontendRequest.accountType || 'Service-to-service',
  scope_ids: frontendRequest.scopeIds || [],
  role_ids: frontendRequest.roleIds || [],
  owner: frontendRequest.owner,
  redirect_uris: frontendRequest.redirectUris || [],
  created_by: frontendRequest.createdBy,
});

// API Methods
export const api = {
  // Health check
  async healthCheck(): Promise<{ status: string }> {
    const response = await apiClient.get('/health');
    return response.data;
  },

  // User Management
  async getUsers(): Promise<import('./mockApi').User[]> {
    const response = await apiClient.get<UserResponse[]>('/users');
    return response.data.map(transformUser);
  },

  async getUser(id: string): Promise<import('./mockApi').User> {
    const response = await apiClient.get<UserResponse>(`/users/${id}`);
    return transformUser(response.data);
  },

  async createUser(userData: import('./mockApi').CreateUserRequest): Promise<import('./mockApi').User> {
    const backendRequest = transformCreateUserRequest(userData);
    const response = await apiClient.post<UserResponse>('/users', backendRequest);
    return transformUser(response.data);
  },

  async updateUser(id: string, userData: import('./mockApi').UpdateUserRequest): Promise<import('./mockApi').User> {
    const backendRequest = transformUpdateUserRequest(userData);
    const response = await apiClient.put<UserResponse>(`/users/${id}`, backendRequest);
    return transformUser(response.data);
  },

  async deleteUser(id: string): Promise<void> {
    await apiClient.delete(`/users/${id}`);
  },

  async lockUser(id: string): Promise<import('./mockApi').User> {
    const response = await apiClient.post<UserResponse>(`/users/${id}/lock`);
    return transformUser(response.data);
  },

  async unlockUser(id: string): Promise<import('./mockApi').User> {
    const response = await apiClient.post<UserResponse>(`/users/${id}/unlock`);
    return transformUser(response.data);
  },

  async resetUserPassword(id: string, newPassword: string): Promise<void> {
    await apiClient.post(`/users/${id}/reset-password`, { new_password: newPassword });
  },

  // Role Management
  async getRoles(): Promise<import('./mockApi').Role[]> {
    const response = await apiClient.get<RoleResponse[]>('/roles');
    return response.data.map(transformRole);
  },

  async getRole(id: string): Promise<import('./mockApi').Role> {
    const response = await apiClient.get<RoleResponse>(`/roles/${id}`);
    return transformRole(response.data);
  },

  async createRole(roleData: import('./mockApi').CreateRoleRequest): Promise<import('./mockApi').Role> {
    const backendRequest = transformCreateRoleRequest(roleData);
    const response = await apiClient.post<RoleResponse>('/roles', backendRequest);
    return transformRole(response.data);
  },

  async updateRole(id: string, roleData: import('./mockApi').UpdateRoleRequest): Promise<import('./mockApi').Role> {
    const backendRequest = transformUpdateRoleRequest(roleData);
    const response = await apiClient.put<RoleResponse>(`/roles/${id}`, backendRequest);
    return transformRole(response.data);
  },

  async deleteRole(id: string): Promise<void> {
    await apiClient.delete(`/roles/${id}`);
  },

  async assignRoleToUser(userId: string, roleId: string): Promise<void> {
    await apiClient.post(`/users/${userId}/roles/${roleId}`);
  },

  async removeRoleFromUser(userId: string, roleId: string): Promise<void> {
    await apiClient.delete(`/users/${userId}/roles/${roleId}`);
  },

  // Service Account Management
  async getServiceAccounts(): Promise<import('./mockApi').ServiceAccount[]> {
    const response = await apiClient.get<PaginatedResponse<ServiceAccountResponse>>('/service-accounts');
    return response.data.items.map(transformServiceAccount);
  },

  async getServiceAccount(id: string): Promise<import('./mockApi').ServiceAccount> {
    const response = await apiClient.get<ServiceAccountResponse>(`/service-accounts/${id}`);
    return transformServiceAccount(response.data);
  },

  async createServiceAccount(serviceAccountData: import('./mockApi').CreateServiceAccountRequest): Promise<import('./mockApi').ServiceAccount> {
    const backendRequest = transformCreateServiceAccountRequest(serviceAccountData);
    const response = await apiClient.post<ServiceAccountResponse>('/service-accounts', backendRequest);
    return transformServiceAccount(response.data);
  },

  async updateServiceAccount(id: string, serviceAccountData: import('./mockApi').UpdateServiceAccountRequest): Promise<import('./mockApi').ServiceAccount> {
    const backendRequest = {
      client_name: serviceAccountData.clientName,
      description: serviceAccountData.description,
      is_active: serviceAccountData.isActive,
      scope_ids: serviceAccountData.scopeIds,
      owner: serviceAccountData.owner,
      redirect_uris: serviceAccountData.redirectUris,
      role_ids: serviceAccountData.roleIds,
    };
    const response = await apiClient.put<ServiceAccountResponse>(`/service-accounts/${id}`, backendRequest);
    return transformServiceAccount(response.data);
  },

  async deleteServiceAccount(id: string): Promise<void> {
    await apiClient.delete(`/service-accounts/${id}`);
  },

  // Service Account Role Management
  async assignRoleToServiceAccount(serviceAccountId: string, roleId: string): Promise<ServiceAccount> {
    const response = await apiClient.post<ServiceAccountResponse>(`/service-accounts/${serviceAccountId}/roles/${roleId}`);
    return transformServiceAccount(response.data);
  },

  async removeRoleFromServiceAccount(serviceAccountId: string, roleId: string): Promise<ServiceAccount> {
    const response = await apiClient.delete<ServiceAccountResponse>(`/service-accounts/${serviceAccountId}/roles/${roleId}`);
    return transformServiceAccount(response.data);
  },

  // Audit Logs
  async getAuditLogs(resourceType?: string, resourceId?: string): Promise<import('./mockApi').AuditLog[]> {
    let url = '/audit-logs';
    const params = new URLSearchParams();
    if (resourceType) params.append('resource_type', resourceType);
    if (resourceId) params.append('resource_id', resourceId);
    if (params.toString()) url += `?${params.toString()}`;
    
    const response = await apiClient.get<AuditLogResponse[]>(url);
    return response.data.map(transformAuditLog);
  },

  async getUserAuditLogs(userId: string): Promise<import('./mockApi').AuditLog[]> {
    const response = await apiClient.get<AuditLogResponse[]>(`/users/${userId}/audit-logs`);
    return response.data.map(transformAuditLog);
  },

  // System Statistics
  async getSystemStats(): Promise<{
    totalUsers: number;
    totalRoles: number;
    activeUsers: number;
    inactiveUsers: number;
    lockedUsers: number;
    serviceAccounts: number;
  }> {
    try {
      // Try to get from backend endpoint first
      const response = await apiClient.get<{users: number, services: number, roles: number}>('/system-stats');
      
      // Transform backend response to frontend format
      // Note: Backend only provides basic counts, so we'll use those for totals
      // and fallback to individual API calls for detailed stats
      return {
        totalUsers: response.data.users,
        totalRoles: response.data.roles,
        serviceAccounts: response.data.services,
        // For these detailed stats, we need to get individual user data
        activeUsers: response.data.users, // Placeholder - backend doesn't provide breakdown
        inactiveUsers: 0, // Placeholder
        lockedUsers: 0, // Placeholder
      };
    } catch (error) {
      // Fallback to calculating from existing data
      const users = await this.getUsers();
      const serviceAccounts = await this.getServiceAccounts();
      const roles = await this.getRoles();
      
      return {
        totalUsers: users.length,
        totalRoles: roles.length,
        activeUsers: users.filter(u => u.isActive).length,
        inactiveUsers: users.filter(u => !u.isActive).length,
        lockedUsers: users.filter(u => u.lockedUntil && new Date(u.lockedUntil) > new Date()).length,
        serviceAccounts: serviceAccounts.length,
      };
    }
  },

  // JWT Public Key
  async getJWTPublicKey(): Promise<string> {
    try {
      const response = await apiClient.get<string>('/jwt-public-key');
      return response.data;
    } catch (error) {
      // Return placeholder if endpoint not available
      return 'PUBLIC_KEY_PLACEHOLDER';
    }
  },

  // Scope Management
  async getScopes(): Promise<Scope[]> {
    try {
      const response = await apiClient.get<any>('/scopes/');
      
      // Transform backend response to frontend type
      const scopes = (response.data.scopes || response.data || []).map((scope: any) => ({
        ...scope,
        appliesTo: scope.applies_to || scope.appliesTo || [],
        isActive: scope.is_active ?? scope.isActive ?? true,
        serviceAccountCount: scope.service_account_count || scope.serviceAccountCount || 0,
        createdAt: scope.created_at || scope.createdAt || new Date().toISOString(),
        updatedAt: scope.updated_at || scope.updatedAt || new Date().toISOString(),
      }));
      
      return scopes;
    } catch (error) {
      console.error('Error fetching scopes:', error);
      throw error;
    }
  },

  async getScope(id: string): Promise<Scope | null> {
    try {
      const response = await apiClient.get<any>(`/scopes/${id}`);
      
      // Transform backend response to frontend type
      return {
        ...response.data,
        appliesTo: response.data.applies_to || response.data.appliesTo || [],
        isActive: response.data.is_active ?? response.data.isActive ?? true,
        serviceAccountCount: response.data.service_account_count || response.data.serviceAccountCount || 0,
        createdAt: response.data.created_at || response.data.createdAt || new Date().toISOString(),
        updatedAt: response.data.updated_at || response.data.updatedAt || new Date().toISOString(),
      };
    } catch (error) {
      console.error('Error fetching scope:', error);
      return null;
    }
  },

  async createScope(scopeData: CreateScopeRequest): Promise<Scope> {
    try {
      // Transform frontend type to backend type
      const backendData = {
        name: scopeData.name,
        description: scopeData.description,
        applies_to: scopeData.appliesTo, // Convert from appliesTo to applies_to
        is_active: scopeData.isActive ?? true,
      };
      
      const response = await apiClient.post<Scope>('/scopes/', backendData);
      
      // Transform backend response to frontend type
      return {
        ...response.data,
        appliesTo: (response.data as any).applies_to || [], // Convert from applies_to to appliesTo
        isActive: (response.data as any).is_active ?? true,
        serviceAccountCount: (response.data as any).service_account_count || 0,
        createdAt: (response.data as any).created_at || new Date().toISOString(),
        updatedAt: (response.data as any).updated_at || new Date().toISOString(),
      };
    } catch (error) {
      console.error('Error creating scope:', error);
      throw error;
    }
  },

  async updateScope(id: string, updates: UpdateScopeRequest): Promise<Scope | null> {
    try {
      // Transform frontend type to backend type
      const backendData: any = {};
      if (updates.description !== undefined) backendData.description = updates.description;
      if (updates.appliesTo !== undefined) backendData.applies_to = updates.appliesTo;
      if (updates.isActive !== undefined) backendData.is_active = updates.isActive;
      
      const response = await apiClient.put<Scope>(`/scopes/${id}`, backendData);
      
      // Transform backend response to frontend type
      return {
        ...response.data,
        appliesTo: (response.data as any).applies_to || [],
        isActive: (response.data as any).is_active ?? true,
        serviceAccountCount: (response.data as any).service_account_count || 0,
        createdAt: (response.data as any).created_at || new Date().toISOString(),
        updatedAt: (response.data as any).updated_at || new Date().toISOString(),
      };
    } catch (error) {
      console.error('Error updating scope:', error);
      return null;
    }
  },

  async deleteScope(id: string): Promise<boolean> {
    try {
      await apiClient.delete(`/scopes/${id}`);
      return true;
    } catch (error) {
      console.error('Error deleting scope:', error);
      throw error;
    }
  },

  async getScopesForAccountType(accountType: 'Service-to-service' | 'Browser'): Promise<Scope[]> {
    try {
      const response = await apiClient.get<{ scopes: Scope[] }>(`/scopes/for-account-type/${encodeURIComponent(accountType)}`);
      return response.data.scopes.map(scope => ({
        ...scope,
        appliesTo: (scope as any).applies_to || [],
        isActive: (scope as any).is_active ?? true,
        serviceAccountCount: (scope as any).service_account_count || 0,
        createdAt: (scope as any).created_at || new Date().toISOString(),
        updatedAt: (scope as any).updated_at || new Date().toISOString(),
      }));
    } catch (error) {
      console.error('Error fetching scopes for account type:', error);
      throw error;
    }
  },

  async bulkActivateScopes(scopeIds: string[]): Promise<{ updated: number }> {
    try {
      const response = await apiClient.post<{ message: string }>('/scopes/bulk/activate', {
        scope_ids: scopeIds,
      });
      // Extract number from message like "Activated 3 scopes"
      const match = response.data.message.match(/\d+/);
      return { updated: match ? parseInt(match[0]) : 0 };
    } catch (error) {
      console.error('Error bulk activating scopes:', error);
      throw error;
    }
  },

  async bulkDeactivateScopes(scopeIds: string[]): Promise<{ updated: number }> {
    try {
      const response = await apiClient.post<{ message: string }>('/scopes/bulk/deactivate', {
        scope_ids: scopeIds,
      });
      // Extract number from message like "Deactivated 3 scopes"
      const match = response.data.message.match(/\d+/);
      return { updated: match ? parseInt(match[0]) : 0 };
    } catch (error) {
      console.error('Error bulk deactivating scopes:', error);
      throw error;
    }
  },

  async bulkDeleteScopes(scopeIds: string[]): Promise<{ deleted: number }> {
    try {
      const response = await apiClient.post<{ message: string }>('/scopes/bulk/delete', {
        scope_ids: scopeIds,
      });
      // Extract number from message like "Deleted 3 scopes"
      const match = response.data.message.match(/\d+/);
      return { deleted: match ? parseInt(match[0]) : 0 };
    } catch (error) {
      console.error('Error bulk deleting scopes:', error);
      throw error;
    }
  },
};
