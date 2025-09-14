import React, { useState } from 'react';
import { useQuery } from 'react-query';
import { Shield, Search, Filter } from 'lucide-react';
import { getAvailableRules } from '../services/api';

const Rules = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedSeverity, setSelectedSeverity] = useState('all');

  const { data: rules, isLoading, error } = useQuery('rules', getAvailableRules);

  const filteredRules = rules?.filter(rule => {
    const matchesSearch = rule.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         rule.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || rule.category === selectedCategory;
    const matchesSeverity = selectedSeverity === 'all' || rule.severity === selectedSeverity;
    
    return matchesSearch && matchesCategory && matchesSeverity;
  }) || [];

  const categories = [...new Set(rules?.map(rule => rule.category) || [])];
  const severities = ['critical', 'high', 'medium', 'low'];

  const severityColors = {
    critical: 'bg-red-100 text-red-800',
    high: 'bg-orange-100 text-orange-800',
    medium: 'bg-yellow-100 text-yellow-800',
    low: 'bg-green-100 text-green-800',
  };

  const categoryColors = {
    security: 'bg-red-100 text-red-800',
    quality: 'bg-blue-100 text-blue-800',
    ai_ml: 'bg-purple-100 text-purple-800',
    general: 'bg-gray-100 text-gray-800',
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-md p-4">
        <p className="text-red-700">Error loading rules: {error.message}</p>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Audit Rules</h1>
        <p className="text-gray-600">
          Browse and understand the security and quality rules used in code analysis
        </p>
      </div>

      {/* Search and Filters */}
      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 mb-6">
        <div className="flex flex-col md:flex-row md:items-center space-y-4 md:space-y-0 md:space-x-4">
          {/* Search */}
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search rules..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          {/* Category Filter */}
          <div className="flex items-center space-x-2">
            <Filter className="h-4 w-4 text-gray-400" />
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="border border-gray-300 rounded-md px-3 py-2 text-sm"
            >
              <option value="all">All Categories</option>
              {categories.map(category => (
                <option key={category} value={category}>
                  {category.replace('_', ' ').toUpperCase()}
                </option>
              ))}
            </select>
          </div>

          {/* Severity Filter */}
          <div>
            <select
              value={selectedSeverity}
              onChange={(e) => setSelectedSeverity(e.target.value)}
              className="border border-gray-300 rounded-md px-3 py-2 text-sm"
            >
              <option value="all">All Severities</option>
              {severities.map(severity => (
                <option key={severity} value={severity}>
                  {severity.toUpperCase()}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Rules Count */}
      <div className="mb-6">
        <p className="text-gray-600">
          Showing {filteredRules.length} of {rules?.length || 0} rules
        </p>
      </div>

      {/* Rules Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredRules.map((rule) => (
          <div key={rule.id} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center space-x-2">
                <Shield className="h-5 w-5 text-blue-600" />
                <h3 className="font-semibold text-gray-900 text-sm">{rule.name}</h3>
              </div>
              <div className="flex flex-col space-y-1">
                <span className={`px-2 py-1 text-xs font-medium rounded-full ${severityColors[rule.severity]}`}>
                  {rule.severity.toUpperCase()}
                </span>
              </div>
            </div>

            <p className="text-gray-600 text-sm mb-4 line-clamp-3">{rule.description}</p>

            <div className="flex items-center justify-between">
              <span className={`px-2 py-1 text-xs font-medium rounded-full ${categoryColors[rule.category] || categoryColors.general}`}>
                {rule.category.replace('_', ' ').toUpperCase()}
              </span>
              
              {rule.languages && rule.languages.length > 0 && (
                <div className="flex items-center space-x-1">
                  {rule.languages.slice(0, 3).map((lang, index) => (
                    <span key={index} className="px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded">
                      {lang.replace('.', '')}
                    </span>
                  ))}
                  {rule.languages.length > 3 && (
                    <span className="text-xs text-gray-500">+{rule.languages.length - 3}</span>
                  )}
                </div>
              )}
            </div>

            {rule.tags && rule.tags.length > 0 && (
              <div className="mt-3 pt-3 border-t border-gray-100">
                <div className="flex flex-wrap gap-1">
                  {rule.tags.map((tag, index) => (
                    <span key={index} className="px-2 py-1 text-xs bg-blue-50 text-blue-700 rounded">
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>

      {filteredRules.length === 0 && (
        <div className="text-center py-12">
          <Shield className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600 mb-2">No rules found</p>
          <p className="text-sm text-gray-500">Try adjusting your search or filter criteria</p>
        </div>
      )}
    </div>
  );
};

export default Rules;