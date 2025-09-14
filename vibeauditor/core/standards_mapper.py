"""
Standards and compliance mapping for security issues.
Maps vulnerabilities to industry standards, best practices, and compliance frameworks.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional, Set
import re

class StandardType(Enum):
    """Types of standards and frameworks."""
    SECURITY_STANDARD = "security"
    COMPLIANCE_FRAMEWORK = "compliance"
    BEST_PRACTICE = "best_practice"
    CODING_STANDARD = "coding"
    INDUSTRY_GUIDELINE = "industry"

@dataclass
class StandardReference:
    """Reference to a specific standard or best practice."""
    id: str
    name: str
    type: StandardType
    description: str
    url: str
    section: Optional[str] = None
    severity_mapping: Optional[str] = None
    
class StandardsMapper:
    """Maps security issues to industry standards and best practices."""
    
    def __init__(self):
        self.standards_db = self._initialize_standards_database()
        self.cwe_mappings = self._initialize_cwe_mappings()
        self.compliance_mappings = self._initialize_compliance_mappings()
    
    def _initialize_standards_database(self) -> Dict[str, StandardReference]:
        """Initialize comprehensive standards database."""
        return {
            # OWASP Standards
            "owasp_top10_2021_a01": StandardReference(
                id="owasp_top10_2021_a01",
                name="OWASP Top 10 2021 - A01 Broken Access Control",
                type=StandardType.SECURITY_STANDARD,
                description="Restrictions on what authenticated users are allowed to do are often not properly enforced",
                url="https://owasp.org/Top10/A01_2021-Broken_Access_Control/",
                severity_mapping="High"
            ),
            "owasp_top10_2021_a02": StandardReference(
                id="owasp_top10_2021_a02",
                name="OWASP Top 10 2021 - A02 Cryptographic Failures",
                type=StandardType.SECURITY_STANDARD,
                description="Failures related to cryptography which often leads to sensitive data exposure",
                url="https://owasp.org/Top10/A02_2021-Cryptographic_Failures/",
                severity_mapping="High"
            ),
            "owasp_top10_2021_a03": StandardReference(
                id="owasp_top10_2021_a03",
                name="OWASP Top 10 2021 - A03 Injection",
                type=StandardType.SECURITY_STANDARD,
                description="Application is vulnerable to injection attacks",
                url="https://owasp.org/Top10/A03_2021-Injection/",
                severity_mapping="Critical"
            ),
            "owasp_top10_2021_a04": StandardReference(
                id="owasp_top10_2021_a04",
                name="OWASP Top 10 2021 - A04 Insecure Design",
                type=StandardType.SECURITY_STANDARD,
                description="Risks related to design flaws and missing or ineffective control design",
                url="https://owasp.org/Top10/A04_2021-Insecure_Design/",
                severity_mapping="High"
            ),
            "owasp_top10_2021_a05": StandardReference(
                id="owasp_top10_2021_a05",
                name="OWASP Top 10 2021 - A05 Security Misconfiguration",
                type=StandardType.SECURITY_STANDARD,
                description="Security misconfiguration is commonly a result of insecure default configurations",
                url="https://owasp.org/Top10/A05_2021-Security_Misconfiguration/",
                severity_mapping="Medium"
            ),
            "owasp_top10_2021_a06": StandardReference(
                id="owasp_top10_2021_a06",
                name="OWASP Top 10 2021 - A06 Vulnerable and Outdated Components",
                type=StandardType.SECURITY_STANDARD,
                description="Using components with known vulnerabilities",
                url="https://owasp.org/Top10/A06_2021-Vulnerable_and_Outdated_Components/",
                severity_mapping="High"
            ),
            "owasp_top10_2021_a07": StandardReference(
                id="owasp_top10_2021_a07",
                name="OWASP Top 10 2021 - A07 Identification and Authentication Failures",
                type=StandardType.SECURITY_STANDARD,
                description="Confirmation of the user's identity, authentication, and session management",
                url="https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/",
                severity_mapping="High"
            ),
            "owasp_top10_2021_a08": StandardReference(
                id="owasp_top10_2021_a08",
                name="OWASP Top 10 2021 - A08 Software and Data Integrity Failures",
                type=StandardType.SECURITY_STANDARD,
                description="Software and data integrity failures relate to code and infrastructure",
                url="https://owasp.org/Top10/A08_2021-Software_and_Data_Integrity_Failures/",
                severity_mapping="High"
            ),
            "owasp_top10_2021_a09": StandardReference(
                id="owasp_top10_2021_a09",
                name="OWASP Top 10 2021 - A09 Security Logging and Monitoring Failures",
                type=StandardType.SECURITY_STANDARD,
                description="Insufficient logging and monitoring, coupled with missing or ineffective integration",
                url="https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/",
                severity_mapping="Medium"
            ),
            "owasp_top10_2021_a10": StandardReference(
                id="owasp_top10_2021_a10",
                name="OWASP Top 10 2021 - A10 Server-Side Request Forgery",
                type=StandardType.SECURITY_STANDARD,
                description="SSRF flaws occur whenever a web application is fetching a remote resource",
                url="https://owasp.org/Top10/A10_2021-Server-Side_Request_Forgery_%28SSRF%29/",
                severity_mapping="Medium"
            ),
            
            # NIST Standards
            "nist_csf_identify": StandardReference(
                id="nist_csf_identify",
                name="NIST Cybersecurity Framework - Identify",
                type=StandardType.SECURITY_STANDARD,
                description="Develop organizational understanding to manage cybersecurity risk",
                url="https://www.nist.gov/cyberframework/online-learning/components-framework/core/identify",
                section="ID"
            ),
            "nist_csf_protect": StandardReference(
                id="nist_csf_protect",
                name="NIST Cybersecurity Framework - Protect",
                type=StandardType.SECURITY_STANDARD,
                description="Develop and implement appropriate safeguards",
                url="https://www.nist.gov/cyberframework/online-learning/components-framework/core/protect",
                section="PR"
            ),
            "nist_800_53_ac": StandardReference(
                id="nist_800_53_ac",
                name="NIST SP 800-53 - Access Control",
                type=StandardType.SECURITY_STANDARD,
                description="Security controls for federal information systems",
                url="https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final",
                section="AC - Access Control"
            ),
            "nist_800_53_sc": StandardReference(
                id="nist_800_53_sc",
                name="NIST SP 800-53 - System and Communications Protection",
                type=StandardType.SECURITY_STANDARD,
                description="System and communications protection controls",
                url="https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final",
                section="SC - System and Communications Protection"
            ),
            
            # ISO Standards
            "iso_27001_a12": StandardReference(
                id="iso_27001_a12",
                name="ISO/IEC 27001:2013 - A.12 Operations Security",
                type=StandardType.SECURITY_STANDARD,
                description="Ensure correct and secure operations of information processing facilities",
                url="https://www.iso.org/standard/54534.html",
                section="A.12 Operations Security"
            ),
            "iso_27001_a14": StandardReference(
                id="iso_27001_a14",
                name="ISO/IEC 27001:2013 - A.14 System Acquisition, Development and Maintenance",
                type=StandardType.SECURITY_STANDARD,
                description="Ensure security is built into information systems",
                url="https://www.iso.org/standard/54534.html",
                section="A.14 System Acquisition, Development and Maintenance"
            ),
            
            # PCI DSS
            "pci_dss_req_6": StandardReference(
                id="pci_dss_req_6",
                name="PCI DSS Requirement 6 - Secure Systems and Applications",
                type=StandardType.COMPLIANCE_FRAMEWORK,
                description="Develop and maintain secure systems and applications",
                url="https://www.pcisecuritystandards.org/document_library/",
                section="Requirement 6"
            ),
            
            # SOX Compliance
            "sox_404": StandardReference(
                id="sox_404",
                name="Sarbanes-Oxley Act Section 404",
                type=StandardType.COMPLIANCE_FRAMEWORK,
                description="Management assessment of internal controls",
                url="https://www.sec.gov/about/laws/soa2002.pdf",
                section="Section 404"
            ),
            
            # GDPR
            "gdpr_art_25": StandardReference(
                id="gdpr_art_25",
                name="GDPR Article 25 - Data Protection by Design and by Default",
                type=StandardType.COMPLIANCE_FRAMEWORK,
                description="Privacy by design and privacy by default",
                url="https://gdpr-info.eu/art-25-gdpr/",
                section="Article 25"
            ),
            "gdpr_art_32": StandardReference(
                id="gdpr_art_32",
                name="GDPR Article 32 - Security of Processing",
                type=StandardType.COMPLIANCE_FRAMEWORK,
                description="Appropriate technical and organisational measures",
                url="https://gdpr-info.eu/art-32-gdpr/",
                section="Article 32"
            ),
            
            # HIPAA
            "hipaa_164_312": StandardReference(
                id="hipaa_164_312",
                name="HIPAA 45 CFR 164.312 - Technical Safeguards",
                type=StandardType.COMPLIANCE_FRAMEWORK,
                description="Technical safeguards for electronic protected health information",
                url="https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-C/section-164.312",
                section="164.312"
            ),
            
            # SANS Top 25
            "sans_top25_cwe_79": StandardReference(
                id="sans_top25_cwe_79",
                name="SANS Top 25 - Cross-site Scripting",
                type=StandardType.SECURITY_STANDARD,
                description="Most dangerous software weaknesses",
                url="https://www.sans.org/top25-software-errors/",
                section="CWE-79"
            ),
            "sans_top25_cwe_89": StandardReference(
                id="sans_top25_cwe_89",
                name="SANS Top 25 - SQL Injection",
                type=StandardType.SECURITY_STANDARD,
                description="Most dangerous software weaknesses",
                url="https://www.sans.org/top25-software-errors/",
                section="CWE-89"
            ),
            
            # ASVS (Application Security Verification Standard)
            "asvs_v1": StandardReference(
                id="asvs_v1",
                name="OWASP ASVS V1 - Architecture, Design and Threat Modeling",
                type=StandardType.SECURITY_STANDARD,
                description="Application Security Verification Standard",
                url="https://owasp.org/www-project-application-security-verification-standard/",
                section="V1"
            ),
            "asvs_v2": StandardReference(
                id="asvs_v2",
                name="OWASP ASVS V2 - Authentication",
                type=StandardType.SECURITY_STANDARD,
                description="Authentication verification requirements",
                url="https://owasp.org/www-project-application-security-verification-standard/",
                section="V2"
            ),
            "asvs_v5": StandardReference(
                id="asvs_v5",
                name="OWASP ASVS V5 - Validation, Sanitization and Encoding",
                type=StandardType.SECURITY_STANDARD,
                description="Input validation and output encoding requirements",
                url="https://owasp.org/www-project-application-security-verification-standard/",
                section="V5"
            ),
            
            # NIST AI Risk Management Framework
            "eu_ai_act_high_risk": StandardReference(
                id="eu_ai_act_high_risk",
                name="EU AI Act - High-Risk AI Systems",
                type=StandardType.COMPLIANCE_FRAMEWORK,
                description="Requirements for high-risk AI systems under EU regulation",
                url="https://digital-strategy.ec.europa.eu/en/policies/european-approach-artificial-intelligence",
                section="Article 6"
            ),
            "nist_ai_rmf_govern": StandardReference(
                id="nist_ai_rmf_govern",
                name="NIST AI RMF - Govern Function",
                type=StandardType.SECURITY_STANDARD,
                description="AI Risk Management Framework - Governance",
                url="https://www.nist.gov/itl/ai-risk-management-framework",
                section="GOVERN"
            ),
            "nist_ai_rmf_measure": StandardReference(
                id="nist_ai_rmf_measure",
                name="NIST AI RMF - Measure Function",
                type=StandardType.SECURITY_STANDARD,
                description="AI Risk Management Framework - Measurement",
                url="https://www.nist.gov/itl/ai-risk-management-framework",
                section="MEASURE"
            ),
            
            # Coding Standards
            "pep8": StandardReference(
                id="pep8",
                name="PEP 8 - Style Guide for Python Code",
                type=StandardType.CODING_STANDARD,
                description="Python Enhancement Proposal 8",
                url="https://pep8.org/",
                section="Style Guide"
            ),
            "google_style_python": StandardReference(
                id="google_style_python",
                name="Google Python Style Guide",
                type=StandardType.CODING_STANDARD,
                description="Google's Python coding standards",
                url="https://google.github.io/styleguide/pyguide.html"
            ),
            "airbnb_javascript": StandardReference(
                id="airbnb_javascript",
                name="Airbnb JavaScript Style Guide",
                type=StandardType.CODING_STANDARD,
                description="A mostly reasonable approach to JavaScript",
                url="https://github.com/airbnb/javascript"
            ),
            
            # Industry Best Practices
            "microsoft_sdl": StandardReference(
                id="microsoft_sdl",
                name="Microsoft Security Development Lifecycle",
                type=StandardType.BEST_PRACTICE,
                description="Security practices for software development",
                url="https://www.microsoft.com/en-us/securityengineering/sdl/"
            ),
            "google_secure_coding": StandardReference(
                id="google_secure_coding",
                name="Google Secure Coding Practices",
                type=StandardType.BEST_PRACTICE,
                description="Security best practices for developers",
                url="https://developers.google.com/web/fundamentals/security/"
            ),
            "aws_security_best_practices": StandardReference(
                id="aws_security_best_practices",
                name="AWS Security Best Practices",
                type=StandardType.BEST_PRACTICE,
                description="Security best practices for AWS",
                url="https://aws.amazon.com/architecture/security-identity-compliance/"
            ),
        }
    
    def _initialize_cwe_mappings(self) -> Dict[str, List[str]]:
        """Map CWE IDs to relevant standards."""
        return {
            "CWE-79": ["owasp_top10_2021_a03", "sans_top25_cwe_79", "asvs_v5"],  # XSS
            "CWE-89": ["owasp_top10_2021_a03", "sans_top25_cwe_89", "asvs_v5"],  # SQL Injection
            "CWE-22": ["owasp_top10_2021_a01", "asvs_v1"],  # Path Traversal
            "CWE-502": ["owasp_top10_2021_a08", "asvs_v5"],  # Deserialization
            "CWE-16": ["owasp_top10_2021_a05", "nist_800_53_sc"],  # Configuration
            "CWE-20": ["owasp_top10_2021_a03", "asvs_v5"],  # Input Validation
            "CWE-200": ["owasp_top10_2021_a02", "gdpr_art_32"],  # Information Exposure
            "CWE-287": ["owasp_top10_2021_a07", "asvs_v2"],  # Authentication
            "CWE-352": ["owasp_top10_2021_a01", "asvs_v4"],  # CSRF
            "CWE-918": ["owasp_top10_2021_a10"],  # SSRF
        }
    
    def _initialize_compliance_mappings(self) -> Dict[str, List[str]]:
        """Map issue categories to compliance frameworks."""
        return {
            "data_privacy": ["gdpr_art_25", "gdpr_art_32", "hipaa_164_312"],
            "authentication": ["pci_dss_req_6", "nist_800_53_ac", "asvs_v2"],
            "encryption": ["pci_dss_req_6", "nist_800_53_sc", "gdpr_art_32"],
            "access_control": ["nist_800_53_ac", "iso_27001_a12"],
            "secure_development": ["iso_27001_a14", "microsoft_sdl"],
            "ai_ml_security": ["nist_ai_rmf_govern", "nist_ai_rmf_measure", "eu_ai_act_high_risk"],
            "ai_risk_management": ["eu_ai_act_high_risk", "nist_ai_rmf_govern"],
            "logging_monitoring": ["owasp_top10_2021_a09", "sox_404"],
        }
    
    def get_standards_for_issue(self, rule_id: str, cwe_id: Optional[str] = None, 
                               category: Optional[str] = None, 
                               framework: Optional[str] = None) -> List[StandardReference]:
        """Get relevant standards for a specific issue."""
        standards = []
        standard_ids = set()
        
        # Map by CWE ID
        if cwe_id and cwe_id in self.cwe_mappings:
            standard_ids.update(self.cwe_mappings[cwe_id])
        
        # Map by category
        if category and category in self.compliance_mappings:
            standard_ids.update(self.compliance_mappings[category])
        
        # Framework-specific mappings
        if framework:
            framework_standards = self._get_framework_specific_standards(framework, rule_id)
            standard_ids.update(framework_standards)
        
        # Rule-specific mappings
        rule_standards = self._get_rule_specific_standards(rule_id)
        standard_ids.update(rule_standards)
        
        # Convert IDs to StandardReference objects
        for std_id in standard_ids:
            if std_id in self.standards_db:
                standards.append(self.standards_db[std_id])
        
        return standards
    
    def _get_framework_specific_standards(self, framework: str, rule_id: str) -> List[str]:
        """Get standards specific to a framework."""
        framework_mappings = {
            "django": {
                "django.security": ["owasp_top10_2021_a05", "asvs_v1", "google_secure_coding"],
                "django.sql_injection": ["owasp_top10_2021_a03", "sans_top25_cwe_89"],
                "django.xss": ["owasp_top10_2021_a03", "sans_top25_cwe_79"],
            },
            "flask": {
                "flask.security": ["owasp_top10_2021_a05", "asvs_v1"],
                "flask.session": ["owasp_top10_2021_a07", "asvs_v2"],
            },
            "nodejs": {
                "nodejs.hardcoded_secrets": ["owasp_top10_2021_a02", "iso_27001_a12", "pci_dss_req_6"],
                "nodejs.input_validation": ["owasp_top10_2021_a03", "asvs_v5"],
                "nodejs.logging_security": ["owasp_top10_2021_a09", "gdpr_art_32", "iso_27001_a12"],
                "nodejs.authentication": ["owasp_top10_2021_a07", "asvs_v2", "iso_27001_a12"],
            },
            "express": {
                "express.security_misconfiguration": ["owasp_top10_2021_a05", "iso_27001_a12", "asvs_v1"],
                "express.cors": ["owasp_top10_2021_a05", "iso_27001_a12"],
                "express.error_handling": ["owasp_top10_2021_a09", "iso_27001_a12"],
            },
            "pytorch": {
                "pytorch.security": ["nist_ai_rmf_govern", "owasp_top10_2021_a08"],
                "pytorch.model_loading": ["nist_ai_rmf_measure", "owasp_top10_2021_a08"],
            },
            "tensorflow": {
                "tensorflow.security": ["nist_ai_rmf_govern", "owasp_top10_2021_a08"],
                "tensorflow.data_privacy": ["gdpr_art_25", "nist_ai_rmf_measure"],
            },
            "react": {
                "react.security": ["owasp_top10_2021_a03", "asvs_v5"],
                "react.xss": ["sans_top25_cwe_79", "owasp_top10_2021_a03"],
            },
        }
        
        if framework in framework_mappings and rule_id in framework_mappings[framework]:
            return framework_mappings[framework][rule_id]
        
        return []
    
    def _get_rule_specific_standards(self, rule_id: str) -> List[str]:
        """Get standards for specific rule patterns."""
        rule_patterns = {
            r".*hardcoded.*secret.*": ["owasp_top10_2021_a02", "asvs_v2"],
            r".*sql.*injection.*": ["owasp_top10_2021_a03", "sans_top25_cwe_89"],
            r".*xss.*": ["owasp_top10_2021_a03", "sans_top25_cwe_79"],
            r".*authentication.*": ["owasp_top10_2021_a07", "asvs_v2"],
            r".*authorization.*": ["owasp_top10_2021_a01", "nist_800_53_ac"],
            r".*encryption.*": ["owasp_top10_2021_a02", "nist_800_53_sc"],
            r".*logging.*": ["owasp_top10_2021_a09", "sox_404"],
            r".*ai.*ml.*": ["nist_ai_rmf_govern", "nist_ai_rmf_measure"],
            r".*privacy.*": ["gdpr_art_25", "gdpr_art_32"],
            r".*bias.*": ["nist_ai_rmf_measure", "gdpr_art_25"],
        }
        
        standards = []
        rule_lower = rule_id.lower()
        
        for pattern, std_list in rule_patterns.items():
            if re.search(pattern, rule_lower):
                standards.extend(std_list)
        
        return standards
    
    def get_compliance_summary(self, issues: List) -> Dict[str, Dict]:
        """Generate compliance summary for a set of issues."""
        compliance_summary = {}
        
        # Count issues by compliance framework
        framework_counts = {}
        
        for issue in issues:
            standards = self.get_standards_for_issue(
                rule_id=issue.rule_id,
                cwe_id=issue.metadata.get("cwe"),
                category=issue.category,
                framework=issue.metadata.get("framework")
            )
            
            for standard in standards:
                if standard.type == StandardType.COMPLIANCE_FRAMEWORK:
                    if standard.id not in framework_counts:
                        framework_counts[standard.id] = {
                            "name": standard.name,
                            "count": 0,
                            "critical": 0,
                            "high": 0,
                            "medium": 0,
                            "low": 0
                        }
                    
                    framework_counts[standard.id]["count"] += 1
                    severity = issue.severity.value.lower()
                    if severity in framework_counts[standard.id]:
                        framework_counts[standard.id][severity] += 1
        
        return framework_counts
    
    def get_remediation_guidance(self, standards: List[StandardReference]) -> Dict[str, str]:
        """Get remediation guidance based on standards."""
        guidance = {}
        
        for standard in standards:
            if standard.type == StandardType.SECURITY_STANDARD:
                guidance[standard.name] = f"Follow {standard.name} guidelines: {standard.url}"
            elif standard.type == StandardType.COMPLIANCE_FRAMEWORK:
                guidance[standard.name] = f"Ensure compliance with {standard.name}: {standard.url}"
            elif standard.type == StandardType.BEST_PRACTICE:
                guidance[standard.name] = f"Apply {standard.name}: {standard.url}"
        
        return guidance