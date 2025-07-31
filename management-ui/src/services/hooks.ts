import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from './api';
import { type User, type Role, type ServiceAccount, type AuditLog, type Scope, type CreateUserRequest, type UpdateUserRequest, type CreateServiceAccountRequest, type UpdateServiceAccountRequest, type CreateRoleRequest, type UpdateRoleRequest, type CreateScopeRequest, type UpdateScopeRequest } from './mockApi';

// Query keys for React Query
export const queryKeys = {
  users: ['users'] as const,
  user: (id: string) => ['user', id] as const,
  serviceAccounts: ['serviceAccounts'] as const,
  serviceAccount: (id: string) => ['serviceAccount', id] as const,
  roles: ['roles'] as const,
  role: (id: string) => ['role', id] as const,
  scopes: ['scopes'] as const,
  scope: (id: string) => ['scope', id] as const,
  scopesForAccountType: (accountType: string) => ['scopesForAccountType', accountType] as const,
  auditLogs: (resourceType?: string, resourceId?: string) => ['auditLogs', resourceType, resourceId] as const,
  userAuditLogs: (userId: string) => ['userAuditLogs', userId] as const,
  systemStats: ['systemStats'] as const,
  jwtPublicKey: ['jwtPublicKey'] as const,
};

// Users hooks
export const useUsers = () => {
  return useQuery({
    queryKey: queryKeys.users,
    queryFn: api.getUsers,
  });
};

export const useUser = (id: string) => {
  return useQuery({
    queryKey: queryKeys.user(id),
    queryFn: () => api.getUser(id),
    enabled: !!id,
  });
};

export const useCreateUser = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (userData: CreateUserRequest) => api.createUser(userData),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.users });
      queryClient.invalidateQueries({ queryKey: queryKeys.serviceAccounts });
      queryClient.invalidateQueries({ queryKey: queryKeys.systemStats });
    },
  });
};

export const useUpdateUser = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ id, userData }: { id: string; userData: UpdateUserRequest }) =>
      api.updateUser(id, userData),
    onSuccess: (updatedUser, { id }) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.users });
      queryClient.invalidateQueries({ queryKey: queryKeys.serviceAccounts });
      queryClient.invalidateQueries({ queryKey: queryKeys.systemStats });
      if (updatedUser) {
        queryClient.setQueryData(queryKeys.user(id), updatedUser);
      }
    },
  });
};

export const useDeleteUser = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (id: string) => api.deleteUser(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.users });
      queryClient.invalidateQueries({ queryKey: queryKeys.serviceAccounts });
      queryClient.invalidateQueries({ queryKey: queryKeys.systemStats });
    },
  });
};

// Service Account hooks
export const useServiceAccounts = () => {
  return useQuery({
    queryKey: queryKeys.serviceAccounts,
    queryFn: api.getServiceAccounts,
  });
};

export const useServiceAccount = (id: string) => {
  return useQuery({
    queryKey: queryKeys.serviceAccount(id),
    queryFn: () => api.getServiceAccount(id),
    enabled: !!id,
  });
};

export const useCreateServiceAccount = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (serviceAccountData: CreateServiceAccountRequest) => api.createServiceAccount(serviceAccountData),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.serviceAccounts });
      queryClient.invalidateQueries({ queryKey: queryKeys.systemStats });
    },
  });
};

export const useUpdateServiceAccount = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ id, serviceAccountData }: { id: string; serviceAccountData: UpdateServiceAccountRequest }) =>
      api.updateServiceAccount(id, serviceAccountData),
    onSuccess: (updatedServiceAccount, { id }) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.serviceAccounts });
      queryClient.invalidateQueries({ queryKey: queryKeys.systemStats });
      if (updatedServiceAccount) {
        queryClient.setQueryData(queryKeys.serviceAccount(id), updatedServiceAccount);
      }
    },
  });
};

export const useDeleteServiceAccount = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (id: string) => api.deleteServiceAccount(id),
    onSuccess: (_, id) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.serviceAccounts });
      queryClient.removeQueries({ queryKey: queryKeys.serviceAccount(id) });
      queryClient.invalidateQueries({ queryKey: queryKeys.systemStats });
    },
  });
};

export const useResetUserPassword = () => {
  return useMutation({
    mutationFn: ({ id, newPassword }: { id: string; newPassword: string }) =>
      api.resetUserPassword(id, newPassword),
  });
};

// Roles hooks
export const useRoles = () => {
  return useQuery({
    queryKey: queryKeys.roles,
    queryFn: api.getRoles,
  });
};

export const useRole = (id: string) => {
  return useQuery({
    queryKey: queryKeys.role(id),
    queryFn: () => api.getRole(id),
    enabled: !!id,
  });
};

export const useCreateRole = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (roleData: CreateRoleRequest) => api.createRole(roleData),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.roles });
      queryClient.invalidateQueries({ queryKey: queryKeys.serviceAccounts });
      queryClient.invalidateQueries({ queryKey: queryKeys.systemStats });
    },
  });
};

export const useUpdateRole = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ id, roleData }: { id: string; roleData: UpdateRoleRequest }) =>
      api.updateRole(id, roleData),
    onSuccess: (updatedRole, { id }) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.roles });
      if (updatedRole) {
        queryClient.setQueryData(queryKeys.role(id), updatedRole);
      }
    },
  });
};

export const useDeleteRole = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (id: string) => api.deleteRole(id),
    onSuccess: (_, id) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.roles });
      queryClient.removeQueries({ queryKey: queryKeys.role(id) });
      queryClient.invalidateQueries({ queryKey: queryKeys.users });
      queryClient.invalidateQueries({ queryKey: queryKeys.serviceAccounts });
      queryClient.invalidateQueries({ queryKey: queryKeys.systemStats });
    },
  });
};

// Role assignment hooks
export const useAssignRoleToUser = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ userId, roleId }: { userId: string; roleId: string }) =>
      api.assignRoleToUser(userId, roleId),
    onSuccess: (_, { userId, roleId }) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.users });
      queryClient.invalidateQueries({ queryKey: queryKeys.user(userId) });
      queryClient.invalidateQueries({ queryKey: queryKeys.roles });
      queryClient.invalidateQueries({ queryKey: [...queryKeys.roles, 'users', roleId] });
      queryClient.invalidateQueries({ queryKey: [...queryKeys.roles, 'users-not-in', roleId] });
    },
  });
};

export const useRemoveRoleFromUser = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ userId, roleId }: { userId: string; roleId: string }) =>
      api.removeRoleFromUser(userId, roleId),
    onSuccess: (_, { userId, roleId }) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.users });
      queryClient.invalidateQueries({ queryKey: queryKeys.user(userId) });
      queryClient.invalidateQueries({ queryKey: queryKeys.roles });
      queryClient.invalidateQueries({ queryKey: [...queryKeys.roles, 'users', roleId] });
      queryClient.invalidateQueries({ queryKey: [...queryKeys.roles, 'users-not-in', roleId] });
    },
  });
};

// Note: These hooks would need corresponding backend endpoints
// For now, they'll use filtering on the frontend

export const useUsersByRole = (roleId: string) => {
  return useQuery({
    queryKey: [...queryKeys.roles, 'users', roleId],
    queryFn: async () => {
      const users = await api.getUsers();
      return users.filter(user => user.roles.some(role => role.id === roleId));
    },
    enabled: !!roleId,
  });
};

export const useServiceAccountsByRole = (roleId: string) => {
  return useQuery({
    queryKey: [...queryKeys.roles, 'service-accounts', roleId],
    queryFn: async () => {
      // Since the mock API was updated to have separate service accounts
      // we need to update this to use the new mockApi method
      const { mockApi } = await import('./mockApi');
      return mockApi.getServiceAccountsByRole(roleId);
    },
    enabled: !!roleId,
  });
};

export const useUsersNotInRole = (roleId: string) => {
  return useQuery({
    queryKey: [...queryKeys.roles, 'users-not-in', roleId],
    queryFn: async () => {
      const users = await api.getUsers();
      return users.filter(user => 
        !user.roles.some(role => role.id === roleId)
      );
    },
    enabled: !!roleId,
  });
};

export const useServiceAccountsNotInRole = (roleId: string) => {
  return useQuery({
    queryKey: [...queryKeys.roles, 'service-accounts-not-in', roleId],
    queryFn: async () => {
      const { api } = await import('./api');
      const serviceAccounts = await api.getServiceAccounts();
      // Filter out service accounts that already have this role
      return serviceAccounts.filter(serviceAccount => 
        !serviceAccount.roles.some(role => role.id === roleId)
      );
    },
    enabled: !!roleId,
  });
};

export const useAssignRoleToServiceAccount = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async ({ serviceAccountId, roleId }: { serviceAccountId: string; roleId: string }) => {
      const { mockApi } = await import('./mockApi');
      return mockApi.assignRoleToServiceAccount(serviceAccountId, roleId);
    },
    onSuccess: (_, { roleId }) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.serviceAccounts });
      queryClient.invalidateQueries({ queryKey: queryKeys.roles });
      queryClient.invalidateQueries({ queryKey: [...queryKeys.roles, 'service-accounts', roleId] });
      queryClient.invalidateQueries({ queryKey: [...queryKeys.roles, 'service-accounts-not-in', roleId] });
    },
  });
};

export const useRemoveRoleFromServiceAccount = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async ({ serviceAccountId, roleId }: { serviceAccountId: string; roleId: string }) => {
      const { mockApi } = await import('./mockApi');
      return mockApi.removeRoleFromServiceAccount(serviceAccountId, roleId);
    },
    onSuccess: (_, { roleId }) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.serviceAccounts });
      queryClient.invalidateQueries({ queryKey: queryKeys.roles });
      queryClient.invalidateQueries({ queryKey: [...queryKeys.roles, 'service-accounts', roleId] });
      queryClient.invalidateQueries({ queryKey: [...queryKeys.roles, 'service-accounts-not-in', roleId] });
    },
  });
};

// Scope hooks
export const useScopes = () => {
  return useQuery({
    queryKey: queryKeys.scopes,
    queryFn: api.getScopes,
  });
};

export const useScope = (id: string) => {
  return useQuery({
    queryKey: queryKeys.scope(id),
    queryFn: () => api.getScope(id),
    enabled: !!id,
  });
};

export const useCreateScope = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (scopeData: CreateScopeRequest) => api.createScope(scopeData),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.scopes });
      queryClient.invalidateQueries({ queryKey: queryKeys.serviceAccounts });
      queryClient.invalidateQueries({ queryKey: queryKeys.systemStats });
    },
  });
};

export const useUpdateScope = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ id, updates }: { id: string; updates: UpdateScopeRequest }) =>
      api.updateScope(id, updates),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.scopes });
      queryClient.invalidateQueries({ queryKey: queryKeys.scope(id) });
      queryClient.invalidateQueries({ queryKey: queryKeys.serviceAccounts });
    },
  });
};

export const useDeleteScope = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (id: string) => api.deleteScope(id),
    onSuccess: (_, id) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.scopes });
      queryClient.removeQueries({ queryKey: queryKeys.scope(id) });
      queryClient.invalidateQueries({ queryKey: queryKeys.serviceAccounts });
      queryClient.invalidateQueries({ queryKey: queryKeys.systemStats });
    },
  });
};

export const useScopesForAccountType = (accountType: 'Service-to-service' | 'Browser') => {
  return useQuery({
    queryKey: queryKeys.scopesForAccountType(accountType),
    queryFn: () => api.getScopesForAccountType(accountType),
    enabled: !!accountType,
  });
};

export const useBulkActivateScopes = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (scopeIds: string[]) => api.bulkActivateScopes(scopeIds),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.scopes });
      queryClient.invalidateQueries({ queryKey: queryKeys.serviceAccounts });
    },
  });
};

export const useBulkDeactivateScopes = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (scopeIds: string[]) => api.bulkDeactivateScopes(scopeIds),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.scopes });
      queryClient.invalidateQueries({ queryKey: queryKeys.serviceAccounts });
    },
  });
};

export const useBulkDeleteScopes = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (scopeIds: string[]) => api.bulkDeleteScopes(scopeIds),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.scopes });
      queryClient.invalidateQueries({ queryKey: queryKeys.serviceAccounts });
      queryClient.invalidateQueries({ queryKey: queryKeys.systemStats });
    },
  });
};

// Audit logs hooks
export const useAuditLogs = (resourceType?: string, resourceId?: string) => {
  return useQuery({
    queryKey: queryKeys.auditLogs(resourceType, resourceId),
    queryFn: () => api.getAuditLogs(resourceType, resourceId),
  });
};

export const useUserAuditLogs = (userId: string) => {
  return useQuery({
    queryKey: queryKeys.userAuditLogs(userId),
    queryFn: () => api.getUserAuditLogs(userId),
    enabled: !!userId,
  });
};

// System hooks
export const useSystemStats = () => {
  return useQuery({
    queryKey: queryKeys.systemStats,
    queryFn: api.getSystemStats,
  });
};

export const useJwtPublicKey = () => {
  return useQuery({
    queryKey: queryKeys.jwtPublicKey,
    queryFn: api.getJWTPublicKey,
  });
};

// Lock/unlock user hooks (if needed)
export const useLockUser = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (userId: string) => api.lockUser(userId),
    onSuccess: (updatedUser, userId) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.users });
      if (updatedUser) {
        queryClient.setQueryData(queryKeys.user(userId), updatedUser);
      }
    },
  });
};

export const useUnlockUser = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (userId: string) => api.unlockUser(userId),
    onSuccess: (updatedUser, userId) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.users });
      if (updatedUser) {
        queryClient.setQueryData(queryKeys.user(userId), updatedUser);
      }
    },
  });
};

// Export types for convenience
export type {
  User,
  Role,
  ServiceAccount,
  AuditLog,
  CreateUserRequest,
  UpdateUserRequest,
  CreateServiceAccountRequest,
  UpdateServiceAccountRequest,
  CreateRoleRequest,
  UpdateRoleRequest,
};
