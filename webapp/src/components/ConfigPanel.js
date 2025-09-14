import React from 'react';

const ConfigPanel = ({ config, onChange }) => {
  const handleChange = (field, value) => {
    onChange({
      ...config,
      [field]: value
    });
  };

  return (
    <div className="space-y-6">
      {/* Severity Settings */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Minimum Severity Level
        </label>
        <select
          value={config?.min_severity || 'medium'}
          onChange={(e) => handleChange('min_severity', e.target.value)}
          className="w-full border border-gray-300 rounded-md px-3 py-2"
        >
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
          <option value="critical">Critical</option>
        </select>
      </div>

      {/* AI/ML Checks */}
      <div>
        <h3 className="text-sm font-medium text-gray-700 mb-3">AI/ML Specific Checks</h3>
        <div className="space-y-2">
          <div className="flex items-center">
            <input
              type="checkbox"
              id="check_data_privacy"
              checked={config?.check_data_privacy ?? true}
              onChange={(e) => handleChange('check_data_privacy', e.target.checked)}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label htmlFor="check_data_privacy" className="ml-2 text-sm text-gray-700">
              Data Privacy Compliance
            </label>
          </div>
          
          <div className="flex items-center">
            <input
              type="checkbox"
              id="check_model_security"
              checked={config?.check_model_security ?? true}
              onChange={(e) => handleChange('check_model_security', e.target.checked)}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label htmlFor="check_model_security" className="ml-2 text-sm text-gray-700">
              Model Security Issues
            </label>
          </div>
          
          <div className="flex items-center">
            <input
              type="checkbox"
              id="check_bias_detection"
              checked={config?.check_bias_detection ?? true}
              onChange={(e) => handleChange('check_bias_detection', e.target.checked)}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label htmlFor="check_bias_detection" className="ml-2 text-sm text-gray-700">
              Bias Detection
            </label>
          </div>
        </div>
      </div>

      {/* Report Settings */}
      <div>
        <h3 className="text-sm font-medium text-gray-700 mb-3">Report Settings</h3>
        <div className="space-y-2">
          <div className="flex items-center">
            <input
              type="checkbox"
              id="include_code_snippets"
              checked={config?.include_code_snippets ?? true}
              onChange={(e) => handleChange('include_code_snippets', e.target.checked)}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label htmlFor="include_code_snippets" className="ml-2 text-sm text-gray-700">
              Include Code Snippets
            </label>
          </div>
          
          <div className="flex items-center">
            <input
              type="checkbox"
              id="show_remediation"
              checked={config?.show_remediation ?? true}
              onChange={(e) => handleChange('show_remediation', e.target.checked)}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label htmlFor="show_remediation" className="ml-2 text-sm text-gray-700">
              Show Remediation Suggestions
            </label>
          </div>
        </div>
      </div>

      {/* Max Issues */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Maximum Issues Per File
        </label>
        <input
          type="number"
          min="1"
          max="1000"
          value={config?.max_issues_per_file || 50}
          onChange={(e) => handleChange('max_issues_per_file', parseInt(e.target.value))}
          className="w-full border border-gray-300 rounded-md px-3 py-2"
        />
      </div>
    </div>
  );
};

export default ConfigPanel;