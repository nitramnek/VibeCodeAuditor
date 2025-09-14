/**
 * Compliance Dashboard Widget
 * Shows compliance status overview on the main dashboard
 */

import React from 'react'
import { Shield, AlertTriangle, CheckCircle, Clock, TrendingUp } from 'lucide-react'
import { useCompliance } from '../hooks/useCompliance'

const ComplianceDashboardWidget = () => {
  const { complianceData, loading, error } = useCompliance()

  if (loading) {
    return (
      <div className="bg-white rounded-xl shadow-modern p-6">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-1/3 mb-4"></div>
          <div className="space-y-3">
            <div className="h-3 bg-gray-200 rounded"></div>
            <div className="h-3 bg-gray-200 rounded w-5/6"></div>
          </div>
        </div>
      </div>
    )
  }

  if (error || !complianceData) {
    return (
      <div className="bg-white rounded-xl shadow-modern p-6">
        <div className="flex items-center text-gray-500">
          <Shield className="h-5 w-5 mr-2" />
          <span className="text-sm">Compliance data unavailable</span>
        </div>
      </div>
    )
  }

  const { overallScore, frameworks, issueStats } = complianceData

  const getScoreColor = (score) => {
    if (score >= 90) return 'text-green-600'
    if (score >= 80) return 'text-yellow-600'
    if (score >= 70) return 'text-orange-600'
    return 'text-red-600'
  }

  const getScoreBgColor = (score) => {
    if (score >= 90) return 'bg-green-100'
    if (score >= 80) return 'bg-yellow-100'
    if (score >= 70) return 'bg-orange-100'
    return 'bg-red-100'
  }

  const compliantFrameworks = frameworks.filter(f => f.score >= 80).length
  const needsAttention = frameworks.filter(f => f.score < 80).length

  return (
    <div className="bg-white rounded-xl shadow-modern p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center">
          <div className="p-2 bg-blue-100 rounded-lg mr-3">
            <Shield className="h-5 w-5 text-blue-600" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900">Compliance Status</h3>
            <p className="text-sm text-gray-600">Regulatory framework compliance</p>
          </div>
        </div>
        <div className="text-right">
          <div className={`text-2xl font-bold ${getScoreColor(overallScore)}`}>
            {overallScore}%
          </div>
          <div className="text-xs text-gray-500">Overall Score</div>
        </div>
      </div>

      {/* Overall Status */}
      <div className={`p-3 rounded-lg mb-4 ${getScoreBgColor(overallScore)}`}>
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            {overallScore >= 80 ? (
              <CheckCircle className="h-5 w-5 text-green-600 mr-2" />
            ) : (
              <AlertTriangle className="h-5 w-5 text-orange-600 mr-2" />
            )}
            <span className={`font-medium ${getScoreColor(overallScore)}`}>
              {overallScore >= 80 ? 'Good Standing' : 'Needs Attention'}
            </span>
          </div>
          <div className="text-sm text-gray-600">
            {frameworks.length} framework{frameworks.length !== 1 ? 's' : ''} monitored
          </div>
        </div>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-2 gap-4 mb-4">
        <div className="text-center">
          <div className="text-xl font-bold text-green-600">{compliantFrameworks}</div>
          <div className="text-xs text-gray-500">Compliant</div>
        </div>
        <div className="text-center">
          <div className="text-xl font-bold text-orange-600">{needsAttention}</div>
          <div className="text-xs text-gray-500">Need Attention</div>
        </div>
      </div>

      {/* Framework List */}
      {frameworks.length > 0 && (
        <div className="space-y-2 mb-4">
          <h4 className="text-sm font-medium text-gray-700">Active Frameworks</h4>
          {frameworks.slice(0, 3).map((framework) => (
            <div key={framework.id} className="flex items-center justify-between py-2">
              <div className="flex items-center">
                <div className={`w-2 h-2 rounded-full mr-2 ${
                  framework.score >= 80 ? 'bg-green-500' : 'bg-orange-500'
                }`}></div>
                <span className="text-sm text-gray-700 truncate">
                  {framework.name.length > 20 ? `${framework.name.substring(0, 20)}...` : framework.name}
                </span>
              </div>
              <span className={`text-sm font-medium ${getScoreColor(framework.score)}`}>
                {framework.score}%
              </span>
            </div>
          ))}
          {frameworks.length > 3 && (
            <div className="text-xs text-gray-500 text-center pt-2">
              +{frameworks.length - 3} more frameworks
            </div>
          )}
        </div>
      )}

      {/* Issue Summary */}
      {issueStats && issueStats.total > 0 && (
        <div className="border-t pt-4">
          <h4 className="text-sm font-medium text-gray-700 mb-2">Open Issues</h4>
          <div className="flex items-center justify-between text-sm">
            <div className="flex space-x-4">
              {issueStats.critical > 0 && (
                <span className="text-red-600 font-medium">
                  {issueStats.critical} Critical
                </span>
              )}
              {issueStats.high > 0 && (
                <span className="text-orange-600 font-medium">
                  {issueStats.high} High
                </span>
              )}
              {issueStats.medium > 0 && (
                <span className="text-yellow-600 font-medium">
                  {issueStats.medium} Medium
                </span>
              )}
            </div>
            <span className="text-gray-500">
              {issueStats.total} total
            </span>
          </div>
        </div>
      )}

      {/* Action Button */}
      <div className="mt-4 pt-4 border-t">
        <button 
          onClick={() => window.location.href = '/compliance'}
          className="w-full inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg text-blue-600 bg-blue-50 hover:bg-blue-100 transition-colors"
        >
          <TrendingUp className="mr-2 h-4 w-4" />
          View Full Compliance Dashboard
        </button>
      </div>
    </div>
  )
}

export default ComplianceDashboardWidget