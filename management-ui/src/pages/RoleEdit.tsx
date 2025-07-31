import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  TextField,
  Grid,
  Alert,
  CircularProgress,
  Paper,
  Avatar,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  IconButton,
  Autocomplete,
  Tabs,
  Tab,
} from '@mui/material';
import {
  ArrowBack as ArrowBackIcon,
  Save as SaveIcon,
  Security as SecurityIcon,
  Person as PersonIcon,
  Storage as StorageIcon,
  Delete as DeleteIcon,
} from '@mui/icons-material';
import { useNavigation } from '../contexts/NavigationContext';
import { usePageTracking } from '../hooks/usePageTracking';
import { 
  useRole, 
  useUpdateRole, 
  useUsersByRole, 
  useServiceAccountsByRole,
  useUsersNotInRole,
  useServiceAccountsNotInRole,
  useAssignRoleToUser,
  useRemoveRoleFromUser,
  useAssignRoleToServiceAccount,
  useRemoveRoleFromServiceAccount
} from '../services/hooks';
import type { UpdateRoleRequest, ServiceAccount } from '../services/mockApi';

const RoleEdit: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: role, isLoading, error } = useRole(id!);
  const updateRole = useUpdateRole();
  const { goBack, getBackLabel, canGoBack } = useNavigation();
  
  // Track this page for breadcrumb navigation
  usePageTracking({ 
    pageLabel: role ? `Edit ${role.name} Role` : 'Edit Role',
    shouldTrack: false // Don't track edit pages in breadcrumbs
  });

  const handleBackClick = () => {
    if (canGoBack()) {
      goBack();
    } else {
      navigate(`/roles/${id}`);
    }
  };

  // Role membership data
  const { data: usersWithRole = [], isLoading: usersLoading } = useUsersByRole(id!);
  const { data: servicesWithRole = [], isLoading: servicesLoading } = useServiceAccountsByRole(id!);
  const { data: availableUsers = [] } = useUsersNotInRole(id!);
  const { data: availableServices = [] } = useServiceAccountsNotInRole(id!);

  // Role assignment mutations
  const assignRoleToUser = useAssignRoleToUser();
  const removeRoleFromUser = useRemoveRoleFromUser();
  const assignRoleToService = useAssignRoleToServiceAccount();
  const removeRoleFromService = useRemoveRoleFromServiceAccount();

  const [formData, setFormData] = useState<UpdateRoleRequest>({
    name: '',
    description: '',
  });

  const [formErrors, setFormErrors] = useState<Record<string, string>>({});
  const [activeTab, setActiveTab] = useState(0);

  useEffect(() => {
    if (role) {
      setFormData({
        name: role.name,
        description: role.description || '',
      });
    }
  }, [role]);

  const validateForm = (): boolean => {
    const errors: Record<string, string> = {};

    if (!formData.name || !formData.name.trim()) {
      errors.name = 'Role name is required';
    } else if (formData.name.trim().length < 2) {
      errors.name = 'Role name must be at least 2 characters';
    }

    if (formData.description && formData.description.length > 500) {
      errors.description = 'Description must be less than 500 characters';
    }

    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    try {
      await updateRole.mutateAsync({ 
        id: id!, 
        roleData: {
          ...formData,
          name: formData.name?.trim(),
          description: formData.description?.trim() || undefined,
        }
      });
      navigate(`/roles/${id}`);
    } catch (error) {
      console.error('Error updating role:', error);
    }
  };

  const handleCancel = () => {
    handleBackClick();
  };

  const handleChange = (field: keyof UpdateRoleRequest) => (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    setFormData(prev => ({
      ...prev,
      [field]: e.target.value,
    }));
    
    // Clear field error when user starts typing
    if (formErrors[field]) {
      setFormErrors(prev => ({
        ...prev,
        [field]: '',
      }));
    }
  };

  const handleAssignUser = async (userId: string) => {
    try {
      await assignRoleToUser.mutateAsync({ userId, roleId: id! });
    } catch (error) {
      console.error('Error assigning role to user:', error);
    }
  };

  const handleRemoveUser = async (userId: string) => {
    try {
      await removeRoleFromUser.mutateAsync({ userId, roleId: id! });
    } catch (error) {
      console.error('Error removing role from user:', error);
    }
  };

  const handleAssignService = async (serviceId: string) => {
    try {
      await assignRoleToService.mutateAsync({ serviceAccountId: serviceId, roleId: id! });
    } catch (error) {
      console.error('Error assigning role to service account:', error);
    }
  };

  const handleRemoveService = async (serviceId: string) => {
    try {
      await removeRoleFromService.mutateAsync({ serviceAccountId: serviceId, roleId: id! });
    } catch (error) {
      console.error('Error removing role from service account:', error);
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
            Edit Role
          </Typography>
        </Box>
        <Box display="flex" gap={2}>
          <Button
            onClick={handleCancel}
            variant="outlined"
            disabled={updateRole.isPending}
          >
            Cancel
          </Button>
          <Button
            startIcon={<SaveIcon />}
            onClick={handleSubmit}
            variant="contained"
            color="primary"
            disabled={updateRole.isPending}
          >
            {updateRole.isPending ? 'Saving...' : 'Save Changes'}
          </Button>
        </Box>
      </Box>

      {updateRole.error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          Error updating role. Please try again.
        </Alert>
      )}

      {/* Tabs */}
      <Paper sx={{ mb: 3 }}>
        <Tabs value={activeTab} onChange={(e, newValue) => setActiveTab(newValue)}>
          <Tab label="Role Details" />
          <Tab label="User Assignments" />
          <Tab label="Service Assignments" />
        </Tabs>
      </Paper>

      {/* Tab Content */}
      {activeTab === 0 && (
        <Grid container spacing={3}>
          {/* Role Edit Form */}
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
                    <Typography variant="body2" color="text.secondary">
                      Role ID: {role.id}
                    </Typography>
                  </Box>
                </Box>

                <Box component="form" onSubmit={handleSubmit}>
                  <Grid container spacing={3}>
                    <Grid item xs={12}>
                      <TextField
                        fullWidth
                        label="Role Name"
                        value={formData.name || ''}
                        onChange={handleChange('name')}
                        error={!!formErrors.name}
                        helperText={formErrors.name}
                        required
                        variant="outlined"
                      />
                    </Grid>

                    <Grid item xs={12}>
                      <TextField
                        fullWidth
                        label="Description"
                        value={formData.description || ''}
                        onChange={handleChange('description')}
                        error={!!formErrors.description}
                        helperText={formErrors.description || 'Optional description for this role'}
                        multiline
                        rows={4}
                        variant="outlined"
                      />
                    </Grid>
                  </Grid>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          {/* Role Information Panel */}
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Role Information
              </Typography>
              <Box display="flex" flexDirection="column" gap={2}>
                <Box>
                  <Typography variant="subtitle2" color="text.secondary">
                    Created
                  </Typography>
                  <Typography variant="body2">
                    {new Date(role.createdAt).toLocaleString()}
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="subtitle2" color="text.secondary">
                    Last Updated
                  </Typography>
                  <Typography variant="body2">
                    {new Date(role.updatedAt).toLocaleString()}
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="subtitle2" color="text.secondary">
                    Users with this role
                  </Typography>
                  <Typography variant="body2">
                    {role.userCount || 0} users
                  </Typography>
                </Box>
              </Box>
            </Paper>

            <Paper sx={{ p: 3, mt: 2 }}>
              <Typography variant="h6" gutterBottom>
                Edit Guidelines
              </Typography>
              <Typography variant="body2" color="text.secondary">
                • Role name should be descriptive and unique
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                • Description helps other administrators understand the role's purpose
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                • Changes will affect all users assigned to this role
              </Typography>
            </Paper>
          </Grid>
        </Grid>
      )}

      {/* User Assignments Tab */}
      {activeTab === 1 && (
        <Grid container spacing={3}>
          <Grid item xs={12} md={8}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Users with this Role
                </Typography>
                <List>
                  {usersWithRole?.map((user) => (
                    <ListItem key={user.id}>
                      <ListItemAvatar>
                        <Avatar sx={{ bgcolor: 'secondary.main' }}>
                          <PersonIcon />
                        </Avatar>
                      </ListItemAvatar>
                      <ListItemText
                        primary={user.displayName || user.email}
                        secondary={`${user.email} • ${user.roles?.length || 0} roles`}
                      />
                      <IconButton
                        edge="end"
                        onClick={() => handleRemoveUser(user.id)}
                        color="error"
                        size="small"
                      >
                        <DeleteIcon />
                      </IconButton>
                    </ListItem>
                  ))}
                  {(!usersWithRole || usersWithRole.length === 0) && (
                    <ListItem>
                      <ListItemText
                        primary="No users assigned to this role"
                        secondary="Use the form below to assign users"
                      />
                    </ListItem>
                  )}
                </List>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Assign User to Role
                </Typography>
                <Autocomplete
                  options={availableUsers}
                  getOptionLabel={(option) => `${option.displayName || option.email} (${option.email})`}
                  onChange={(event, newValue) => {
                    if (newValue) {
                      handleAssignUser(newValue.id);
                    }
                  }}
                  renderInput={(params) => (
                    <TextField
                      {...params}
                      label="Select a user"
                      variant="outlined"
                      fullWidth
                    />
                  )}
                />
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {/* Service Assignments Tab */}
      {activeTab === 2 && (
        <Grid container spacing={3}>
          <Grid item xs={12} md={8}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Service Accounts with this Role
                </Typography>
                <List>
                  {servicesWithRole?.map((service: ServiceAccount) => (
                    <ListItem key={service.id}>
                      <ListItemAvatar>
                        <Avatar sx={{ bgcolor: 'info.main' }}>
                          <StorageIcon />
                        </Avatar>
                      </ListItemAvatar>
                      <ListItemText
                        primary={service.clientName || service.clientId}
                        secondary={`Client ID: ${service.clientId} • ${service.roles?.length || 0} roles`}
                      />
                      <IconButton
                        edge="end"
                        onClick={() => handleRemoveService(service.id)}
                        color="error"
                        size="small"
                      >
                        <DeleteIcon />
                      </IconButton>
                    </ListItem>
                  ))}
                  {(!servicesWithRole || servicesWithRole.length === 0) && (
                    <ListItem>
                      <ListItemText
                        primary="No services assigned to this role"
                        secondary="Use the form below to assign services"
                      />
                    </ListItem>
                  )}
                </List>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Assign Service Account to Role
                </Typography>
                <Autocomplete
                  options={availableServices}
                  getOptionLabel={(option: any) => `${option.clientName || option.clientId} (${option.clientId})`}
                  onChange={(event, newValue: any) => {
                    if (newValue) {
                      handleAssignService(newValue.id);
                    }
                  }}
                  renderInput={(params) => (
                    <TextField
                      {...params}
                      label="Select a service account"
                      variant="outlined"
                      fullWidth
                    />
                  )}
                />
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}
    </Box>
  );
};

export default RoleEdit;
