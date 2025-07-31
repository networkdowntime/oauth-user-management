import React, { createContext, useContext, useState, useCallback, useEffect, ReactNode } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

interface BreadcrumbItem {
  path: string;
  label: string;
  timestamp: number;
}

interface NavigationContextType {
  breadcrumbs: BreadcrumbItem[];
  addBreadcrumb: (path: string, label: string) => void;
  setCurrentPageInfo: (path: string, label: string) => void;
  goBack: () => void;
  getBackLabel: () => string;
  canGoBack: () => boolean;
  clearBreadcrumbs: () => void;
  removeCurrentPageFromBreadcrumbs: (currentPath: string) => void;
}

const NavigationContext = createContext<NavigationContextType | undefined>(undefined);

export const useNavigation = () => {
  const context = useContext(NavigationContext);
  if (!context) {
    throw new Error('useNavigation must be used within a NavigationProvider');
  }
  return context;
};

interface NavigationProviderProps {
  children: ReactNode;
}

export const NavigationProvider: React.FC<NavigationProviderProps> = ({ children }) => {
  const [breadcrumbs, setBreadcrumbs] = useState<BreadcrumbItem[]>([]);
  const [currentPage, setCurrentPage] = useState<{ path: string; label: string } | null>(null);
  const [isNavigatingBack, setIsNavigatingBack] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  const addBreadcrumb = useCallback((path: string, label: string) => {
    setBreadcrumbs(prev => {
      // Don't add if it's the same as the current path
      if (prev.length > 0 && prev[prev.length - 1].path === path) {
        return prev;
      }

      // Remove any existing breadcrumb with the same path to avoid loops
      const filtered = prev.filter(item => item.path !== path);
      
      // Add the new breadcrumb
      const newBreadcrumb: BreadcrumbItem = {
        path,
        label,
        timestamp: Date.now(),
      };

      // Keep only the last 10 breadcrumbs to prevent memory issues
      const updated = [...filtered, newBreadcrumb].slice(-10);
      
      return updated;
    });
  }, []);

  const setCurrentPageInfo = useCallback((path: string, label: string) => {
    setCurrentPage({ path, label });
  }, []);

  // Track navigation changes to add previous page to breadcrumbs
  useEffect(() => {
    // If we have a current page and the location has changed, add the previous page to breadcrumbs
    // But only if we're not navigating back (which would be redundant)
    if (currentPage && currentPage.path !== location.pathname && !isNavigatingBack) {
      addBreadcrumb(currentPage.path, currentPage.label);
    }
    
    // Reset the navigating back flag after processing
    if (isNavigatingBack) {
      setIsNavigatingBack(false);
    }
  }, [location.pathname, currentPage, isNavigatingBack, addBreadcrumb]);

  const goBack = useCallback(() => {
    if (breadcrumbs.length > 0) {
      const lastBreadcrumb = breadcrumbs[breadcrumbs.length - 1];
      
      // Set flag to indicate we're navigating back
      setIsNavigatingBack(true);
      
      // Remove the current breadcrumb before navigating
      setBreadcrumbs(prev => prev.slice(0, -1));
      
      navigate(lastBreadcrumb.path);
    } else {
      // Fallback to browser back if no breadcrumbs
      window.history.back();
    }
  }, [breadcrumbs, navigate]);

  const getBackLabel = useCallback(() => {
    if (breadcrumbs.length > 0) {
      return `Back to ${breadcrumbs[breadcrumbs.length - 1].label}`;
    }
    return 'Back';
  }, [breadcrumbs]);

  const canGoBack = useCallback(() => {
    return breadcrumbs.length > 0 || window.history.length > 1;
  }, [breadcrumbs]);

  const clearBreadcrumbs = useCallback(() => {
    setBreadcrumbs([]);
  }, []);

  const removeCurrentPageFromBreadcrumbs = useCallback((currentPath: string) => {
    setBreadcrumbs(prev => {
      // If the most recent breadcrumb is for the current page, remove it
      if (prev.length > 0 && prev[prev.length - 1].path === currentPath) {
        return prev.slice(0, -1);
      }
      return prev;
    });
  }, []);

  const value: NavigationContextType = {
    breadcrumbs,
    addBreadcrumb,
    setCurrentPageInfo,
    goBack,
    getBackLabel,
    canGoBack,
    clearBreadcrumbs,
    removeCurrentPageFromBreadcrumbs,
  };

  return (
    <NavigationContext.Provider value={value}>
      {children}
    </NavigationContext.Provider>
  );
};
