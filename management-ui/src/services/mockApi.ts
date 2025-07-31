// Mock API service for development
// This will be replaced with real API calls later

export interface User {
  id: string;
  email: string;
  displayName?: string;
  isActive: boolean;
  lastLoginAt?: string;
  failedLoginAttempts: number;
  lockedUntil?: string;
  socialProvider?: string;
  createdAt: string;
  updatedAt: string;
  roles: Role[];
}

export interface Role {
  id: string;
  name: string;
  description?: string;
  createdAt: string;
  updatedAt: string;
  userCount?: number;
}

export type ScopeAppliesTo = 'Service-to-service' | 'Browser';

export interface Scope {
  id: string;
  name: string;
  description: string;
  appliesTo: ScopeAppliesTo[];
  isActive: boolean;
  serviceAccountCount: number;
  createdAt: string;
  updatedAt: string;
}

export interface ServiceAccount {
  id: string;
  clientId: string;
  clientName: string;
  description?: string;
  accountType: 'Service-to-service' | 'Browser';
  grantTypes: string[];
  scopes: Scope[];
  tokenEndpointAuthMethod: string;
  audience?: string[];
  owner?: string;
  clientMetadata?: Record<string, any>;
  redirectUris?: string[];
  skipConsent: boolean;
  isActive: boolean;
  clientSecret?: string;
  responseTypes: string[];
  lastUsedAt?: string;
  createdBy: string;
  createdAt: string;
  updatedAt: string;
  roles: Role[];
}

export interface AuditLog {
  id: string;
  action: string;
  resourceType: string;
  resourceId?: string;
  details?: Record<string, any>;
  performedBy: string;
  ipAddress?: string;
  userAgent?: string;
  timestamp: string;
}

export interface CreateUserRequest {
  email: string;
  displayName?: string;
  password: string;
}

export interface UpdateUserRequest {
  displayName?: string;
  isActive?: boolean;
  roleIds?: string[];
}

export interface CreateServiceAccountRequest {
  clientId: string;
  clientName: string;
  description?: string;
  accountType?: 'Service-to-service' | 'Browser';
  scopeIds?: string[];
  roleIds?: string[];
  owner?: string;
  redirectUris?: string[];
  grantTypes?: string[];
  createdBy: string;
}

export interface UpdateServiceAccountRequest {
  clientName?: string;
  description?: string;
  isActive?: boolean;
  scopeIds?: string[];
  owner?: string;
  redirectUris?: string[];
  grantTypes?: string[];
  roleIds?: string[];
}

export interface CreateRoleRequest {
  name: string;
  description?: string;
}

export interface UpdateRoleRequest {
  name?: string;
  description?: string;
}

export interface CreateScopeRequest {
  name: string;
  description: string;
  appliesTo: ScopeAppliesTo[];
  isActive?: boolean;
}

export interface UpdateScopeRequest {
  description?: string;
  appliesTo?: ScopeAppliesTo[];
  isActive?: boolean;
}

// Mock data
const mockRoles: Role[] = [
  {
    id: '1',
    name: 'user_admin',
    description: 'Administrator role with full system access',
    createdAt: '2024-01-01T00:00:00Z',
    updatedAt: '2024-01-01T00:00:00Z',
    userCount: 2,
  },
  {
    id: '2',
    name: 'read_only',
    description: 'Read-only access to system resources',
    createdAt: '2024-01-01T00:00:00Z',
    updatedAt: '2024-01-01T00:00:00Z',
    userCount: 5,
  },
  {
    id: '3',
    name: 'service_access',
    description: 'Service-to-service communication access',
    createdAt: '2024-01-01T00:00:00Z',
    updatedAt: '2024-01-01T00:00:00Z',
    userCount: 3,
  },
];

const mockScopes: Scope[] = [
  {
    id: '1',
    name: 'user:read',
    description: 'Read access to user information',
    appliesTo: ['Service-to-service', 'Browser'],
    isActive: true,
    serviceAccountCount: 3,
    createdAt: '2024-01-01T00:00:00Z',
    updatedAt: '2024-01-01T00:00:00Z',
  },
  {
    id: '2',
    name: 'user:write',
    description: 'Write access to user information',
    appliesTo: ['Service-to-service'],
    isActive: true,
    serviceAccountCount: 2,
    createdAt: '2024-01-01T00:00:00Z',
    updatedAt: '2024-01-01T00:00:00Z',
  },
  {
    id: '3',
    name: 'analytics:read',
    description: 'Read access to analytics data',
    appliesTo: ['Service-to-service', 'Browser'],
    isActive: true,
    serviceAccountCount: 1,
    createdAt: '2024-01-01T00:00:00Z',
    updatedAt: '2024-01-01T00:00:00Z',
  },
  {
    id: '4',
    name: 'analytics:write',
    description: 'Write access to analytics data',
    appliesTo: ['Service-to-service'],
    isActive: true,
    serviceAccountCount: 1,
    createdAt: '2024-01-01T00:00:00Z',
    updatedAt: '2024-01-01T00:00:00Z',
  },
  {
    id: '5',
    name: 'reporting:read',
    description: 'Read access to reporting data',
    appliesTo: ['Service-to-service', 'Browser'],
    isActive: false,
    serviceAccountCount: 0,
    createdAt: '2024-01-01T00:00:00Z',
    updatedAt: '2024-01-01T00:00:00Z',
  },
];

// Mock data - remove service users and replace with separate service accounts
const mockUsers: User[] = [
  {
    id: '1',
    email: 'admin@example.com',
    displayName: 'Admin User',
    isActive: true,
    failedLoginAttempts: 0,
    lastLoginAt: '2024-01-15T10:30:00Z',
    createdAt: '2024-01-01T00:00:00Z',
    updatedAt: '2024-01-15T10:30:00Z',
    roles: [mockRoles[0], mockRoles[1]],
  },
  {
    id: '2',
    email: 'john.doe@example.com',
    displayName: 'John Doe',
    isActive: true,
    failedLoginAttempts: 0,
    createdAt: '2024-01-02T00:00:00Z',
    updatedAt: '2024-01-02T00:00:00Z',
    roles: [mockRoles[2]],
  },
];

// Mock service accounts - separate from users
const mockServiceAccounts: ServiceAccount[] = [
  {
    id: 'sa-1',
    clientId: 'analytics-service-client',
    clientName: 'Analytics Service',
    description: 'Service account for analytics and reporting',
    accountType: 'Service-to-service',
    grantTypes: ['client_credentials'],
    scopes: [mockScopes[2], mockScopes[3]], // analytics:read, analytics:write
    tokenEndpointAuthMethod: 'client_secret_basic',
    audience: ['https://api.example.com'],
    owner: 'team-analytics',
    clientMetadata: {
      team: 'analytics',
      environment: 'production'
    },
    redirectUris: [],
    skipConsent: true,
    isActive: true,
    clientSecret: 'secret_sa1',
    responseTypes: [],
    lastUsedAt: '2024-01-15T08:00:00Z',
    createdBy: 'admin@example.com',
    createdAt: '2024-01-03T00:00:00Z',
    updatedAt: '2024-01-15T08:00:00Z',
    roles: [mockRoles[2]],
  },
  {
    id: 'sa-2',
    clientId: 'monitoring-service-client',
    clientName: 'Monitoring Service',
    description: 'Service account for system monitoring',
    accountType: 'Browser',
    grantTypes: ['client_credentials'],
    scopes: [mockScopes[0]], // user:read (Note: using index 0 instead of non-existent monitoring scope)
    tokenEndpointAuthMethod: 'client_secret_basic',
    audience: ['https://api.example.com'],
    owner: 'team-devops',
    clientMetadata: {
      team: 'devops',
      environment: 'production'
    },
    redirectUris: [],
    skipConsent: true,
    isActive: true,
    clientSecret: 'secret_sa2',
    responseTypes: [],
    lastUsedAt: '2024-01-14T12:00:00Z',
    createdBy: 'admin@example.com',
    createdAt: '2024-01-04T00:00:00Z',
    updatedAt: '2024-01-14T12:00:00Z',
    roles: [mockRoles[1]],
  },
];


const mockAuditLogs: AuditLog[] = [
  {
    id: '1',
    action: 'user_created',
    resourceType: 'user',
    resourceId: '2',
    details: { email: 'john.doe@example.com', createdBy: 'admin@example.com' },
    performedBy: 'admin@example.com',
    ipAddress: '192.168.1.100',
    userAgent: 'Mozilla/5.0...',
    timestamp: '2024-01-02T00:00:00Z',
  },
  {
    id: '2',
    action: 'login_success',
    resourceType: 'auth',
    resourceId: '1',
    details: { method: 'password' },
    performedBy: 'admin@example.com',
    ipAddress: '192.168.1.100',
    userAgent: 'Mozilla/5.0...',
    timestamp: '2024-01-15T10:30:00Z',
  },
  {
    id: '3',
    action: 'role_assigned',
    resourceType: 'user',
    resourceId: '2',
    details: { role: 'read_only', assignedBy: 'admin@example.com' },
    performedBy: 'admin@example.com',
    ipAddress: '192.168.1.100',
    userAgent: 'Mozilla/5.0...',
    timestamp: '2024-01-02T00:05:00Z',
  },
];

// Simulate API delay
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

// Mock API implementation
export const mockApi = {
  // Users
  async getUsers(): Promise<User[]> {
    await delay(500);
    return [...mockUsers];
  },

  async getUser(id: string): Promise<User | null> {
    await delay(300);
    return mockUsers.find(user => user.id === id) || null;
  },

  async createUser(userData: CreateUserRequest): Promise<User> {
    await delay(800);
    const newUser: User = {
      id: String(mockUsers.length + 1),
      ...userData,
      isActive: true,
      failedLoginAttempts: 0,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      roles: [],
    };
    mockUsers.push(newUser);
    return newUser;
  },

  async updateUser(id: string, userData: UpdateUserRequest): Promise<User | null> {
    await delay(600);
    const userIndex = mockUsers.findIndex(user => user.id === id);
    if (userIndex === -1) return null;
    
    // Handle role assignments if provided
    let updatedRoles = mockUsers[userIndex].roles;
    if (userData.roleIds !== undefined) {
      updatedRoles = mockRoles.filter(role => userData.roleIds!.includes(role.id));
    }
    
    mockUsers[userIndex] = {
      ...mockUsers[userIndex],
      ...userData,
      roles: updatedRoles,
      updatedAt: new Date().toISOString(),
    };
    return mockUsers[userIndex];
  },

  async deleteUser(id: string): Promise<boolean> {
    await delay(400);
    const userIndex = mockUsers.findIndex(user => user.id === id);
    if (userIndex === -1) return false;
    
    mockUsers.splice(userIndex, 1);
    return true;
  },

  async resetUserPassword(id: string, newPassword: string): Promise<boolean> {
    await delay(600);
    // In real implementation, this would hash and store the password
    return mockUsers.some(user => user.id === id);
  },

  // Service Accounts
  async getServiceAccounts(): Promise<ServiceAccount[]> {
    await delay(500);
    return [...mockServiceAccounts];
  },

  async getServiceAccount(id: string): Promise<ServiceAccount | null> {
    await delay(300);
    return mockServiceAccounts.find(serviceAccount => serviceAccount.id === id) || null;
  },

  async createServiceAccount(serviceAccountData: CreateServiceAccountRequest): Promise<ServiceAccount> {
    await delay(800);
    
    // Handle scope assignments if provided
    let assignedScopes: Scope[] = [];
    if (serviceAccountData.scopeIds) {
      assignedScopes = mockScopes.filter(scope => serviceAccountData.scopeIds!.includes(scope.id));
    }
    
    // Handle role assignments if provided
    let assignedRoles: Role[] = [];
    if (serviceAccountData.roleIds) {
      assignedRoles = mockRoles.filter(role => serviceAccountData.roleIds!.includes(role.id));
    }
    
    const newServiceAccount: ServiceAccount = {
      id: `sa-${mockServiceAccounts.length + 1}`,
      clientId: serviceAccountData.clientId,
      clientName: serviceAccountData.clientName,
      description: serviceAccountData.description,
      accountType: serviceAccountData.accountType || 'Service-to-service',
      grantTypes: serviceAccountData.grantTypes || ['client_credentials'],
      scopes: assignedScopes,
      tokenEndpointAuthMethod: 'client_secret_basic',
      audience: [],
      owner: serviceAccountData.owner,
      clientMetadata: {},
      redirectUris: serviceAccountData.redirectUris || [],
      skipConsent: true,
      isActive: true,
      clientSecret: `secret_${Date.now()}`,
      responseTypes: [],
      lastUsedAt: undefined,
      createdBy: serviceAccountData.createdBy,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      roles: assignedRoles,
    };
    
    mockServiceAccounts.push(newServiceAccount);
    return newServiceAccount;
  },

  async updateServiceAccount(id: string, serviceAccountData: UpdateServiceAccountRequest): Promise<ServiceAccount | null> {
    await delay(600);
    const serviceAccountIndex = mockServiceAccounts.findIndex(serviceAccount => serviceAccount.id === id);
    if (serviceAccountIndex === -1) return null;
    
    // Handle role assignments if provided
    let updatedRoles = mockServiceAccounts[serviceAccountIndex].roles;
    if (serviceAccountData.roleIds !== undefined) {
      updatedRoles = mockRoles.filter(role => serviceAccountData.roleIds!.includes(role.id));
    }
    
    // Handle scope assignments if provided
    let updatedScopes = mockServiceAccounts[serviceAccountIndex].scopes;
    if (serviceAccountData.scopeIds !== undefined) {
      updatedScopes = mockScopes.filter(scope => serviceAccountData.scopeIds!.includes(scope.id));
    }
    
    mockServiceAccounts[serviceAccountIndex] = {
      ...mockServiceAccounts[serviceAccountIndex],
      ...serviceAccountData,
      roles: updatedRoles,
      scopes: updatedScopes,
      updatedAt: new Date().toISOString(),
    };
    return mockServiceAccounts[serviceAccountIndex];
  },

  async deleteServiceAccount(id: string): Promise<void> {
    await delay(500);
    const serviceAccountIndex = mockServiceAccounts.findIndex(serviceAccount => serviceAccount.id === id);
    if (serviceAccountIndex === -1) {
      throw new Error('Service account not found');
    }
    mockServiceAccounts.splice(serviceAccountIndex, 1);
  },

  // Roles
  async getRoles(): Promise<Role[]> {
    await delay(400);
    return [...mockRoles];
  },

  async getRole(id: string): Promise<Role | null> {
    await delay(300);
    return mockRoles.find(role => role.id === id) || null;
  },

  async createRole(roleData: CreateRoleRequest): Promise<Role> {
    await delay(700);
    const newRole: Role = {
      id: String(mockRoles.length + 1),
      ...roleData,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      userCount: 0,
    };
    mockRoles.push(newRole);
    return newRole;
  },

  async updateRole(id: string, roleData: UpdateRoleRequest): Promise<Role | null> {
    await delay(600);
    const roleIndex = mockRoles.findIndex(role => role.id === id);
    if (roleIndex === -1) return null;
    
    mockRoles[roleIndex] = {
      ...mockRoles[roleIndex],
      ...roleData,
      updatedAt: new Date().toISOString(),
    };
    return mockRoles[roleIndex];
  },

  async deleteRole(id: string): Promise<boolean> {
    await delay(400);
    const roleIndex = mockRoles.findIndex(role => role.id === id);
    if (roleIndex === -1) return false;
    
    mockRoles.splice(roleIndex, 1);
    return true;
  },

  // Role assignments
  async assignRoleToUser(userId: string, roleId: string): Promise<boolean> {
    await delay(500);
    const user = mockUsers.find(u => u.id === userId);
    const role = mockRoles.find(r => r.id === roleId);
    
    if (!user || !role) return false;
    
    if (!user.roles.some(r => r.id === roleId)) {
      user.roles.push(role);
      role.userCount = (role.userCount || 0) + 1;
    }
    
    return true;
  },

  async removeRoleFromUser(userId: string, roleId: string): Promise<boolean> {
    await delay(500);
    const user = mockUsers.find(u => u.id === userId);
    const role = mockRoles.find(r => r.id === roleId);
    
    if (!user || !role) return false;
    
    const roleIndex = user.roles.findIndex(r => r.id === roleId);
    if (roleIndex !== -1) {
      user.roles.splice(roleIndex, 1);
      role.userCount = Math.max(0, (role.userCount || 0) - 1);
    }
    
    return true;
  },

  // Audit logs
  async getAuditLogs(resourceType?: string, resourceId?: string): Promise<AuditLog[]> {
    await delay(400);
    let logs = [...mockAuditLogs];
    
    if (resourceType) {
      logs = logs.filter(log => log.resourceType === resourceType);
    }
    
    if (resourceId) {
      logs = logs.filter(log => log.resourceId === resourceId);
    }
    
    return logs.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());
  },

  async getUserAuditLogs(userId: string): Promise<AuditLog[]> {
    await delay(400);
    return mockAuditLogs
      .filter(log => log.resourceId === userId || log.performedBy === mockUsers.find(u => u.id === userId)?.email)
      .sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime())
      .slice(0, 10);
  },

  // System info
  async getJwtPublicKey(): Promise<string> {
    await delay(200);
    return `-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA1234567890...
-----END PUBLIC KEY-----`;
  },

  async getSystemStats(): Promise<{ users: number; serviceAccounts: number; roles: number; }> {
    await delay(300);
    return {
      users: mockUsers.length,
      serviceAccounts: mockServiceAccounts.length,
      roles: mockRoles.length,
    };
  },

  // Role membership functions
  async getUsersByRole(roleId: string): Promise<User[]> {
    await delay(400);
    return mockUsers.filter(user => 
      user.roles.some(role => role.id === roleId)
    );
  },

  async getServiceAccountsByRole(roleId: string): Promise<ServiceAccount[]> {
    await delay(400);
    return mockServiceAccounts.filter(serviceAccount => 
      serviceAccount.roles.some(role => role.id === roleId)
    );
  },

  async getAllUsersNotInRole(roleId: string): Promise<User[]> {
    await delay(400);
    return mockUsers.filter(user => 
      !user.roles.some(role => role.id === roleId)
    );
  },

  async getAllServiceAccountsNotInRole(roleId: string): Promise<ServiceAccount[]> {
    await delay(400);
    return mockServiceAccounts.filter(serviceAccount => 
      !serviceAccount.roles.some(role => role.id === roleId)
    );
  },

  async assignRoleToServiceAccount(serviceAccountId: string, roleId: string): Promise<boolean> {
    await delay(500);
    const serviceAccount = mockServiceAccounts.find(sa => sa.id === serviceAccountId);
    const role = mockRoles.find(r => r.id === roleId);
    
    if (!serviceAccount || !role) return false;
    
    if (!serviceAccount.roles.some(r => r.id === roleId)) {
      serviceAccount.roles.push(role);
      role.userCount = (role.userCount || 0) + 1;
      serviceAccount.updatedAt = new Date().toISOString();
      return true;
    }
    return false;
  },

  async removeRoleFromServiceAccount(serviceAccountId: string, roleId: string): Promise<boolean> {
    await delay(500);
    const serviceAccount = mockServiceAccounts.find(sa => sa.id === serviceAccountId);
    const role = mockRoles.find(r => r.id === roleId);
    
    if (!serviceAccount || !role) return false;
    
    const roleIndex = serviceAccount.roles.findIndex(r => r.id === roleId);
    if (roleIndex !== -1) {
      serviceAccount.roles.splice(roleIndex, 1);
      role.userCount = Math.max((role.userCount || 1) - 1, 0);
      serviceAccount.updatedAt = new Date().toISOString();
      return true;
    }
    return false;
  },

  // Scope Management APIs
  async getScopes(): Promise<Scope[]> {
    await delay(500);
    return [...mockScopes];
  },

  async getScope(id: string): Promise<Scope | null> {
    await delay(500);
    return mockScopes.find(scope => scope.id === id) || null;
  },

  async createScope(scopeData: CreateScopeRequest): Promise<Scope> {
    await delay(500);
    const newScope: Scope = {
      id: String(mockScopes.length + 1),
      name: scopeData.name,
      description: scopeData.description,
      appliesTo: scopeData.appliesTo,
      isActive: scopeData.isActive ?? true,
      serviceAccountCount: 0,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };
    mockScopes.push(newScope);
    return newScope;
  },

  async updateScope(id: string, updates: UpdateScopeRequest): Promise<Scope | null> {
    await delay(500);
    const scopeIndex = mockScopes.findIndex(scope => scope.id === id);
    if (scopeIndex === -1) return null;

    mockScopes[scopeIndex] = {
      ...mockScopes[scopeIndex],
      ...updates,
      updatedAt: new Date().toISOString(),
    };
    return mockScopes[scopeIndex];
  },

  async deleteScope(id: string): Promise<boolean> {
    await delay(500);
    const scopeIndex = mockScopes.findIndex(scope => scope.id === id);
    if (scopeIndex === -1) return false;
    
    // Check if scope is assigned to any service accounts
    if (mockScopes[scopeIndex].serviceAccountCount > 0) {
      throw new Error('Cannot delete scope that is assigned to service accounts');
    }
    
    mockScopes.splice(scopeIndex, 1);
    return true;
  },

  async getScopesForAccountType(accountType: 'Service-to-service' | 'Browser'): Promise<Scope[]> {
    await delay(500);
    const appliesTo: ScopeAppliesTo = accountType === 'Service-to-service' ? 'Service-to-service' : 'Browser';
    return mockScopes.filter(scope => 
      scope.isActive && scope.appliesTo.includes(appliesTo)
    );
  },

  async bulkActivateScopes(scopeIds: string[]): Promise<{ updated: number }> {
    await delay(500);
    let updated = 0;
    scopeIds.forEach(id => {
      const scope = mockScopes.find(s => s.id === id);
      if (scope && !scope.isActive) {
        scope.isActive = true;
        scope.updatedAt = new Date().toISOString();
        updated++;
      }
    });
    return { updated };
  },

  async bulkDeactivateScopes(scopeIds: string[]): Promise<{ updated: number }> {
    await delay(500);
    let updated = 0;
    scopeIds.forEach(id => {
      const scope = mockScopes.find(s => s.id === id);
      if (scope && scope.isActive) {
        scope.isActive = false;
        scope.updatedAt = new Date().toISOString();
        updated++;
      }
    });
    return { updated };
  },

  async bulkDeleteScopes(scopeIds: string[]): Promise<{ deleted: number }> {
    await delay(500);
    let deleted = 0;
    scopeIds.forEach(id => {
      const scopeIndex = mockScopes.findIndex(s => s.id === id);
      if (scopeIndex !== -1 && mockScopes[scopeIndex].serviceAccountCount === 0) {
        mockScopes.splice(scopeIndex, 1);
        deleted++;
      }
    });
    return { deleted };
  },
};
