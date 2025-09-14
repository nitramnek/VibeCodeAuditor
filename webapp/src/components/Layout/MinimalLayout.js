import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

const MinimalLayout = ({ children }) => {
  const [isMobile, setIsMobile] = useState(false);
  const location = useLocation();
  const { user, isSupabaseEnabled } = useAuth();

  // Check if current route requires authentication
  const isAuthRoute = ['/login', '/signup'].includes(location.pathname);

  // Handle responsive behavior
  useEffect(() => {
    const checkScreenSize = () => {
      const mobile = window.innerWidth < 1024;
      setIsMobile(mobile);
    };

    checkScreenSize();
    window.addEventListener('resize', checkScreenSize);
    return () => window.removeEventListener('resize', checkScreenSize);
  }, []);

  // Don't show layout for auth pages
  if (isAuthRoute) {
    return <div className="min-h-screen bg-gray-50">{children}</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Desktop Sidebar */}
      <div className="hidden lg:flex lg:flex-shrink-0">
        <div className="flex flex-col w-64 bg-white border-r border-gray-200">
          <div className="flex items-center justify-center h-16 px-4 border-b border-gray-200">
            <h2 className="text-lg font-bold text-gray-900">VibeCodeAuditor</h2>
          </div>
          <div className="flex-1 p-4">
            <nav className="space-y-2">
              <div className="px-3 py-2 text-sm font-medium text-gray-900 bg-blue-50 rounded-md">
                Dashboard
              </div>
              <div className="px-3 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md">
                Scanner
              </div>
              <div className="px-3 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md">
                Results
              </div>
            </nav>
          </div>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Bar */}
        <header className="bg-white shadow-sm border-b border-gray-200">
          <div className="flex items-center justify-between h-16 px-4 sm:px-6 lg:px-8">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold">V</span>
              </div>
              <div>
                <h1 className="text-lg font-bold text-gray-900">VibeCodeAuditor</h1>
                <p className="text-xs text-gray-500">Enterprise Security</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              {isSupabaseEnabled && user && (
                <div className="text-sm text-gray-700">{user.email}</div>
              )}
              <div className="w-8 h-8 bg-gray-300 rounded-full"></div>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="flex-1 relative overflow-y-auto focus:outline-none">
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

export default MinimalLayout;