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
  AlertTriangle,
  CheckCircle,
  Database
} from 'lucide-react';

const MobileNav = ({ onClose }) => {
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

  const quickStats = [
    { name: 'Active Scans', value: '2', color: 'text-blue-600' },
    { name: 'Critical Issues', value: '5', color: 'text-red-600' },
    { name: 'Resolved Today', value: '23', color: 'text-green-600' }
  ];

  return (
    <div className="flex flex-col h-full bg-white">
      {/* Mobile Header */}
      <div className="flex items-center justify-between h-16 px-4 border-b border-gray-200">
        <div className="flex items-center space-x-3">
          <div className="flex items-center justify-center w-8 h-8 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg">
            <Shield className="h-5 w-5 text-white" />
          </div>
          <div>
            <h2 className="text-sm font-bold text-gray-900">VibeCodeAuditor</h2>
            <p className="text-xs text-gray-500">Security Platform</p>
          </div>
        </div>
        <button
          onClick={onClose}
          className="p-2 rounded-md text-gray-600 hover:text-gray-900 hover:bg-gray-100"
        >
          <X className="h-6 w-6" />
        </button>
      </div>

      {/* Quick Stats */}
      <div className="p-4 border-b border-gray-200">
        <h3 className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-3">
          Quick Overview
        </h3>
        <div className="grid grid-cols-3 gap-3">
          {quickStats.map((stat) => (
            <div key={stat.name} className="text-center">
              <div className={`text-lg font-bold ${stat.color}`}>{stat.value}</div>
              <div className="text-xs text-gray-500">{stat.name}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Navigation */}
      <div className="flex-1 px-4 py-4 overflow-y-auto">
        <nav className="space-y-1">
          {navigation.map((item) => {
            const Icon = item.icon;
            return (
              <Link
                key={item.name}
                to={item.href}
                onClick={onClose}
                className={`group flex items-center justify-between px-3 py-3 text-base font-medium rounded-lg transition-all duration-200 ${
                  item.current
                    ? 'bg-blue-50 text-blue-700 border-r-4 border-blue-600'
                    : 'text-gray-700 hover:text-gray-900 hover:bg-gray-50'
                }`}
              >
                <div className="flex items-center space-x-3">
                  <Icon className={`h-6 w-6 ${
                    item.current ? 'text-blue-600' : 'text-gray-400 group-hover:text-gray-600'
                  }`} />
                  <span>{item.name}</span>
                </div>
                {item.badge && (
                  <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800">
                    {item.badge}
                  </span>
                )}
              </Link>
            );
          })}
        </nav>
      </div>

      {/* Mobile Footer */}
      <div className="p-4 border-t border-gray-200">
        <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-3">
          <div className="text-center">
            <p className="text-sm font-medium text-gray-900">Enterprise Plan</p>
            <p className="text-xs text-gray-500 mt-1">Unlimited scans & compliance</p>
            <div className="mt-2">
              <div className="bg-white rounded-full h-2">
                <div className="bg-gradient-to-r from-blue-500 to-purple-600 h-2 rounded-full" style={{ width: '75%' }}></div>
              </div>
              <p className="text-xs text-gray-500 mt-1">75% quota used</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MobileNav;