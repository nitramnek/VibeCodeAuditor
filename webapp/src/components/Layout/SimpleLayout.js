import React from 'react';
import { useLocation } from 'react-router-dom';

const SimpleLayout = ({ children }) => {
  const location = useLocation();
  
  // Don't show layout for auth pages
  const isAuthRoute = ['/login', '/signup'].includes(location.pathname);
  
  if (isAuthRoute) {
    return <div className="min-h-screen bg-gray-50">{children}</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Simple Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <h1 className="text-xl font-bold text-gray-900">🛡️ VibeCodeAuditor</h1>
            <div className="text-sm text-gray-600">Enterprise Security Platform</div>
          </div>
        </div>
      </header>
      
      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>
    </div>
  );
};

export default SimpleLayout;