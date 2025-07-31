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
  Person as PersonIcon,
  Email as EmailIcon,
  AccessTime as AccessTimeIcon,
  Security as SecurityIcon,
} from '@mui/icons-material';
import { useUser } from '../services/hooks';
import { useNavigation } from '../contexts/NavigationContext';
import { usePageTracking } from '../hooks/usePageTracking';

const UserDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: user, isLoading, error } = useUser(id!);
  const { goBack, getBackLabel, canGoBack, removeCurrentPageFromBreadcrumbs } = useNavigation();
  
  // Track this page for breadcrumb navigation
  usePageTracking({ 
    pageLabel: user ? `${user.displayName || user.email}` : 'User Details',
    shouldTrack: !!user 
  });

  // Remove current page from breadcrumbs if it's the most recent (e.g., after saving from edit)
  useEffect(() => {
    if (user) {
      const currentPath = `/users/${id}`;
      removeCurrentPageFromBreadcrumbs(currentPath);
    }
  }, [user, id, removeCurrentPageFromBreadcrumbs]);

  const handleBackClick = () => {
    if (canGoBack()) {
      goBack();
    } else {
      navigate('/users');
    }
  };

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error || !user) {
    return (
      <Box>
        <Alert severity="error" sx={{ mb: 2 }}>
          {error ? 'Error loading user details' : 'User not found'}
        </Alert>
        <Button
          startIcon={<ArrowBackIcon />}
          onClick={handleBackClick}
          variant="outlined"
        >
          {getBackLabel()}
        </Button>
      </Box>
    );
  }

  const getStatusColor = (isActive: boolean) => {
    return isActive ? 'success' : 'error';
  };

  return (
    <Box>
      {/* Header */}
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box display="flex" alignItems="center" gap={2}>
          <Button
            startIcon={<ArrowBackIcon />}
            onClick={handleBackClick}
            variant="outlined"
          >
            {getBackLabel()}
          </Button>
          <Typography variant="h4" component="h1">
            User Details
          </Typography>
        </Box>
        <Button
          startIcon={<EditIcon />}
          onClick={() => navigate(`/users/${id}/edit`)}
          variant="contained"
          color="primary"
        >
          Edit User
        </Button>
      </Box>

      <Grid container spacing={3}>
        {/* User Information Card */}
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" gap={2} mb={3}>
                <Avatar sx={{ width: 60, height: 60, bgcolor: 'primary.main' }}>
                  <PersonIcon fontSize="large" />
                </Avatar>
                <Box>
                  <Typography variant="h5" gutterBottom>
                    {user.displayName || user.email}
                  </Typography>
                  <Chip
                    label={user.isActive ? 'Active' : 'Inactive'}
                    color={getStatusColor(user.isActive)}
                    size="small"
                  />
                </Box>
              </Box>

              <Divider sx={{ mb: 3 }} />

              <Grid container spacing={3}>
                <Grid item xs={12} sm={6}>
                  <Paper sx={{ p: 2, bgcolor: 'grey.50' }}>
                    <Box display="flex" alignItems="center" gap={1} mb={1}>
                      <EmailIcon color="primary" />
                      <Typography variant="subtitle1" fontWeight="bold">
                        Email
                      </Typography>
                    </Box>
                    <Typography variant="body1">{user.email}</Typography>
                  </Paper>
                </Grid>

                <Grid item xs={12} sm={6}>
                  <Paper sx={{ p: 2, bgcolor: 'grey.50' }}>
                    <Box display="flex" alignItems="center" gap={1} mb={1}>
                      <PersonIcon color="primary" />
                      <Typography variant="subtitle1" fontWeight="bold">
                        User ID
                      </Typography>
                    </Box>
                    <Typography variant="body1" fontFamily="monospace">
                      {user.id}
                    </Typography>
                  </Paper>
                </Grid>

                <Grid item xs={12} sm={6}>
                  <Paper sx={{ p: 2, bgcolor: 'grey.50' }}>
                    <Box display="flex" alignItems="center" gap={1} mb={1}>
                      <AccessTimeIcon color="primary" />
                      <Typography variant="subtitle1" fontWeight="bold">
                        Created
                      </Typography>
                    </Box>
                    <Typography variant="body1">
                      {new Date(user.createdAt).toLocaleString()}
                    </Typography>
                  </Paper>
                </Grid>

                <Grid item xs={12} sm={6}>
                  <Paper sx={{ p: 2, bgcolor: 'grey.50' }}>
                    <Box display="flex" alignItems="center" gap={1} mb={1}>
                      <AccessTimeIcon color="primary" />
                      <Typography variant="subtitle1" fontWeight="bold">
                        Last Login
                      </Typography>
                    </Box>
                    <Typography variant="body1">
                      {user.lastLoginAt ? new Date(user.lastLoginAt).toLocaleString() : 'Never'}
                    </Typography>
                  </Paper>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Roles Card */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" gap={1} mb={2}>
                <SecurityIcon color="primary" />
                <Typography variant="h6" fontWeight="bold">
                  Assigned Roles
                </Typography>
              </Box>
              <Box display="flex" flexDirection="column" gap={1}>
                {user.roles && user.roles.length > 0 ? (
                  user.roles.map((role) => (
                    <Chip
                      key={role.id}
                      label={role.name}
                      variant="outlined"
                      color="primary"
                      size="small"
                      clickable
                      onClick={() => navigate(`/roles/${role.id}`)}
                      sx={{ cursor: 'pointer' }}
                    />
                  ))
                ) : (
                  <Typography variant="body2" color="text.secondary">
                    No roles assigned
                  </Typography>
                )}
              </Box>
            </CardContent>
          </Card>

          {/* Additional Information */}
          <Card sx={{ mt: 2 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Additional Information
              </Typography>
              <Box display="flex" flexDirection="column" gap={2}>
                <Box>
                  <Typography variant="subtitle2" color="text.secondary">
                    Failed Login Attempts
                  </Typography>
                  <Chip
                    label={user.failedLoginAttempts.toString()}
                    color={user.failedLoginAttempts > 0 ? 'warning' : 'success'}
                    size="small"
                  />
                </Box>
                {user.lockedUntil && (
                  <Box>
                    <Typography variant="subtitle2" color="text.secondary">
                      Locked Until
                    </Typography>
                    <Typography variant="body2" color="error">
                      {new Date(user.lockedUntil).toLocaleString()}
                    </Typography>
                  </Box>
                )}
                {user.socialProvider && (
                  <Box>
                    <Typography variant="subtitle2" color="text.secondary">
                      Social Provider
                    </Typography>
                    <Chip
                      label={user.socialProvider}
                      color="secondary"
                      size="small"
                    />
                  </Box>
                )}
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default UserDetail;
