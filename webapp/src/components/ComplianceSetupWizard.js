/**
 * Compliance Setup Wizard
 * Helps users set up their compliance frameworks
 */

import React, { useState } from 'react'
import { Shield, CheckCircle, ArrowRight, ArrowLeft, X } from 'lucide-react'
import { useCompliance } from '../hooks/useCompliance'

const FRAMEWORK_OPTIONS = [
  {
    code: 'gdpr',
    name: 'General Data Protection Regulation (GDPR)',
    description: 'EU data protection regulation for personal data handling',
    icon: '🇪🇺',
    category: 'Privacy',
    recommended: ['web applications', 'user data', 'european users']
  },
  {
    code: 'hipaa',
    name: 'Health Insurance Portability and Accountability Act (HIPAA)',
    description: 'US healthcare data protection requirements',
    icon: '🏥',
    category: 'Healthcare',
    recommended: ['healthcare', 'medical data', 'phi']
  },
  {
    code: 'soc2',
    name: 'Service Organization Control 2 (SOC 2)',
    description: 'Trust services criteria for service organizations',
    icon: '🛡️',
    category: 'Security',
    recommended: ['saas', 'cloud services', 'customer data']
  },
  {
    code: 'iso27001',
    name: 'ISO 27001',
    description: 'International information security management standard',
    icon: '🏛️',
    category: 'Security',
    recommended: ['enterprise', 'information security', 'risk management']
  },
  {
    code: 'pci_dss',
    name: 'Payment Card Industry Data Security Standard (PCI DSS)',
    description: 'Security standards for payment card data',
    icon: '💳',
    category: 'Financial',
    recommended: ['payments', 'credit cards', 'financial data']
  },
  {
    code: 'nist',
    name: 'NIST Cybersecurity Framework',
    description: 'US cybersecurity framework for critical infrastructure',
    icon: '🏛️',
    category: 'Security',
    recommended: ['government', 'critical infrastructure', 'cybersecurity']
  }
]

const ComplianceSetupWizard = ({ isOpen, onClose, onComplete }) => {
  const [currentStep, setCurrentStep] = useState(1)
  const [selectedFrameworks, setSelectedFrameworks] = useState([])
  const [organizationInfo, setOrganizationInfo] = useState({
    industry: '',
    size: '',
    dataTypes: [],
    regions: []
  })
  const [loading, setLoading] = useState(false)
  const { createFramework } = useCompliance()

  const steps = [
    { id: 1, name: 'Organization Info', description: 'Tell us about your organization' },
    { id: 2, name: 'Select Frameworks', description: 'Choose applicable compliance frameworks' },
    { id: 3, name: 'Configuration', description: 'Configure framework settings' },
    { id: 4, name: 'Complete', description: 'Review and finish setup' }
  ]

  if (!isOpen) return null

  const handleFrameworkToggle = (framework) => {
    setSelectedFrameworks(prev => {
      const exists = prev.find(f => f.code === framework.code)
      if (exists) {
        return prev.filter(f => f.code !== framework.code)
      } else {
        return [...prev, framework]
      }
    })
  }

  const getRecommendedFrameworks = () => {
    const { industry, dataTypes, regions } = organizationInfo
    const recommended = []

    // Industry-based recommendations
    if (industry === 'healthcare') recommended.push('hipaa')
    if (industry === 'financial') recommended.push('pci_dss', 'soc2')
    if (industry === 'technology') recommended.push('soc2', 'iso27001')
    if (industry === 'government') recommended.push('nist', 'iso27001')

    // Data type recommendations
    if (dataTypes.includes('personal_data')) recommended.push('gdpr')
    if (dataTypes.includes('health_data')) recommended.push('hipaa')
    if (dataTypes.includes('payment_data')) recommended.push('pci_dss')

    // Region recommendations
    if (regions.includes('eu')) recommended.push('gdpr')
    if (regions.includes('us')) recommended.push('soc2', 'nist')

    return [...new Set(recommended)]
  }

  const handleComplete = async () => {
    setLoading(true)
    try {
      // Create selected frameworks
      for (const framework of selectedFrameworks) {
        await createFramework({
          name: framework.name,
          code: framework.code,
          description: framework.description,
          status: 'active',
          compliance_score: 0,
          total_controls: 0,
          implemented_controls: 0,
          audit_frequency: 'annual'
        })
      }

      onComplete()
    } catch (error) {
      console.error('Error setting up compliance frameworks:', error)
    } finally {
      setLoading(false)
    }
  }

  const renderStep1 = () => (
    <div className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Industry
        </label>
        <select
          value={organizationInfo.industry}
          onChange={(e) => setOrganizationInfo(prev => ({ ...prev, industry: e.target.value }))}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value="">Select your industry</option>
          <option value="technology">Technology</option>
          <option value="healthcare">Healthcare</option>
          <option value="financial">Financial Services</option>
          <option value="retail">Retail</option>
          <option value="government">Government</option>
          <option value="education">Education</option>
          <option value="other">Other</option>
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Organization Size
        </label>
        <select
          value={organizationInfo.size}
          onChange={(e) => setOrganizationInfo(prev => ({ ...prev, size: e.target.value }))}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value="">Select organization size</option>
          <option value="startup">Startup (1-10 employees)</option>
          <option value="small">Small (11-50 employees)</option>
          <option value="medium">Medium (51-200 employees)</option>
          <option value="large">Large (201-1000 employees)</option>
          <option value="enterprise">Enterprise (1000+ employees)</option>
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Types of Data You Handle
        </label>
        <div className="space-y-2">
          {[
            { value: 'personal_data', label: 'Personal Data (names, emails, addresses)' },
            { value: 'health_data', label: 'Health Information (PHI, medical records)' },
            { value: 'payment_data', label: 'Payment Information (credit cards, financial)' },
            { value: 'sensitive_data', label: 'Sensitive Business Data' }
          ].map((dataType) => (
            <label key={dataType.value} className="flex items-center">
              <input
                type="checkbox"
                checked={organizationInfo.dataTypes.includes(dataType.value)}
                onChange={(e) => {
                  const checked = e.target.checked
                  setOrganizationInfo(prev => ({
                    ...prev,
                    dataTypes: checked
                      ? [...prev.dataTypes, dataType.value]
                      : prev.dataTypes.filter(t => t !== dataType.value)
                  }))
                }}
                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              <span className="ml-2 text-sm text-gray-700">{dataType.label}</span>
            </label>
          ))}
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Operating Regions
        </label>
        <div className="space-y-2">
          {[
            { value: 'us', label: 'United States' },
            { value: 'eu', label: 'European Union' },
            { value: 'canada', label: 'Canada' },
            { value: 'asia', label: 'Asia Pacific' },
            { value: 'global', label: 'Global' }
          ].map((region) => (
            <label key={region.value} className="flex items-center">
              <input
                type="checkbox"
                checked={organizationInfo.regions.includes(region.value)}
                onChange={(e) => {
                  const checked = e.target.checked
                  setOrganizationInfo(prev => ({
                    ...prev,
                    regions: checked
                      ? [...prev.regions, region.value]
                      : prev.regions.filter(r => r !== region.value)
                  }))
                }}
                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              <span className="ml-2 text-sm text-gray-700">{region.label}</span>
            </label>
          ))}
        </div>
      </div>
    </div>
  )

  const renderStep2 = () => {
    const recommended = getRecommendedFrameworks()
    
    return (
      <div className="space-y-6">
        {recommended.length > 0 && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h4 className="text-sm font-medium text-blue-900 mb-2">Recommended for You</h4>
            <p className="text-sm text-blue-700">
              Based on your organization profile, we recommend these frameworks:
            </p>
            <div className="mt-2 flex flex-wrap gap-2">
              {recommended.map(code => {
                const framework = FRAMEWORK_OPTIONS.find(f => f.code === code)
                return framework ? (
                  <span key={code} className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
                    {framework.icon} {framework.name.split('(')[0].trim()}
                  </span>
                ) : null
              })}
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 gap-4">
          {FRAMEWORK_OPTIONS.map((framework) => {
            const isSelected = selectedFrameworks.find(f => f.code === framework.code)
            const isRecommended = recommended.includes(framework.code)
            
            return (
              <div
                key={framework.code}
                onClick={() => handleFrameworkToggle(framework)}
                className={`relative p-4 border-2 rounded-lg cursor-pointer transition-all ${
                  isSelected
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-gray-300'
                } ${isRecommended ? 'ring-2 ring-blue-200' : ''}`}
              >
                <div className="flex items-start space-x-3">
                  <div className="text-2xl">{framework.icon}</div>
                  <div className="flex-1">
                    <div className="flex items-center justify-between">
                      <h3 className="text-sm font-medium text-gray-900">
                        {framework.name}
                        {isRecommended && (
                          <span className="ml-2 px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">
                            Recommended
                          </span>
                        )}
                      </h3>
                      {isSelected && (
                        <CheckCircle className="h-5 w-5 text-blue-600" />
                      )}
                    </div>
                    <p className="text-sm text-gray-600 mt-1">{framework.description}</p>
                    <div className="mt-2">
                      <span className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-full">
                        {framework.category}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      </div>
    )
  }

  const renderStep3 = () => (
    <div className="space-y-6">
      <div className="bg-gray-50 rounded-lg p-4">
        <h4 className="text-sm font-medium text-gray-900 mb-2">Selected Frameworks</h4>
        <div className="space-y-2">
          {selectedFrameworks.map((framework) => (
            <div key={framework.code} className="flex items-center space-x-3">
              <div className="text-lg">{framework.icon}</div>
              <div>
                <div className="text-sm font-medium text-gray-900">{framework.name}</div>
                <div className="text-xs text-gray-600">Initial setup with basic controls</div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h4 className="text-sm font-medium text-blue-900 mb-2">What happens next?</h4>
        <ul className="text-sm text-blue-700 space-y-1">
          <li>• Frameworks will be created with default configurations</li>
          <li>• You can customize controls and requirements later</li>
          <li>• Security scans will automatically map to these frameworks</li>
          <li>• Compliance dashboards will track your progress</li>
        </ul>
      </div>
    </div>
  )

  const renderStep4 = () => (
    <div className="text-center space-y-6">
      <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto">
        <CheckCircle className="h-8 w-8 text-green-600" />
      </div>
      <div>
        <h3 className="text-lg font-medium text-gray-900">Setup Complete!</h3>
        <p className="text-gray-600 mt-2">
          Your compliance frameworks have been configured successfully.
        </p>
      </div>
      <div className="bg-gray-50 rounded-lg p-4">
        <h4 className="text-sm font-medium text-gray-900 mb-2">
          {selectedFrameworks.length} Framework{selectedFrameworks.length !== 1 ? 's' : ''} Created
        </h4>
        <div className="space-y-1">
          {selectedFrameworks.map((framework) => (
            <div key={framework.code} className="text-sm text-gray-600">
              {framework.icon} {framework.name}
            </div>
          ))}
        </div>
      </div>
    </div>
  )

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl shadow-xl max-w-2xl w-full mx-4 max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b">
          <div className="flex items-center">
            <Shield className="h-6 w-6 text-blue-600 mr-3" />
            <div>
              <h2 className="text-xl font-semibold text-gray-900">Compliance Setup</h2>
              <p className="text-sm text-gray-600">Configure your regulatory compliance frameworks</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <X className="h-5 w-5 text-gray-500" />
          </button>
        </div>

        {/* Progress Steps */}
        <div className="px-6 py-4 border-b">
          <div className="flex items-center justify-between">
            {steps.map((step, index) => (
              <div key={step.id} className="flex items-center">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${
                  currentStep >= step.id
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-200 text-gray-600'
                }`}>
                  {step.id}
                </div>
                <div className="ml-2 hidden sm:block">
                  <div className={`text-sm font-medium ${
                    currentStep >= step.id ? 'text-blue-600' : 'text-gray-500'
                  }`}>
                    {step.name}
                  </div>
                </div>
                {index < steps.length - 1 && (
                  <ArrowRight className="h-4 w-4 text-gray-400 mx-4" />
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto max-h-96">
          {currentStep === 1 && renderStep1()}
          {currentStep === 2 && renderStep2()}
          {currentStep === 3 && renderStep3()}
          {currentStep === 4 && renderStep4()}
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between p-6 border-t bg-gray-50">
          <button
            onClick={() => setCurrentStep(prev => Math.max(1, prev - 1))}
            disabled={currentStep === 1}
            className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <ArrowLeft className="mr-2 h-4 w-4" />
            Previous
          </button>

          <div className="text-sm text-gray-500">
            Step {currentStep} of {steps.length}
          </div>

          {currentStep < 4 ? (
            <button
              onClick={() => setCurrentStep(prev => Math.min(4, prev + 1))}
              disabled={
                (currentStep === 1 && !organizationInfo.industry) ||
                (currentStep === 2 && selectedFrameworks.length === 0)
              }
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next
              <ArrowRight className="ml-2 h-4 w-4" />
            </button>
          ) : (
            <button
              onClick={handleComplete}
              disabled={loading}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg text-white bg-green-600 hover:bg-green-700 disabled:opacity-50"
            >
              {loading ? 'Setting up...' : 'Complete Setup'}
              <CheckCircle className="ml-2 h-4 w-4" />
            </button>
          )}
        </div>
      </div>
    </div>
  )
}

export default ComplianceSetupWizard