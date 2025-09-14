import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  Shield, 
  Menu, 
  Search, 
  Bell, 
  Settings, 
  User, 
  LogOut, 
  ChevronDown,
  Sun,
  Globe,
  X,
  Command
} from 'lucide-react';
import { useAuth } from '../../contexts/AuthContext';

const DynamicTopBar = ({ onMenuClick, isMobile, sidebarState }) => {
  const [searchOpen, setSearchOpen] = useState(false);
  const [profileOpen, setProfileOpen] = useState(false);
  const [notificationsOpen, setNotificationsOpen] = useState(false);
  const [mobileSearchOpen, setMobileSearchOpen] = useState(false);
  const { user, signOut, isSupabaseEnabled } = useAuth();
  const navigate = useNavigate();

  const handleSignOut = async () => {
    await signOut();
    navigate('/login');
  };

  const notifications = [
    { id: 1, title: 'Scan completed', message: 'Your security scan has finished', time: '2 min ago', unread: true },
    { id: 2, title: 'New vulnerability detected', message: 'Critical issue found in authentication module', time: '1 hour ago', unread: true },
    { id: 3, title: 'Compliance report ready', message: 'ISO 27001 compliance report is available', time: '3 hours ago', unread: false },
  ];

  const unreadCount = notifications.filter(n => n.unread).length;

  // Close dropdowns when clicking outside
  React.useEffect(() => {
    const handleClickOutside = (event) => {
      if (!event.target.closest('.dropdown-container')) {
        setSearchOpen(false);
        setProfileOpen(false);
        setNotificationsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <>
      <header className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-30">
        <div className="flex items-center justify-between h-16 px-4 sm:px-6 lg:px-8">
          {/* Left Section */}
          <div className="flex items-center space-x-4">
            {/* Menu Button */}
            <button
              onClick={onMenuClick}
              className="p-2 rounded-md text-gray-600 hover:text-gray-900 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors"
              aria-label={isMobile ? "Open mobile menu" : "Toggle sidebar"}
            >
              <Menu className="h-6 w-6" />
            </button>

            {/* Logo - Show on mobile or when sidebar is collapsed */}
            {(isMobile || sidebarState === 'collapsed') && (
              <Link to="/dashboard" className="flex items-center space-x-3">
                <div className="flex items-center justify-center w-10 h-10 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg">
                  <Shield className="h-6 w-6 text-white" />
                </div>
                <div className="hidden sm:block">
                  <h1 className="text-xl font-bold text-gray-900">VibeCodeAuditor</h1>
                  <p className="text-xs text-gray-500">Enterprise Security Platform</p>
                </div>
              </Link>
            )}

            {/* Breadcrumb for mobile */}
            {isMobile && (
              <div className="hidden sm:flex items-center space-x-2 text-sm text-gray-500">
                <span>/</span>
                <span className="text-gray-900 font-medium">Dashboard</span>
              </div>
            )}
          </div>

          {/* Center Section - Search (Desktop) */}
          <div className="flex-1 max-w-2xl mx-4 hidden md:block">
            <div className="relative dropdown-container">
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Search className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  type="text"
                  placeholder="Search scans, issues, or compliance frameworks..."
                  className="block w-full pl-10 pr-10 py-2 border border-gray-300 rounded-lg leading-5 bg-gray-50 placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 focus:bg-white sm:text-sm transition-all duration-200"
                  onFocus={() => setSearchOpen(true)}
                />
                <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                  <kbd className="inline-flex items-center px-2 py-1 border border-gray-200 rounded text-xs font-sans font-medium text-gray-400">
                    <Command className="h-3 w-3 mr-1" />
                    K
                  </kbd>
                </div>
              </div>
              
              {/* Search Dropdown */}
              {searchOpen && (
                <div className="absolute top-full left-0 right-0 mt-1 bg-white rounded-lg shadow-lg border border-gray-200 py-2 z-50 animate-fade-in">
                  <div className="px-4 py-2 text-xs font-medium text-gray-500 uppercase tracking-wide border-b border-gray-100">
                    Recent Searches
                  </div>
                  <div className="max-h-64 overflow-y-auto">
                    <div className="px-4 py-3 hover:bg-gray-50 cursor-pointer transition-colors">
                      <div className="flex items-center space-x-3">
                        <Search className="h-4 w-4 text-gray-400" />
                        <div>
                          <div className="text-sm text-gray-900">SQL Injection vulnerabilities</div>
                          <div className="text-xs text-gray-500">in authentication module</div>
                        </div>
                      </div>
                    </div>
                    <div className="px-4 py-3 hover:bg-gray-50 cursor-pointer transition-colors">
                      <div className="flex items-center space-x-3">
                        <Search className="h-4 w-4 text-gray-400" />
                        <div>
                          <div className="text-sm text-gray-900">OWASP Top 10 compliance</div>
                          <div className="text-xs text-gray-500">security standards</div>
                        </div>
                      </div>
                    </div>
                    <div className="px-4 py-3 hover:bg-gray-50 cursor-pointer transition-colors">
                      <div className="flex items-center space-x-3">
                        <Search className="h-4 w-4 text-gray-400" />
                        <div>
                          <div className="text-sm text-gray-900">Critical security issues</div>
                          <div className="text-xs text-gray-500">last 30 days</div>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div className="px-4 py-2 border-t border-gray-100">
                    <button className="text-sm text-blue-600 hover:text-blue-800 font-medium">
                      Advanced search
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Right Section */}
          <div className="flex items-center space-x-1 sm:space-x-2">
            {/* Mobile Search */}
            <button 
              onClick={() => setMobileSearchOpen(true)}
              className="p-2 rounded-md text-gray-600 hover:text-gray-900 hover:bg-gray-100 md:hidden transition-colors"
            >
              <Search className="h-5 w-5" />
            </button>

            {/* Theme Toggle */}
            <button className="p-2 rounded-md text-gray-600 hover:text-gray-900 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors">
              <Sun className="h-5 w-5" />
            </button>

            {/* Notifications */}
            <div className="relative dropdown-container">
              <button
                onClick={() => setNotificationsOpen(!notificationsOpen)}
                className="p-2 rounded-md text-gray-600 hover:text-gray-900 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 relative transition-colors"
              >
                <Bell className="h-5 w-5" />
                {unreadCount > 0 && (
                  <span className="absolute -top-1 -right-1 h-4 w-4 bg-red-500 text-white text-xs rounded-full flex items-center justify-center animate-pulse">
                    {unreadCount}
                  </span>
                )}
              </button>

              {/* Notifications Dropdown */}
              {notificationsOpen && (
                <div className="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-lg border border-gray-200 py-2 z-50 animate-fade-in">
                  <div className="px-4 py-3 border-b border-gray-200">
                    <div className="flex items-center justify-between">
                      <h3 className="text-sm font-medium text-gray-900">Notifications</h3>
                      <div className="flex items-center space-x-2">
                        <span className="text-xs text-gray-500">{unreadCount} unread</span>
                        <button className="text-xs text-blue-600 hover:text-blue-800 font-medium">
                          Mark all read
                        </button>
                      </div>
                    </div>
                  </div>
                  <div className="max-h-64 overflow-y-auto scrollbar-thin">
                    {notifications.map((notification) => (
                      <div
                        key={notification.id}
                        className={`px-4 py-3 hover:bg-gray-50 cursor-pointer border-l-4 transition-colors ${
                          notification.unread ? 'border-blue-500 bg-blue-50' : 'border-transparent'
                        }`}
                      >
                        <div className="flex items-start space-x-3">
                          <div className="flex-1 min-w-0">
                            <p className="text-sm font-medium text-gray-900">{notification.title}</p>
                            <p className="text-sm text-gray-500 truncate">{notification.message}</p>
                            <p className="text-xs text-gray-400 mt-1">{notification.time}</p>
                          </div>
                          {notification.unread && (
                            <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 animate-pulse"></div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                  <div className="px-4 py-2 border-t border-gray-200">
                    <button className="text-sm text-blue-600 hover:text-blue-800 font-medium">
                      View all notifications
                    </button>
                  </div>
                </div>
              )}
            </div>

            {/* User Profile */}
            <div className="relative dropdown-container">
              <button
                onClick={() => setProfileOpen(!profileOpen)}
                className="flex items-center space-x-2 p-2 rounded-md text-gray-600 hover:text-gray-900 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors"
              >
                <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                  <User className="h-4 w-4 text-white" />
                </div>
                <div className="hidden sm:block text-left">
                  <div className="text-sm font-medium text-gray-900">
                    {isSupabaseEnabled && user ? user.email?.split('@')[0] : 'Demo User'}
                  </div>
                  <div className="text-xs text-gray-500">Security Admin</div>
                </div>
                <ChevronDown className="h-4 w-4 text-gray-400 hidden sm:block" />
              </button>

              {/* Profile Dropdown */}
              {profileOpen && (
                <div className="absolute right-0 mt-2 w-56 bg-white rounded-lg shadow-lg border border-gray-200 py-2 z-50 animate-fade-in">
                  <div className="px-4 py-3 border-b border-gray-200">
                    <div className="text-sm font-medium text-gray-900">
                      {isSupabaseEnabled && user ? user.email : 'demo@vibeauditor.com'}
                    </div>
                    <div className="text-xs text-gray-500">Security Administrator</div>
                  </div>
                  
                  <div className="py-1">
                    <Link
                      to="/profile"
                      className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors"
                    >
                      <User className="h-4 w-4 mr-3" />
                      Your Profile
                    </Link>
                    <Link
                      to="/settings"
                      className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors"
                    >
                      <Settings className="h-4 w-4 mr-3" />
                      Settings
                    </Link>
                    <button className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors">
                      <Globe className="h-4 w-4 mr-3" />
                      Language
                    </button>
                  </div>
                  
                  {isSupabaseEnabled && (
                    <div className="border-t border-gray-200 py-1">
                      <button
                        onClick={handleSignOut}
                        className="flex items-center w-full px-4 py-2 text-sm text-red-700 hover:bg-red-50 transition-colors"
                      >
                        <LogOut className="h-4 w-4 mr-3" />
                        Sign Out
                      </button>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Mobile Search Overlay */}
      {mobileSearchOpen && (
        <div className="fixed inset-0 z-50 bg-white md:hidden">
          <div className="flex items-center h-16 px-4 border-b border-gray-200">
            <div className="flex-1 flex items-center space-x-3">
              <Search className="h-5 w-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search scans, issues, compliance..."
                className="flex-1 text-lg placeholder-gray-500 focus:outline-none"
                autoFocus
              />
            </div>
            <button
              onClick={() => setMobileSearchOpen(false)}
              className="p-2 text-gray-400 hover:text-gray-600"
            >
              <X className="h-6 w-6" />
            </button>
          </div>
          
          <div className="p-4">
            <div className="text-sm font-medium text-gray-500 mb-3">Recent Searches</div>
            <div className="space-y-3">
              <div className="flex items-center space-x-3 p-3 rounded-lg hover:bg-gray-50">
                <Search className="h-4 w-4 text-gray-400" />
                <div>
                  <div className="text-sm text-gray-900">SQL Injection vulnerabilities</div>
                  <div className="text-xs text-gray-500">in authentication module</div>
                </div>
              </div>
              <div className="flex items-center space-x-3 p-3 rounded-lg hover:bg-gray-50">
                <Search className="h-4 w-4 text-gray-400" />
                <div>
                  <div className="text-sm text-gray-900">OWASP Top 10 compliance</div>
                  <div className="text-xs text-gray-500">security standards</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default DynamicTopBar;