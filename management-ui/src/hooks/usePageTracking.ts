import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { useNavigation } from '../contexts/NavigationContext';

interface UsePageTrackingOptions {
  pageLabel: string;
  shouldTrack?: boolean;
}

export const usePageTracking = ({ pageLabel, shouldTrack = true }: UsePageTrackingOptions) => {
  const { setCurrentPageInfo } = useNavigation();
  const location = useLocation();

  useEffect(() => {
    if (shouldTrack) {
      // Set the current page info so it can be added to breadcrumbs when navigating away
      setCurrentPageInfo(location.pathname, pageLabel);
    }
  }, [location.pathname, pageLabel, shouldTrack, setCurrentPageInfo]);
};
