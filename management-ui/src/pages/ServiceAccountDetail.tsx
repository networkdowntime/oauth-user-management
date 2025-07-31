import React, { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Chip,
  Grid,
  Paper,
  Divider,
  Avatar,
  Alert,
  CircularProgress,
} from '@mui/material';
import {
  ArrowBack as ArrowBackIcon,
  Edit as EditIcon,
  Settings as SettingsIcon,
  AccountBox as AccountBoxIcon,
  AccessTime as AccessTimeIcon,
  Security as SecurityIcon,
  Key as KeyIcon,
  Api as ApiIcon,
} from '@mui/icons-material';
import { useServiceAccount } from '../services/hooks';
import { useNavigation } from '../contexts/NavigationContext';
import { usePageTracking } from '../hooks/usePageTracking';

const ServiceAccountDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: serviceAccount, isLoading, error } = useServiceAccount(id!);
  const { goBack, getBackLabel, canGoBack, removeCurrentPageFromBreadcrumbs } = useNavigation();
  
  // Track this page for breadcrumb navigation
  usePageTracking({ 
    pageLabel: serviceAccount ? serviceAccount.clientName : 'Service Account Details',
    shouldTrack: !!serviceAccount 
  });

  // Remove current page from breadcrumbs if it's the most recent (e.g., after saving from edit)
  useEffect(() => {
    if (serviceAccount) {
      const currentPath = `/service-accounts/${id}`;
      removeCurrentPageFromBreadcrumbs(currentPath);
    }
  }, [serviceAccount, id, removeCurrentPageFromBreadcrumbs]);

  const handleBackClick = () => {
    if (canGoBack()) {
      goBack();
    } else {
      navigate('/service-accounts');
    }
  };

  const handleEditClick = () => {
    navigate(`/service-accounts/${id}/edit`);
  };

  const getStatusColor = (isActive: boolean) => {
    return isActive ? 'success' : 'default';
  };

  if (isLoading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error || !serviceAccount) {
    return (
      <Box sx={{ p: 3 }}>
        <Alert severity="error">
          Failed to load service account details. Please try again.
        </Alert>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
        <Button
          startIcon={<ArrowBackIcon />}
          onClick={handleBackClick}
          sx={{ mr: 2 }}
        >
          {getBackLabel() || 'Back to Service Accounts'}
        </Button>
        <Typography variant="h4" component="h1" sx={{ flexGrow: 1 }}>
          Service Account Details
        </Typography>
        <Button
          variant="contained"
          startIcon={<EditIcon />}
          onClick={handleEditClick}
        >
          Edit
        </Button>
      </Box>

      <Grid container spacing={3}>
        {/* Main Info Card */}
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                <Avatar sx={{ mr: 2, bgcolor: 'primary.main' }}>
                  <SettingsIcon />
                </Avatar>
                <Box sx={{ flexGrow: 1 }}>
                  <Typography variant="h5" component="h2">
                    {serviceAccount.clientName}
                  </Typography>
                  <Box sx={{ mt: 1 }}>
                    <Chip
                      label={serviceAccount.isActive ? 'Active' : 'Inactive'}
                      color={getStatusColor(serviceAccount.isActive)}
                      size="small"
                    />
                  </Box>
                </Box>
              </Box>

              <Grid container spacing={3}>
                {/* Client ID */}
                <Grid item xs={12} sm={6}>
                  <Paper sx={{ p: 2 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                      <KeyIcon color="primary" />
                      <Typography variant="subtitle2" sx={{ ml: 1 }}>
                        Client ID
                      </Typography>
                    </Box>
                    <Typography variant="body1" sx={{ fontFamily: 'monospace', wordBreak: 'break-all' }}>
                      {serviceAccount.clientId}
                    </Typography>
                  </Paper>
                </Grid>

                {/* Owner */}
                <Grid item xs={12} sm={6}>
                  <Paper sx={{ p: 2 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                      <AccountBoxIcon color="primary" />
                      <Typography variant="subtitle2" sx={{ ml: 1 }}>
                        Owner
                      </Typography>
                    </Box>
                    <Typography variant="body1">{serviceAccount.owner}</Typography>
                  </Paper>
                </Grid>

                {/* Created At */}
                <Grid item xs={12} sm={6}>
                  <Paper sx={{ p: 2 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                      <AccessTimeIcon color="primary" />
                      <Typography variant="subtitle2" sx={{ ml: 1 }}>
                        Created
                      </Typography>
                    </Box>
                    <Typography variant="body1">
                      {new Date(serviceAccount.createdAt).toLocaleString()}
                    </Typography>
                  </Paper>
                </Grid>

                {/* Updated At */}
                <Grid item xs={12} sm={6}>
                  <Paper sx={{ p: 2 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                      <AccessTimeIcon color="primary" />
                      <Typography variant="subtitle2" sx={{ ml: 1 }}>
                        Last Updated
                      </Typography>
                    </Box>
                    <Typography variant="body1">
                      {new Date(serviceAccount.updatedAt).toLocaleString()}
                    </Typography>
                  </Paper>
                </Grid>

                {/* Description */}
                {serviceAccount.description && (
                  <Grid item xs={12}>
                    <Paper sx={{ p: 2 }}>
                      <Typography variant="subtitle2" gutterBottom>
                        Description
                      </Typography>
                      <Typography variant="body1">{serviceAccount.description}</Typography>
                    </Paper>
                  </Grid>
                )}

                {/* Scope */}
                <Grid item xs={12}>
                  <Paper sx={{ p: 2 }}>
                    <Typography variant="subtitle2" gutterBottom>
                      Scopes
                    </Typography>
                    {serviceAccount.scopes && serviceAccount.scopes.length > 0 ? (
                      <Box display="flex" flexWrap="wrap" gap={1}>
                        {serviceAccount.scopes.map((scope) => (
                          <Chip
                            key={scope.id}
                            label={scope.name}
                            size="small"
                            variant="outlined"
                          />
                        ))}
                      </Box>
                    ) : (
                      <Typography variant="body2" color="text.secondary">
                        No scopes assigned
                      </Typography>
                    )}
                  </Paper>
                </Grid>

                {/* Grant Types */}
                <Grid item xs={12}>
                  <Paper sx={{ p: 2 }}>
                    <Typography variant="subtitle2" gutterBottom>
                      Grant Types
                    </Typography>
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                      {serviceAccount.grantTypes.map((grantType) => (
                        <Chip
                          key={grantType}
                          label={grantType}
                          variant="outlined"
                          size="small"
                        />
                      ))}
                    </Box>
                  </Paper>
                </Grid>

                {/* Redirect URIs */}
                {serviceAccount.redirectUris && serviceAccount.redirectUris.length > 0 && (
                  <Grid item xs={12}>
                    <Paper sx={{ p: 2 }}>
                      <Typography variant="subtitle2" gutterBottom>
                        Redirect URIs
                      </Typography>
                      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                        {serviceAccount.redirectUris.map((uri, index) => (
                          <Typography 
                            key={index} 
                            variant="body2" 
                            sx={{ fontFamily: 'monospace', wordBreak: 'break-all' }}
                          >
                            {uri}
                          </Typography>
                        ))}
                      </Box>
                    </Paper>
                  </Grid>
                )}

                {/* Token Endpoint Auth Method */}
                <Grid item xs={12} sm={6}>
                  <Paper sx={{ p: 2 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                      <SecurityIcon color="primary" />
                      <Typography variant="subtitle2" sx={{ ml: 1 }}>
                        Token Endpoint Auth Method
                      </Typography>
                    </Box>
                    <Typography variant="body1">{serviceAccount.tokenEndpointAuthMethod}</Typography>
                  </Paper>
                </Grid>

                {/* Audience */}
                {serviceAccount.audience && (
                  <Grid item xs={12} sm={6}>
                    <Paper sx={{ p: 2 }}>
                      <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                        <ApiIcon color="primary" />
                        <Typography variant="subtitle2" sx={{ ml: 1 }}>
                          Audience
                        </Typography>
                      </Box>
                      <Typography variant="body1" sx={{ fontFamily: 'monospace' }}>
                        {serviceAccount.audience}
                      </Typography>
                    </Paper>
                  </Grid>
                )}
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Roles Card */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Assigned Roles
              </Typography>
              <Divider sx={{ mb: 2 }} />
              {serviceAccount.roles && serviceAccount.roles.length > 0 ? (
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                  {serviceAccount.roles.map((role: any) => (
                    <Chip
                      key={role.id}
                      label={role.name}
                      color="primary"
                      variant="outlined"
                      onClick={() => navigate(`/roles/${role.id}`)}
                      clickable
                    />
                  ))}
                </Box>
              ) : (
                <Typography variant="body2" color="text.secondary">
                  No roles assigned
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default ServiceAccountDetail;
