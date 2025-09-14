"""
Add this to your vibeauditor/api/main.py to handle demo scan results.
"""

# Add this endpoint to your existing API

@app.get("/api/scan/demo-scan-123/results")
async def get_demo_scan_results():
    """Return demo scan results for testing the enhanced UI."""
    
    demo_results = {
        "scan_id": "demo-scan-123",
        "summary": {
            "total_issues": 5,
            "critical": 2,
            "high": 2,
            "medium": 1,
            "low": 0,
            "files_scanned": 3,
            "files_with_errors": 0
        },
        "compliance_summary": {
            "ISO 27001": {"name": "ISO 27001", "count": 4},
            "OWASP": {"name": "OWASP Top 10", "count": 3},
            "GDPR": {"name": "GDPR", "count": 2},
            "PCI DSS": {"name": "PCI DSS", "count": 2},
            "HIPAA": {"name": "HIPAA", "count": 1}
        },
        "detected_frameworks": {
            "nodejs": {
                "name": "Node.js",
                "type": "runtime",
                "confidence": 0.95,
                "files": ["test.js", "package.json"]
            },
            "express": {
                "name": "Express.js",
                "type": "web_framework", 
                "confidence": 0.88,
                "files": ["test.js"]
            }
        },
        "issues": [
            {
                "rule_id": "nodejs.hardcoded_secrets",
                "severity": "critical",
                "category": "security",
                "message": "Node.js Security: Hardcoded JWT secret",
                "file_path": "/tmp/vibeaudit_demo/test.js",
                "line_number": 20,
                "code_snippet": "const JWT_SECRET = 'supersecretjwtkey'; // <-- hard-coded secret",
                "remediation": "Use environment variables or secure configuration management. Never commit secrets to source code.",
                "confidence": 0.9,
                "metadata": {
                    "framework": "nodejs",
                    "cwe": "CWE-798",
                    "iso27001": "A.9.4.3, A.10.1.2",
                    "owasp": "A02-2021",
                    "gdpr": "Art. 32"
                },
                "standards": [
                    {
                        "id": "iso27001_a943",
                        "name": "ISO 27001",
                        "type": "security",
                        "url": "https://www.iso.org/standard/54534.html",
                        "section": "A.9.4.3 - Access Control"
                    },
                    {
                        "id": "owasp_a02_2021",
                        "name": "OWASP Top 10 2021",
                        "type": "security",
                        "url": "https://owasp.org/Top10/A02_2021-Cryptographic_Failures/",
                        "section": "A02-2021 - Cryptographic Failures"
                    },
                    {
                        "id": "cwe_798",
                        "name": "CWE",
                        "type": "security",
                        "url": "https://cwe.mitre.org/data/definitions/798.html",
                        "section": "CWE-798 - Use of Hard-coded Credentials"
                    }
                ],
                "compliance_frameworks": ["ISO 27001", "OWASP", "GDPR", "PCI DSS"]
            },
            {
                "rule_id": "express.security_misconfiguration",
                "severity": "high",
                "category": "security",
                "message": "Express Security: Permissive CORS configuration allows any origin",
                "file_path": "/tmp/vibeaudit_demo/test.js",
                "line_number": 12,
                "code_snippet": "app.use(cors());",
                "remediation": "Configure CORS with specific origins. Use: cors({origin: ['https://yourdomain.com']})",
                "confidence": 0.8,
                "metadata": {
                    "framework": "express",
                    "cwe": "CWE-346",
                    "iso27001": "A.13.1.3",
                    "owasp": "A05-2021"
                },
                "standards": [
                    {
                        "id": "iso27001_a1313",
                        "name": "ISO 27001",
                        "type": "security",
                        "url": "https://www.iso.org/standard/54534.html",
                        "section": "A.13.1.3 - Network Controls"
                    },
                    {
                        "id": "owasp_a05_2021",
                        "name": "OWASP Top 10 2021",
                        "type": "security",
                        "url": "https://owasp.org/Top10/A05_2021-Security_Misconfiguration/",
                        "section": "A05-2021 - Security Misconfiguration"
                    }
                ],
                "compliance_frameworks": ["ISO 27001", "OWASP", "PCI DSS"]
            },
            {
                "rule_id": "nodejs.information_disclosure",
                "severity": "high",
                "category": "security",
                "message": "Node.js Logging: Error stack trace returned to client",
                "file_path": "/tmp/vibeaudit_demo/test.js",
                "line_number": 18,
                "code_snippet": "res.status(500).json({ error: err.message, stack: err.stack });",
                "remediation": "Never return stack traces to clients in production",
                "confidence": 0.8,
                "metadata": {
                    "framework": "nodejs",
                    "cwe": "CWE-209",
                    "iso27001": "A.12.4.1",
                    "owasp": "A09-2021"
                },
                "standards": [
                    {
                        "id": "iso27001_a1241",
                        "name": "ISO 27001",
                        "type": "security",
                        "url": "https://www.iso.org/standard/54534.html",
                        "section": "A.12.4.1 - Event Logging"
                    }
                ],
                "compliance_frameworks": ["ISO 27001", "OWASP"]
            },
            {
                "rule_id": "nodejs.authentication",
                "severity": "critical",
                "category": "security",
                "message": "Node.js Authentication: Admin endpoint without authentication middleware",
                "file_path": "/tmp/vibeaudit_demo/test.js",
                "line_number": 25,
                "code_snippet": "app.get('/admin/config', (req, res) => {",
                "remediation": "Implement authentication middleware for all admin endpoints",
                "confidence": 0.8,
                "metadata": {
                    "framework": "nodejs",
                    "cwe": "CWE-306",
                    "iso27001": "A.9.1.2",
                    "owasp": "A07-2021"
                },
                "standards": [
                    {
                        "id": "iso27001_a912",
                        "name": "ISO 27001",
                        "type": "security",
                        "url": "https://www.iso.org/standard/54534.html",
                        "section": "A.9.1.2 - Access to Networks and Network Services"
                    }
                ],
                "compliance_frameworks": ["ISO 27001", "OWASP", "PCI DSS"]
            },
            {
                "rule_id": "nodejs.logging_security",
                "severity": "medium",
                "category": "security",
                "message": "Node.js Logging: Request body logged to file without encryption",
                "file_path": "/tmp/vibeaudit_demo/test.js",
                "line_number": 42,
                "code_snippet": "fs.appendFileSync('./app_logs.txt', JSON.stringify(req.body));",
                "remediation": "Encrypt sensitive data before logging and implement access controls",
                "confidence": 0.8,
                "metadata": {
                    "framework": "nodejs",
                    "cwe": "CWE-532",
                    "iso27001": "A.8.2.3",
                    "gdpr": "Art.32"
                },
                "standards": [
                    {
                        "id": "gdpr_art32",
                        "name": "GDPR",
                        "type": "compliance",
                        "url": "https://gdpr-info.eu/art-32-gdpr/",
                        "section": "Art. 32 - Security of Processing"
                    }
                ],
                "compliance_frameworks": ["GDPR", "HIPAA"]
            }
        ],
        "errors": {}
    }
    
    return demo_results