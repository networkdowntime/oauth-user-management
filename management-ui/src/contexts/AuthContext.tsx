/**
 * Authentication Context for OAuth2 integration with Hydra
 * 
 * Provides authentication state management and auto-refresh functionality
 */

import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { authService, UserInfo } from '../services/authService';

interface AuthContextType {
  isAuthenticated: boolean;
  isLoading: boolean;
  user: UserInfo | null;
  login: () => Promise<void>;
  logout: () => Promise<void>;
  refreshToken: () => Promise<boolean>;
  setIsAuthenticated: (authenticated: boolean) => void;
  setUser: (user: UserInfo | null) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [user, setUser] = useState<UserInfo | null>(null);

  useEffect(() => {
    // Check authentication status on app start
    checkAuthStatus();
    
    // Set up token refresh timer
    const refreshInterval = setInterval(() => {
      if (authService.isAuthenticated()) {
        // Refresh token if it expires in the next 5 minutes
        const expiresAt = localStorage.getItem('token_expires_at');
        if (expiresAt) {
          const timeUntilExpiry = parseInt(expiresAt, 10) - Date.now();
          if (timeUntilExpiry < 5 * 60 * 1000) { // 5 minutes
            authService.refreshToken().then((success) => {
              if (!success) {
                // Refresh failed, user needs to login again
                setIsAuthenticated(false);
                setUser(null);
              }
            });
          }
        }
      }
    }, 60000); // Check every minute

    return () => clearInterval(refreshInterval);
  }, []);

  const checkAuthStatus = async () => {
    setIsLoading(true);
    
    try {
      // Only check existing authentication - callback is handled by AuthCallback component
      const authenticated = authService.isAuthenticated();
      setIsAuthenticated(authenticated);
      
      if (authenticated) {
        setUser(authService.getUserInfo());
      } else {
        setUser(null);
        
        // Try to refresh token if we have a refresh token
        const refreshSuccess = await authService.refreshToken();
        if (refreshSuccess) {
          setIsAuthenticated(true);
          setUser(authService.getUserInfo());
        }
      }
    } catch (error) {
      console.error('Auth check failed:', error);
      setIsAuthenticated(false);
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  };

  const login = async () => {
    await authService.login();
  };

  const logout = async () => {
    setIsAuthenticated(false);
    setUser(null);
    await authService.logout();
  };

  const refreshToken = async (): Promise<boolean> => {
    const success = await authService.refreshToken();
    if (success) {
      setUser(authService.getUserInfo());
    } else {
      setIsAuthenticated(false);
      setUser(null);
    }
    return success;
  };

  const value: AuthContextType = {
    isAuthenticated,
    isLoading,
    user,
    login,
    logout,
    refreshToken,
    setIsAuthenticated,
    setUser,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
