import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  FormControlLabel,
  Switch,
  Alert,
  CircularProgress,
  Autocomplete,
  Chip,
  Grid,
  Divider,
} from '@mui/material';
import {
  ArrowBack as ArrowBackIcon,
  Save as SaveIcon,
  Cancel as CancelIcon,
} from '@mui/icons-material';
import { useUser, useUpdateUser, useRoles } from '../services/hooks';
import { useNavigation } from '../contexts/NavigationContext';
import { usePageTracking } from '../hooks/usePageTracking';
import type { UpdateUserRequest } from '../services/mockApi';

const UserEdit: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: user, isLoading: userLoading, error: userError } = useUser(id!);
  const { data: roles = [], isLoading: rolesLoading } = useRoles();
  const updateUserMutation = useUpdateUser();
  const { goBack, getBackLabel, canGoBack } = useNavigation();
  
  // Track this page for breadcrumb navigation
  usePageTracking({ 
    pageLabel: user ? `Edit ${user.displayName || user.email}` : 'Edit User',
    shouldTrack: false // Don't track edit pages in breadcrumbs
  });

  const handleBackClick = () => {
    if (canGoBack()) {
      goBack();
    } else {
      navigate(`/users/${id}`);
    }
  };

  const [formData, setFormData] = useState<UpdateUserRequest>({
    displayName: '',
    isActive: true,
    roleIds: [],
  });

  const [password, setPassword] = useState('******************'); // Placeholder for existing password
  const [passwordChanged, setPasswordChanged] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    if (user) {
      setFormData({
        displayName: user.displayName || '',
        isActive: user.isActive,
        roleIds: user.roles.map(role => role.id),
      });
      // Reset password state when user changes
      setPassword('******************');
      setPasswordChanged(false);
    }
  }, [user]);

  const handleInputChange = (field: keyof UpdateUserRequest, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    // Clear error when field is modified
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }));
    }
  };

  const handlePasswordChange = (newPassword: string) => {
    setPassword(newPassword);
    setPasswordChanged(true);
    // Clear password error
    if (errors.password) {
      setErrors(prev => ({ ...prev, password: '' }));
    }
  };

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.displayName?.trim()) {
      newErrors.displayName = 'Display name is required';
    }

    // Validate password if it was changed
    if (passwordChanged && (!password || password.trim().length < 8)) {
      newErrors.password = 'Password must be at least 8 characters long';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    try {
      // Prepare update data
      const updateData: UpdateUserRequest = { ...formData };
      // TODO: Handle password updates separately if needed
      // if (passwordChanged) {
      //   updateData.password = password;
      // }

      await updateUserMutation.mutateAsync({
        id: id!,
        userData: updateData,
      });
      navigate(`/users/${id}`);
    } catch (error) {
      console.error('Failed to update user:', error);
    }
  };

  const handleCancel = () => {
    navigate(`/users/${id}`);
  };

  if (userLoading || rolesLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (userError || !user) {
    return (
      <Box>
        <Alert severity="error" sx={{ mb: 2 }}>
          {userError ? 'Error loading user details' : 'User not found'}
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
            Edit User
          </Typography>
        </Box>
      </Box>

      {updateUserMutation.error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          Failed to update user. Please try again.
        </Alert>
      )}

      <Card>
        <CardContent>
          <form onSubmit={handleSubmit}>
            <Grid container spacing={3}>
              {/* Basic Information */}
              <Grid item xs={12}>
                <Typography variant="h6" gutterBottom>
                  Basic Information
                </Typography>
                <Divider sx={{ mb: 2 }} />
              </Grid>

              <Grid item xs={12} md={6}>
                <TextField
                  label="Email"
                  type="email"
                  value={user.email}
                  disabled
                  fullWidth
                  helperText="Email cannot be changed"
                />
              </Grid>

              <Grid item xs={12} md={6}>
                <TextField
                  label="Display Name"
                  value={formData.displayName}
                  onChange={(e) => handleInputChange('displayName', e.target.value)}
                  error={!!errors.displayName}
                  helperText={errors.displayName}
                  fullWidth
                  required
                />
              </Grid>

              {/* Security Section */}
              <Grid item xs={12}>
                <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
                  Security
                </Typography>
                <Divider sx={{ mb: 2 }} />
              </Grid>

              <Grid item xs={12} md={6}>
                <TextField
                  label="Password"
                  type="password"
                  value={password}
                  onChange={(e) => handlePasswordChange(e.target.value)}
                  error={!!errors.password}
                  helperText={errors.password || (passwordChanged ? 'Password will be updated' : 'Leave unchanged to keep current password')}
                  fullWidth
                  placeholder="Enter new password to change"
                />
              </Grid>

              <Grid item xs={12} md={6}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={formData.isActive}
                      onChange={(e) => handleInputChange('isActive', e.target.checked)}
                    />
                  }
                  label="Active"
                />
              </Grid>

              {/* Roles Section */}
              <Grid item xs={12}>
                <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
                  Roles
                </Typography>
                <Divider sx={{ mb: 2 }} />
              </Grid>

              <Grid item xs={12}>
                <Autocomplete
                  multiple
                  options={roles}
                  getOptionLabel={(option) => option.name}
                  value={roles.filter(role => formData.roleIds?.includes(role.id) ?? false)}
                  onChange={(_, newValue) => {
                    handleInputChange('roleIds', newValue.map(role => role.id));
                  }}
                  renderTags={(value, getTagProps) =>
                    value.map((option, index) => (
                      <Chip
                        variant="outlined"
                        label={option.name}
                        {...getTagProps({ index })}
                        key={option.id}
                      />
                    ))
                  }
                  renderInput={(params) => (
                    <TextField
                      {...params}
                      label="Assigned Roles"
                      placeholder="Select roles"
                    />
                  )}
                />
              </Grid>

              {/* Action Buttons */}
              <Grid item xs={12}>
                <Box display="flex" justifyContent="flex-end" gap={2} mt={3}>
                  <Button
                    startIcon={<CancelIcon />}
                    onClick={handleCancel}
                    variant="outlined"
                    disabled={updateUserMutation.isPending}
                  >
                    Cancel
                  </Button>
                  <Button
                    type="submit"
                    startIcon={<SaveIcon />}
                    variant="contained"
                    disabled={updateUserMutation.isPending}
                  >
                    {updateUserMutation.isPending ? 'Saving...' : 'Save Changes'}
                  </Button>
                </Box>
              </Grid>
            </Grid>
          </form>
        </CardContent>
      </Card>

      {/* User Information Display */}
      <Card sx={{ mt: 2 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Current User Information
          </Typography>
          <Divider sx={{ mb: 2 }} />
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
              <Typography variant="subtitle2" color="text.secondary">
                User ID
              </Typography>
              <Typography variant="body1" fontFamily="monospace">
                {user.id}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="subtitle2" color="text.secondary">
                Created At
              </Typography>
              <Typography variant="body1">
                {new Date(user.createdAt).toLocaleString()}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="subtitle2" color="text.secondary">
                Last Login
              </Typography>
              <Typography variant="body1">
                {user.lastLoginAt ? new Date(user.lastLoginAt).toLocaleString() : 'Never'}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="subtitle2" color="text.secondary">
                Failed Login Attempts
              </Typography>
              <Typography variant="body1">
                {user.failedLoginAttempts}
              </Typography>
            </Grid>
          </Grid>
        </CardContent>
      </Card>
    </Box>
  );
};

export default UserEdit;
