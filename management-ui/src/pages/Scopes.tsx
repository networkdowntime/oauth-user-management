import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Checkbox,
  FormControlLabel,
  Alert,
  Tooltip,
  Stack,
  OutlinedInput,
  SelectChangeEvent,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Visibility as VisibilityIcon,
  VisibilityOff as VisibilityOffIcon,
  Refresh as RefreshIcon,
} from '@mui/icons-material';

// Import hooks instead of direct API
import {
  useScopes,
  useCreateScope,
  useUpdateScope,
  useDeleteScope,
  useBulkActivateScopes,
  useBulkDeactivateScopes,
  useBulkDeleteScopes,
} from '../services/hooks';
import type { Scope, ScopeAppliesTo, CreateScopeRequest, UpdateScopeRequest } from '../services/mockApi';

interface ScopeFormData {
  name: string;
  description: string;
  appliesTo: ScopeAppliesTo[];
  isActive: boolean;
}

const Scopes: React.FC = () => {
  const { data: scopes = [], isLoading: loading, error: queryError, refetch: loadScopes } = useScopes();
  const createScopeMutation = useCreateScope();
  const updateScopeMutation = useUpdateScope();
  const deleteScopeMutation = useDeleteScope();
  const bulkActivateMutation = useBulkActivateScopes();
  const bulkDeactivateMutation = useBulkDeactivateScopes();
  const bulkDeleteMutation = useBulkDeleteScopes();

  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [selectedScope, setSelectedScope] = useState<Scope | null>(null);
  const [formData, setFormData] = useState<ScopeFormData>({
    name: '',
    description: '',
    appliesTo: [],
    isActive: true,
  });
  const [selectedScopes, setSelectedScopes] = useState<string[]>([]);

  const error = queryError?.message || createScopeMutation.error?.message || updateScopeMutation.error?.message || 
                deleteScopeMutation.error?.message || bulkActivateMutation.error?.message || 
                bulkDeactivateMutation.error?.message || bulkDeleteMutation.error?.message || null;

  const handleCreateScope = async () => {
    try {
      const createRequest: CreateScopeRequest = {
        name: formData.name,
        description: formData.description,
        appliesTo: formData.appliesTo,
        isActive: formData.isActive,
      };
      
      await createScopeMutation.mutateAsync(createRequest);
      setCreateDialogOpen(false);
      resetForm();
    } catch (err: any) {
      // Error is handled by React Query and displayed via the error state
    }
  };

  const handleEditScope = async () => {
    if (!selectedScope) return;
    
    try {
      const updateRequest: UpdateScopeRequest = {
        description: formData.description,
        appliesTo: formData.appliesTo,
        isActive: formData.isActive,
      };
      
      await updateScopeMutation.mutateAsync({ id: selectedScope.id, updates: updateRequest });
      setEditDialogOpen(false);
      resetForm();
      setSelectedScope(null);
    } catch (err: any) {
      // Error is handled by React Query and displayed via the error state
    }
  };

  const handleDeleteScope = async () => {
    if (!selectedScope) return;
    
    try {
      await deleteScopeMutation.mutateAsync(selectedScope.id);
      setDeleteDialogOpen(false);
      setSelectedScope(null);
    } catch (err: any) {
      // Error is handled by React Query and displayed via the error state
    }
  };

  const handleBulkActivate = async () => {
    try {
      await bulkActivateMutation.mutateAsync(selectedScopes);
      setSelectedScopes([]);
    } catch (err: any) {
      // Error is handled by React Query and displayed via the error state
    }
  };

  const handleBulkDeactivate = async () => {
    try {
      await bulkDeactivateMutation.mutateAsync(selectedScopes);
      setSelectedScopes([]);
    } catch (err: any) {
      // Error is handled by React Query and displayed via the error state
    }
  };

  const handleBulkDelete = async () => {
    try {
      await bulkDeleteMutation.mutateAsync(selectedScopes);
      setSelectedScopes([]);
    } catch (err: any) {
      // Error is handled by React Query and displayed via the error state
    }
  };

  const resetForm = () => {
    setFormData({
      name: '',
      description: '',
      appliesTo: [],
      isActive: true,
    });
  };

  const openCreateDialog = () => {
    resetForm();
    setCreateDialogOpen(true);
  };

  const openEditDialog = (scope: Scope) => {
    setSelectedScope(scope);
    setFormData({
      name: scope.name,
      description: scope.description,
      appliesTo: scope.appliesTo,
      isActive: scope.isActive,
    });
    setEditDialogOpen(true);
  };

  const openDeleteDialog = (scope: Scope) => {
    setSelectedScope(scope);
    setDeleteDialogOpen(true);
  };

  const handleAppliesToChange = (event: SelectChangeEvent<ScopeAppliesTo[]>) => {
    const value = event.target.value;
    setFormData(prev => ({
      ...prev,
      appliesTo: typeof value === 'string' ? value.split(',') as ScopeAppliesTo[] : value,
    }));
  };

  const handleScopeSelection = (scopeId: string, selected: boolean) => {
    if (selected) {
      setSelectedScopes(prev => [...prev, scopeId]);
    } else {
      setSelectedScopes(prev => prev.filter(id => id !== scopeId));
    }
  };

  const handleSelectAll = (selected: boolean) => {
    if (selected) {
      setSelectedScopes(scopes.map(scope => scope.id));
    } else {
      setSelectedScopes([]);
    }
  };

  const getScopeTypeColor = (appliesTo: ScopeAppliesTo[] | undefined): 'primary' | 'secondary' | 'success' => {
    if (!appliesTo || !Array.isArray(appliesTo)) {
      return 'secondary';
    }
    
    if (appliesTo.includes('Service-to-service') && appliesTo.includes('Browser')) {
      return 'success'; // Both
    } else if (appliesTo.includes('Service-to-service')) {
      return 'primary'; // Service only
    } else {
      return 'secondary'; // Browser only
    }
  };

  const getScopeTypeLabel = (appliesTo: ScopeAppliesTo[] | undefined): string => {
    if (!appliesTo || !Array.isArray(appliesTo)) {
      return 'None';
    }
    
    if (appliesTo.includes('Service-to-service') && appliesTo.includes('Browser')) {
      return 'Service-to-service & Browser';
    } else if (appliesTo.includes('Service-to-service')) {
      return 'Service-to-service Only';
    } else if (appliesTo.includes('Browser')) {
      return 'Browser Only';
    } else {
      return 'None';
    }
  };

  if (loading) {
    return (
      <Box sx={{ p: 3 }}>
        <Typography>Loading scopes...</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h4" component="h1">
          OAuth2 Scopes Management
        </Typography>
        <Stack direction="row" spacing={2}>
          <Button
            variant="outlined"
            startIcon={<RefreshIcon />}
            onClick={() => loadScopes()}
            disabled={loading}
          >
            Refresh
          </Button>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={openCreateDialog}
          >
            Add Scope
          </Button>
        </Stack>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {selectedScopes.length > 0 && (
        <Paper sx={{ p: 2, mb: 3 }}>
          <Typography variant="subtitle1" sx={{ mb: 2 }}>
            {selectedScopes.length} scope(s) selected
          </Typography>
          <Stack direction="row" spacing={2}>
            <Button
              variant="outlined"
              startIcon={<VisibilityIcon />}
              onClick={handleBulkActivate}
            >
              Activate
            </Button>
            <Button
              variant="outlined"
              startIcon={<VisibilityOffIcon />}
              onClick={handleBulkDeactivate}
            >
              Deactivate
            </Button>
            <Button
              variant="outlined"
              color="error"
              startIcon={<DeleteIcon />}
              onClick={handleBulkDelete}
            >
              Delete
            </Button>
          </Stack>
        </Paper>
      )}

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell padding="checkbox">
                <Checkbox
                  indeterminate={selectedScopes.length > 0 && selectedScopes.length < scopes.length}
                  checked={scopes.length > 0 && selectedScopes.length === scopes.length}
                  onChange={(e) => handleSelectAll(e.target.checked)}
                />
              </TableCell>
              <TableCell>Name</TableCell>
              <TableCell>Description</TableCell>
              <TableCell>Applies To</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Service Accounts</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {scopes.map((scope) => (
              <TableRow key={scope.id}>
                <TableCell padding="checkbox">
                  <Checkbox
                    checked={selectedScopes.includes(scope.id)}
                    onChange={(e) => handleScopeSelection(scope.id, e.target.checked)}
                  />
                </TableCell>
                <TableCell>
                  <Typography variant="body2" fontWeight="medium">
                    {scope.name}
                  </Typography>
                </TableCell>
                <TableCell>
                  <Typography variant="body2" color="text.secondary">
                    {scope.description}
                  </Typography>
                </TableCell>
                <TableCell>
                  <Chip
                    label={getScopeTypeLabel(scope.appliesTo)}
                    color={getScopeTypeColor(scope.appliesTo)}
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  <Chip
                    label={scope.isActive ? 'Active' : 'Inactive'}
                    color={scope.isActive ? 'success' : 'default'}
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  <Typography variant="body2">
                    {scope.serviceAccountCount}
                  </Typography>
                </TableCell>
                <TableCell>
                  <Tooltip title="Edit scope">
                    <IconButton
                      size="small"
                      onClick={() => openEditDialog(scope)}
                    >
                      <EditIcon />
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="Delete scope">
                    <IconButton
                      size="small"
                      color="error"
                      onClick={() => openDeleteDialog(scope)}
                      disabled={scope.serviceAccountCount > 0}
                    >
                      <DeleteIcon />
                    </IconButton>
                  </Tooltip>
                </TableCell>
              </TableRow>
            ))}
            {scopes.length === 0 && (
              <TableRow>
                <TableCell colSpan={7} align="center" sx={{ py: 3 }}>
                  <Typography color="text.secondary">
                    No scopes found. Click "Add Scope" to create your first scope.
                  </Typography>
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Create Scope Dialog */}
      <Dialog open={createDialogOpen} onClose={() => setCreateDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Create New Scope</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="Scope Name"
            value={formData.name}
            onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
            margin="normal"
            placeholder="e.g., user:read, analytics:write"
            helperText="Scope name should be alphanumeric with colons (e.g., resource:action)"
          />
          <TextField
            fullWidth
            label="Description"
            value={formData.description}
            onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
            margin="normal"
            multiline
            rows={3}
            placeholder="Describe what this scope allows..."
          />
          <FormControl fullWidth margin="normal">
            <InputLabel>Applies To</InputLabel>
            <Select
              multiple
              value={formData.appliesTo}
              onChange={handleAppliesToChange}
              input={<OutlinedInput label="Applies To" />}
              renderValue={(selected) => (
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                  {selected.map((value) => (
                    <Chip key={value} label={value} size="small" />
                  ))}
                </Box>
              )}
            >
              <MenuItem value="Service-to-service">Service-to-service</MenuItem>
              <MenuItem value="Browser">Browser applications</MenuItem>
            </Select>
          </FormControl>
          <FormControlLabel
            control={
              <Checkbox
                checked={formData.isActive}
                onChange={(e) => setFormData(prev => ({ ...prev, isActive: e.target.checked }))}
              />
            }
            label="Active"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCreateDialogOpen(false)}>Cancel</Button>
          <Button
            onClick={handleCreateScope}
            variant="contained"
            disabled={!formData.name || !formData.description || formData.appliesTo.length === 0}
          >
            Create
          </Button>
        </DialogActions>
      </Dialog>

      {/* Edit Scope Dialog */}
      <Dialog open={editDialogOpen} onClose={() => setEditDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Edit Scope</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="Scope Name"
            value={formData.name}
            margin="normal"
            disabled
            helperText="Scope name cannot be changed"
          />
          <TextField
            fullWidth
            label="Description"
            value={formData.description}
            onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
            margin="normal"
            multiline
            rows={3}
            placeholder="Describe what this scope allows..."
          />
          <FormControl fullWidth margin="normal">
            <InputLabel>Applies To</InputLabel>
            <Select
              multiple
              value={formData.appliesTo}
              onChange={handleAppliesToChange}
              input={<OutlinedInput label="Applies To" />}
              renderValue={(selected) => (
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                  {selected.map((value) => (
                    <Chip key={value} label={value} size="small" />
                  ))}
                </Box>
              )}
            >
              <MenuItem value="Service">Service-to-service</MenuItem>
              <MenuItem value="Browser">Browser applications</MenuItem>
            </Select>
          </FormControl>
          <FormControlLabel
            control={
              <Checkbox
                checked={formData.isActive}
                onChange={(e) => setFormData(prev => ({ ...prev, isActive: e.target.checked }))}
              />
            }
            label="Active"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setEditDialogOpen(false)}>Cancel</Button>
          <Button
            onClick={handleEditScope}
            variant="contained"
            disabled={!formData.description || formData.appliesTo.length === 0}
          >
            Update
          </Button>
        </DialogActions>
      </Dialog>

      {/* Delete Scope Dialog */}
      <Dialog open={deleteDialogOpen} onClose={() => setDeleteDialogOpen(false)}>
        <DialogTitle>Delete Scope</DialogTitle>
        <DialogContent>
          <Typography>
            Are you sure you want to delete the scope "{selectedScope?.name}"?
            {selectedScope?.serviceAccountCount && selectedScope.serviceAccountCount > 0 && (
              <>
                <br />
                <Typography color="error" sx={{ mt: 1 }}>
                  This scope is assigned to {selectedScope.serviceAccountCount} service account(s) and cannot be deleted.
                </Typography>
              </>
            )}
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)}>Cancel</Button>
          <Button
            onClick={handleDeleteScope}
            color="error"
            variant="contained"
            disabled={(selectedScope?.serviceAccountCount ?? 0) > 0}
          >
            Delete
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Scopes;
