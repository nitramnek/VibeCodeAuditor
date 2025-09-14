#!/usr/bin/env python3
"""
Demo script to show enhanced UI functionality with sample data.
This creates a static HTML demo of the enhanced compliance UI.
"""

import json
import webbrowser
from pathlib import Path

def create_enhanced_demo():
    """Create an enhanced demo HTML file with comprehensive sample data."""
    
    # Enhanced sample data with comprehensive compliance information
    sample_data = {
        "scan_id": "demo-scan-001",
        "summary": {
            "total_issues": 5,
            "critical": 2,
            "high": 2,
            "medium": 1,
            "low": 0
        },
        "compliance_summary": {
            "ISO 27001": 4,
            "OWASP": 3,
            "GDPR": 2,
            "PCI DSS": 3,
            "HIPAA": 1
        },
        "issues": [
            {
                "rule_id": "nodejs_hardcoded_secrets",
                "severity": "critical",
                "category": "Security",
                "message": "Hardcoded secret detected in source code. This exposes sensitive credentials and violates multiple security standards.",
                "file_path": "src/config/database.js",
                "line_number": 13,
                "code_snippet": "const DB_PASS = 'changeme123';",
                "confidence": 0.95,
                "metadata": {
                    "iso27001": "A.9.4.3",
                    "owasp": "A02-2021",
                    "cwe": "CWE-798",
                    "gdpr": "Art. 32"
                },
                "standards": [
                    {
                        "name": "ISO 27001",
                        "section": "A.9.4.3 - Access Control",
                        "description": "Privileged access rights shall be allocated and used on a restricted basis",
                        "url": "https://www.iso.org/standard/54534.html"
                    },
                    {
                        "name": "OWASP Top 10 2021",
                        "section": "A02-2021 - Cryptographic Failures",
                        "description": "Failures related to cryptography which often leads to sensitive data exposure",
                        "url": "https://owasp.org/Top10/A02_2021-Cryptographic_Failures/"
                    },
                    {
                        "name": "CWE",
                        "section": "CWE-798 - Use of Hard-coded Credentials",
                        "description": "The software contains hard-coded credentials, such as a password or cryptographic key",
                        "url": "https://cwe.mitre.org/data/definitions/798.html"
                    }
                ],
                "compliance_frameworks": ["ISO 27001", "GDPR", "PCI DSS", "HIPAA"],
                "remediation": "Remove hardcoded credentials and use environment variables or secure configuration management instead. Implement proper secrets management using tools like HashiCorp Vault or AWS Secrets Manager."
            },
            {
                "rule_id": "express_cors_misconfiguration",
                "severity": "high",
                "category": "Security Configuration",
                "message": "Permissive CORS configuration allows requests from any origin, potentially enabling cross-origin attacks.",
                "file_path": "src/middleware/cors.js",
                "line_number": 8,
                "code_snippet": "app.use(cors());",
                "confidence": 0.88,
                "metadata": {
                    "iso27001": "A.13.1.1",
                    "owasp": "A05-2021",
                    "cwe": "CWE-346"
                },
                "standards": [
                    {
                        "name": "ISO 27001",
                        "section": "A.13.1.1 - Network Controls",
                        "description": "Network controls shall be managed and controlled to protect information",
                        "url": "https://www.iso.org/standard/54534.html"
                    },
                    {
                        "name": "OWASP Top 10 2021",
                        "section": "A05-2021 - Security Misconfiguration",
                        "description": "Security misconfiguration is commonly a result of insecure default configurations",
                        "url": "https://owasp.org/Top10/A05_2021-Security_Misconfiguration/"
                    }
                ],
                "compliance_frameworks": ["ISO 27001", "OWASP", "PCI DSS"],
                "remediation": "Configure CORS to only allow specific trusted origins instead of using wildcard (*) or no restrictions. Implement proper origin validation."
            },
            {
                "rule_id": "nodejs_information_disclosure",
                "severity": "high",
                "category": "Information Disclosure",
                "message": "Error handler returns detailed stack traces to clients, potentially exposing sensitive system information.",
                "file_path": "src/middleware/errorHandler.js",
                "line_number": 18,
                "code_snippet": "res.status(500).json({ error: err.message, stack: err.stack });",
                "confidence": 0.92,
                "metadata": {
                    "iso27001": "A.12.4.1",
                    "owasp": "A09-2021",
                    "cwe": "CWE-209"
                },
                "standards": [
                    {
                        "name": "ISO 27001",
                        "section": "A.12.4.1 - Event Logging",
                        "description": "Event logs recording user activities shall be produced and kept",
                        "url": "https://www.iso.org/standard/54534.html"
                    },
                    {
                        "name": "OWASP Top 10 2021",
                        "section": "A09-2021 - Security Logging and Monitoring Failures",
                        "description": "Insufficient logging and monitoring, coupled with missing or ineffective integration",
                        "url": "https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/"
                    }
                ],
                "compliance_frameworks": ["ISO 27001", "GDPR"],
                "remediation": "Return generic error messages to clients and log detailed errors server-side only. Implement proper error handling that doesn't expose internal system details."
            },
            {
                "rule_id": "nodejs_missing_authentication",
                "severity": "critical",
                "category": "Authentication",
                "message": "Admin endpoint lacks authentication, allowing unauthorized access to sensitive configuration data.",
                "file_path": "src/routes/admin.js",
                "line_number": 25,
                "code_snippet": "app.get('/admin/config', (req, res) => {",
                "confidence": 0.98,
                "metadata": {
                    "iso27001": "A.9.1.2",
                    "owasp": "A07-2021",
                    "cwe": "CWE-306"
                },
                "standards": [
                    {
                        "name": "ISO 27001",
                        "section": "A.9.1.2 - Access to Networks and Network Services",
                        "description": "Access to networks and network services shall be controlled",
                        "url": "https://www.iso.org/standard/54534.html"
                    },
                    {
                        "name": "OWASP Top 10 2021",
                        "section": "A07-2021 - Identification and Authentication Failures",
                        "description": "Confirmation of the user's identity, authentication, and session management",
                        "url": "https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/"
                    }
                ],
                "compliance_frameworks": ["ISO 27001", "PCI DSS", "HIPAA"],
                "remediation": "Implement proper authentication middleware for admin endpoints. Use JWT tokens, session management, or OAuth2 for secure access control."
            },
            {
                "rule_id": "nodejs_pii_logging",
                "severity": "medium",
                "category": "Privacy",
                "message": "Potential PII data is being logged in plaintext without encryption or access controls.",
                "file_path": "src/utils/logger.js",
                "line_number": 42,
                "code_snippet": "fs.appendFileSync('./app_logs.txt', JSON.stringify(req.body));",
                "confidence": 0.85,
                "metadata": {
                    "iso27001": "A.10.1.2",
                    "gdpr": "Art. 25",
                    "cwe": "CWE-532"
                },
                "standards": [
                    {
                        "name": "GDPR",
                        "section": "Art. 25 - Data Protection by Design",
                        "description": "Data protection by design and by default",
                        "url": "https://gdpr-info.eu/art-25-gdpr/"
                    },
                    {
                        "name": "ISO 27001",
                        "section": "A.10.1.2 - Key Management",
                        "description": "Keys shall be protected against modification, loss and destruction",
                        "url": "https://www.iso.org/standard/54534.html"
                    }
                ],
                "compliance_frameworks": ["GDPR", "HIPAA"],
                "remediation": "Implement data classification and avoid logging PII. If logging is necessary, use encryption and proper access controls. Consider data anonymization techniques."
            }
        ]
    }
    
    # Create enhanced HTML demo
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VibeCodeAuditor - Enhanced Compliance UI Demo</title>
    <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <script src="https://unpkg.com/lucide-react@latest/dist/umd/lucide-react.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif; }}
        .demo-header {{ 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            margin-bottom: 2rem;
        }}
    </style>
</head>
<body class="bg-gray-50">
    <div class="demo-header">
        <div class="max-w-7xl mx-auto">
            <h1 class="text-4xl font-bold mb-2">🛡️ VibeCodeAuditor</h1>
            <h2 class="text-2xl font-semibold mb-4">Enhanced Compliance UI Demo</h2>
            <p class="text-lg opacity-90">World-class security auditing with comprehensive compliance standards display</p>
            <div class="mt-4 flex items-center space-x-6 text-sm">
                <span>✅ ISO 27001 Controls</span>
                <span>✅ OWASP Top 10 2021</span>
                <span>✅ GDPR Compliance</span>
                <span>✅ PCI DSS Standards</span>
                <span>✅ HIPAA Requirements</span>
            </div>
        </div>
    </div>
    
    <div id="root"></div>

    <script type="text/babel">
        const {{ useState }} = React;
        const {{ AlertTriangle, CheckCircle, Info, XCircle, ChevronDown, ChevronUp, ExternalLink, Shield, BookOpen, Download, Filter }} = lucideReact;

        // Sample data
        const sampleData = {json.dumps(sample_data, indent=8)};

        // Enhanced IssueCard Component (same as production)
        const IssueCard = ({{ issue, index }}) => {{
            const [showDetails, setShowDetails] = useState(false);

            const severityColors = {{
                critical: 'text-red-600 bg-red-50 border-red-200',
                high: 'text-orange-600 bg-orange-50 border-orange-200',
                medium: 'text-yellow-600 bg-yellow-50 border-yellow-200',
                low: 'text-green-600 bg-green-50 border-green-200',
            }};

            const severityIcons = {{
                critical: XCircle,
                high: AlertTriangle,
                medium: Info,
                low: CheckCircle,
            }};

            const Icon = severityIcons[issue.severity];

            // Helper function to render standards badges
            const renderStandardsBadges = () => {{
                const badges = [];
                
                if (issue.metadata?.iso27001) {{
                    badges.push(
                        React.createElement('span', {{
                            key: "iso-meta",
                            className: "inline-flex items-center px-2 py-1 text-xs bg-red-100 text-red-800 rounded-full border border-red-200"
                        }}, [
                            React.createElement(Shield, {{ key: "icon", className: "w-3 h-3 mr-1" }}),
                            `ISO 27001: ${{issue.metadata.iso27001}}`
                        ])
                    );
                }}
                
                if (issue.metadata?.owasp) {{
                    badges.push(
                        React.createElement('span', {{
                            key: "owasp-meta",
                            className: "inline-flex items-center px-2 py-1 text-xs bg-orange-100 text-orange-800 rounded-full border border-orange-200"
                        }}, [
                            React.createElement(Shield, {{ key: "icon", className: "w-3 h-3 mr-1" }}),
                            `OWASP: ${{issue.metadata.owasp}}`
                        ])
                    );
                }}
                
                if (issue.metadata?.cwe) {{
                    badges.push(
                        React.createElement('span', {{
                            key: "cwe-meta",
                            className: "inline-flex items-center px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-full border border-blue-200"
                        }}, [
                            React.createElement(BookOpen, {{ key: "icon", className: "w-3 h-3 mr-1" }}),
                            issue.metadata.cwe
                        ])
                    );
                }}
                
                if (issue.metadata?.gdpr) {{
                    badges.push(
                        React.createElement('span', {{
                            key: "gdpr-meta",
                            className: "inline-flex items-center px-2 py-1 text-xs bg-green-100 text-green-800 rounded-full border border-green-200"
                        }}, [
                            React.createElement(Shield, {{ key: "icon", className: "w-3 h-3 mr-1" }}),
                            `GDPR: ${{issue.metadata.gdpr}}`
                        ])
                    );
                }}

                return badges.length > 0 ? (
                    <div className="flex flex-wrap gap-2 mb-3">
                        {{badges}}
                    </div>
                ) : null;
            }};

            // Helper function to render compliance frameworks
            const renderComplianceFrameworks = () => {{
                if (!issue.compliance_frameworks || issue.compliance_frameworks.length === 0) return null;

                const frameworkColors = {{
                    'ISO 27001': 'bg-red-100 text-red-700 border-red-200',
                    'OWASP': 'bg-orange-100 text-orange-700 border-orange-200',
                    'GDPR': 'bg-green-100 text-green-700 border-green-200',
                    'PCI DSS': 'bg-blue-100 text-blue-700 border-blue-200',
                    'HIPAA': 'bg-purple-100 text-purple-700 border-purple-200',
                    'NIST': 'bg-indigo-100 text-indigo-700 border-indigo-200',
                }};

                return (
                    <div className="bg-red-50 border border-red-200 p-4 rounded-md mb-3">
                        <div className="flex items-center justify-between mb-3">
                            <p className="text-sm font-semibold text-red-900 flex items-center">
                                <AlertTriangle className="w-4 h-4 mr-2" />
                                Regulatory Compliance Impact
                            </p>
                            <span className="text-xs text-red-700 bg-red-100 px-2 py-1 rounded-full">
                                {{issue.compliance_frameworks.length}} framework{{issue.compliance_frameworks.length !== 1 ? 's' : ''}} affected
                            </span>
                        </div>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                            {{issue.compliance_frameworks.map((framework, idx) => {{
                                const colorClass = frameworkColors[framework] || 'bg-gray-100 text-gray-700 border-gray-200';
                                return (
                                    <div key={{idx}} className={{`px-3 py-2 text-sm rounded-md border ${{colorClass}} flex items-center justify-between`}}>
                                        <div className="flex items-center space-x-2">
                                            <Shield className="w-3 h-3" />
                                            <span className="font-medium">{{framework}}</span>
                                        </div>
                                        <span className="text-xs opacity-75">Violation</span>
                                    </div>
                                );
                            }})}}
                        </div>
                        <div className="mt-3 p-2 bg-red-100 rounded text-xs text-red-800">
                            <strong>Impact:</strong> This security issue may result in non-compliance with the above regulatory frameworks, potentially leading to audit failures, penalties, or security breaches.
                        </div>
                    </div>
                );
            }};

            return (
                <div className={{`bg-white rounded-lg shadow-sm border-l-4 ${{severityColors[issue.severity]}} p-6 mb-4`}}>
                    <div className="flex items-start space-x-4">
                        <Icon className={{`h-6 w-6 mt-1 ${{severityColors[issue.severity].split(' ')[0]}}`}} />
                        <div className="flex-1">
                            <div className="flex items-center justify-between mb-2">
                                <h3 className="text-lg font-semibold text-gray-900">{{issue.rule_id}}</h3>
                                <div className="flex items-center space-x-2">
                                    <span className={{`px-2 py-1 text-xs font-medium rounded-full ${{severityColors[issue.severity]}}`}}>
                                        {{issue.severity.toUpperCase()}}
                                    </span>
                                    <span className="px-2 py-1 text-xs font-medium rounded-full bg-gray-100 text-gray-800">
                                        {{issue.category}}
                                    </span>
                                    {{(issue.standards && issue.standards.length > 0) && (
                                        <span className="px-2 py-1 text-xs font-medium rounded-full bg-purple-100 text-purple-800 flex items-center">
                                            <Shield className="w-3 h-3 mr-1" />
                                            {{issue.standards.length}} Standards
                                        </span>
                                    )}}
                                    {{(issue.compliance_frameworks && issue.compliance_frameworks.length > 0) && (
                                        <span className="px-2 py-1 text-xs font-medium rounded-full bg-red-100 text-red-800 flex items-center">
                                            <AlertTriangle className="w-3 h-3 mr-1" />
                                            {{issue.compliance_frameworks.length}} Compliance
                                        </span>
                                    )}}
                                </div>
                            </div>

                            {{/* Quick Compliance Summary */}}
                            {{(issue.compliance_frameworks?.length > 0 || issue.standards?.length > 0) && (
                                <div className={{`border p-3 rounded-md mb-3 ${{
                                    issue.severity === 'critical' ? 'bg-red-50 border-red-200' :
                                    issue.severity === 'high' ? 'bg-orange-50 border-orange-200' :
                                    'bg-yellow-50 border-yellow-200'
                                }}`}}>
                                    <div className="flex items-start space-x-2">
                                        <AlertTriangle className={{`w-4 h-4 mt-0.5 flex-shrink-0 ${{
                                            issue.severity === 'critical' ? 'text-red-600' :
                                            issue.severity === 'high' ? 'text-orange-600' :
                                            'text-yellow-600'
                                        }}`}} />
                                        <div className="text-sm">
                                            <span className={{`font-medium ${{
                                                issue.severity === 'critical' ? 'text-red-800' :
                                                issue.severity === 'high' ? 'text-orange-800' :
                                                'text-yellow-800'
                                            }}`}}>
                                                {{issue.severity === 'critical' ? 'Critical Compliance Risk:' :
                                                 issue.severity === 'high' ? 'High Compliance Risk:' :
                                                 'Compliance Alert:'}}
                                            </span>
                                            <span className={{`ml-1 ${{
                                                issue.severity === 'critical' ? 'text-red-700' :
                                                issue.severity === 'high' ? 'text-orange-700' :
                                                'text-yellow-700'
                                            }}`}}>
                                                This issue violates {{issue.compliance_frameworks?.length || 0}} regulatory framework{{(issue.compliance_frameworks?.length || 0) !== 1 ? 's' : ''}} 
                                                {{issue.standards?.length > 0 && ` and ${{issue.standards.length}} security standard${{issue.standards.length !== 1 ? 's' : ''}}`}}.
                                                {{issue.severity === 'critical' && ' Immediate remediation required to avoid audit failures.'}}
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            )}}

                            {{renderStandardsBadges()}}

                            <p className="text-gray-700 mb-3">{{issue.message}}</p>

                            <div className="text-sm text-gray-600 mb-3">
                                <span className="font-medium">File:</span> {{issue.file_path}}
                                {{issue.line_number && (
                                    <>
                                        <span className="mx-2">•</span>
                                        <span className="font-medium">Line:</span> {{issue.line_number}}
                                    </>
                                )}}
                            </div>

                            {{issue.code_snippet && (
                                <div className="bg-gray-50 p-3 rounded-md mb-3">
                                    <p className="text-sm font-medium text-gray-700 mb-1">Code:</p>
                                    <code className="text-sm text-gray-800 font-mono">{{issue.code_snippet}}</code>
                                </div>
                            )}}

                            <button
                                onClick={{() => setShowDetails(!showDetails)}}
                                className="flex items-center space-x-2 text-sm text-blue-600 hover:text-blue-800 mb-3"
                            >
                                {{showDetails ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}}
                                <span>{{showDetails ? 'Hide' : 'Show'}} Standards & Compliance Details</span>
                            </button>

                            {{showDetails && (
                                <div className="space-y-3">
                                    {{renderComplianceFrameworks()}}
                                </div>
                            )}}

                            {{issue.remediation && (
                                <div className="bg-blue-50 p-3 rounded-md">
                                    <p className="text-sm font-medium text-blue-800 mb-1 flex items-center">
                                        <CheckCircle className="w-4 h-4 mr-2" />
                                        Remediation
                                    </p>
                                    <p className="text-sm text-blue-700">{{issue.remediation}}</p>
                                </div>
                            )}}
                        </div>
                    </div>
                </div>
            );
        }};

        const App = () => {{
            return (
                <div className="max-w-7xl mx-auto px-4 pb-8">
                    {{/* Summary Cards */}}
                    <div className="grid grid-cols-1 md:grid-cols-5 gap-6 mb-8">
                        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
                            <div className="text-center">
                                <p className="text-2xl font-bold text-gray-900">{{sampleData.summary.total_issues}}</p>
                                <p className="text-sm text-gray-600">Total Issues</p>
                            </div>
                        </div>
                        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
                            <div className="text-center">
                                <p className="text-2xl font-bold text-red-600">{{sampleData.summary.critical}}</p>
                                <p className="text-sm text-gray-600">Critical</p>
                            </div>
                        </div>
                        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
                            <div className="text-center">
                                <p className="text-2xl font-bold text-orange-600">{{sampleData.summary.high}}</p>
                                <p className="text-sm text-gray-600">High</p>
                            </div>
                        </div>
                        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
                            <div className="text-center">
                                <p className="text-2xl font-bold text-yellow-600">{{sampleData.summary.medium}}</p>
                                <p className="text-sm text-gray-600">Medium</p>
                            </div>
                        </div>
                        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
                            <div className="text-center">
                                <p className="text-2xl font-bold text-green-600">{{sampleData.summary.low}}</p>
                                <p className="text-sm text-gray-600">Low</p>
                            </div>
                        </div>
                    </div>

                    {{/* Compliance Overview */}}
                    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 mb-6">
                        <div className="flex items-center mb-4">
                            <Shield className="h-5 w-5 text-purple-600 mr-2" />
                            <h2 className="text-lg font-semibold text-gray-900">Compliance Impact Overview</h2>
                        </div>
                        <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
                            {{Object.entries(sampleData.compliance_summary).map(([framework, count]) => (
                                <div key={{framework}} className="bg-red-50 border border-red-200 p-3 rounded-md">
                                    <div className="flex items-center justify-between">
                                        <span className="text-sm font-medium text-red-900">{{framework}}</span>
                                        <span className="text-sm font-bold text-red-700">{{count}} violations</span>
                                    </div>
                                </div>
                            ))}}
                        </div>
                    </div>

                    {{/* Issues List */}}
                    <div className="space-y-4">
                        {{sampleData.issues.map((issue, index) => (
                            <IssueCard key={{index}} issue={{issue}} index={{index}} />
                        ))}}
                    </div>

                    {{/* Demo Footer */}}
                    <div className="mt-12 bg-white p-6 rounded-lg shadow-sm border border-gray-200">
                        <h3 className="text-lg font-semibold text-gray-900 mb-4">🎉 Enhanced Compliance UI Features</h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div>
                                <h4 className="font-medium text-gray-900 mb-2">✅ Compliance Standards</h4>
                                <ul className="text-sm text-gray-600 space-y-1">
                                    <li>• ISO 27001 control mappings</li>
                                    <li>• OWASP Top 10 2021 alignment</li>
                                    <li>• GDPR privacy requirements</li>
                                    <li>• PCI DSS security standards</li>
                                    <li>• HIPAA healthcare compliance</li>
                                </ul>
                            </div>
                            <div>
                                <h4 className="font-medium text-gray-900 mb-2">🚀 Enhanced Features</h4>
                                <ul className="text-sm text-gray-600 space-y-1">
                                    <li>• Severity-based compliance risk indicators</li>
                                    <li>• Interactive expandable compliance details</li>
                                    <li>• Professional standards badges</li>
                                    <li>• Regulatory framework impact assessment</li>
                                    <li>• Direct links to official documentation</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            );
        }};

        ReactDOM.render(<App />, document.getElementById('root'));
    </script>
</body>
</html>"""
    
    # Write the demo file
    demo_file = Path("enhanced_compliance_demo.html")
    demo_file.write_text(html_content, encoding='utf-8')
    
    print("🎉 Enhanced Compliance UI Demo Created!")
    print("=" * 50)
    print(f"📁 Demo file: {demo_file.absolute()}")
    print("🌐 Opening in browser...")
    
    # Try to open in browser
    try:
        webbrowser.open(f"file://{demo_file.absolute()}")
        print("✅ Demo opened in browser!")
    except Exception as e:
        print(f"⚠️  Could not auto-open browser: {e}")
        print(f"💡 Manually open: {demo_file.absolute()}")
    
    print("\n🛡️  Demo Features:")
    print("   ✅ Enhanced IssueCard with compliance standards")
    print("   ✅ Severity-based compliance risk indicators")
    print("   ✅ Interactive expandable compliance details")
    print("   ✅ Professional standards badges (ISO 27001, OWASP, etc.)")
    print("   ✅ Regulatory framework impact assessment")
    print("   ✅ Compliance overview dashboard")
    
    return demo_file

if __name__ == "__main__":
    create_enhanced_demo()