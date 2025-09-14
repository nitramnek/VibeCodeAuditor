import React, { useState } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { useNavigate } from 'react-router-dom'
import { useScan } from '../hooks/useScan'
import { Upload, FileText, Shield, BarChart3, Settings, LogOut, User, Info, Clock, AlertTriangle, CheckCircle, TrendingUp, LayoutDashboard } from 'lucide-react'

const Dashboard = () => {
  const { user, signOut, isSupabaseEnabled } = useAuth()
  const navigate = useNavigate()
  const [dragActive, setDragActive] = useState(false)
  const { loading, performScan } = useScan()

  const handleSignOut = async () => {
    await signOut()
    navigate('/login')
  }

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFiles(e.dataTransfer.files)
    }
  }

  const handleFileInput = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFiles(e.target.files)
    }
  }

  const handleFiles = async (files) => {
    console.log('Files to scan:', files)
    const scanName = files[0]?.name ? `${files[0].name} - Dashboard Scan` : 'Dashboard Scan'
    await performScan(files, scanName)
  }

  return (
    <div>
        {/* Enhanced Welcome Section */}
        <div className="mb-8 text-center">
          <h2 className="text-4xl font-bold text-gray-900 mb-3">
            Welcome to VibeCodeAuditor
          </h2>
          <p className="text-xl text-gray-600 mb-4">
            Enterprise-grade security auditing with comprehensive compliance standards
          </p>
          <div className="flex justify-center items-center space-x-6 text-sm text-gray-500">
            <div className="flex items-center space-x-1">
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              <span>13+ Security Standards</span>
            </div>
            <div className="flex items-center space-x-1">
              <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
              <span>Real-time Analysis</span>
            </div>
            <div className="flex items-center space-x-1">
              <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
              <span>Audit-ready Reports</span>
            </div>
          </div>
        </div>

        {/* Quick Overview Stats */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="text-2xl font-bold text-gray-900">Security Overview</h2>
              <p className="text-gray-600">Real-time security metrics and system status</p>
            </div>
            <div className="flex items-center space-x-2 text-sm text-gray-500">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span>Live data • Updated 2 min ago</span>
            </div>
          </div>
          
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-6">
            <div className="bg-white p-6 rounded-xl shadow-modern border border-gray-200 hover:shadow-modern-md transition-all duration-200 hover-lift">
              <div className="flex items-center justify-between mb-4">
                <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center">
                  <Clock className="h-6 w-6 text-blue-600" />
                </div>
                <span className="text-xs font-medium px-2 py-1 bg-blue-100 text-blue-800 rounded-full">Active</span>
              </div>
              <div className="space-y-1">
                <div className="text-3xl font-bold text-gray-900">2</div>
                <div className="text-sm text-gray-600">Active Scans</div>
                <div className="text-xs text-blue-600 font-medium">+1 from yesterday</div>
              </div>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-modern border border-gray-200 hover:shadow-modern-md transition-all duration-200 hover-lift">
              <div className="flex items-center justify-between mb-4">
                <div className="w-12 h-12 bg-red-100 rounded-xl flex items-center justify-center">
                  <AlertTriangle className="h-6 w-6 text-red-600" />
                </div>
                <span className="text-xs font-medium px-2 py-1 bg-red-100 text-red-800 rounded-full">Critical</span>
              </div>
              <div className="space-y-1">
                <div className="text-3xl font-bold text-gray-900">5</div>
                <div className="text-sm text-gray-600">Critical Issues</div>
                <div className="text-xs text-red-600 font-medium">Requires attention</div>
              </div>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-modern border border-gray-200 hover:shadow-modern-md transition-all duration-200 hover-lift">
              <div className="flex items-center justify-between mb-4">
                <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center">
                  <CheckCircle className="h-6 w-6 text-green-600" />
                </div>
                <span className="text-xs font-medium px-2 py-1 bg-green-100 text-green-800 rounded-full">Resolved</span>
              </div>
              <div className="space-y-1">
                <div className="text-3xl font-bold text-gray-900">23</div>
                <div className="text-sm text-gray-600">Issues Resolved</div>
                <div className="text-xs text-green-600 font-medium">This week</div>
              </div>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-modern border border-gray-200 hover:shadow-modern-md transition-all duration-200 hover-lift">
              <div className="flex items-center justify-between mb-4">
                <div className="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center">
                  <TrendingUp className="h-6 w-6 text-purple-600" />
                </div>
                <span className="text-xs font-medium px-2 py-1 bg-purple-100 text-purple-800 rounded-full">Trend</span>
              </div>
              <div className="space-y-1">
                <div className="text-3xl font-bold text-gray-900">+12%</div>
                <div className="text-sm text-gray-600">Security Score</div>
                <div className="text-xs text-purple-600 font-medium">Improvement</div>
              </div>
            </div>
          </div>
        </div>

        {/* Enhanced Stats Cards */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-6 mb-8">
          <div className="bg-white p-4 lg:p-6 rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-10 h-10 lg:w-12 lg:h-12 bg-blue-100 rounded-full flex items-center justify-center">
                  <Shield className="h-5 w-5 lg:h-6 lg:w-6 text-blue-600" />
                </div>
              </div>
              <div className="ml-3 lg:ml-4">
                <p className="text-xs lg:text-sm font-medium text-gray-600">Security Standards</p>
                <p className="text-xl lg:text-2xl font-bold text-gray-900">13+</p>
              </div>
            </div>
          </div>
          
          <div className="bg-white p-4 lg:p-6 rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-10 h-10 lg:w-12 lg:h-12 bg-green-100 rounded-full flex items-center justify-center">
                  <BarChart3 className="h-5 w-5 lg:h-6 lg:w-6 text-green-600" />
                </div>
              </div>
              <div className="ml-3 lg:ml-4">
                <p className="text-xs lg:text-sm font-medium text-gray-600">Compliance Frameworks</p>
                <p className="text-xl lg:text-2xl font-bold text-gray-900">ISO 27001</p>
              </div>
            </div>
          </div>
          
          <div className="bg-white p-4 lg:p-6 rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-10 h-10 lg:w-12 lg:h-12 bg-purple-100 rounded-full flex items-center justify-center">
                  <FileText className="h-5 w-5 lg:h-6 lg:w-6 text-purple-600" />
                </div>
              </div>
              <div className="ml-3 lg:ml-4">
                <p className="text-xs lg:text-sm font-medium text-gray-600">Supported Languages</p>
                <p className="text-xl lg:text-2xl font-bold text-gray-900">10+</p>
              </div>
            </div>
          </div>
          
          <div className="bg-white p-4 lg:p-6 rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-10 h-10 lg:w-12 lg:h-12 bg-indigo-100 rounded-full flex items-center justify-center">
                  <Upload className="h-5 w-5 lg:h-6 lg:w-6 text-indigo-600" />
                </div>
              </div>
              <div className="ml-3 lg:ml-4">
                <p className="text-xs lg:text-sm font-medium text-gray-600">Ready to Scan</p>
                <p className="text-xl lg:text-2xl font-bold text-gray-900">Upload</p>
              </div>
            </div>
          </div>
        </div>

        {/* Upload Section */}
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-8">
          <div className="lg:col-span-3">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
              <div className="text-center">
                <h3 className="text-xl font-semibold text-gray-900 mb-4">
                  Start Security Audit
                </h3>
                <p className="text-gray-600 mb-6">
                  Upload your code files to begin comprehensive security analysis with compliance mapping
                </p>
                
                <div
                  className={`border-2 border-dashed rounded-lg p-12 transition-all duration-300 ${
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
                      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
                      <p className="text-lg font-medium text-blue-900 mb-2">
                        Processing Files...
                      </p>
                      <p className="text-sm text-blue-700">
                        Analyzing code for security vulnerabilities and compliance issues
                      </p>
                    </div>
                  ) : (
                    <>
                      <Upload className={`mx-auto h-12 w-12 mb-4 transition-colors ${
                        dragActive ? 'text-blue-500' : 'text-gray-400'
                      }`} />
                      <p className="text-lg font-medium text-gray-900 mb-2">
                        {dragActive ? 'Drop files to start scanning' : 'Drop files here or click to upload'}
                      </p>
                      <p className="text-sm text-gray-600 mb-6">
                        Supports JavaScript, Python, Java, C#, PHP, Ruby, Go, C/C++
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
                        className={`inline-flex items-center px-8 py-4 border border-transparent text-base font-medium rounded-lg text-white transition-all duration-200 ${
                          loading 
                            ? 'bg-gray-400 cursor-not-allowed' 
                            : 'bg-blue-600 hover:bg-blue-700 hover:shadow-lg cursor-pointer transform hover:scale-105'
                        }`}
                      >
                        <Upload className="h-5 w-5 mr-2" />
                        {loading ? 'Processing...' : 'Choose Files'}
                      </label>
                      
                      <div className="mt-4 text-xs text-gray-500">
                        Maximum file size: 10MB per file • Batch upload supported
                      </div>
                    </>
                  )}
                </div>
              </div>
            </div>
          </div>
          
          {/* Quick Actions Sidebar */}
          <div className="space-y-4">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h4 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h4>
              <div className="space-y-3">
                <button className="w-full flex items-center space-x-3 p-3 text-left rounded-md hover:bg-gray-50 transition-colors">
                  <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                    <FileText className="h-4 w-4 text-blue-600" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-900">View Recent Scans</p>
                    <p className="text-xs text-gray-500">Access your scan history</p>
                  </div>
                </button>
                
                <button className="w-full flex items-center space-x-3 p-3 text-left rounded-md hover:bg-gray-50 transition-colors">
                  <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                    <Settings className="h-4 w-4 text-green-600" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-900">Configure Rules</p>
                    <p className="text-xs text-gray-500">Customize security rules</p>
                  </div>
                </button>
                
                <button className="w-full flex items-center space-x-3 p-3 text-left rounded-md hover:bg-gray-50 transition-colors">
                  <div className="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center">
                    <BarChart3 className="h-4 w-4 text-purple-600" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-900">Compliance Dashboard</p>
                    <p className="text-xs text-gray-500">View compliance status</p>
                  </div>
                </button>
              </div>
            </div>
            
            {/* Tips */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <div className="flex items-start space-x-2">
                <Info className="h-4 w-4 text-blue-600 mt-0.5 flex-shrink-0" />
                <div>
                  <p className="text-sm font-medium text-blue-900">Pro Tip</p>
                  <p className="text-xs text-blue-700 mt-1">
                    Upload multiple files at once for batch scanning. Supported formats include .js, .py, .java, and more.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Enhanced Features Section */}
        <div className="mt-16">
          <div className="text-center mb-12">
            <h3 className="text-2xl font-bold text-gray-900 mb-4">
              Why Choose VibeCodeAuditor?
            </h3>
            <p className="text-lg text-gray-600 max-w-3xl mx-auto">
              Built for enterprise security teams who need comprehensive vulnerability detection 
              with regulatory compliance mapping and audit-ready documentation.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-white p-8 rounded-xl shadow-sm border border-gray-200 hover:shadow-md transition-all duration-300 group">
              <div className="flex justify-center mb-6">
                <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center group-hover:bg-blue-200 transition-colors">
                  <Shield className="h-8 w-8 text-blue-600" />
                </div>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3 text-center">
                Advanced Security Analysis
              </h3>
              <p className="text-gray-600 text-center leading-relaxed">
                Detect vulnerabilities across 10+ programming languages using advanced pattern matching, 
                static analysis, and machine learning-powered threat detection.
              </p>
              <div className="mt-4 flex justify-center">
                <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                  10+ Languages Supported
                </span>
              </div>
            </div>
            
            <div className="bg-white p-8 rounded-xl shadow-sm border border-gray-200 hover:shadow-md transition-all duration-300 group">
              <div className="flex justify-center mb-6">
                <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center group-hover:bg-green-200 transition-colors">
                  <BarChart3 className="h-8 w-8 text-green-600" />
                </div>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3 text-center">
                Regulatory Compliance
              </h3>
              <p className="text-gray-600 text-center leading-relaxed">
                Automatic mapping to 13+ compliance frameworks including ISO 27001, OWASP Top 10, 
                GDPR, PCI DSS, HIPAA, and NIST cybersecurity standards.
              </p>
              <div className="mt-4 flex justify-center">
                <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                  13+ Compliance Frameworks
                </span>
              </div>
            </div>
            
            <div className="bg-white p-8 rounded-xl shadow-sm border border-gray-200 hover:shadow-md transition-all duration-300 group">
              <div className="flex justify-center mb-6">
                <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center group-hover:bg-purple-200 transition-colors">
                  <FileText className="h-8 w-8 text-purple-600" />
                </div>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3 text-center">
                Audit-Ready Reports
              </h3>
              <p className="text-gray-600 text-center leading-relaxed">
                Generate professional security reports with detailed remediation guidance, 
                compliance evidence, and executive summaries for stakeholders and auditors.
              </p>
              <div className="mt-4 flex justify-center">
                <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                  Enterprise Reports
                </span>
              </div>
            </div>
          </div>
        </div>
    </div>
  )
}

export default Dashboard