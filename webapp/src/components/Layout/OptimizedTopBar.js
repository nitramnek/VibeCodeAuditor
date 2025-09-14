import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
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
  Moon,
  Globe,
  X,
  Command,
  Clock,
  AlertTriangle,
  CheckCircle,
  Zap,
  HelpCircle,
  Bookmark,
  ArrowRight,
  Wifi,
  WifiOff,
  LayoutDashboard
} from 'lucide-react';
import { useAuth } from '../../contexts/AuthContext';

const OptimizedTopBar = ({ onMenuClick, isMobile, sidebarState }) => {
  // State management
  const [searchOpen, setSearchOpen] = useState(false);
  const [profileOpen, setProfileOpen] = useState(false);
  const [notificationsOpen, setNotificationsOpen] = useState(false);
  const [mobileSearchOpen, setMobileSearchOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const [currentTime, setCurrentTime] = useState(new Date());
  const [darkMode, setDarkMode] = useState(false);
  const [searchLoading, setSearchLoading] = useState(false);

  // Refs
  const searchInputRef = useRef(null);
  const mobileSearchInputRef = useRef(null);
  const searchDropdownRef = useRef(null);
  const notificationsRef = useRef(null);
  const profileRef = useRef(null);

  // Hooks
  const { user, signOut, isSupabaseEnabled } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  // Mock data for realistic experience
  const notifications = [
    { 
      id: 1, 
      title: 'Critical vulnerability detected', 
      message: 'SQL injection found in user authentication module', 
      time: '2 min ago', 
      unread: true,
      type: 'critical',
      icon: AlertTriangle,
      color: 'text-red-600 bg-red-100'
    },
    { 
      id: 2, 
      title: 'Scan completed successfully', 
      message: 'Security scan for project "E-commerce API" finished', 
      time: '15 min ago', 
      unread: true,
      type: 'success',
      icon: CheckCircle,
      color: 'text-green-600 bg-green-100'
    },
    { 
      id: 3, 
      title: 'Compliance report ready', 
      message: 'ISO 27001 compliance report is available for download', 
      time: '1 hour ago', 
      unread: false,
      type: 'info',
      icon: Shield,
      color: 'text-blue-600 bg-blue-100'
    },
    { 
      id: 4, 
      title: 'Team member added', 
      message: 'Sarah Johnson joined your security team', 
      time: '3 hours ago', 
      unread: false,
      type: 'info',
      icon: User,
      color: 'text-purple-600 bg-purple-100'
    }
  ];

  const searchSuggestions = [
    { type: 'recent', title: 'SQL injection vulnerabilities', subtitle: 'in authentication module', icon: Search },
    { type: 'recent', title: 'OWASP Top 10 compliance', subtitle: 'security standards', icon: Search },
    { type: 'recent', title: 'Critical security issues', subtitle: 'last 30 days', icon: Search },
    { type: 'shortcut', title: 'New Security Scan', subtitle: 'Ctrl+N', icon: Zap },
    { type: 'shortcut', title: 'View Dashboard', subtitle: 'Ctrl+D', icon: LayoutDashboard },
    { type: 'shortcut', title: 'Compliance Report', subtitle: 'Ctrl+R', icon: Shield }
  ];

  const unreadCount = notifications.filter(n => n.unread).length;

  // Get current page title for breadcrumb
  const getPageTitle = () => {
    const path = location.pathname;
    const titles = {
      '/dashboard': 'Dashboard',
      '/scanner': 'Security Scanner',
      '/results': 'Scan Results',
      '/compliance': 'Compliance',
      '/analytics': 'Analytics',
      '/history': 'Scan History',
      '/rules': 'Security Rules',
      '/team': 'Team Management',
      '/integrations': 'Integrations',
      '/settings': 'Settings'
    };
    return titles[path] || 'Dashboard';
  };

  // Handle sign out
  const handleSignOut = async () => {
    try {
      await signOut();
      navigate('/login');
    } catch (error) {
      console.error('Sign out error:', error);
    }
  };

  // Search functionality
  const handleSearch = useCallback(async (query) => {
    if (!query.trim()) {
      setSearchResults([]);
      return;
    }

    setSearchLoading(true);
    
    // Simulate API call
    setTimeout(() => {
      const filtered = searchSuggestions.filter(item => 
        item.title.toLowerCase().includes(query.toLowerCase()) ||
        item.subtitle.toLowerCase().includes(query.toLowerCase())
      );
      setSearchResults(filtered);
      setSearchLoading(false);
    }, 300);
  }, []);

  // Debounced search
  useEffect(() => {
    const timer = setTimeout(() => {
      handleSearch(searchQuery);
    }, 300);

    return () => clearTimeout(timer);
  }, [searchQuery, handleSearch]);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e) => {
      // CMD/Ctrl + K for search
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        if (isMobile) {
          setMobileSearchOpen(true);
        } else {
          searchInputRef.current?.focus();
          setSearchOpen(true);
        }
      }
      
      // Escape to close dropdowns
      if (e.key === 'Escape') {
        setSearchOpen(false);
        setProfileOpen(false);
        setNotificationsOpen(false);
        setMobileSearchOpen(false);
      }

      // CMD/Ctrl + N for new scan
      if ((e.metaKey || e.ctrlKey) && e.key === 'n') {
        e.preventDefault();
        navigate('/scanner');
      }

      // CMD/Ctrl + D for dashboard
      if ((e.metaKey || e.ctrlKey) && e.key === 'd') {
        e.preventDefault();
        navigate('/dashboard');
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isMobile, navigate]);

  // Online/offline detection
  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  // Update time every minute
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 60000);

    return () => clearInterval(timer);
  }, []);

  // Click outside to close dropdowns
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (searchDropdownRef.current && !searchDropdownRef.current.contains(event.target)) {
        setSearchOpen(false);
      }
      if (notificationsRef.current && !notificationsRef.current.contains(event.target)) {
        setNotificationsOpen(false);
      }
      if (profileRef.current && !profileRef.current.contains(event.target)) {
        setProfileOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Focus mobile search input when opened
  useEffect(() => {
    if (mobileSearchOpen && mobileSearchInputRef.current) {
      mobileSearchInputRef.current.focus();
    }
  }, [mobileSearchOpen]);

  // Mark notification as read
  const markAsRead = (notificationId) => {
    // In real app, this would update the backend
    console.log('Marking notification as read:', notificationId);
  };

  // Toggle dark mode
  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
    // In real app, this would persist to localStorage and apply theme
    document.documentElement.classList.toggle('dark');
  };

  return (
    <>
      <header className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-30 backdrop-blur-sm bg-white/95">
        <div className="flex items-center justify-between h-16 px-4 sm:px-6 lg:px-8">
          {/* Left Section */}
          <div className="flex items-center space-x-4">
            {/* Menu Button */}
            <button
              onClick={onMenuClick}
              className="p-2 rounded-lg text-gray-600 hover:text-gray-900 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all duration-200 active:scale-95"
              aria-label={isMobile ? "Open mobile menu" : "Toggle sidebar"}
            >
              <Menu className="h-6 w-6" />
            </button>

            {/* Logo & Breadcrumb */}
            <div className="flex items-center space-x-4">
              {/* Logo - Show on mobile or when sidebar is collapsed */}
              {(isMobile || sidebarState === 'collapsed') && (
                <Link to="/dashboard" className="flex items-center space-x-3 group">
                  <div className="flex items-center justify-center w-10 h-10 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg shadow-md group-hover:shadow-lg transition-all duration-200">
                    <Shield className="h-6 w-6 text-white" />
                  </div>
                  <div className="hidden sm:block">
                    <h1 className="text-xl font-bold text-gray-900 group-hover:text-blue-600 transition-colors">
                      VibeCodeAuditor
                    </h1>
                    <p className="text-xs text-gray-500">Enterprise Security Platform</p>
                  </div>
                </Link>
              )}

              {/* Breadcrumb */}
              {!isMobile && (
                <div className="hidden md:flex items-center space-x-2 text-sm">
                  <span className="text-gray-400">/</span>
                  <span className="text-gray-900 font-medium">{getPageTitle()}</span>
                  {location.pathname.includes('/results/') && (
                    <>
                      <span className="text-gray-400">/</span>
                      <span className="text-gray-600">Scan Results</span>
                    </>
                  )}
                </div>
              )}
            </div>
          </div>

          {/* Center Section - Search (Desktop) */}
          <div className="flex-1 max-w-2xl mx-4 hidden md:block" ref={searchDropdownRef}>
            <div className="relative">
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Search className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  ref={searchInputRef}
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search scans, issues, compliance frameworks..."
                  className="block w-full pl-10 pr-20 py-2.5 border border-gray-300 rounded-xl leading-5 bg-gray-50 placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 focus:bg-white sm:text-sm transition-all duration-200"
                  onFocus={() => setSearchOpen(true)}
                />
                <div className="absolute inset-y-0 right-0 pr-3 flex items-center space-x-2">
                  {searchLoading && (
                    <div className="animate-spin rounded-full h-4 w-4 border-2 border-blue-500 border-t-transparent"></div>
                  )}
                  <kbd className="hidden sm:inline-flex items-center px-2 py-1 border border-gray-200 rounded text-xs font-sans font-medium text-gray-400 bg-white">
                    <Command className="h-3 w-3 mr-1" />
                    K
                  </kbd>
                </div>
              </div>
              
              {/* Search Dropdown */}
              {searchOpen && (
                <div className="absolute top-full left-0 right-0 mt-2 bg-white rounded-xl shadow-lg border border-gray-200 py-2 z-50 animate-fade-in max-h-96 overflow-y-auto scrollbar-thin">
                  {searchQuery ? (
                    <>
                      {searchResults.length > 0 ? (
                        <>
                          <div className="px-4 py-2 text-xs font-medium text-gray-500 uppercase tracking-wide border-b border-gray-100">
                            Search Results
                          </div>
                          {searchResults.map((result, index) => {
                            const Icon = result.icon;
                            return (
                              <div key={index} className="px-4 py-3 hover:bg-gray-50 cursor-pointer transition-colors group">
                                <div className="flex items-center space-x-3">
                                  <Icon className="h-4 w-4 text-gray-400 group-hover:text-blue-500" />
                                  <div className="flex-1">
                                    <div className="text-sm text-gray-900 group-hover:text-blue-600">{result.title}</div>
                                    <div className="text-xs text-gray-500">{result.subtitle}</div>
                                  </div>
                                  <ArrowRight className="h-4 w-4 text-gray-300 group-hover:text-blue-500" />
                                </div>
                              </div>
                            );
                          })}
                        </>
                      ) : (
                        <div className="px-4 py-8 text-center">
                          <Search className="h-8 w-8 text-gray-300 mx-auto mb-2" />
                          <div className="text-sm text-gray-500">No results found for "{searchQuery}"</div>
                          <div className="text-xs text-gray-400 mt-1">Try different keywords or check spelling</div>
                        </div>
                      )}
                    </>
                  ) : (
                    <>
                      <div className="px-4 py-2 text-xs font-medium text-gray-500 uppercase tracking-wide border-b border-gray-100">
                        Recent Searches
                      </div>
                      {searchSuggestions.slice(0, 3).map((suggestion, index) => {
                        const Icon = suggestion.icon;
                        return (
                          <div key={index} className="px-4 py-3 hover:bg-gray-50 cursor-pointer transition-colors group">
                            <div className="flex items-center space-x-3">
                              <Icon className="h-4 w-4 text-gray-400 group-hover:text-blue-500" />
                              <div className="flex-1">
                                <div className="text-sm text-gray-900 group-hover:text-blue-600">{suggestion.title}</div>
                                <div className="text-xs text-gray-500">{suggestion.subtitle}</div>
                              </div>
                              <Clock className="h-3 w-3 text-gray-300" />
                            </div>
                          </div>
                        );
                      })}
                      
                      <div className="px-4 py-2 text-xs font-medium text-gray-500 uppercase tracking-wide border-t border-gray-100 mt-2">
                        Quick Actions
                      </div>
                      {searchSuggestions.slice(3).map((action, index) => {
                        const Icon = action.icon;
                        return (
                          <div key={index} className="px-4 py-3 hover:bg-gray-50 cursor-pointer transition-colors group">
                            <div className="flex items-center space-x-3">
                              <Icon className="h-4 w-4 text-gray-400 group-hover:text-blue-500" />
                              <div className="flex-1">
                                <div className="text-sm text-gray-900 group-hover:text-blue-600">{action.title}</div>
                                <div className="text-xs text-gray-500">{action.subtitle}</div>
                              </div>
                              <Zap className="h-3 w-3 text-gray-300 group-hover:text-blue-500" />
                            </div>
                          </div>
                        );
                      })}
                    </>
                  )}
                  
                  <div className="px-4 py-2 border-t border-gray-100 mt-2">
                    <button className="text-sm text-blue-600 hover:text-blue-800 font-medium flex items-center space-x-1">
                      <span>Advanced search</span>
                      <ArrowRight className="h-3 w-3" />
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Right Section */}
          <div className="flex items-center space-x-1 sm:space-x-2">
            {/* Connection Status */}
            <div className="hidden sm:flex items-center space-x-2 px-3 py-1 rounded-full bg-gray-100 text-xs">
              {isOnline ? (
                <>
                  <Wifi className="h-3 w-3 text-green-500" />
                  <span className="text-green-700">Online</span>
                </>
              ) : (
                <>
                  <WifiOff className="h-3 w-3 text-red-500" />
                  <span className="text-red-700">Offline</span>
                </>
              )}
            </div>

            {/* Mobile Search */}
            <button 
              onClick={() => setMobileSearchOpen(true)}
              className="p-2 rounded-lg text-gray-600 hover:text-gray-900 hover:bg-gray-100 md:hidden transition-all duration-200 active:scale-95"
              aria-label="Open search"
            >
              <Search className="h-5 w-5" />
            </button>

            {/* Theme Toggle */}
            <button 
              onClick={toggleDarkMode}
              className="p-2 rounded-lg text-gray-600 hover:text-gray-900 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all duration-200 active:scale-95"
              aria-label="Toggle theme"
            >
              {darkMode ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
            </button>

            {/* Help */}
            <button className="p-2 rounded-lg text-gray-600 hover:text-gray-900 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all duration-200 active:scale-95">
              <HelpCircle className="h-5 w-5" />
            </button>

            {/* Notifications */}
            <div className="relative" ref={notificationsRef}>
              <button
                onClick={() => setNotificationsOpen(!notificationsOpen)}
                className="p-2 rounded-lg text-gray-600 hover:text-gray-900 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 relative transition-all duration-200 active:scale-95"
                aria-label="Notifications"
              >
                <Bell className="h-5 w-5" />
                {unreadCount > 0 && (
                  <span className="absolute -top-1 -right-1 h-5 w-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center animate-pulse font-medium">
                    {unreadCount > 9 ? '9+' : unreadCount}
                  </span>
                )}
              </button>

              {/* Notifications Dropdown */}
              {notificationsOpen && (
                <div className="absolute right-0 mt-2 w-96 bg-white rounded-xl shadow-lg border border-gray-200 py-2 z-50 animate-fade-in max-h-96 overflow-hidden">
                  <div className="px-4 py-3 border-b border-gray-200">
                    <div className="flex items-center justify-between">
                      <h3 className="text-sm font-medium text-gray-900">Notifications</h3>
                      <div className="flex items-center space-x-3">
                        <span className="text-xs text-gray-500">{unreadCount} unread</span>
                        <button className="text-xs text-blue-600 hover:text-blue-800 font-medium">
                          Mark all read
                        </button>
                      </div>
                    </div>
                  </div>
                  
                  <div className="max-h-80 overflow-y-auto scrollbar-thin">
                    {notifications.map((notification) => {
                      const Icon = notification.icon;
                      return (
                        <div
                          key={notification.id}
                          onClick={() => markAsRead(notification.id)}
                          className={`px-4 py-4 hover:bg-gray-50 cursor-pointer border-l-4 transition-all duration-200 ${
                            notification.unread ? 'border-blue-500 bg-blue-50/30' : 'border-transparent'
                          }`}
                        >
                          <div className="flex items-start space-x-3">
                            <div className={`w-8 h-8 rounded-full flex items-center justify-center ${notification.color}`}>
                              <Icon className="h-4 w-4" />
                            </div>
                            <div className="flex-1 min-w-0">
                              <p className="text-sm font-medium text-gray-900">{notification.title}</p>
                              <p className="text-sm text-gray-600 mt-1 line-clamp-2">{notification.message}</p>
                              <div className="flex items-center justify-between mt-2">
                                <p className="text-xs text-gray-400">{notification.time}</p>
                                {notification.unread && (
                                  <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
                                )}
                              </div>
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                  
                  <div className="px-4 py-3 border-t border-gray-200">
                    <button className="text-sm text-blue-600 hover:text-blue-800 font-medium flex items-center space-x-1 w-full justify-center">
                      <span>View all notifications</span>
                      <ArrowRight className="h-3 w-3" />
                    </button>
                  </div>
                </div>
              )}
            </div>

            {/* User Profile */}
            <div className="relative" ref={profileRef}>
              <button
                onClick={() => setProfileOpen(!profileOpen)}
                className="flex items-center space-x-2 p-2 rounded-lg text-gray-600 hover:text-gray-900 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all duration-200 active:scale-95"
              >
                <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center shadow-md">
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
                <div className="absolute right-0 mt-2 w-64 bg-white rounded-xl shadow-lg border border-gray-200 py-2 z-50 animate-fade-in">
                  <div className="px-4 py-3 border-b border-gray-200">
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                        <User className="h-5 w-5 text-white" />
                      </div>
                      <div>
                        <div className="text-sm font-medium text-gray-900">
                          {isSupabaseEnabled && user ? user.email : 'demo@vibeauditor.com'}
                        </div>
                        <div className="text-xs text-gray-500">Security Administrator</div>
                      </div>
                    </div>
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
                      <Bookmark className="h-4 w-4 mr-3" />
                      Bookmarks
                    </button>
                    <button className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors">
                      <Globe className="h-4 w-4 mr-3" />
                      Language
                    </button>
                  </div>
                  
                  <div className="border-t border-gray-200 py-1">
                    <div className="px-4 py-2 text-xs text-gray-500">
                      Last login: {currentTime.toLocaleString()}
                    </div>
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
        <div className="fixed inset-0 z-50 bg-white md:hidden animate-fade-in">
          <div className="flex items-center h-16 px-4 border-b border-gray-200">
            <div className="flex-1 flex items-center space-x-3">
              <Search className="h-5 w-5 text-gray-400" />
              <input
                ref={mobileSearchInputRef}
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search scans, issues, compliance..."
                className="flex-1 text-lg placeholder-gray-500 focus:outline-none bg-transparent"
              />
            </div>
            <button
              onClick={() => setMobileSearchOpen(false)}
              className="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <X className="h-6 w-6" />
            </button>
          </div>
          
          <div className="p-4 overflow-y-auto h-full pb-20">
            {searchQuery ? (
              <>
                {searchResults.length > 0 ? (
                  <>
                    <div className="text-sm font-medium text-gray-500 mb-3">Search Results</div>
                    <div className="space-y-2">
                      {searchResults.map((result, index) => {
                        const Icon = result.icon;
                        return (
                          <div key={index} className="flex items-center space-x-3 p-4 rounded-xl hover:bg-gray-50 transition-colors">
                            <Icon className="h-5 w-5 text-gray-400" />
                            <div className="flex-1">
                              <div className="text-sm text-gray-900">{result.title}</div>
                              <div className="text-xs text-gray-500">{result.subtitle}</div>
                            </div>
                            <ArrowRight className="h-4 w-4 text-gray-300" />
                          </div>
                        );
                      })}
                    </div>
                  </>
                ) : (
                  <div className="text-center py-12">
                    <Search className="h-12 w-12 text-gray-300 mx-auto mb-4" />
                    <div className="text-lg text-gray-500 mb-2">No results found</div>
                    <div className="text-sm text-gray-400">Try different keywords or check spelling</div>
                  </div>
                )}
              </>
            ) : (
              <>
                <div className="text-sm font-medium text-gray-500 mb-3">Recent Searches</div>
                <div className="space-y-2 mb-6">
                  {searchSuggestions.slice(0, 3).map((suggestion, index) => {
                    const Icon = suggestion.icon;
                    return (
                      <div key={index} className="flex items-center space-x-3 p-4 rounded-xl hover:bg-gray-50 transition-colors">
                        <Icon className="h-5 w-5 text-gray-400" />
                        <div className="flex-1">
                          <div className="text-sm text-gray-900">{suggestion.title}</div>
                          <div className="text-xs text-gray-500">{suggestion.subtitle}</div>
                        </div>
                        <Clock className="h-4 w-4 text-gray-300" />
                      </div>
                    );
                  })}
                </div>
                
                <div className="text-sm font-medium text-gray-500 mb-3">Quick Actions</div>
                <div className="space-y-2">
                  {searchSuggestions.slice(3).map((action, index) => {
                    const Icon = action.icon;
                    return (
                      <div key={index} className="flex items-center space-x-3 p-4 rounded-xl hover:bg-gray-50 transition-colors">
                        <Icon className="h-5 w-5 text-gray-400" />
                        <div className="flex-1">
                          <div className="text-sm text-gray-900">{action.title}</div>
                          <div className="text-xs text-gray-500">{action.subtitle}</div>
                        </div>
                        <Zap className="h-4 w-4 text-gray-300" />
                      </div>
                    );
                  })}
                </div>
              </>
            )}
          </div>
        </div>
      )}
    </>
  );
};

export default OptimizedTopBar;