import React from 'react';
import { AlertTriangle, Shield, Info } from 'lucide-react';

const ComplianceOverview = ({ complianceSummary }) => {
  if (!complianceSummary || Object.keys(complianceSummary).length === 0) {
    return null;
  }

  // Framework-specific styling configuration
  const frameworkStyles = {
    'ISO 27001': {
      bg: 'bg-red-100',
      text: 'text-red-700',
      border: 'border-red-200',
      icon: '🛡️'
    },
    'OWASP': {
      bg: 'bg-orange-100',
      text: 'text-orange-700',
      border: 'border-orange-200',
      icon: '🔒'
    },
    'GDPR': {
      bg: 'bg-green-100',
      text: 'text-green-700',
      border: 'border-green-200',
      icon: '🔐'
    },
    'PCI DSS': {
      bg: 'bg-blue-100',
      text: 'text-blue-700',
      border: 'border-blue-200',
      icon: '💳'
    },
    'HIPAA': {
      bg: 'bg-purple-100',
      text: 'text-purple-700',
      border: 'border-purple-200',
      icon: '🏥'
    },
    'NIST': {
      bg: 'bg-indigo-100',
      text: 'text-indigo-700',
      border: 'border-indigo-200',
      icon: '🏛️'
    },
    'SOX': {
      bg: 'bg-yellow-100',
      text: 'text-yellow-700',
      border: 'border-yellow-200',
      icon: '📊'
    }
  };

  const defaultStyle = {
    bg: 'bg-gray-100',
    text: 'text-gray-700',
    border: 'border-gray-200',
    icon: '📋'
  };

  const totalViolations = Object.values(complianceSummary).reduce((total, data) => {
    return total + (typeof data === 'object' ? data.count || 0 : data || 0);
  }, 0);

  return (
    <div className="bg-white rounded-lg shadow-sm border-l-4 border-purple-200 p-6 mb-6">
      <div className="flex items-start space-x-4">
        <div className="flex-shrink-0">
          <div className="w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center">
            <Shield className="h-6 w-6 text-purple-600" />
          </div>
        </div>
        <div className="flex-1">
          {/* Header */}
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-lg font-semibold text-gray-900">Regulatory Compliance Impact</h2>
            <div className="flex items-center space-x-2">
              <span className="px-2 py-1 text-xs font-medium rounded-full bg-purple-100 text-purple-800 flex items-center">
                <Shield className="w-3 h-3 mr-1" />
                {Object.keys(complianceSummary).length} Frameworks
              </span>
              <span className="px-2 py-1 text-xs font-medium rounded-full bg-red-100 text-red-800 flex items-center">
                <AlertTriangle className="w-3 h-3 mr-1" />
                {totalViolations} Total Violations
              </span>
            </div>
          </div>

          {/* Compliance Alert */}
          <div className="bg-red-50 border border-red-200 p-3 rounded-md mb-4">
            <div className="flex items-start space-x-2">
              <AlertTriangle className="w-4 h-4 text-red-600 mt-0.5 flex-shrink-0" />
              <div className="text-sm">
                <span className="font-medium text-red-800">Compliance Risk Alert:</span>
                <span className="text-red-700 ml-1">
                  Security issues detected across {Object.keys(complianceSummary).length} regulatory frameworks. 
                  Immediate attention required to maintain compliance posture and avoid audit findings.
                </span>
              </div>
            </div>
          </div>

          {/* Framework Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 mb-4">
            {Object.entries(complianceSummary).map(([framework, data]) => {
              const count = typeof data === 'object' ? data.count || 0 : data || 0;
              const name = typeof data === 'object' ? data.name || framework : framework;
              
              const style = frameworkStyles[framework] || frameworkStyles[name] || defaultStyle;
              
              return (
                <div 
                  key={framework} 
                  className={`border rounded-md p-4 hover:shadow-sm transition-all duration-200 ${style.bg} ${style.text} ${style.border}`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center space-x-2">
                      <span className="text-lg">{style.icon}</span>
                      <span className="text-sm font-medium">{name}</span>
                    </div>
                    <div className="text-right">
                      <span className="text-xl font-bold">{count}</span>
                    </div>
                  </div>
                  
                  <div className="text-xs opacity-75 mb-2">
                    {count === 1 ? 'violation' : 'violations'}
                  </div>
                  
                  {/* Severity breakdown if available */}
                  {typeof data === 'object' && (data.critical || data.high || data.medium || data.low) && (
                    <div className="flex items-center space-x-1 flex-wrap">
                      {data.critical > 0 && (
                        <span className="px-1.5 py-0.5 text-xs bg-red-200 text-red-800 rounded-full font-medium">
                          {data.critical} Critical
                        </span>
                      )}
                      {data.high > 0 && (
                        <span className="px-1.5 py-0.5 text-xs bg-orange-200 text-orange-800 rounded-full font-medium">
                          {data.high} High
                        </span>
                      )}
                      {data.medium > 0 && (
                        <span className="px-1.5 py-0.5 text-xs bg-yellow-200 text-yellow-800 rounded-full font-medium">
                          {data.medium} Medium
                        </span>
                      )}
                      {data.low > 0 && (
                        <span className="px-1.5 py-0.5 text-xs bg-green-200 text-green-800 rounded-full font-medium">
                          {data.low} Low
                        </span>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>

          {/* Impact Assessment */}
          <div className="p-4 bg-purple-50 border border-purple-200 rounded-md">
            <div className="flex items-start space-x-3">
              <Info className="w-5 h-5 text-purple-600 mt-0.5 flex-shrink-0" />
              <div className="text-sm text-purple-800">
                <div className="font-medium mb-1">Regulatory Compliance Impact Assessment</div>
                <p className="leading-relaxed">
                  These security violations may result in non-compliance with regulatory requirements, 
                  potentially leading to audit findings, regulatory penalties, operational restrictions, 
                  and increased security risk exposure. Immediate remediation is recommended to maintain 
                  compliance posture and avoid regulatory sanctions.
                </p>
                <div className="mt-2 text-xs text-purple-700">
                  <strong>Next Steps:</strong> Review each violation, implement recommended fixes, 
                  and document remediation efforts for audit trail purposes.
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ComplianceOverview;