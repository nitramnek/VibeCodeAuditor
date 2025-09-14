import React, { useState } from 'react';
import { useCompliance } from '../hooks/useCompliance';
import {
  Shield,
  CheckCircle,
  AlertTriangle,
  XCircle,
  FileText,
  Calendar,
  Eye,
  Download,
  Settings,
  BarChart3,
  Clock,
  Target,
  AlertCircle,
  BookOpen,
  Activity,
  X,
  Save
} from 'lucide-react';

const Compliance = () => {
  const { complianceData, loading, error, refetch, updateFramework } = useCompliance();
  const [activeTab, setActiveTab] = useState('overview');
  const [configModal, setConfigModal] = useState({ isOpen: false, framework: null });
  const [configForm, setConfigForm] = useState({
    auditFrequency: 'quarterly',
    notificationEnabled: true,
    autoRemediation: false,
    riskThreshold: 'medium',
    complianceTarget: 90,
    monitoringEnabled: true
  });

  const getStatusColor = (status) => {
    switch (status) {
      case 'compliant': return 'bg-green-100 text-green-800';
      case 'partial': return 'bg-yellow-100 text-yellow-800';
      case 'review': return 'bg-orange-100 text-orange-800';
      case 'non-compliant': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'compliant': return <CheckCircle className="h-4 w-4" />;
      case 'partial': return <AlertTriangle className="h-4 w-4" />;
      case 'review': return <Clock className="h-4 w-4" />;
      case 'non-compliant': return <XCircle className="h-4 w-4" />;
      default: return <AlertCircle className="h-4 w-4" />;
    }
  };

  const getScoreColor = (score) => {
    if (score >= 90) return 'text-green-600';
    if (score >= 80) return 'text-yellow-600';
    if (score >= 70) return 'text-orange-600';
    return 'text-red-600';
  };

  const handleConfigSave = async () => {
    try {
      // Save the configuration to backend via updateFramework
      if (!configModal.framework) {
        console.error('No framework selected for configuration');
        return;
      }
      const updates = {
        auditFrequency: configForm.auditFrequency,
        notificationEnabled: configForm.notificationEnabled,
        autoRemediation: configForm.autoRemediation,
        riskThreshold: configForm.riskThreshold,
        complianceTarget: configForm.complianceTarget,
        monitoringEnabled: configForm.monitoringEnabled
      };
      await updateFramework(configModal.framework.id, updates);
      // Close modal and reset form
      setConfigModal({ isOpen: false, framework: null });
      setConfigForm({
        auditFrequency: 'quarterly',
        notificationEnabled: true,
        autoRemediation: false,
        riskThreshold: 'medium',
        complianceTarget: 90,
        monitoringEnabled: true
      });
    } catch (error) {
      console.error('Error saving configuration:', error);
      // Optionally show error to user
    }
  };

  const handleConfigClose = () => {
    setConfigModal({ isOpen: false, framework: null });
    setConfigForm({
      auditFrequency: 'quarterly',
      notificationEnabled: true,
      autoRemediation: false,
      riskThreshold: 'medium',
      complianceTarget: 90,
      monitoringEnabled: true
    });
  };

  if (loading) {
    return (
      <div className="p-6">
        <div className="flex items-center justify-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <span className="ml-2 text-gray-600">Loading compliance data...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 flex items-center">
            <Shield className="mr-3 h-8 w-8 text-blue-600" />
            Compliance Center
          </h1>
          <p className="mt-2 text-gray-600">
            Monitor and manage regulatory compliance across all frameworks
          </p>
        </div>
        <div className="flex items-center space-x-3">
          <div className="text-right">
            <div className="text-2xl font-bold text-gray-900">{complianceData?.overallScore}%</div>
            <div className="text-sm text-gray-500">Overall Compliance</div>
          </div>
          <div className={`px-4 py-2 rounded-lg ${complianceData?.overallScore >= 80 ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
            {complianceData?.overallScore >= 80 ? 'Good Standing' : 'Needs Attention'}
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="border-b border-gray-200 mb-6">
        <nav className="-mb-px flex space-x-8">
          {[
            { id: 'overview', name: 'Overview', icon: BarChart3 },
            { id: 'frameworks', name: 'Frameworks', icon: Shield },
            { id: 'audits', name: 'Audit History', icon: FileText },
            { id: 'risks', name: 'Risk Assessments', icon: AlertTriangle },
            { id: 'policies', name: 'Policies', icon: BookOpen }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`py-2 px-1 border-b-2 font-medium text-sm flex items-center ${
                activeTab === tab.id
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <tab.icon className="mr-2 h-4 w-4" />
              {tab.name}
            </button>
          ))}
        </nav>
      </div>

      {/* Tab Content */}
      {activeTab === 'overview' && (
        <div className="space-y-6">
          {/* Compliance Score Overview */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="bg-white rounded-xl shadow-modern p-6">
              <div className="flex items-center">
                <div className="p-2 bg-green-100 rounded-lg">
                  <CheckCircle className="h-6 w-6 text-green-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Compliant Frameworks</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {complianceData?.frameworks.filter(f => f.status === 'compliant').length}
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-modern p-6">
              <div className="flex items-center">
                <div className="p-2 bg-yellow-100 rounded-lg">
                  <AlertTriangle className="h-6 w-6 text-yellow-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Needs Attention</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {complianceData?.frameworks.filter(f => f.status !== 'compliant').length}
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-modern p-6">
              <div className="flex items-center">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <FileText className="h-6 w-6 text-blue-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Active Policies</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {complianceData?.policies.filter(p => p.status === 'approved').length}
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-modern p-6">
              <div className="flex items-center">
                <div className="p-2 bg-purple-100 rounded-lg">
                  <Activity className="h-6 w-6 text-purple-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Recent Audits</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {complianceData?.recentAudits.length}
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Framework Status Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {complianceData?.frameworks.map((framework) => (
              <div key={framework.id} className="bg-white rounded-xl shadow-modern p-6">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">{framework.name}</h3>
                    <div className="flex items-center mt-1">
                      {getStatusIcon(framework.status)}
                      <span className={`ml-2 px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(framework.status)}`}>
                        {framework.status}
                      </span>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className={`text-2xl font-bold ${getScoreColor(framework.score)}`}>
                      {framework.score}%
                    </div>
                    <div className="text-xs text-gray-500">Compliance Score</div>
                  </div>
                </div>

                <div className="space-y-3">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Controls Implemented</span>
                    <span className="font-medium">{framework.implemented}/{framework.controls}</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-blue-600 h-2 rounded-full"
                      style={{ width: `${(framework.implemented / framework.controls) * 100}%` }}
                    ></div>
                  </div>

                  <div className="grid grid-cols-3 gap-4 text-center">
                    <div>
                      <div className="text-lg font-bold text-red-600">{framework.criticalIssues}</div>
                      <div className="text-xs text-gray-500">Critical</div>
                    </div>
                    <div>
                      <div className="text-lg font-bold text-orange-600">{framework.highIssues}</div>
                      <div className="text-xs text-gray-500">High</div>
                    </div>
                    <div>
                      <div className="text-lg font-bold text-yellow-600">{framework.mediumIssues}</div>
                      <div className="text-xs text-gray-500">Medium</div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {activeTab === 'frameworks' && (
        <div className="space-y-6">
          {complianceData?.frameworks.map((framework) => (
            <div key={framework.id} className="bg-white rounded-xl shadow-modern p-6">
              <div className="flex justify-between items-start mb-6">
                <div>
                  <h3 className="text-xl font-semibold text-gray-900">{framework.name}</h3>
                  <p className="text-gray-600 mt-1">Framework compliance details and controls</p>
                </div>
                <div className="flex items-center space-x-3">
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(framework.status)}`}>
                    {framework.status}
                  </span>
                  <button
                    className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
                    onClick={() => setConfigModal({ isOpen: true, framework })}
                  >
                    <Settings className="mr-2 h-4 w-4" />
                    Configure
                  </button>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="space-y-4">
                  <h4 className="font-medium text-gray-900">Compliance Score</h4>
                  <div className="text-3xl font-bold text-blue-600">{framework.score}%</div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div
                      className="bg-blue-600 h-3 rounded-full"
                      style={{ width: `${framework.score}%` }}
                    ></div>
                  </div>
                </div>

                <div className="space-y-4">
                  <h4 className="font-medium text-gray-900">Audit Schedule</h4>
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">Last Audit</span>
                      <span className="font-medium">{new Date(framework.lastAudit).toLocaleDateString()}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">Next Audit</span>
                      <span className="font-medium">{new Date(framework.nextAudit).toLocaleDateString()}</span>
                    </div>
                  </div>
                </div>

                <div className="space-y-4">
                  <h4 className="font-medium text-gray-900">Issues Summary</h4>
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span className="text-red-600">Critical</span>
                      <span className="font-medium">{framework.criticalIssues}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-orange-600">High</span>
                      <span className="font-medium">{framework.highIssues}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-yellow-600">Medium</span>
                      <span className="font-medium">{framework.mediumIssues}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {activeTab === 'audits' && (
        <div className="space-y-6">
          <div className="flex justify-between items-center">
            <h2 className="text-xl font-semibold text-gray-900">Audit History</h2>
            <button className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg text-white bg-blue-600 hover:bg-blue-700">
              <FileText className="mr-2 h-4 w-4" />
              Schedule Audit
            </button>
          </div>

          <div className="bg-white rounded-xl shadow-modern overflow-hidden">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Framework
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Type
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Date
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Findings
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {complianceData?.recentAudits.map((audit) => (
                  <tr key={audit.id}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {audit.framework}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {audit.type}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {new Date(audit.date).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        audit.status === 'passed' ? 'bg-green-100 text-green-800' :
                        audit.status === 'needs_attention' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {audit.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {audit.findings} ({audit.critical} critical)
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      <button className="text-blue-600 hover:text-blue-900">
                        <Eye className="h-4 w-4" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {activeTab === 'risks' && (
        <div className="space-y-6">
          <div className="flex justify-between items-center">
            <h2 className="text-xl font-semibold text-gray-900">Risk Assessments</h2>
            <button className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg text-white bg-blue-600 hover:bg-blue-700">
              <Target className="mr-2 h-4 w-4" />
              New Assessment
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {complianceData?.riskAssessments.map((assessment) => (
              <div key={assessment.id} className="bg-white rounded-xl shadow-modern p-6">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">{assessment.title}</h3>
                    <p className="text-sm text-gray-600">{assessment.framework}</p>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                    assessment.status === 'completed' ? 'bg-green-100 text-green-800' :
                    assessment.status === 'in_progress' ? 'bg-blue-100 text-blue-800' :
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {assessment.status}
                  </span>
                </div>

                <div className="space-y-3">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Risk Score</span>
                    <span className={`font-medium ${getScoreColor(assessment.score)}`}>
                      {assessment.score}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-orange-500 h-2 rounded-full"
                      style={{ width: `${assessment.score}%` }}
                    ></div>
                  </div>

                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="text-gray-600">Last Updated</span>
                      <div className="font-medium">{new Date(assessment.lastUpdated).toLocaleDateString()}</div>
                    </div>
                    <div>
                      <span className="text-gray-600">Next Review</span>
                      <div className="font-medium">{new Date(assessment.nextReview).toLocaleDateString()}</div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {activeTab === 'policies' && (
        <div className="space-y-6">
          <div className="flex justify-between items-center">
            <h2 className="text-xl font-semibold text-gray-900">Policy Management</h2>
            <button className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg text-white bg-blue-600 hover:bg-blue-700">
              <BookOpen className="mr-2 h-4 w-4" />
              Create Policy
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {complianceData?.policies.map((policy) => (
              <div key={policy.id} className="bg-white rounded-xl shadow-modern p-6">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">{policy.title}</h3>
                    <p className="text-sm text-gray-600">{policy.framework} • v{policy.version}</p>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                    policy.status === 'approved' ? 'bg-green-100 text-green-800' :
                    policy.status === 'draft' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {policy.status}
                  </span>
                </div>

                <div className="space-y-3">
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="text-gray-600">Last Reviewed</span>
                      <div className="font-medium">{new Date(policy.lastReviewed).toLocaleDateString()}</div>
                    </div>
                    <div>
                      <span className="text-gray-600">Next Review</span>
                      <div className="font-medium">{new Date(policy.nextReview).toLocaleDateString()}</div>
                    </div>
                  </div>

                  <div className="flex justify-between items-center pt-3">
                    <div className="flex space-x-2">
                      <button className="inline-flex items-center px-3 py-1 border border-gray-300 rounded text-xs font-medium text-gray-700 bg-white hover:bg-gray-50">
                        <Eye className="mr-1 h-3 w-3" />
                        View
                      </button>
                      <button className="inline-flex items-center px-3 py-1 border border-gray-300 rounded text-xs font-medium text-gray-700 bg-white hover:bg-gray-50">
                        <Download className="mr-1 h-3 w-3" />
                        Download
                      </button>
                    </div>
                    <button className="inline-flex items-center px-3 py-1 border border-transparent text-xs font-medium text-blue-600 bg-blue-50 hover:bg-blue-100 rounded">
                      <Settings className="mr-1 h-3 w-3" />
                      Edit
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Configuration Modal */}
      {configModal.isOpen && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-semibold text-gray-900 flex items-center">
                <Settings className="mr-2 h-5 w-5 text-blue-600" />
                Configure {configModal.framework?.name}
              </h3>
              <button
                onClick={handleConfigClose}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="h-6 w-6" />
              </button>
            </div>

            <div className="space-y-6">
              {/* Audit Frequency */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Audit Frequency
                </label>
                <select
                  value={configForm.auditFrequency}
                  onChange={(e) => setConfigForm({ ...configForm, auditFrequency: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="monthly">Monthly</option>
                  <option value="quarterly">Quarterly</option>
                  <option value="semi-annual">Semi-Annual</option>
                  <option value="annual">Annual</option>
                </select>
              </div>

              {/* Compliance Target */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Compliance Target (%)
                </label>
                <input
                  type="number"
                  min="0"
                  max="100"
                  value={configForm.complianceTarget}
                  onChange={(e) => setConfigForm({ ...configForm, complianceTarget: parseInt(e.target.value) })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              {/* Risk Threshold */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Risk Threshold
                </label>
                <select
                  value={configForm.riskThreshold}
                  onChange={(e) => setConfigForm({ ...configForm, riskThreshold: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                  <option value="critical">Critical</option>
                </select>
              </div>

              {/* Toggle Options */}
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium text-gray-700">Enable Notifications</label>
                    <p className="text-xs text-gray-500">Receive alerts for compliance issues</p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={configForm.notificationEnabled}
                      onChange={(e) => setConfigForm({ ...configForm, notificationEnabled: e.target.checked })}
                      className="sr-only peer"
                    />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                  </label>
                </div>

                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium text-gray-700">Auto Remediation</label>
                    <p className="text-xs text-gray-500">Automatically fix minor compliance issues</p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={configForm.autoRemediation}
                      onChange={(e) => setConfigForm({ ...configForm, autoRemediation: e.target.checked })}
                      className="sr-only peer"
                    />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                  </label>
                </div>

                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium text-gray-700">Continuous Monitoring</label>
                    <p className="text-xs text-gray-500">Monitor compliance in real-time</p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={configForm.monitoringEnabled}
                      onChange={(e) => setConfigForm({ ...configForm, monitoringEnabled: e.target.checked })}
                      className="sr-only peer"
                    />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                  </label>
                </div>
              </div>
            </div>

            <div className="flex justify-end space-x-3 mt-6 pt-4 border-t">
              <button
                onClick={handleConfigClose}
                className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                onClick={handleConfigSave}
                className="px-4 py-2 border border-transparent rounded-md text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
              >
                <Save className="mr-2 h-4 w-4" />
                Save Configuration
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Compliance;
