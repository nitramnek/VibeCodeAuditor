import React, { useState } from 'react';
import { useQuery } from 'react-query';
import { Save, RefreshCw, AlertCircle } from 'lucide-react';
import { getDefaultConfig } from '../services/api';

const Settings = () => {
  const { data: defaultConfig, isLoading } = useQuery('defaultConfig', getDefaultConfig);
  const [config, setConfig] = useState(null);
  const [saved, setSaved] = useState(false);

  React.useEffect(() => {
    if (defaultConfig && !config) {
      setConfig(defaultConfig);
    }
  }, [defaultConfig, config]);

  const handleSave = () => {
    // In a real app, you'd save to localStorage or send to API
    localStorage.setItem('vibeauditor_config', JSON.stringify(config));
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  const handleReset = () => {
    setConfig(defaultConfig);
  };

  if (isLoading || !config) {
    return (
      <div className="flex items-center justify-center min-h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Settings</h1>
        <p className="text-gray-600">
          Configure your code auditing preferences and scan settings
        </p>
      </div>

      {/* Save Status */}
      {saved && (
        <div className="mb-6 bg-green-50 border border-green-200 rounded-md p-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm font-medium text-green-800">Settings saved successfully!</p>
            </div>
          </div>
        </div>
      )}

      <div className="space-y-6">
        {/* General Settings */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">General Settings</h2>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Minimum Severity Level
              </label>
              <select
                value={config.min_severity}
                onChange={(e) => setConfig({...config, min_severity: e.target.value})}
                className="w-full border border-gray-300 rounded-md px-3 py-2"
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="critical">Critical</option>
              </select>
              <p className="text-sm text-gray-500 mt-1">
                Only issues at or above this severity level will be reported
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Maximum Issues Per File
              </label>
              <input
                type="number"
                min="1"
                max="1000"
                value={config.max_issues_per_file}
                onChange={(e) => setConfig({...config, max_issues_per_file: parseInt(e.target.value)})}
                className="w-full border border-gray-300 rounded-md px-3 py-2"
              />
              <p className="text-sm text-gray-500 mt-1">
                Limit the number of issues reported per file to avoid overwhelming output
              </p>
            </div>
          </div>
        </div>

        {/* Report Settings */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Report Settings</h2>
          
          <div className="space-y-4">
            <div className="flex items-center">
              <input
                type="checkbox"
                id="include_code_snippets"
                checked={config.include_code_snippets}
                onChange={(e) => setConfig({...config, include_code_snippets: e.target.checked})}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label htmlFor="include_code_snippets" className="ml-2 block text-sm text-gray-900">
                Include code snippets in reports
              </label>
            </div>

            <div className="flex items-center">
              <input
                type="checkbox"
                id="show_remediation"
                checked={config.show_remediation}
                onChange={(e) => setConfig({...config, show_remediation: e.target.checked})}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label htmlFor="show_remediation" className="ml-2 block text-sm text-gray-900">
                Show remediation suggestions
              </label>
            </div>
          </div>
        </div>

        {/* AI/ML Settings */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">AI/ML Specific Checks</h2>
          
          <div className="space-y-4">
            <div className="flex items-center">
              <input
                type="checkbox"
                id="check_data_privacy"
                checked={config.check_data_privacy}
                onChange={(e) => setConfig({...config, check_data_privacy: e.target.checked})}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label htmlFor="check_data_privacy" className="ml-2 block text-sm text-gray-900">
                Check for data privacy issues (GDPR, CCPA compliance)
              </label>
            </div>

            <div className="flex items-center">
              <input
                type="checkbox"
                id="check_model_security"
                checked={config.check_model_security}
                onChange={(e) => setConfig({...config, check_model_security: e.target.checked})}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label htmlFor="check_model_security" className="ml-2 block text-sm text-gray-900">
                Check for model security issues
              </label>
            </div>

            <div className="flex items-center">
              <input
                type="checkbox"
                id="check_bias_detection"
                checked={config.check_bias_detection}
                onChange={(e) => setConfig({...config, check_bias_detection: e.target.checked})}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label htmlFor="check_bias_detection" className="ml-2 block text-sm text-gray-900">
                Check for potential algorithmic bias
              </label>
            </div>
          </div>
        </div>

        {/* File Patterns */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">File Patterns</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Include Patterns
              </label>
              <textarea
                value={config.include_patterns.join('\n')}
                onChange={(e) => setConfig({...config, include_patterns: e.target.value.split('\n').filter(p => p.trim())})}
                rows={6}
                className="w-full border border-gray-300 rounded-md px-3 py-2 font-mono text-sm"
                placeholder="*.py&#10;*.js&#10;*.ts"
              />
              <p className="text-sm text-gray-500 mt-1">
                File patterns to include in scans (one per line)
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Exclude Patterns
              </label>
              <textarea
                value={config.exclude_patterns.join('\n')}
                onChange={(e) => setConfig({...config, exclude_patterns: e.target.value.split('\n').filter(p => p.trim())})}
                rows={6}
                className="w-full border border-gray-300 rounded-md px-3 py-2 font-mono text-sm"
                placeholder="*.pyc&#10;__pycache__&#10;node_modules"
              />
              <p className="text-sm text-gray-500 mt-1">
                File patterns to exclude from scans (one per line)
              </p>
            </div>
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center justify-between pt-6 border-t border-gray-200">
          <button
            onClick={handleReset}
            className="flex items-center space-x-2 px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
          >
            <RefreshCw className="h-4 w-4" />
            <span>Reset to Defaults</span>
          </button>

          <button
            onClick={handleSave}
            className="flex items-center space-x-2 px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            <Save className="h-4 w-4" />
            <span>Save Settings</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default Settings;