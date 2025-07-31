/**
 * Protected Route Component
 * 
 * Ensures only authenticated users can access certain routes.
 * Redirects to login for unauthenticated users.
 */

import React, { ReactNode } from 'react';
import { Box, CircularProgress, Typography } from '@mui/material';
import { useAuth } from '../../contexts/AuthContext';

interface ProtectedRouteProps {
  children: ReactNode;
  fallback?: ReactNode;
}

export const ProtectedRoute = ({ 
  children, 
  fallback 
}: ProtectedRouteProps): JSX.Element => {
  const { isAuthenticated, isLoading, login } = useAuth();

  // Auto-trigger login flow if not authenticated
  React.useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      const handleLogin = async () => {
        try {
          await login();
        } catch (error) {
          console.error('Login failed:', error);
        }
      };
      handleLogin();
    }
  }, [isLoading, isAuthenticated, login]);

  // Show loading spinner while checking authentication
  if (isLoading) {
    return (
      <>
        {fallback || (
          <Box
            display="flex"
            flexDirection="column"
            alignItems="center"
            justifyContent="center"
            minHeight="200px"
            gap={2}
          >
            <CircularProgress size={40} />
            <Typography variant="body2" color="text.secondary">
              Checking authentication...
            </Typography>
          </Box>
        )}
      </>
    );
  }

  // If not authenticated, show redirecting message
  if (!isAuthenticated) {
    return (
      <Box
        display="flex"
        flexDirection="column"
        alignItems="center"
        justifyContent="center"
        minHeight="200px"
        gap={2}
      >
        <CircularProgress size={40} />
        <Typography variant="body2" color="text.secondary">
          Redirecting to login...
        </Typography>
      </Box>
    );
  }

  // User is authenticated, render the protected content
  return <>{children}</>;
};
