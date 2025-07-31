import React from 'react';
import {
  AppBar,
  Box,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Typography,
  IconButton,
  useTheme,
  useMediaQuery,
  Button,
  Divider,
  Alert,
  Snackbar,
  CircularProgress,
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  People as PeopleIcon,
  Settings as SettingsIcon,
  Security as SecurityIcon,
  Menu as MenuIcon,
  Analytics as AnalyticsIcon,
  Api as ApiIcon,
  Sync as SyncIcon,
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';
import { useNavigation } from '../../contexts/NavigationContext';
import { api } from '../../services/api';

const drawerWidth = 240;

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const [mobileOpen, setMobileOpen] = React.useState(false);
  const [isSyncing, setIsSyncing] = React.useState(false);
  const [syncResult, setSyncResult] = React.useState<{
    success: boolean;
    message: string;
  } | null>(null);
  const navigate = useNavigate();
  const location = useLocation();
  const { clearBreadcrumbs } = useNavigation();

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const handleSyncHydra = async () => {
    setIsSyncing(true);
    setSyncResult(null);
    
    try {
      const result = await api.syncHydra();
      
      if (result.success) {
        const summary = result.summary;
        const totalChanges = summary.clients_created + summary.clients_updated + summary.clients_deleted;
        
        if (totalChanges === 0) {
          setSyncResult({
            success: true,
            message: 'Hydra is already in sync with the database'
          });
        } else {
          setSyncResult({
            success: true,
            message: `Sync completed: ${summary.clients_created} created, ${summary.clients_updated} updated, ${summary.clients_deleted} deleted`
          });
        }
      } else {
        setSyncResult({
          success: false,
          message: `Sync completed with errors: ${result.details.errors.join(', ')}`
        });
      }
    } catch (error) {
      setSyncResult({
        success: false,
        message: `Sync failed: ${error instanceof Error ? error.message : 'Unknown error'}`
      });
    } finally {
      setIsSyncing(false);
    }
  };

  const menuItems = [
    {
      text: 'Dashboard',
      icon: <DashboardIcon />,
      path: '/',
    },
    {
      text: 'Users',
      icon: <PeopleIcon />,
      path: '/users',
    },
    {
      text: 'Service Accounts',
      icon: <SettingsIcon />,
      path: '/service-accounts',
    },
    {
      text: 'Roles',
      icon: <SecurityIcon />,
      path: '/roles',
    },
    {
      text: 'Scopes',
      icon: <ApiIcon />,
      path: '/scopes',
    },
    {
      text: 'Audit Logs',
      icon: <AnalyticsIcon />,
      path: '/audit-logs',
    },
  ];

  const drawer = (
    <div>
      <Toolbar>
        <Typography variant="h6" noWrap component="div">
          OAuth Manager
        </Typography>
      </Toolbar>
      <List>
        {menuItems.map((item) => (
          <ListItem key={item.text} disablePadding>
            <ListItemButton
              selected={location.pathname === item.path}
              onClick={() => {
                clearBreadcrumbs(); // Clear breadcrumbs when navigating via menu
                navigate(item.path);
                if (isMobile) {
                  setMobileOpen(false);
                }
              }}
            >
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText primary={item.text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
      
      {/* Resync Hydra Button */}
      <Box sx={{ position: 'absolute', bottom: 16, left: 16, right: 16 }}>
        <Divider sx={{ mb: 2 }} />
        <Button
          variant="outlined"
          fullWidth
          startIcon={isSyncing ? <CircularProgress size={20} /> : <SyncIcon />}
          onClick={handleSyncHydra}
          disabled={isSyncing}
          sx={{
            textTransform: 'none',
            fontSize: '0.875rem',
          }}
        >
          {isSyncing ? 'Syncing...' : 'Resync Hydra'}
        </Button>
      </Box>
    </div>
  );

  return (
    <Box sx={{ display: 'flex' }}>
      <AppBar
        position="fixed"
        sx={{
          width: { md: `calc(100% - ${drawerWidth}px)` },
          ml: { md: `${drawerWidth}px` },
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { md: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div">
            OAuth User Management
          </Typography>
        </Toolbar>
      </AppBar>
      
      <Box
        component="nav"
        sx={{ width: { md: drawerWidth }, flexShrink: { md: 0 } }}
      >
        {/* Mobile drawer */}
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true, // Better open performance on mobile
          }}
          sx={{
            display: { xs: 'block', md: 'none' },
            '& .MuiDrawer-paper': {
              boxSizing: 'border-box',
              width: drawerWidth,
            },
          }}
        >
          {drawer}
        </Drawer>
        
        {/* Desktop drawer */}
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', md: 'block' },
            '& .MuiDrawer-paper': {
              boxSizing: 'border-box',
              width: drawerWidth,
            },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>
      
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { md: `calc(100% - ${drawerWidth}px)` },
        }}
      >
        <Toolbar />
        {children}
      </Box>
      
      {/* Sync Result Snackbar */}
      <Snackbar
        open={syncResult !== null}
        autoHideDuration={6000}
        onClose={() => setSyncResult(null)}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert
          onClose={() => setSyncResult(null)}
          severity={syncResult?.success ? 'success' : 'error'}
          sx={{ width: '100%' }}
        >
          {syncResult?.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default Layout;
