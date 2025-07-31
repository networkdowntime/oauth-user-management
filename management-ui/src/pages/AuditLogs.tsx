import React from 'react';
import {
  Box,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  CircularProgress,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
} from '@mui/material';
import {
  Analytics as AnalyticsIcon,
} from '@mui/icons-material';
import { useAuditLogs } from '../services/hooks';

const AuditLogs: React.FC = () => {
  const [resourceType, setResourceType] = React.useState<string>('');
  const [resourceId, setResourceId] = React.useState<string>('');
  
  const { data: auditLogs, isLoading, error } = useAuditLogs(
    resourceType || undefined,
    resourceId || undefined
  );

  const getActionColor = (action: string) => {
    if (action.includes('delete') || action.includes('fail')) return 'error';
    if (action.includes('create') || action.includes('success')) return 'success';
    if (action.includes('update') || action.includes('modify')) return 'warning';
    return 'default';
  };

  const getActionIcon = (action: string) => {
    return <AnalyticsIcon fontSize="small" />;
  };

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
          Error loading audit logs. Please try again later.
        </Typography>
      </Box>
    );
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" component="h1">
          Audit Logs
        </Typography>
      </Box>

      {/* Filters */}
      <Box display="flex" gap={2} mb={3}>
        <FormControl size="small" sx={{ minWidth: 150 }}>
          <InputLabel>Resource Type</InputLabel>
          <Select
            value={resourceType}
            label="Resource Type"
            onChange={(e) => setResourceType(e.target.value)}
          >
            <MenuItem value="">All</MenuItem>
            <MenuItem value="user">User</MenuItem>
            <MenuItem value="auth">Authentication</MenuItem>
            <MenuItem value="role">Role</MenuItem>
            <MenuItem value="service">Service</MenuItem>
          </Select>
        </FormControl>
        <TextField
          size="small"
          label="Resource ID"
          value={resourceId}
          onChange={(e) => setResourceId(e.target.value)}
          sx={{ minWidth: 200 }}
          placeholder="Filter by specific resource ID"
        />
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Timestamp</TableCell>
              <TableCell>Action</TableCell>
              <TableCell>Resource</TableCell>
              <TableCell>Performed By</TableCell>
              <TableCell>IP Address</TableCell>
              <TableCell>Details</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {auditLogs?.map((log) => (
              <TableRow key={log.id}>
                <TableCell>
                  <Typography variant="body2">
                    {new Date(log.timestamp).toLocaleString()}
                  </Typography>
                </TableCell>
                <TableCell>
                  <Box display="flex" alignItems="center" gap={1}>
                    {getActionIcon(log.action)}
                    <Chip
                      label={log.action}
                      size="small"
                      color={getActionColor(log.action)}
                    />
                  </Box>
                </TableCell>
                <TableCell>
                  <Box>
                    <Typography variant="body2" fontWeight="medium">
                      {log.resourceType}
                    </Typography>
                    {log.resourceId && (
                      <Typography variant="caption" color="text.secondary">
                        ID: {log.resourceId}
                      </Typography>
                    )}
                  </Box>
                </TableCell>
                <TableCell>{log.performedBy}</TableCell>
                <TableCell>
                  <Typography variant="body2" fontFamily="monospace">
                    {log.ipAddress || '-'}
                  </Typography>
                </TableCell>
                <TableCell>
                  {log.details ? (
                    <Box>
                      {Object.entries(log.details).map(([key, value]) => (
                        <Typography key={key} variant="caption" display="block">
                          <strong>{key}:</strong> {String(value)}
                        </Typography>
                      ))}
                    </Box>
                  ) : (
                    '-'
                  )}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {auditLogs && auditLogs.length === 0 && (
        <Box textAlign="center" py={4}>
          <Typography color="text.secondary">
            No audit logs found matching the current filters.
          </Typography>
        </Box>
      )}
    </Box>
  );
};

export default AuditLogs;
