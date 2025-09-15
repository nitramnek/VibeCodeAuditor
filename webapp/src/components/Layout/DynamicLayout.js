import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import OptimizedTopBar from './OptimizedTopBar';
import DynamicSideBar from './DynamicSideBar';
import MobileSideBar from './MobileSideBar';

const DynamicLayout = ({ children }) => {
  const [sidebarState, setSidebarState] = useState('expanded'); // expanded, collapsed, hidden, mobile
  const [isMobile, setIsMobile] = useState(false);
  const [isTablet, setIsTablet] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const location = useLocation();

  // Responsive breakpoints
  const MOBILE_BREAKPOINT = 768;
  const TABLET_BREAKPOINT = 1024;
  const DESKTOP_BREAKPOINT = 1280;

  // Check if current route requires authentication
  const isAuthRoute = ['/login', '/signup'].includes(location.pathname);

  // Handle responsive behavior with dynamic sidebar states
  useEffect(() => {
    const handleResize = () => {
      const width = window.innerWidth;
      
      if (width < MOBILE_BREAKPOINT) {
        // Mobile: Hide sidebar, use mobile menu
        setIsMobile(true);
        setIsTablet(false);
        setSidebarState('hidden');
      } else if (width < TABLET_BREAKPOINT) {
        // Tablet: Collapsed sidebar with icons
        setIsMobile(false);
        setIsTablet(true);
        setSidebarState('collapsed');
      } else if (width < DESKTOP_BREAKPOINT) {
        // Small desktop: Collapsed by default, expandable
        setIsMobile(false);
        setIsTablet(false);
        setSidebarState('collapsed');
      } else {
        // Large desktop: Expanded sidebar
        setIsMobile(false);
        setIsTablet(false);
        setSidebarState('expanded');
      }
      
      // Close mobile menu on resize
      if (width >= MOBILE_BREAKPOINT) {
        setMobileMenuOpen(false);
      }
    };

    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Close mobile menu on route change
  useEffect(() => {
    setMobileMenuOpen(false);
  }, [location.pathname]);

  // Toggle sidebar state (for desktop/tablet)
  const toggleSidebar = () => {
    if (isMobile) {
      setMobileMenuOpen(!mobileMenuOpen);
    } else {
      setSidebarState(prev => 
        prev === 'expanded' ? 'collapsed' : 'expanded'
      );
    }
  };

  // Don't show layout for auth pages
  if (isAuthRoute) {
    return <div className="min-h-screen bg-gray-50">{children}</div>;
  }

  // Calculate sidebar width based on state
  const getSidebarWidth = () => {
    switch (sidebarState) {
      case 'expanded': return 'w-64';
      case 'collapsed': return 'w-16';
      case 'hidden': return 'w-0';
      default: return 'w-64';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex overflow-hidden">
      {/* Desktop/Tablet Sidebar */}
      {!isMobile && (
        <div className={`${getSidebarWidth()} transition-all duration-300 ease-in-out flex-shrink-0`}>
          <DynamicSideBar 
            state={sidebarState}
            onToggle={toggleSidebar}
            isTablet={isTablet}
          />
        </div>
      )}

      {/* Mobile Sidebar Overlay */}
      {isMobile && mobileMenuOpen && (
        <>
          {/* Backdrop */}
          <div 
            className="fixed inset-0 z-40 bg-gray-600 bg-opacity-75 transition-opacity lg:hidden"
            onClick={() => setMobileMenuOpen(false)}
          />
          
          {/* Mobile Sidebar */}
          <div className="fixed inset-y-0 left-0 z-50 w-64 bg-white transform transition-transform lg:hidden">
            <MobileSideBar onClose={() => setMobileMenuOpen(false)} />
          </div>
        </>
      )}

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Optimized Top Bar */}
        <OptimizedTopBar 
          onMenuClick={toggleSidebar}
          isMobile={isMobile}
          sidebarState={sidebarState}
        />

        {/* Main Content */}
        <main className="flex-1 relative overflow-y-auto focus:outline-none scrollbar-thin">
          <div className="py-6">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              {children}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

export default DynamicLayout;