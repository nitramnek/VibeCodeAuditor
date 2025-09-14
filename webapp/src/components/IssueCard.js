import React, { useState } from 'react';
import { AlertTriangle, CheckCircle, Info, XCircle, ChevronDown, ChevronUp, ExternalLink, Shield, BookOpen } from 'lucide-react';

const IssueCard = ({ issue, index }) => {
  const [showDetails, setShowDetails] = useState(false);

  const severityColors = {
    critical: 'text-red-600 bg-red-50 border-red-200',
    high: 'text-orange-600 bg-orange-50 border-orange-200',
    medium: 'text-yellow-600 bg-yellow-50 border-yellow-200',
    low: 'text-green-600 bg-green-50 border-green-200',
  };

  const severityIcons = {
    critical: XCircle,
    high: AlertTriangle,
    medium: Info,
    low: CheckCircle,
  };

  const Icon = severityIcons[issue.severity];

  // Helper function to render standards badges
  const renderStandardsBadges = () => {
    const badges = [];
    
    // Check metadata for quick standards references
    if (issue.metadata?.iso27001) {
      badges.push(
        <span key="iso-meta" className="inline-flex items-center px-2 py-1 text-xs bg-red-100 text-red-800 rounded-full border border-red-200">
          <Shield className="w-3 h-3 mr-1" />
          ISO 27001: {issue.metadata.iso27001}
        </span>
      );
    }
    
    if (issue.metadata?.owasp) {
      badges.push(
        <span key="owasp-meta" className="inline-flex items-center px-2 py-1 text-xs bg-orange-100 text-orange-800 rounded-full border border-orange-200">
          <Shield className="w-3 h-3 mr-1" />
          OWASP: {issue.metadata.owasp}
        </span>
      );
    }
    
    if (issue.metadata?.cwe) {
      badges.push(
        <span key="cwe-meta" className="inline-flex items-center px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-full border border-blue-200">
          <BookOpen className="w-3 h-3 mr-1" />
          {issue.metadata.cwe}
        </span>
      );
    }
    
    if (issue.metadata?.gdpr) {
      badges.push(
        <span key="gdpr-meta" className="inline-flex items-center px-2 py-1 text-xs bg-green-100 text-green-800 rounded-full border border-green-200">
          <Shield className="w-3 h-3 mr-1" />
          GDPR: {issue.metadata.gdpr}
        </span>
      );
    }

    // Check standards array for additional compliance references
    if (issue.standards && issue.standards.length > 0) {
      const uniqueFrameworks = [...new Set(issue.standards.map(s => s.name))];
      uniqueFrameworks.slice(0, 3).forEach((framework, idx) => {
        if (!badges.some(badge => badge.key && badge.key.includes(framework.toLowerCase()))) {
          badges.push(
            <span key={`std-${idx}`} className="inline-flex items-center px-2 py-1 text-xs bg-purple-100 text-purple-800 rounded-full border border-purple-200">
              <Shield className="w-3 h-3 mr-1" />
              {framework}
            </span>
          );
        }
      });
    }

    // Check compliance_frameworks for additional references
    if (issue.compliance_frameworks && issue.compliance_frameworks.length > 0) {
      issue.compliance_frameworks.slice(0, 2).forEach((framework, idx) => {
        if (!badges.some(badge => badge.key && badge.key.includes(framework.toLowerCase()))) {
          badges.push(
            <span key={`comp-${idx}`} className="inline-flex items-center px-2 py-1 text-xs bg-indigo-100 text-indigo-800 rounded-full border border-indigo-200">
              <Shield className="w-3 h-3 mr-1" />
              {framework}
            </span>
          );
        }
      });
    }

    return badges.length > 0 ? (
      <div className="flex flex-wrap gap-2 mb-3">
        {badges}
        {(issue.standards?.length > 3 || issue.compliance_frameworks?.length > 2) && (
          <span className="inline-flex items-center px-2 py-1 text-xs bg-gray-100 text-gray-600 rounded-full border border-gray-200">
            +{Math.max(0, (issue.standards?.length || 0) + (issue.compliance_frameworks?.length || 0) - badges.length)} more
          </span>
        )}
      </div>
    ) : null;
  };

  // Helper function to render detailed standards
  const renderDetailedStandards = () => {
    if (!issue.standards || issue.standards.length === 0) return null;

    return (
      <div className="bg-purple-50 border border-purple-200 p-4 rounded-md mb-3">
        <div className="flex items-center justify-between mb-3">
          <h4 className="text-sm font-semibold text-purple-900 flex items-center">
            <Shield className="w-4 h-4 mr-2" />
            Compliance Standards Violated
          </h4>
          <span className="text-xs text-purple-700 bg-purple-100 px-2 py-1 rounded-full">
            {issue.standards.length} standard{issue.standards.length !== 1 ? 's' : ''}
          </span>
        </div>
        <div className="space-y-2">
          {issue.standards.slice(0, 6).map((standard, idx) => (
            <div key={idx} className="flex items-center justify-between p-3 bg-white rounded border hover:bg-gray-50 transition-colors">
              <div className="flex items-center space-x-3">
                <div className="flex-shrink-0">
                  <Shield className="w-4 h-4 text-purple-600" />
                </div>
                <div>
                  <span className="text-sm font-medium text-gray-900">{standard.name}</span>
                  {standard.section && (
                    <div className="flex items-center space-x-2 mt-1">
                      <span className="text-xs text-gray-600 bg-gray-100 px-2 py-1 rounded">
                        {standard.section}
                      </span>
                      {standard.description && (
                        <span className="text-xs text-gray-500 truncate max-w-xs">
                          {standard.description}
                        </span>
                      )}
                    </div>
                  )}
                </div>
              </div>
              {standard.url && (
                <a 
                  href={standard.url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="flex items-center space-x-1 text-xs text-purple-600 hover:text-purple-800 transition-colors px-2 py-1 rounded hover:bg-purple-100"
                >
                  <span>View</span>
                  <ExternalLink className="h-3 w-3" />
                </a>
              )}
            </div>
          ))}
          {issue.standards.length > 6 && (
            <div className="text-center pt-2">
              <span className="text-xs text-purple-600 bg-purple-100 px-3 py-1 rounded-full">
                +{issue.standards.length - 6} more standards
              </span>
            </div>
          )}
        </div>
      </div>
    );
  };

  // Helper function to render compliance frameworks
  const renderComplianceFrameworks = () => {
    if (!issue.compliance_frameworks || issue.compliance_frameworks.length === 0) return null;

    const frameworkColors = {
      'ISO 27001': 'bg-red-100 text-red-700 border-red-200',
      'OWASP': 'bg-orange-100 text-orange-700 border-orange-200',
      'GDPR': 'bg-green-100 text-green-700 border-green-200',
      'PCI DSS': 'bg-blue-100 text-blue-700 border-blue-200',
      'HIPAA': 'bg-purple-100 text-purple-700 border-purple-200',
      'NIST': 'bg-indigo-100 text-indigo-700 border-indigo-200',
    };

    return (
      <div className="bg-red-50 border border-red-200 p-4 rounded-md mb-3">
        <div className="flex items-center justify-between mb-3">
          <p className="text-sm font-semibold text-red-900 flex items-center">
            <AlertTriangle className="w-4 h-4 mr-2" />
            Regulatory Compliance Impact
          </p>
          <span className="text-xs text-red-700 bg-red-100 px-2 py-1 rounded-full">
            {issue.compliance_frameworks.length} framework{issue.compliance_frameworks.length !== 1 ? 's' : ''} affected
          </span>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
          {issue.compliance_frameworks.map((framework, idx) => {
            const colorClass = frameworkColors[framework] || 'bg-gray-100 text-gray-700 border-gray-200';
            return (
              <div key={idx} className={`px-3 py-2 text-sm rounded-md border ${colorClass} flex items-center justify-between`}>
                <div className="flex items-center space-x-2">
                  <Shield className="w-3 h-3" />
                  <span className="font-medium">{framework}</span>
                </div>
                <span className="text-xs opacity-75">Violation</span>
              </div>
            );
          })}
        </div>
        <div className="mt-3 p-2 bg-red-100 rounded text-xs text-red-800">
          <strong>Impact:</strong> This security issue may result in non-compliance with the above regulatory frameworks, potentially leading to audit failures, penalties, or security breaches.
        </div>
      </div>
    );
  };

  return (
    <div className={`bg-white rounded-lg shadow-sm border-l-4 ${severityColors[issue.severity]} p-6 hover:shadow-md transition-all duration-200 animate-fade-in`}>
      <div className="flex items-start space-x-4">
        <Icon className={`h-6 w-6 mt-1 ${severityColors[issue.severity].split(' ')[0]}`} />
        <div className="flex-1">
          {/* Header */}
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-lg font-semibold text-gray-900">{issue.rule_id}</h3>
            <div className="flex items-center space-x-2">
              <span className={`px-2 py-1 text-xs font-medium rounded-full ${severityColors[issue.severity]}`}>
                {issue.severity.toUpperCase()}
              </span>
              <span className="px-2 py-1 text-xs font-medium rounded-full bg-gray-100 text-gray-800">
                {issue.category}
              </span>
              {(issue.standards && issue.standards.length > 0) && (
                <span className="px-2 py-1 text-xs font-medium rounded-full bg-purple-100 text-purple-800 flex items-center">
                  <Shield className="w-3 h-3 mr-1" />
                  {issue.standards.length} Standards
                </span>
              )}
              {(issue.compliance_frameworks && issue.compliance_frameworks.length > 0) && (
                <span className="px-2 py-1 text-xs font-medium rounded-full bg-red-100 text-red-800 flex items-center">
                  <AlertTriangle className="w-3 h-3 mr-1" />
                  {issue.compliance_frameworks.length} Compliance
                </span>
              )}
            </div>
          </div>

          {/* Quick Compliance Summary - always visible for high-impact issues */}
          {(issue.compliance_frameworks?.length > 0 || issue.standards?.length > 0) && (
            <div className={`border p-3 rounded-md mb-3 ${
              issue.severity === 'critical' ? 'bg-red-50 border-red-200' :
              issue.severity === 'high' ? 'bg-orange-50 border-orange-200' :
              'bg-yellow-50 border-yellow-200'
            }`}>
              <div className="flex items-start space-x-2">
                <AlertTriangle className={`w-4 h-4 mt-0.5 flex-shrink-0 ${
                  issue.severity === 'critical' ? 'text-red-600' :
                  issue.severity === 'high' ? 'text-orange-600' :
                  'text-yellow-600'
                }`} />
                <div className="text-sm">
                  <span className={`font-medium ${
                    issue.severity === 'critical' ? 'text-red-800' :
                    issue.severity === 'high' ? 'text-orange-800' :
                    'text-yellow-800'
                  }`}>
                    {issue.severity === 'critical' ? 'Critical Compliance Risk:' :
                     issue.severity === 'high' ? 'High Compliance Risk:' :
                     'Compliance Alert:'}
                  </span>
                  <span className={`ml-1 ${
                    issue.severity === 'critical' ? 'text-red-700' :
                    issue.severity === 'high' ? 'text-orange-700' :
                    'text-yellow-700'
                  }`}>
                    This issue violates {issue.compliance_frameworks?.length || 0} regulatory framework{(issue.compliance_frameworks?.length || 0) !== 1 ? 's' : ''} 
                    {issue.standards?.length > 0 && ` and ${issue.standards.length} security standard${issue.standards.length !== 1 ? 's' : ''}`}.
                    {issue.severity === 'critical' && ' Immediate remediation required to avoid audit failures.'}
                  </span>
                </div>
              </div>
            </div>
          )}

          {/* Standards badges - always visible */}
          {renderStandardsBadges()}

          {/* Message */}
          <p className="text-gray-700 mb-3">{issue.message}</p>

          {/* File info */}
          <div className="text-sm text-gray-600 mb-3">
            <span className="font-medium">File:</span> {issue.file_path}
            {issue.line_number && (
              <>
                <span className="mx-2">•</span>
                <span className="font-medium">Line:</span> {issue.line_number}
              </>
            )}
          </div>

          {/* Code snippet */}
          {issue.code_snippet && (
            <div className="bg-gray-50 p-3 rounded-md mb-3">
              <p className="text-sm font-medium text-gray-700 mb-1">Code:</p>
              <code className="text-sm text-gray-800 font-mono">{issue.code_snippet}</code>
            </div>
          )}

          {/* Show/Hide Details Button */}
          {(issue.standards || issue.compliance_frameworks || issue.metadata) && (
            <button
              onClick={() => setShowDetails(!showDetails)}
              className="flex items-center space-x-2 text-sm text-blue-600 hover:text-blue-800 mb-3"
            >
              {showDetails ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
              <span>{showDetails ? 'Hide' : 'Show'} Standards & Compliance Details</span>
            </button>
          )}

          {/* Detailed Standards - collapsible */}
          {showDetails && (
            <div className="space-y-3">
              {renderDetailedStandards()}
              {renderComplianceFrameworks()}
              
              {/* Technical metadata */}
              {issue.metadata && (
                <div className="bg-gray-50 p-3 rounded-md">
                  <p className="text-sm font-medium text-gray-700 mb-2 flex items-center">
                    <Info className="w-4 h-4 mr-2" />
                    Technical Details
                  </p>
                  <div className="grid grid-cols-2 gap-2 text-xs">
                    {Object.entries(issue.metadata).map(([key, value]) => (
                      <div key={key}>
                        <span className="font-medium text-gray-600 capitalize">{key.replace('_', ' ')}:</span>
                        <span className="ml-1 text-gray-800">{value}</span>
                      </div>
                    ))}
                    {issue.confidence && (
                      <div>
                        <span className="font-medium text-gray-600">Confidence:</span>
                        <span className="ml-1 text-gray-800">{Math.round(issue.confidence * 100)}%</span>
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Remediation */}
          {issue.remediation && (
            <div className="bg-blue-50 p-3 rounded-md">
              <p className="text-sm font-medium text-blue-800 mb-1 flex items-center">
                <CheckCircle className="w-4 h-4 mr-2" />
                Remediation
              </p>
              <p className="text-sm text-blue-700">{issue.remediation}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default IssueCard;