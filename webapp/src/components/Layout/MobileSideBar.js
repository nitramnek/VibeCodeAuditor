import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  X,
  LayoutDashboard, 
  Shield, 
  FileSearch, 
  BarChart3, 
  Settings, 
  BookOpen, 
  History, 
  Users, 
  Database,
  Globe,
  CheckCircle
} from 'lucide-react';

const MobileSideBar = ({ onClose }) => {
  const location = useLocation();

  const navigation = [
    {
      name: 'Dashboard',
      href: '/dashboard',
      icon: LayoutDashboard,
      current: location.pathname === '/dashboard',
      badge: null
    },
    {
      name: 'Security Scanner',
      href: '/scanner',
      icon: FileSearch,
      current: location.pathname === '/scanner',
      badge: null
    },
    {
      name: 'Scan Results',
      href: '/results',
      icon: Shield,
      current: location.pathname.startsWith('/results'),
      badge: '3'
    },
    {
      name: 'Compliance',
      href: '/compliance',
      icon: CheckCircle,
      current: location.pathname === '/compliance',
      badge: null
    },
    {
      name: 'Analytics',
      href: '/analytics',
      icon: BarChart3,
      current: location.pathname === '/analytics',
      badge: null
    },
    {
      name: 'Scan History',
      href: '/history',
      icon: History,
      current: location.pathname === '/history'
    },
    {
      name: 'Security Rules',
      href: '/rules',
      icon: BookOpen,
      current: location.pathname === '/rules'
    },
    {
      name: 'Team Management',
      href: '/team',
      icon: Users,
      current: location.pathname === '/team'
    },
    {
      name: 'Integrations',
      href: '/integrations',
      icon: Database,
      current: location.pathname === '/integrations'
    },
    {
      name: 'Settings',
      href: '/settings',
      icon: Settings,
      current: location.pathname === '/settings'
    }
  ];



  return (
    <div className="flex flex-col h-full bg-white animate-slide-in-left">
      {/* Mobile Header */}
      <div className="flex items-center justify-between h-16 px-4 border-b border-gray-200 bg-gradient-to-r from-blue-50 to-purple-50">
        <div className="flex items-center space-x-3">
          <div className="flex items-center justify-center w-10 h-10 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg shadow-md">
            <Shield className="h-6 w-6 text-white" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-gray-900">VibeCodeAuditor</h2>
            <p className="text-xs text-gray-500">Enterprise Security Platform</p>
          </div>
        </div>
        <button
          onClick={onClose}
          className="p-2 rounded-md text-gray-600 hover:text-gray-900 hover:bg-white/50 transition-colors"
        >
          <X className="h-6 w-6" />
        </button>
      </div>

      {/* Mobile Navigation Header */}
      <div className="p-4 border-b border-gray-200 bg-gradient-to-r from-blue-50 to-purple-50">
        <div className="text-center">
          <h3 className="text-sm font-medium text-gray-900 mb-1">Navigation Menu</h3>
          <p className="text-xs text-gray-500">Access all security features</p>
        </div>
      </div>

      {/* Navigation */}
      <div className="flex-1 px-4 py-4 overflow-y-auto scrollbar-thin">
        <nav className="space-y-1">
          {navigation.map((item) => {
            const Icon = item.icon;
            return (
              <Link
                key={item.name}
                to={item.href}
                onClick={onClose}
                className={`group flex items-center justify-between px-4 py-3 text-base font-medium rounded-xl transition-all duration-200 ${
                  item.current
                    ? 'bg-gradient-to-r from-blue-50 to-purple-50 text-blue-700 border-l-4 border-blue-600 shadow-sm'
                    : 'text-gray-700 hover:text-gray-900 hover:bg-gray-50 active:bg-gray-100'
                }`}
              >
                <div className="flex items-center space-x-3">
                  <Icon className={`h-6 w-6 ${
                    item.current ? 'text-blue-600' : 'text-gray-400 group-hover:text-gray-600'
                  }`} />
                  <span>{item.name}</span>
                </div>
                {item.badge && (
                  <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800 animate-pulse">
                    {item.badge}
                  </span>
                )}
              </Link>
            );
          })}
        </nav>
      </div>

      {/* Mobile Footer */}
      <div className="p-4 border-t border-gray-200 bg-gradient-to-r from-blue-50 to-purple-50">
        <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
          <div className="flex items-center space-x-3 mb-3">
            <Globe className="h-5 w-5 text-blue-600" />
            <div>
              <p className="text-sm font-medium text-gray-900">Enterprise Plan</p>
              <p className="text-xs text-gray-500">Unlimited scans & compliance</p>
            </div>
          </div>
          <div className="space-y-2">
            <div className="flex justify-between text-xs text-gray-600">
              <span>Monthly Usage</span>
              <span>75%</span>
            </div>
            <div className="bg-gray-200 rounded-full h-2">
              <div 
                className="bg-gradient-to-r from-blue-500 to-purple-600 h-2 rounded-full transition-all duration-500" 
                style={{ width: '75%' }}
              ></div>
            </div>
            <p className="text-xs text-gray-500">Resets in 12 days</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MobileSideBar;