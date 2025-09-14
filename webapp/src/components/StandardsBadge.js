import React from 'react';

const StandardsBadge = ({ standard }) => {
  const getStandardColor = (type) => {
    switch (type) {
      case 'compliance':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'security':
        return 'bg-orange-100 text-orange-800 border-orange-200';
      case 'best_practice':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'coding':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getStandardIcon = (type) => {
    switch (type) {
      case 'compliance':
        return '⚖️';
      case 'security':
        return '🛡️';
      case 'best_practice':
        return '✅';
      case 'coding':
        return '📝';
      default:
        return '📋';
    }
  };

  return (
    <div className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium border ${getStandardColor(standard.type)}`}>
      <span className="mr-1">{getStandardIcon(standard.type)}</span>
      <span className="truncate max-w-xs" title={standard.name}>
        {standard.name.length > 30 ? `${standard.name.substring(0, 30)}...` : standard.name}
      </span>
    </div>
  );
};

export default StandardsBadge;