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
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Visibility as ViewIcon,
  Security as SecurityIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useRoles, useCreateRole, useDeleteRole, type CreateRoleRequest } from '../services/hooks';

const Roles: React.FC = () => {
  const navigate = useNavigate();
  const { data: roles, isLoading, error } = useRoles();
  const createRoleMutation = useCreateRole();
  const deleteRoleMutation = useDeleteRole();
  
  // Track this page for breadcrumb navigation
  usePageTracking({ pageLabel: 'Roles' });
  
  const [createDialogOpen, setCreateDialogOpen] = React.useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = React.useState(false);
  const [selectedRoleId, setSelectedRoleId] = React.useState<string | null>(null);
  const [newRole, setNewRole] = React.useState<CreateRoleRequest>({
    name: '',
    description: '',
  });

  const handleCreateRole = async () => {
    try {
      await createRoleMutation.mutateAsync(newRole);
      setCreateDialogOpen(false);
      setNewRole({
        name: '',
        description: '',
      });
    } catch (error) {
      console.error('Failed to create role:', error);
    }
  };

  const handleDeleteRole = async () => {
    if (selectedRoleId) {
      try {
        await deleteRoleMutation.mutateAsync(selectedRoleId);
        setDeleteDialogOpen(false);
        setSelectedRoleId(null);
      } catch (error) {
        console.error('Failed to delete role:', error);
      }
    }
  };

  const openDeleteDialog = (roleId: string) => {
    setSelectedRoleId(roleId);
    setDeleteDialogOpen(true);
  };

  const selectedRole = roles?.find(role => role.id === selectedRoleId);

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
        <Typography color="error">
          Error loading roles. Please try again later.
        </Typography>
      </Box>
    );
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" component="h1">
          Roles
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => setCreateDialogOpen(true)}
        >
          Add Role
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Description</TableCell>
              <TableCell>Users</TableCell>
              <TableCell>Created</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {roles?.map((role) => (
              <TableRow key={role.id}>
                <TableCell>
                  <Box display="flex" alignItems="center" gap={1}>
                    <SecurityIcon color="primary" />
                    <Typography variant="body2" fontWeight="medium">
                      {role.name}
                    </Typography>
                  </Box>
                </TableCell>
                <TableCell>{role.description || '-'}</TableCell>
                <TableCell>
                  <Chip
                    label={role.userCount || 0}
                    size="small"
                    color={role.userCount && role.userCount > 0 ? 'primary' : 'default'}
                  />
                </TableCell>
                <TableCell>
                  {new Date(role.createdAt).toLocaleDateString()}
                </TableCell>
                <TableCell>
                  <IconButton
                    size="small"
                    onClick={() => navigate(`/roles/${role.id}`)}
                    title="View Details"
                  >
                    <ViewIcon />
                  </IconButton>
                  <IconButton
                    size="small"
                    onClick={() => navigate(`/roles/${role.id}/edit`)}
                    title="Edit Role"
                  >
                    <EditIcon />
                  </IconButton>
                  <IconButton
                    size="small"
                    onClick={() => openDeleteDialog(role.id)}
                    title="Delete Role"
                    color="error"
                  >
                    <DeleteIcon />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Create Role Dialog */}
      <Dialog
        open={createDialogOpen}
        onClose={() => setCreateDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>
          <Box display="flex" alignItems="center" gap={1}>
            <SecurityIcon />
            Create New Role
          </Box>
        </DialogTitle>
        <DialogContent>
          <Box display="flex" flexDirection="column" gap={2} mt={1}>
            <TextField
              label="Role Name"
              fullWidth
              required
              value={newRole.name}
              onChange={(e) => setNewRole({ ...newRole, name: e.target.value })}
              helperText="Use lowercase and underscores (e.g., user_admin, read_only)"
            />
            <TextField
              label="Description"
              fullWidth
              multiline
              rows={3}
              value={newRole.description}
              onChange={(e) => setNewRole({ ...newRole, description: e.target.value })}
              helperText="Brief description of what this role allows"
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCreateDialogOpen(false)}>Cancel</Button>
          <Button
            variant="contained"
            onClick={handleCreateRole}
            disabled={!newRole.name || createRoleMutation.isPending}
          >
            {createRoleMutation.isPending ? 'Creating...' : 'Create Role'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Delete Role Dialog */}
      <Dialog
        open={deleteDialogOpen}
        onClose={() => setDeleteDialogOpen(false)}
      >
        <DialogTitle>Delete Role</DialogTitle>
        <DialogContent>
          <Typography>
            Are you sure you want to delete the role "{selectedRole?.name}"?
          </Typography>
          {selectedRole?.userCount && selectedRole.userCount > 0 && (
            <Typography color="warning.main" mt={1}>
              Warning: This role is currently assigned to {selectedRole.userCount} user(s).
              Deleting it will remove the role from all users.
            </Typography>
          )}
          <Typography variant="body2" color="text.secondary" mt={1}>
            This action cannot be undone.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)}>Cancel</Button>
          <Button
            variant="contained"
            color="error"
            onClick={handleDeleteRole}
            disabled={deleteRoleMutation.isPending}
          >
            {deleteRoleMutation.isPending ? 'Deleting...' : 'Delete'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Roles;
