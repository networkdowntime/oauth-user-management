import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { CssBaseline } from '@mui/material';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { NavigationProvider } from './contexts/NavigationContext';
import { AuthProvider } from './contexts/AuthContext';
import Layout from './components/Layout';
import { ProtectedRoute } from './components/auth/ProtectedRoute';
import { AuthCallback } from './components/auth/AuthCallback';
import { Dashboard, Users, UserDetail, UserEdit, ServiceAccounts, ServiceAccountDetail, ServiceAccountEdit, Roles, RoleDetail, RoleEdit, Scopes, AuditLogs, NotFound } from './pages';

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      refetchOnWindowFocus: false,
    },
  },
});

// Create theme
const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Router>
          <AuthProvider>
            <NavigationProvider>
              <Routes>
                {/* OAuth callback route - no authentication required */}
                <Route path="/auth/callback" element={<AuthCallback />} />
                
                {/* All other routes require authentication */}
                <Route path="/*" element={
                  <ProtectedRoute>
                    <Layout>
                      <Routes>
                        <Route path="/" element={<Dashboard />} />
                        <Route path="/users" element={<Users />} />
                        <Route path="/users/:id" element={<UserDetail />} />
                        <Route path="/users/:id/edit" element={<UserEdit />} />
                        <Route path="/service-accounts" element={<ServiceAccounts />} />
                        <Route path="/service-accounts/:id" element={<ServiceAccountDetail />} />
                        <Route path="/service-accounts/:id/edit" element={<ServiceAccountEdit />} />
                        <Route path="/roles" element={<Roles />} />
                        <Route path="/roles/:id" element={<RoleDetail />} />
                        <Route path="/roles/:id/edit" element={<RoleEdit />} />
                        <Route path="/scopes" element={<Scopes />} />
                        <Route path="/audit-logs" element={<AuditLogs />} />
                        <Route path="*" element={<NotFound />} />
                      </Routes>
                    </Layout>
                  </ProtectedRoute>
                } />
              </Routes>
            </NavigationProvider>
          </AuthProvider>
        </Router>
      </ThemeProvider>
    </QueryClientProvider>
  );
}

export default App;
