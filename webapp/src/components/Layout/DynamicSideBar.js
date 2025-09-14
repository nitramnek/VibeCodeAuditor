import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
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
  ChevronLeft,
  ChevronRight,
  CheckCircle
} from 'lucide-react';
import { useScanCount } from '../../hooks/useScanCount';

const DynamicSideBar = ({ state, onToggle, isTablet }) => {
  const location = useLocation();
  const [hoveredItem, setHoveredItem] = useState(null);
  const { scanCount, loading } = useScanCount();
  
  const isExpanded = state === 'expanded';
  const isCollapsed = state === 'collapsed';

  const navigation = [
    {
      name: 'Dashboard',
      href: '/dashboard',
      icon: LayoutDashboard,
      current: location.pathname === '/dashboard',
      badge: null,
      description: 'Security overview and metrics'
    },
    {
      name: 'Security Scanner',
      href: '/scanner',
      icon: FileSearch,
      current: location.pathname === '/scanner',
      badge: null,
      description: 'Upload and scan code files'
    },
    {
      name: 'Scan Results',
      href: '/scan-results',
      icon: Shield,
      current: location.pathname.startsWith('/scan-results'),
      badge: loading ? null : (scanCount > 0 ? scanCount.toString() : null),
      description: 'View security scan results'
    },
    {
      name: 'Compliance',
      href: '/compliance',
      icon: CheckCircle,
      current: location.pathname === '/compliance',
      badge: null,
      description: 'Regulatory compliance status'
    },
    {
      name: 'Analytics',
      href: '/analytics',
      icon: BarChart3,
      current: location.pathname === '/analytics',
      badge: null,
      description: 'Security trends and insights'
    }
  ];

  const secondaryNavigation = [
    {
      name: 'Scan History',
      href: '/history',
      icon: History,
      current: location.pathname === '/history',
      description: 'Previous security scans'
    },
    {
      name: 'Security Rules',
      href: '/rules',
      icon: BookOpen,
      current: location.pathname === '/rules',
      description: 'Configure security rules'
    },
    {
      name: 'Team Management',
      href: '/team',
      icon: Users,
      current: location.pathname === '/team',
      description: 'Manage team members'
    },
    {
      name: 'Integrations',
      href: '/integrations',
      icon: Database,
      current: location.pathname === '/integrations',
      description: 'Third-party integrations'
    }
  ];



  // Render navigation item
  const renderNavItem = (item, isSecondary = false) => {
    const Icon = item.icon;
    const isActive = item.current;
    
    return (
      <div key={item.name} className="relative">
        <Link
          to={item.href}
          className={`group flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-all duration-200 ${
            isActive
              ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-600'
              : 'text-gray-700 hover:text-gray-900 hover:bg-gray-50'
          } ${isCollapsed ? 'justify-center' : 'justify-between'}`}
          onMouseEnter={() => setHoveredItem(item.name)}
          onMouseLeave={() => setHoveredItem(null)}
        >
          <div className="flex items-center space-x-3">
            <Icon className={`h-5 w-5 flex-shrink-0 ${
              isActive ? 'text-blue-600' : 'text-gray-400 group-hover:text-gray-600'
            }`} />
            {isExpanded && <span className="truncate">{item.name}</span>}
          </div>
          
          {isExpanded && item.badge && (
            <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800">
              {item.badge}
            </span>
          )}
        </Link>
        
        {/* Tooltip for collapsed state */}
        {isCollapsed && hoveredItem === item.name && (
          <div className="absolute left-full top-0 ml-2 px-3 py-2 bg-gray-900 text-white text-sm rounded-lg shadow-lg z-50 whitespace-nowrap">
            <div className="font-medium">{item.name}</div>
            {item.description && (
              <div className="text-xs text-gray-300 mt-1">{item.description}</div>
            )}
            {item.badge && (
              <div className="text-xs text-red-300 mt-1">{item.badge} items</div>
            )}
            {/* Arrow */}
            <div className="absolute top-2 -left-1 w-2 h-2 bg-gray-900 transform rotate-45"></div>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="flex flex-col h-full bg-white border-r border-gray-200 shadow-sm">
      {/* Sidebar Header */}
      <div className={`flex items-center h-16 px-4 border-b border-gray-200 ${
        isCollapsed ? 'justify-center' : 'justify-between'
      }`}>
        {isExpanded && (
          <div className="flex items-center space-x-3">
            <div className="flex items-center justify-center w-8 h-8 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg">
              <Shield className="h-5 w-5 text-white" />
            </div>
            <div>
              <h2 className="text-sm font-bold text-gray-900">VibeCodeAuditor</h2>
              <p className="text-xs text-gray-500">Security Platform</p>
            </div>
          </div>
        )}
        
        {isCollapsed && (
          <div className="flex items-center justify-center w-8 h-8 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg">
            <Shield className="h-5 w-5 text-white" />
          </div>
        )}
        
        {/* Toggle Button */}
        {!isTablet && (
          <button
            onClick={onToggle}
            className="p-1.5 rounded-md text-gray-400 hover:text-gray-600 hover:bg-gray-100 transition-colors"
            title={isExpanded ? 'Collapse sidebar' : 'Expand sidebar'}
          >
            {isExpanded ? (
              <ChevronLeft className="h-4 w-4" />
            ) : (
              <ChevronRight className="h-4 w-4" />
            )}
          </button>
        )}
      </div>



      {/* Main Navigation */}
      <div className="flex-1 px-3 py-6 space-y-1 overflow-y-auto scrollbar-thin">
        {/* Primary Navigation */}
        {isExpanded && (
          <h3 className="px-3 text-xs font-medium text-gray-500 uppercase tracking-wide mb-3">
            Security Platform
          </h3>
        )}
        <nav className="space-y-1 mb-6">
          {navigation.map((item) => renderNavItem(item))}
        </nav>

        {/* Secondary Navigation */}
        <div className="pt-2 border-t border-gray-200">
          {isExpanded && (
            <h3 className="px-3 text-xs font-medium text-gray-500 uppercase tracking-wide mb-3 mt-4">
              Management
            </h3>
          )}
          <nav className="space-y-1">
            {secondaryNavigation.map((item) => renderNavItem(item, true))}
          </nav>
        </div>
      </div>

      {/* Sidebar Footer */}
      {isExpanded && (
        <div className="p-4 border-t border-gray-200">
          <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-3">
            <div className="flex items-center space-x-3">
              <div className="flex-shrink-0">
                <Globe className="h-5 w-5 text-blue-600" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900">Enterprise Plan</p>
                <p className="text-xs text-gray-500">Unlimited scans & compliance</p>
              </div>
            </div>
            <div className="mt-2">
              <div className="bg-white rounded-full h-2">
                <div className="bg-gradient-to-r from-blue-500 to-purple-600 h-2 rounded-full" style={{ width: '75%' }}></div>
              </div>
              <p className="text-xs text-gray-500 mt-1">75% of monthly quota used</p>
            </div>
          </div>
        </div>
      )}

      {/* Collapsed Footer */}
      {isCollapsed && (
        <div className="p-2 border-t border-gray-200 flex justify-center">
          <div 
            className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center relative group"
            onMouseEnter={() => setHoveredItem('enterprise')}
            onMouseLeave={() => setHoveredItem(null)}
          >
            <Globe className="h-4 w-4 text-white" />
            
            {/* Tooltip */}
            {hoveredItem === 'enterprise' && (
              <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-gray-900 text-white text-xs rounded shadow-lg z-50 whitespace-nowrap">
                <div className="font-medium">Enterprise Plan</div>
                <div className="text-gray-300">75% quota used</div>
                <div className="absolute top-full left-1/2 transform -translate-x-1/2 w-2 h-2 bg-gray-900 rotate-45"></div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default DynamicSideBar;