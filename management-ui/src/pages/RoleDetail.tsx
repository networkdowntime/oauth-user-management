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
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  IconButton,
} from '@mui/material';
import {
  ArrowBack as ArrowBackIcon,
  Edit as EditIcon,
  Security as SecurityIcon,
  People as PeopleIcon,
  AccessTime as AccessTimeIcon,
  Description as DescriptionIcon,
  Person as PersonIcon,
  Settings as SettingsIcon,
  Visibility as VisibilityIcon,
} from '@mui/icons-material';
import { useRole, useUsersByRole, useServiceAccountsByRole } from '../services/hooks';
import { useNavigation } from '../contexts/NavigationContext';
import { usePageTracking } from '../hooks/usePageTracking';

const RoleDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: role, isLoading, error } = useRole(id!);
  const { data: usersWithRole = [], isLoading: usersLoading } = useUsersByRole(id!);
  const { data: serviceAccountsWithRole = [], isLoading: serviceAccountsLoading } = useServiceAccountsByRole(id!);
  const { goBack, getBackLabel, canGoBack, removeCurrentPageFromBreadcrumbs } = useNavigation();
  
  // Track this page for breadcrumb navigation
  usePageTracking({ 
    pageLabel: role ? `${role.name} Role` : 'Role Details',
    shouldTrack: !!role 
  });

  // Remove current page from breadcrumbs if it's the most recent (e.g., after saving from edit)
  useEffect(() => {
    if (role) {
      const currentPath = `/roles/${id}`;
      removeCurrentPageFromBreadcrumbs(currentPath);
    }
  }, [role, id, removeCurrentPageFromBreadcrumbs]);

  const handleBackClick = () => {
    if (canGoBack()) {
      goBack();
    } else {
      navigate('/roles');
    }
  };

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error || !role) {
    return (
      <Box>
        <Alert severity="error" sx={{ mb: 2 }}>
          {error ? 'Error loading role details' : 'Role not found'}
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
            Role Details
          </Typography>
        </Box>
        <Button
          startIcon={<EditIcon />}
          onClick={() => navigate(`/roles/${id}/edit`)}
          variant="contained"
          color="primary"
        >
          Edit Role
        </Button>
      </Box>

      <Grid container spacing={3}>
        {/* Role Information Card */}
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" gap={2} mb={3}>
                <Avatar sx={{ width: 60, height: 60, bgcolor: 'primary.main' }}>
                  <SecurityIcon fontSize="large" />
                </Avatar>
                <Box>
                  <Typography variant="h5" gutterBottom>
                    {role.name}
                  </Typography>
                  <Chip
                    label="Role"
                    color="primary"
                    size="small"
                    variant="outlined"
                  />
                </Box>
              </Box>

              <Divider sx={{ mb: 3 }} />

              <Grid container spacing={3}>
                <Grid item xs={12} sm={6}>
                  <Paper sx={{ p: 2, bgcolor: 'grey.50' }}>
                    <Box display="flex" alignItems="center" gap={1} mb={1}>
                      <SecurityIcon color="primary" />
                      <Typography variant="subtitle1" fontWeight="bold">
                        Role Name
                      </Typography>
                    </Box>
                    <Typography variant="body1">{role.name}</Typography>
                  </Paper>
                </Grid>

                <Grid item xs={12} sm={6}>
                  <Paper sx={{ p: 2, bgcolor: 'grey.50' }}>
                    <Box display="flex" alignItems="center" gap={1} mb={1}>
                      <SecurityIcon color="primary" />
                      <Typography variant="subtitle1" fontWeight="bold">
                        Role ID
                      </Typography>
                    </Box>
                    <Typography variant="body1" fontFamily="monospace">
                      {role.id}
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
                      {new Date(role.createdAt).toLocaleString()}
                    </Typography>
                  </Paper>
                </Grid>

                <Grid item xs={12} sm={6}>
                  <Paper sx={{ p: 2, bgcolor: 'grey.50' }}>
                    <Box display="flex" alignItems="center" gap={1} mb={1}>
                      <AccessTimeIcon color="primary" />
                      <Typography variant="subtitle1" fontWeight="bold">
                        Last Updated
                      </Typography>
                    </Box>
                    <Typography variant="body1">
                      {new Date(role.updatedAt).toLocaleString()}
                    </Typography>
                  </Paper>
                </Grid>

                {role.description && (
                  <Grid item xs={12}>
                    <Paper sx={{ p: 2, bgcolor: 'grey.50' }}>
                      <Box display="flex" alignItems="center" gap={1} mb={1}>
                        <DescriptionIcon color="primary" />
                        <Typography variant="subtitle1" fontWeight="bold">
                          Description
                        </Typography>
                      </Box>
                      <Typography variant="body1">{role.description}</Typography>
                    </Paper>
                  </Grid>
                )}
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Role Statistics Card */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" gap={1} mb={2}>
                <PeopleIcon color="primary" />
                <Typography variant="h6" fontWeight="bold">
                  Usage Statistics
                </Typography>
              </Box>
              <Box display="flex" flexDirection="column" gap={2}>
                <Box>
                  <Typography variant="subtitle2" color="text.secondary">
                    Users with this role
                  </Typography>
                  <Typography variant="h4" color="primary">
                    {role.userCount || 0}
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>

          {/* Role Information Summary */}
          <Card sx={{ mt: 2 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Role Information
              </Typography>
              <Box display="flex" flexDirection="column" gap={2}>
                <Box>
                  <Typography variant="subtitle2" color="text.secondary">
                    Role Type
                  </Typography>
                  <Chip
                    label="Access Control Role"
                    color="info"
                    size="small"
                  />
                </Box>
                {role.description && (
                  <Box>
                    <Typography variant="subtitle2" color="text.secondary">
                      Purpose
                    </Typography>
                    <Typography variant="body2">
                      {role.description}
                    </Typography>
                  </Box>
                )}
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Users and Service Accounts with this Role */}
      <Grid container spacing={3} sx={{ mt: 2 }}>
        {/* Users with this Role */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" gap={1} mb={2}>
                <PersonIcon color="primary" />
                <Typography variant="h6" fontWeight="bold">
                  Users with this Role ({usersWithRole.length})
                </Typography>
              </Box>
              {usersLoading ? (
                <CircularProgress size={24} />
              ) : usersWithRole.length > 0 ? (
                <List>
                  {usersWithRole.map((user) => (
                    <ListItem 
                      key={user.id}
                      secondaryAction={
                        <IconButton 
                          edge="end" 
                          onClick={() => navigate(`/users/${user.id}`)}
                          size="small"
                        >
                          <VisibilityIcon />
                        </IconButton>
                      }
                    >
                      <ListItemAvatar>
                        <Avatar sx={{ bgcolor: 'primary.main' }}>
                          <PersonIcon />
                        </Avatar>
                      </ListItemAvatar>
                      <ListItemText
                        primary={user.displayName || user.email}
                        secondary={user.email}
                      />
                    </ListItem>
                  ))}
                </List>
              ) : (
                <Typography variant="body2" color="text.secondary">
                  No users have this role
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Services with this Role */}
                {/* Service Accounts with this Role */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <SettingsIcon color="primary" sx={{ mr: 1 }} />
                <Typography variant="h6">
                  Service Accounts with this Role ({serviceAccountsWithRole.length})
                </Typography>
              </Box>
              {serviceAccountsLoading ? (
                <CircularProgress size={24} />
              ) : serviceAccountsWithRole.length > 0 ? (
                <Box>
                  {serviceAccountsWithRole.map((serviceAccount: any) => (
                    <ListItem
                      key={serviceAccount.id}
                      sx={{
                        border: 1,
                        borderColor: 'divider',
                        borderRadius: 1,
                        mb: 1,
                        cursor: 'pointer',
                        '&:hover': {
                          backgroundColor: 'action.hover',
                        },
                      }}
                      onClick={() => navigate(`/service-accounts/${serviceAccount.id}`)}
                    >
                      <ListItemAvatar>
                        <Avatar>
                          <SettingsIcon />
                        </Avatar>
                      </ListItemAvatar>
                      <ListItemText
                        primary={serviceAccount.clientName}
                        secondary={serviceAccount.clientId}
                      />
                    </ListItem>
                  ))}
                </Box>
              ) : (
                <Typography variant="body2" color="text.secondary">
                  No service accounts have this role
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default RoleDetail;
