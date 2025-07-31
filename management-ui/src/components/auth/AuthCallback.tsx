/**
 * OAuth Callback Handler Component
 * 
 * Handles the OAuth2 authorization code callback from Hydra
 */

import React, { useEffect, useState } from 'react';
import { Box, CircularProgress, Typography, Alert } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { authService } from '../../services/authService';

export const AuthCallback: React.FC = () => {
  const navigate = useNavigate();
  const { setIsAuthenticated, setUser } = useAuth();
  const [isProcessing, setIsProcessing] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [hasProcessed, setHasProcessed] = useState(false);

  useEffect(() => {
    // Prevent duplicate execution in React Strict Mode
    if (hasProcessed) return;

    const handleCallback = async () => {
      setHasProcessed(true);
      
      try {
        // Check for OAuth errors in URL params
        const urlParams = new URLSearchParams(window.location.search);
        const oauthError = urlParams.get('error');
        const errorDescription = urlParams.get('error_description');

        if (oauthError) {
          setError(errorDescription || 'Authentication failed');
          setIsProcessing(false);
          return;
        }

        // Process the OAuth callback
        const success = await authService.handleCallback();
        
        if (success) {
          // Update auth context state
          setIsAuthenticated(true);
          setUser(authService.getUserInfo());
          
          // Navigate to main app and clean up URL
          navigate('/', { replace: true });
        } else {
          setError('Failed to complete authentication');
        }
      } catch (error) {
        console.error('Callback processing failed:', error);
        setError('An unexpected error occurred during authentication');
      } finally {
        setIsProcessing(false);
      }
    };

    // Only run once
    handleCallback();
  }, [hasProcessed, setIsAuthenticated, setUser, navigate]); // Include dependencies but guard with hasProcessed

  if (error) {
    return (
      <Box
        display="flex"
        flexDirection="column"
        alignItems="center"
        justifyContent="center"
        minHeight="400px"
        gap={2}
        p={3}
      >
        <Alert severity="error" sx={{ maxWidth: 400 }}>
          <Typography variant="h6" gutterBottom>
            Authentication Failed
          </Typography>
          <Typography variant="body2">
            {error}
          </Typography>
        </Alert>
      </Box>
    );
  }

  return (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      minHeight="400px"
      gap={2}
    >
      <CircularProgress size={50} />
      <Typography variant="h6" color="text.secondary">
        Processing authentication...
      </Typography>
      <Typography variant="body2" color="text.secondary">
        Please wait while we complete your login.
      </Typography>
    </Box>
  );
};
