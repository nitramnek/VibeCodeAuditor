import React from 'react';

const MetricCard = ({ title, value, change, changeType }) => {
  return (
    <div className="bg-white p-6 rounded-xl shadow-modern border border-gray-200 hover:shadow-modern-md transition-all duration-200 hover-lift">
      <div className="text-center">
        <p className="text-sm font-medium text-gray-600 mb-2">{title}</p>
        <p className="text-3xl font-bold text-gray-900">{value}</p>
        {change && (
          <p className={`text-sm ${changeType === 'positive' ? 'text-green-600' : 'text-red-600'}`}>
            {change}
          </p>
        )}
      </div>
    </div>
  );
};

export default MetricCard;
