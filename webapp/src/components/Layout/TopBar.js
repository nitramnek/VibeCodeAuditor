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
    Globe
} from 'lucide-react';
import { useAuth } from '../../contexts/AuthContext';

const TopBar = ({ onMenuClick, isMobile }) => {
    const [searchOpen, setSearchOpen] = useState(false);
    const [profileOpen, setProfileOpen] = useState(false);
    const [notificationsOpen, setNotificationsOpen] = useState(false);
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

    return (
        <header className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-30">
            <div className="flex items-center justify-between h-16 px-4 sm:px-6 lg:px-8">
                {/* Left Section */}
                <div className="flex items-center space-x-4">
                    {/* Mobile Menu Button */}
                    {isMobile && (
                        <button
                            onClick={onMenuClick}
                            className="p-2 rounded-md text-gray-600 hover:text-gray-900 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 lg:hidden"
                            aria-label="Open sidebar"
                        >
                            <Menu className="h-6 w-6" />
                        </button>
                    )}

                    {/* Logo */}
                    <Link to="/dashboard" className="flex items-center space-x-3">
                        <div className="flex items-center justify-center w-10 h-10 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg">
                            <Shield className="h-6 w-6 text-white" />
                        </div>
                        <div className="hidden sm:block">
                            <h1 className="text-xl font-bold text-gray-900">VibeCodeAuditor</h1>
                            <p className="text-xs text-gray-500">Enterprise Security Platform</p>
                        </div>
                    </Link>
                </div>

                {/* Center Section - Search */}
                <div className="flex-1 max-w-2xl mx-4 hidden md:block">
                    <div className="relative">
                        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                            <Search className="h-5 w-5 text-gray-400" />
                        </div>
                        <input
                            type="text"
                            placeholder="Search scans, issues, or compliance frameworks..."
                            className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg leading-5 bg-gray-50 placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 focus:bg-white sm:text-sm transition-colors"
                            onFocus={() => setSearchOpen(true)}
                            onBlur={() => setTimeout(() => setSearchOpen(false), 200)}
                        />

                        {/* Search Dropdown */}
                        {searchOpen && (
                            <div className="absolute top-full left-0 right-0 mt-1 bg-white rounded-lg shadow-lg border border-gray-200 py-2 z-50">
                                <div className="px-4 py-2 text-xs font-medium text-gray-500 uppercase tracking-wide">Recent Searches</div>
                                <div className="px-4 py-2 hover:bg-gray-50 cursor-pointer">
                                    <div className="text-sm text-gray-900">SQL Injection vulnerabilities</div>
                                    <div className="text-xs text-gray-500">in authentication module</div>
                                </div>
                                <div className="px-4 py-2 hover:bg-gray-50 cursor-pointer">
                                    <div className="text-sm text-gray-900">OWASP Top 10 compliance</div>
                                    <div className="text-xs text-gray-500">security standards</div>
                                </div>
                            </div>
                        )}
                    </div>
                </div>

                {/* Right Section */}
                <div className="flex items-center space-x-2 sm:space-x-4">
                    {/* Mobile Search */}
                    <button className="p-2 rounded-md text-gray-600 hover:text-gray-900 hover:bg-gray-100 md:hidden">
                        <Search className="h-5 w-5" />
                    </button>

                    {/* Theme Toggle */}
                    <button className="p-2 rounded-md text-gray-600 hover:text-gray-900 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500">
                        <Sun className="h-5 w-5" />
                    </button>

                    {/* Notifications */}
                    <div className="relative">
                        <button
                            onClick={() => setNotificationsOpen(!notificationsOpen)}
                            className="p-2 rounded-md text-gray-600 hover:text-gray-900 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 relative"
                        >
                            <Bell className="h-5 w-5" />
                            {unreadCount > 0 && (
                                <span className="absolute -top-1 -right-1 h-4 w-4 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
                                    {unreadCount}
                                </span>
                            )}
                        </button>

                        {/* Notifications Dropdown */}
                        {notificationsOpen && (
                            <div className="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-lg border border-gray-200 py-2 z-50">
                                <div className="px-4 py-2 border-b border-gray-200">
                                    <div className="flex items-center justify-between">
                                        <h3 className="text-sm font-medium text-gray-900">Notifications</h3>
                                        <span className="text-xs text-gray-500">{unreadCount} unread</span>
                                    </div>
                                </div>
                                <div className="max-h-64 overflow-y-auto">
                                    {notifications.map((notification) => (
                                        <div
                                            key={notification.id}
                                            className={`px-4 py-3 hover:bg-gray-50 cursor-pointer border-l-4 ${notification.unread ? 'border-blue-500 bg-blue-50' : 'border-transparent'
                                                }`}
                                        >
                                            <div className="flex items-start space-x-3">
                                                <div className="flex-1 min-w-0">
                                                    <p className="text-sm font-medium text-gray-900">{notification.title}</p>
                                                    <p className="text-sm text-gray-500 truncate">{notification.message}</p>
                                                    <p className="text-xs text-gray-400 mt-1">{notification.time}</p>
                                                </div>
                                                {notification.unread && (
                                                    <div className="w-2 h-2 bg-blue-500 rounded-full mt-2"></div>
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
                    <div className="relative">
                        <button
                            onClick={() => setProfileOpen(!profileOpen)}
                            className="flex items-center space-x-2 p-2 rounded-md text-gray-600 hover:text-gray-900 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
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
                            <ChevronDown className="h-4 w-4 text-gray-400" />
                        </button>

                        {/* Profile Dropdown */}
                        {profileOpen && (
                            <div className="absolute right-0 mt-2 w-56 bg-white rounded-lg shadow-lg border border-gray-200 py-2 z-50">
                                <div className="px-4 py-2 border-b border-gray-200">
                                    <div className="text-sm font-medium text-gray-900">
                                        {isSupabaseEnabled && user ? user.email : 'demo@vibeauditor.com'}
                                    </div>
                                    <div className="text-xs text-gray-500">Security Administrator</div>
                                </div>

                                <div className="py-1">
                                    <Link
                                        to="/profile"
                                        className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                                    >
                                        <User className="h-4 w-4 mr-3" />
                                        Your Profile
                                    </Link>
                                    <Link
                                        to="/settings"
                                        className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                                    >
                                        <Settings className="h-4 w-4 mr-3" />
                                        Settings
                                    </Link>
                                    <button className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                                        <Globe className="h-4 w-4 mr-3" />
                                        Language
                                    </button>
                                </div>

                                {isSupabaseEnabled && (
                                    <div className="border-t border-gray-200 py-1">
                                        <button
                                            onClick={handleSignOut}
                                            className="flex items-center w-full px-4 py-2 text-sm text-red-700 hover:bg-red-50"
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
    );
};

export default TopBar;