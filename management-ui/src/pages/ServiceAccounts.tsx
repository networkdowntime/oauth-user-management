import React from 'react';
import { usePageTracking } from '../hooks/usePageTracking';
import {
  Box,
  Typography,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  IconButton,
  Chip,
  CircularProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Alert,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Autocomplete,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Visibility as ViewIcon,
  Key as KeyIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import {
  useServiceAccounts,
  useCreateServiceAccount,
  useUpdateServiceAccount,
  useDeleteServiceAccount,
  useUsers,
  useRoles,
  useScopesForAccountType,
} from '../services/hooks';
import { CreateServiceAccountRequest, UpdateServiceAccountRequest } from '../services/mockApi';

const ServiceAccounts: React.FC = () => {
  const navigate = useNavigate();
  const { data: serviceAccounts, isLoading, error } = useServiceAccounts();
  const { data: roles = [] } = useRoles();
  const createServiceAccountMutation = useCreateServiceAccount();
  const deleteServiceAccountMutation = useDeleteServiceAccount();
  
  // Track this page for breadcrumb navigation
  usePageTracking({ pageLabel: 'Service Accounts' });
  
  const [createDialogOpen, setCreateDialogOpen] = React.useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = React.useState(false);
  const [selectedServiceAccountId, setSelectedServiceAccountId] = React.useState<string | null>(null);
  const [deleteError, setDeleteError] = React.useState<string | null>(null);
  const [newServiceAccount, setNewServiceAccount] = React.useState<CreateServiceAccountRequest>({
    clientId: '',
    clientName: '',
    description: '',
    accountType: 'Service-to-service',
    owner: '',
    redirectUris: [],
    postLogoutRedirectUris: [],
    allowedCorsOrigins: [],
    grantTypes: [],
    createdBy: 'admin', // TODO: Get from auth context
  });
  
  // State for selected scope IDs in the form
  const [selectedScopeIds, setSelectedScopeIds] = React.useState<string[]>([]);
  
  // State for selected role IDs in the form
  const [selectedRoleIds, setSelectedRoleIds] = React.useState<string[]>([]);
  
  // Available grant types
  const availableGrantTypes = [
    'authorization_code',
    'client_credentials',
    'refresh_token',
    'implicit',
    'password'
  ];
  
  // Fetch scopes based on the selected account type
  const { data: availableScopes } = useScopesForAccountType(newServiceAccount.accountType || 'Service-to-service');

  const handleCreateServiceAccount = async () => {
    try {
      const serviceAccountData = {
        ...newServiceAccount,
        scopeIds: selectedScopeIds,
        roleIds: selectedRoleIds,
      };
      
      await createServiceAccountMutation.mutateAsync(serviceAccountData);
      setCreateDialogOpen(false);
      setNewServiceAccount({
        clientId: '',
        clientName: '',
        description: '',
        accountType: 'Service-to-service',
        owner: '',
        redirectUris: [],
        postLogoutRedirectUris: [],
        allowedCorsOrigins: [],
        grantTypes: [],
        createdBy: 'admin', // TODO: Get from auth context
      });
      setSelectedScopeIds([]);
      setSelectedRoleIds([]);
    } catch (error) {
      console.error('Failed to create service account:', error);
    }
  };
  
  // Handle account type change and clear selected scopes since they're filtered by type
  const handleAccountTypeChange = (accountType: 'Service-to-service' | 'Browser') => {
    setNewServiceAccount({ ...newServiceAccount, accountType });
    setSelectedScopeIds([]); // Clear scopes when account type changes
    setSelectedRoleIds([]); // Clear roles when account type changes
  };
  
  const handleDeleteServiceAccount = async () => {
    if (selectedServiceAccountId) {
      try {
        setDeleteError(null);
        await deleteServiceAccountMutation.mutateAsync(selectedServiceAccountId);
        setDeleteDialogOpen(false);
        setSelectedServiceAccountId(null);
      } catch (error) {
        console.error('Failed to delete service account:', error);
        setDeleteError(error instanceof Error ? error.message : 'Failed to delete service account');
      }
    }
  };

  const openDeleteDialog = (serviceAccountId: string) => {
    setSelectedServiceAccountId(serviceAccountId);
    setDeleteDialogOpen(true);
  };

  const selectedServiceAccount = serviceAccounts?.find(sa => sa.id === selectedServiceAccountId);

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box>
        <Alert severity="error" sx={{ mb: 2 }}>
          Error loading service accounts
        </Alert>
      </Box>
    );
  }

  return (
    <Box>
      {/* Header */}
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" component="h1">
          Service Accounts
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => setCreateDialogOpen(true)}
        >
          Add Service Account
        </Button>
      </Box>

      {/* Service Accounts Table */}
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Client Name</TableCell>
              <TableCell>Client ID</TableCell>
              <TableCell>Account Type</TableCell>
              <TableCell>Owner</TableCell>
              <TableCell>Scopes</TableCell>
              <TableCell>Grant Types</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Last Used</TableCell>
              <TableCell>Roles</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {serviceAccounts?.map((serviceAccount) => (
              <TableRow key={serviceAccount.id}>
                <TableCell>
                  <Box>
                    <Typography variant="body2" fontWeight={500}>
                      {serviceAccount.clientName}
                    </Typography>
                    {serviceAccount.description && (
                      <Typography variant="caption" color="text.secondary">
                        {serviceAccount.description}
                      </Typography>
                    )}
                  </Box>
                </TableCell>
                <TableCell>
                  <Typography variant="body2" fontFamily="monospace">
                    {serviceAccount.clientId}
                  </Typography>
                </TableCell>
                <TableCell>
                  <Chip
                    label={serviceAccount.accountType}
                    color={serviceAccount.accountType === 'Service-to-service' ? 'primary' : 'secondary'}
                    size="small"
                    variant="outlined"
                  />
                </TableCell>
                <TableCell>{serviceAccount.owner || '-'}</TableCell>
                <TableCell>
                  {serviceAccount.scopes && serviceAccount.scopes.length > 0 ? (
                    <Box display="flex" flexWrap="wrap" gap={0.5}>
                      {serviceAccount.scopes.map((scope) => (
                        <Chip
                          key={scope.id}
                          label={scope.name}
                          size="small"
                          variant="outlined"
                        />
                      ))}
                    </Box>
                  ) : '-'}
                </TableCell>
                <TableCell>
                  <Box display="flex" flexWrap="wrap" gap={0.5}>
                    {serviceAccount.grantTypes?.map((grantType) => (
                      <Chip
                        key={grantType}
                        label={grantType}
                        size="small"
                        variant="outlined"
                      />
                    ))}
                  </Box>
                </TableCell>
                <TableCell>
                  <Chip
                    label={serviceAccount.isActive ? 'Active' : 'Inactive'}
                    color={serviceAccount.isActive ? 'success' : 'error'}
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  {serviceAccount.lastUsedAt ? (
                    <Typography variant="body2">
                      {new Date(serviceAccount.lastUsedAt).toLocaleDateString()}
                    </Typography>
                  ) : 'Never'}
                </TableCell>
                <TableCell>
                  <Box display="flex" flexWrap="wrap" gap={0.5}>
                    {serviceAccount.roles.map((role) => (
                      <Chip
                        key={role.id}
                        label={role.name}
                        size="small"
                        variant="outlined"
                      />
                    ))}
                  </Box>
                </TableCell>
                <TableCell align="right">
                  <Box display="flex" gap={1}>
                    <IconButton
                      size="small"
                      color="primary"
                      onClick={() => navigate(`/service-accounts/${serviceAccount.id}`)}
                      title="View Details"
                    >
                      <ViewIcon />
                    </IconButton>
                    <IconButton
                      size="small"
                      color="primary"
                      onClick={() => navigate(`/service-accounts/${serviceAccount.id}/edit`)}
                      title="Edit"
                    >
                      <EditIcon />
                    </IconButton>
                    <IconButton
                      size="small"
                      color="error"
                      onClick={() => openDeleteDialog(serviceAccount.id)}
                      title="Delete"
                    >
                      <DeleteIcon />
                    </IconButton>
                  </Box>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Empty State */}
      {serviceAccounts && serviceAccounts.length === 0 && (
        <Box
          display="flex"
          flexDirection="column"
          alignItems="center"
          justifyContent="center"
          minHeight="200px"
          textAlign="center"
        >
          <KeyIcon sx={{ fontSize: 48, color: 'text.secondary', mb: 2 }} />
          <Typography variant="h6" color="text.secondary" gutterBottom>
            No service accounts found
          </Typography>
          <Typography variant="body2" color="text.secondary" mb={2}>
            Create your first service account to get started with OAuth2 client credentials flow.
          </Typography>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => setCreateDialogOpen(true)}
          >
            Add Service Account
          </Button>
        </Box>
      )}

      {/* Create Service Account Dialog */}
      <Dialog
        open={createDialogOpen}
        onClose={() => setCreateDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Create Service Account</DialogTitle>
        <DialogContent>
          <Box display="flex" flexDirection="column" gap={2} pt={1}>
            <TextField
              label="Client ID"
              fullWidth
              required
              value={newServiceAccount.clientId}
              onChange={(e) => setNewServiceAccount({ ...newServiceAccount, clientId: e.target.value })}
            />
            <TextField
              label="Client Name"
              fullWidth
              required
              value={newServiceAccount.clientName}
              onChange={(e) => setNewServiceAccount({ ...newServiceAccount, clientName: e.target.value })}
            />
            <FormControl fullWidth required>
              <InputLabel>Account Type</InputLabel>
              <Select
                value={newServiceAccount.accountType}
                label="Account Type"
                onChange={(e) => handleAccountTypeChange(e.target.value as 'Service-to-service' | 'Browser')}
              >
                <MenuItem value="Service-to-service">Service-to-service</MenuItem>
                <MenuItem value="Browser">Browser</MenuItem>
              </Select>
            </FormControl>
            <TextField
              label="Description"
              fullWidth
              multiline
              rows={2}
              value={newServiceAccount.description}
              onChange={(e) => setNewServiceAccount({ ...newServiceAccount, description: e.target.value })}
            />
            <TextField
              label="Owner"
              fullWidth
              value={newServiceAccount.owner}
              onChange={(e) => setNewServiceAccount({ ...newServiceAccount, owner: e.target.value })}
            />
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
              renderOption={(props, option) => (
                <Box component="li" {...props}>
                  <Box>
                    <Typography variant="body2" fontWeight={500}>
                      {option.name}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      {option.description}
                    </Typography>
                  </Box>
                </Box>
              )}
              renderInput={(params) => (
                <TextField
                  {...params}
                  label="Scopes"
                  helperText={`Select scopes for ${newServiceAccount.accountType} account type`}
                />
              )}
            />
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
              renderOption={(props, option) => (
                <Box component="li" {...props}>
                  <Box>
                    <Typography variant="body2" fontWeight={500}>
                      {option.name}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      {option.description}
                    </Typography>
                  </Box>
                </Box>
              )}
              renderInput={(params) => (
                <TextField
                  {...params}
                  label="Roles"
                  helperText="Select roles to assign to this service account"
                />
              )}
            />
            <Autocomplete
              multiple
              value={newServiceAccount.grantTypes || []}
              onChange={(_, newValue) => {
                setNewServiceAccount({ ...newServiceAccount, grantTypes: newValue });
              }}
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
                  helperText="Select OAuth2 grant types"
                />
              )}
            />
            <TextField
              label="Redirect URIs"
              fullWidth
              placeholder="one URI per line"
              multiline
              rows={3}
              value={newServiceAccount.redirectUris?.join('\n') || ''}
              onChange={(e) => setNewServiceAccount({ 
                ...newServiceAccount, 
                redirectUris: e.target.value.split('\n').filter(uri => uri.trim()) 
              })}
            />
            <TextField
              label="Post-logout Redirect URIs"
              fullWidth
              placeholder="one URI per line"
              multiline
              rows={3}
              value={newServiceAccount.postLogoutRedirectUris?.join('\n') || ''}
              onChange={(e) => setNewServiceAccount({ 
                ...newServiceAccount, 
                postLogoutRedirectUris: e.target.value.split('\n').filter(uri => uri.trim()) 
              })}
            />
            <TextField
              label="Allowed CORS Origins"
              fullWidth
              placeholder="one origin per line"
              multiline
              rows={3}
              value={newServiceAccount.allowedCorsOrigins?.join('\n') || ''}
              onChange={(e) => setNewServiceAccount({ 
                ...newServiceAccount, 
                allowedCorsOrigins: e.target.value.split('\n').filter(uri => uri.trim()) 
              })}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCreateDialogOpen(false)}>Cancel</Button>
          <Button
            onClick={handleCreateServiceAccount}
            variant="contained"
            disabled={!newServiceAccount.clientName.trim()}
          >
            Create
          </Button>
        </DialogActions>
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <Dialog
        open={deleteDialogOpen}
        onClose={() => setDeleteDialogOpen(false)}
        maxWidth="sm"
      >
        <DialogTitle>Delete Service Account</DialogTitle>
        <DialogContent>
          {deleteError && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {deleteError}
            </Alert>
          )}
          <Typography>
            Are you sure you want to delete the service account "{selectedServiceAccount?.clientName}"?
          </Typography>
          <Typography variant="body2" color="text.secondary" mt={1}>
            This action cannot be undone and will revoke all tokens for this service account.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button 
            onClick={() => {
              setDeleteDialogOpen(false);
              setDeleteError(null);
            }}
          >
            Cancel
          </Button>
          <Button
            onClick={handleDeleteServiceAccount}
            variant="contained"
            color="error"
            disabled={deleteServiceAccountMutation.isPending}
          >
            {deleteServiceAccountMutation.isPending ? 'Deleting...' : 'Delete'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default ServiceAccounts;
