import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  TextField,
  FormControlLabel,
  Switch,
  Alert,
  CircularProgress,
  Autocomplete,
  Chip,
  Grid,
  Divider,
  MenuItem,
  FormControl,
  InputLabel,
  Select,
} from '@mui/material';
import {
  ArrowBack as ArrowBackIcon,
  Save as SaveIcon,
  Cancel as CancelIcon,
} from '@mui/icons-material';
import { useServiceAccount, useUpdateServiceAccount, useRoles, useScopesForAccountType } from '../services/hooks';
import { useNavigation } from '../contexts/NavigationContext';
import { usePageTracking } from '../hooks/usePageTracking';
import type { ServiceAccount } from '../services/mockApi';

interface ServiceAccountFormData {
  clientName: string;
  description: string;
  accountType: 'Service-to-service' | 'Browser';
  owner: string;
  grantTypes: string[];
  redirectUris: string[];
  tokenEndpointAuthMethod: string;
  audience: string;
  isActive: boolean;
}

const ServiceAccountEdit: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: serviceAccount, isLoading: serviceAccountLoading, error: serviceAccountError } = useServiceAccount(id!);
  const { data: roles = [], isLoading: rolesLoading } = useRoles();
  const updateServiceAccountMutation = useUpdateServiceAccount();
  const { goBack, getBackLabel, canGoBack } = useNavigation();
  
  // Track this page for breadcrumb navigation
  usePageTracking({ 
    pageLabel: serviceAccount ? `Edit ${serviceAccount.clientName}` : 'Edit Service Account',
    shouldTrack: false // Don't track edit pages in breadcrumbs
  });

  const [formData, setFormData] = useState<ServiceAccountFormData>({
    clientName: '',
    description: '',
    accountType: 'Service-to-service',
    owner: '',
    grantTypes: [],
    redirectUris: [],
    tokenEndpointAuthMethod: 'client_secret_basic',
    audience: '',
    isActive: true,
  });

  const [errors, setErrors] = useState<Partial<ServiceAccountFormData>>({});
  const [redirectUri, setRedirectUri] = useState('');
  const [selectedScopeIds, setSelectedScopeIds] = useState<string[]>([]);
  const [selectedRoleIds, setSelectedRoleIds] = useState<string[]>([]);
  
  // Fetch scopes based on the selected account type
  const { data: availableScopes } = useScopesForAccountType(formData.accountType);

  const availableGrantTypes = [
    'authorization_code',
    'client_credentials',
    'refresh_token',
    'implicit',
    'password'
  ];

  const availableAuthMethods = [
    'client_secret_basic',
    'client_secret_post',
    'none'
  ];

  useEffect(() => {
    if (serviceAccount) {
      setFormData({
        clientName: serviceAccount.clientName,
        description: serviceAccount.description || '',
        accountType: serviceAccount.accountType || 'Service-to-service',
        owner: serviceAccount.owner || '',
        grantTypes: serviceAccount.grantTypes || [],
        redirectUris: serviceAccount.redirectUris || [],
        tokenEndpointAuthMethod: serviceAccount.tokenEndpointAuthMethod,
        audience: typeof serviceAccount.audience === 'string' ? serviceAccount.audience : '',
        isActive: serviceAccount.isActive,
      });
    }
  }, [serviceAccount]);

  // Update selected scope IDs when service account data or available scopes change
  useEffect(() => {
    if (serviceAccount && availableScopes) {
      const currentScopeIds = serviceAccount.scopes ? serviceAccount.scopes.map(scope => scope.id) : [];
      setSelectedScopeIds(currentScopeIds);
    }
  }, [serviceAccount, availableScopes]);

  // Update selected role IDs when service account data or roles change
  useEffect(() => {
    if (serviceAccount && roles) {
      const currentRoleIds = serviceAccount.roles ? serviceAccount.roles.map(role => role.id) : [];
      setSelectedRoleIds(currentRoleIds);
    }
  }, [serviceAccount, roles]);

  const handleBackClick = () => {
    if (canGoBack()) {
      goBack();
    } else {
      navigate(`/service-accounts/${id}`);
    }
  };

  const handleInputChange = (field: keyof ServiceAccountFormData, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: undefined }));
    }
  };

  // Handle account type change and clear selected scopes since they're filtered by type
  const handleAccountTypeChange = (accountType: 'Service-to-service' | 'Browser') => {
    handleInputChange('accountType', accountType);
    setSelectedScopeIds([]); // Clear scopes when account type changes
  };

  const validateForm = (): boolean => {
    const newErrors: Partial<ServiceAccountFormData> = {};

    if (!formData.clientName?.trim()) {
      newErrors.clientName = 'Client name is required';
    }

    if (selectedScopeIds.length === 0) {
      // We'll show scope errors in the UI directly rather than using the errors object
      // since scopes are not part of the formData but handled separately
    }

    if (!formData.owner?.trim()) {
      newErrors.owner = 'Owner is required';
    }

    if (!formData.grantTypes || formData.grantTypes.length === 0) {
      newErrors.grantTypes = ['At least one grant type is required'];
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async () => {
    if (!validateForm()) {
      return;
    }

    try {
      const serviceAccountData = {
        ...formData,
        scopeIds: selectedScopeIds, // Send scope IDs as expected by backend
        roleIds: selectedRoleIds,   // Send role IDs for bulk assignment
      };
      
      // Update the main service account data with roles and scopes
      await updateServiceAccountMutation.mutateAsync({
        id: id!,
        serviceAccountData,
      });
      
      navigate(`/service-accounts/${id}`);
    } catch (error) {
      console.error('Failed to update service account:', error);
    }
  };

  const handleAddRedirectUri = () => {
    if (redirectUri.trim() && !formData.redirectUris.includes(redirectUri.trim())) {
      handleInputChange('redirectUris', [...formData.redirectUris, redirectUri.trim()]);
      setRedirectUri('');
    }
  };

  const handleRemoveRedirectUri = (uri: string) => {
    handleInputChange('redirectUris', formData.redirectUris.filter(u => u !== uri));
  };

  if (serviceAccountLoading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (serviceAccountError || !serviceAccount) {
    return (
      <Box sx={{ p: 3 }}>
        <Alert severity="error">
          Failed to load service account. Please try again.
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
          {getBackLabel() || 'Back to Details'}
        </Button>
        <Typography variant="h4" component="h1" sx={{ flexGrow: 1 }}>
          Edit Service Account
        </Typography>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button
            startIcon={<CancelIcon />}
            onClick={handleBackClick}
            variant="outlined"
          >
            Cancel
          </Button>
          <Button
            startIcon={<SaveIcon />}
            onClick={handleSubmit}
            variant="contained"
            disabled={updateServiceAccountMutation.isPending}
          >
            {updateServiceAccountMutation.isPending ? 'Saving...' : 'Save Changes'}
          </Button>
        </Box>
      </Box>

      {updateServiceAccountMutation.isError && (
        <Alert severity="error" sx={{ mb: 3 }}>
          Failed to update service account. Please try again.
        </Alert>
      )}

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Basic Information
              </Typography>
              <Divider sx={{ mb: 3 }} />

              <Grid container spacing={3}>
                {/* Client ID (read-only) */}
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Client ID"
                    value={serviceAccount.clientId}
                    disabled
                    helperText="Client ID cannot be changed"
                  />
                </Grid>

                {/* Client Name */}
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Client Name"
                    value={formData.clientName}
                    onChange={(e) => handleInputChange('clientName', e.target.value)}
                    error={!!errors.clientName}
                    helperText={errors.clientName}
                    required
                  />
                </Grid>

                {/* Owner */}
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Owner"
                    value={formData.owner}
                    onChange={(e) => handleInputChange('owner', e.target.value)}
                    error={!!errors.owner}
                    helperText={errors.owner}
                    required
                  />
                </Grid>

                {/* Account Type */}
                <Grid item xs={12} sm={6}>
                  <FormControl fullWidth required>
                    <InputLabel>Account Type</InputLabel>
                    <Select
                      value={formData.accountType}
                      label="Account Type"
                      onChange={(e) => handleAccountTypeChange(e.target.value as 'Service-to-service' | 'Browser')}
                    >
                      <MenuItem value="Service-to-service">Service-to-service</MenuItem>
                      <MenuItem value="Browser">Browser</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>

                {/* Description */}
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    label="Description"
                    value={formData.description}
                    onChange={(e) => handleInputChange('description', e.target.value)}
                    multiline
                    rows={3}
                  />
                </Grid>

                {/* Scope */}
                <Grid item xs={12}>
                  <Autocomplete
                    multiple
                    value={availableScopes?.filter(scope => selectedScopeIds.includes(scope.id)) || []}
                    onChange={(_, newValue) => {
                      setSelectedScopeIds(newValue.map(scope => scope.id));
                    }}
                    options={availableScopes || []}
                    getOptionLabel={(option) => option.name}
                    renderTags={(value, getTagProps) =>
                      value.map((option, index) => {
                        const { key, ...chipProps } = getTagProps({ index });
                        return (
                          <Chip key={key} variant="outlined" label={option.name} {...chipProps} />
                        );
                      })
                    }
                    renderOption={(props, option) => {
                      const { key, ...otherProps } = props;
                      return (
                        <Box component="li" key={key} {...otherProps}>
                          <Box>
                            <Typography variant="body2" fontWeight={500}>
                              {option.name}
                            </Typography>
                            <Typography variant="caption" color="text.secondary">
                              {option.description}
                            </Typography>
                          </Box>
                        </Box>
                      );
                    }}
                    renderInput={(params) => (
                      <TextField
                        {...params}
                        label="Scopes"
                        error={selectedScopeIds.length === 0}
                        helperText={selectedScopeIds.length === 0 ? 'At least one scope is required' : `Select scopes for ${formData.accountType} account type`}
                        required
                      />
                    )}
                  />
                </Grid>

                {/* Grant Types */}
                <Grid item xs={12}>
                  <Autocomplete
                    multiple
                    value={formData.grantTypes}
                    onChange={(_, newValue) => handleInputChange('grantTypes', newValue)}
                    options={availableGrantTypes}
                    renderTags={(value, getTagProps) =>
                      value.map((option, index) => {
                        const { key, ...chipProps } = getTagProps({ index });
                        return (
                          <Chip key={key} variant="outlined" label={option} {...chipProps} />
                        );
                      })
                    }
                    renderInput={(params) => (
                      <TextField
                        {...params}
                        label="Grant Types"
                        error={!!errors.grantTypes}
                        helperText={errors.grantTypes?.[0] || 'Select OAuth2 grant types'}
                        required
                      />
                    )}
                  />
                </Grid>

                {/* Roles */}
                <Grid item xs={12}>
                  <Autocomplete
                    multiple
                    value={roles?.filter(role => selectedRoleIds.includes(role.id)) || []}
                    onChange={(_, newValue) => {
                      setSelectedRoleIds(newValue.map(role => role.id));
                    }}
                    options={roles || []}
                    getOptionLabel={(option) => option.name}
                    renderTags={(value, getTagProps) =>
                      value.map((option, index) => {
                        const { key, ...chipProps } = getTagProps({ index });
                        return (
                          <Chip key={key} variant="outlined" label={option.name} {...chipProps} />
                        );
                      })
                    }
                    renderOption={(props, option) => {
                      const { key, ...otherProps } = props;
                      return (
                        <Box component="li" key={key} {...otherProps}>
                          <Box>
                            <Typography variant="body2" fontWeight={500}>
                              {option.name}
                            </Typography>
                            <Typography variant="caption" color="text.secondary">
                              {option.description}
                            </Typography>
                          </Box>
                        </Box>
                      );
                    }}
                    renderInput={(params) => (
                      <TextField
                        {...params}
                        label="Roles"
                        helperText="Select roles to assign to this service account"
                      />
                    )}
                  />
                </Grid>

                {/* Token Endpoint Auth Method */}
                <Grid item xs={12} sm={6}>
                  <FormControl fullWidth>
                    <InputLabel>Token Endpoint Auth Method</InputLabel>
                    <Select
                      value={formData.tokenEndpointAuthMethod}
                      onChange={(e) => handleInputChange('tokenEndpointAuthMethod', e.target.value)}
                      label="Token Endpoint Auth Method"
                    >
                      {availableAuthMethods.map((method) => (
                        <MenuItem key={method} value={method}>
                          {method}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                </Grid>

                {/* Audience */}
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Audience"
                    value={formData.audience}
                    onChange={(e) => handleInputChange('audience', e.target.value)}
                    helperText="Optional audience for the service account"
                  />
                </Grid>

                {/* Redirect URIs */}
                <Grid item xs={12}>
                  <Typography variant="subtitle2" gutterBottom>
                    Redirect URIs
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
                    <TextField
                      fullWidth
                      placeholder="https://example.com/callback"
                      value={redirectUri}
                      onChange={(e) => setRedirectUri(e.target.value)}
                      onKeyPress={(e) => {
                        if (e.key === 'Enter') {
                          e.preventDefault();
                          handleAddRedirectUri();
                        }
                      }}
                    />
                    <Button
                      variant="outlined"
                      onClick={handleAddRedirectUri}
                      disabled={!redirectUri.trim()}
                    >
                      Add
                    </Button>
                  </Box>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                    {formData.redirectUris.map((uri) => (
                      <Chip
                        key={uri}
                        label={uri}
                        onDelete={() => handleRemoveRedirectUri(uri)}
                        variant="outlined"
                      />
                    ))}
                  </Box>
                </Grid>

                {/* Status */}
                <Grid item xs={12}>
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
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Side Panel */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Service Account Information
              </Typography>
              <Divider sx={{ mb: 2 }} />
              
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <Box>
                  <Typography variant="subtitle2" color="text.secondary">
                    Created
                  </Typography>
                  <Typography variant="body2">
                    {new Date(serviceAccount.createdAt).toLocaleString()}
                  </Typography>
                </Box>
                
                <Box>
                  <Typography variant="subtitle2" color="text.secondary">
                    Last Updated
                  </Typography>
                  <Typography variant="body2">
                    {new Date(serviceAccount.updatedAt).toLocaleString()}
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default ServiceAccountEdit;
