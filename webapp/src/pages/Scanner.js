// webapp/src/pages/Scanner.js
import React, { useState } from 'react';
import { Upload, FileText, Shield, CheckCircle } from 'lucide-react';
import { useScan } from '../hooks/useScan';

const Scanner = () => {
  const [dragActive, setDragActive] = useState(false);
  const { loading, performScan } = useScan();

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFiles(e.dataTransfer.files);
    }
  };

  const handleFileInput = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      handleFiles(e.target.files);
    }
  };

  const handleFiles = async (files) => {
    console.log('Files to scan:', files);
    const scanName = files[0]?.name ? `${files[0].name} - Security Scanner` : 'Security Scanner Scan'
    await performScan(files, scanName)
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Security Scanner</h1>
        <p className="mt-2 text-gray-600">
          Upload your code files for comprehensive security analysis and compliance checking.
        </p>
      </div>

      {/* Scanner Interface */}
      <div className="bg-white rounded-xl shadow-modern p-8">
        <div className="text-center">
          <div
            className={`border-2 border-dashed rounded-xl p-12 transition-all duration-300 ${
              loading
                ? 'border-blue-400 bg-blue-50 animate-pulse'
                : dragActive
                ? 'border-blue-400 bg-blue-50 scale-105'
                : 'border-gray-300 hover:border-gray-400 hover:bg-gray-50'
            }`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            {loading ? (
              <div className="text-center">
                <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
                <h3 className="text-xl font-medium text-blue-900 mb-2">
                  Analyzing Code...
                </h3>
                <p className="text-blue-700">
                  Scanning for vulnerabilities and compliance issues
                </p>
              </div>
            ) : (
              <>
                <Upload
                  className={`mx-auto h-16 w-16 mb-6 transition-colors ${
                    dragActive ? 'text-blue-500' : 'text-gray-400'
                  }`}
                />
                <h3 className="text-2xl font-medium text-gray-900 mb-2">
                  {dragActive ? 'Drop files to start scanning' : 'Upload Code Files'}
                </h3>
                <p className="text-gray-600 mb-8">
                  Supports JavaScript, Python, Java, C#, PHP, Ruby, Go, C/C++, and more
                </p>

                <input
                  type="file"
                  multiple
                  onChange={handleFileInput}
                  className="hidden"
                  id="file-upload"
                  accept=".js,.ts,.py,.java,.cs,.php,.rb,.go,.cpp,.c,.h,.jsx,.tsx,.vue,.swift,.kt"
                  disabled={loading}
                />

                <label
                  htmlFor="file-upload"
                  className="inline-flex items-center px-8 py-4 border border-transparent text-lg font-medium rounded-xl text-white bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 cursor-pointer transform hover:scale-105 transition-all duration-200 shadow-modern-md"
                >
                  <Upload className="h-6 w-6 mr-3" />
                  {loading ? 'Processing...' : 'Choose Files to Scan'}
                </label>

                <div className="mt-6 text-sm text-gray-500">
                  Maximum file size: 10MB per file • Batch upload supported • Enterprise encryption
                </div>
              </>
            )}
          </div>
        </div>
      </div>

      {/* Features Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-xl shadow-modern p-6 hover:shadow-modern-md transition-all duration-200">
          <div className="flex items-center space-x-4 mb-4">
            <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center">
              <Shield className="h-6 w-6 text-blue-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900">Advanced Detection</h3>
          </div>
          <p className="text-gray-600">
            AI-powered vulnerability detection across 10+ programming languages with real-time analysis.
          </p>
        </div>

        <div className="bg-white rounded-xl shadow-modern p-6 hover:shadow-modern-md transition-all duration-200">
          <div className="flex items-center space-x-4 mb-4">
            <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center">
              <CheckCircle className="h-6 w-6 text-green-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900">Compliance Ready</h3>
          </div>
          <p className="text-gray-600">
            Automatic mapping to 13+ regulatory frameworks including ISO 27001, OWASP, and GDPR.
          </p>
        </div>

        <div className="bg-white rounded-xl shadow-modern p-6 hover:shadow-modern-md transition-all duration-200">
          <div className="flex items-center space-x-4 mb-4">
            <div className="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center">
              <FileText className="h-6 w-6 text-purple-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900">Detailed Reports</h3>
          </div>
          <p className="text-gray-600">
            Professional audit reports with remediation guidance and executive summaries.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Scanner;
