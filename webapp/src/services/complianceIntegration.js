/**
 * Compliance Integration Service
 * Maps security scan results to compliance frameworks and requirements
 */

import { complianceIssuesApi, complianceFrameworksApi } from './complianceApi'

// Compliance framework mappings for security issues
const COMPLIANCE_MAPPINGS = {
  // GDPR mappings
  gdpr: {
    patterns: [
      { pattern: /data.*protection|privacy|personal.*data|gdpr/i, severity: 'high' },
      { pattern: /encryption|crypto|hash/i, severity: 'medium' },
      { pattern: /authentication|authorization|access.*control/i, severity: 'medium' },
      { pattern: /logging|audit.*trail|monitoring/i, severity: 'low' }
    ],
    articles: {
      'Article 25': ['encryption', 'data protection by design'],
      'Article 32': ['security measures', 'encryption', 'access control'],
      'Article 33': ['breach notification', 'logging', 'monitoring'],
      'Article 35': ['privacy impact assessment', 'risk assessment']
    }
  },

  // HIPAA mappings
  hipaa: {
    patterns: [
      { pattern: /health.*information|phi|medical.*data|hipaa/i, severity: 'critical' },
      { pattern: /encryption|crypto/i, severity: 'high' },
      { pattern: /access.*control|authentication|authorization/i, severity: 'high' },
      { pattern: /audit.*log|monitoring|tracking/i, severity: 'medium' }
    ],
    safeguards: {
      'Administrative': ['access management', 'workforce training'],
      'Physical': ['facility access', 'workstation security'],
      'Technical': ['access control', 'audit controls', 'integrity', 'transmission security']
    }
  },

  // SOC 2 mappings
  soc2: {
    patterns: [
      { pattern: /security|soc.*2|trust.*services/i, severity: 'high' },
      { pattern: /availability|system.*availability/i, severity: 'medium' },
      { pattern: /processing.*integrity|data.*integrity/i, severity: 'medium' },
      { pattern: /confidentiality|data.*protection/i, severity: 'high' },
      { pattern: /privacy|personal.*information/i, severity: 'medium' }
    ],
    criteria: {
      'Security': ['access controls', 'logical security', 'system operations'],
      'Availability': ['system availability', 'capacity planning'],
      'Processing Integrity': ['data processing', 'system monitoring'],
      'Confidentiality': ['data protection', 'encryption'],
      'Privacy': ['personal information', 'privacy notice']
    }
  },

  // ISO 27001 mappings
  iso27001: {
    patterns: [
      { pattern: /information.*security|iso.*27001|isms/i, severity: 'high' },
      { pattern: /risk.*management|risk.*assessment/i, severity: 'medium' },
      { pattern: /access.*control|identity.*management/i, severity: 'medium' },
      { pattern: /incident.*response|security.*incident/i, severity: 'high' },
      { pattern: /business.*continuity|disaster.*recovery/i, severity: 'medium' }
    ],
    controls: {
      'A.5': ['Information Security Policies'],
      'A.6': ['Organization of Information Security'],
      'A.7': ['Human Resource Security'],
      'A.8': ['Asset Management'],
      'A.9': ['Access Control'],
      'A.10': ['Cryptography'],
      'A.11': ['Physical and Environmental Security'],
      'A.12': ['Operations Security'],
      'A.13': ['Communications Security'],
      'A.14': ['System Acquisition, Development and Maintenance'],
      'A.15': ['Supplier Relationships'],
      'A.16': ['Information Security Incident Management'],
      'A.17': ['Information Security Aspects of Business Continuity Management'],
      'A.18': ['Compliance']
    }
  },

  // PCI DSS mappings
  pci_dss: {
    patterns: [
      { pattern: /payment.*card|credit.*card|pci.*dss|cardholder.*data/i, severity: 'critical' },
      { pattern: /encryption|crypto.*key/i, severity: 'high' },
      { pattern: /network.*security|firewall/i, severity: 'high' },
      { pattern: /access.*control|authentication/i, severity: 'high' },
      { pattern: /vulnerability.*scan|security.*test/i, severity: 'medium' }
    ],
    requirements: {
      'Req 1': ['Install and maintain firewall configuration'],
      'Req 2': ['Do not use vendor-supplied defaults'],
      'Req 3': ['Protect stored cardholder data'],
      'Req 4': ['Encrypt transmission of cardholder data'],
      'Req 5': ['Protect all systems against malware'],
      'Req 6': ['Develop and maintain secure systems'],
      'Req 7': ['Restrict access to cardholder data'],
      'Req 8': ['Identify and authenticate access'],
      'Req 9': ['Restrict physical access'],
      'Req 10': ['Track and monitor access'],
      'Req 11': ['Regularly test security systems'],
      'Req 12': ['Maintain information security policy']
    }
  }
}

export class ComplianceIntegrationService {
  /**
   * Map security scan issues to compliance frameworks
   */
  static async mapIssuesToCompliance(scanId, issues, userId) {
    try {
      // Get user's active compliance frameworks
      const frameworks = await complianceFrameworksApi.getAll(userId)
      const activeFrameworks = frameworks.filter(fw => fw.status === 'active')

      const complianceIssues = []
      const frameworkImpacts = {}

      // Initialize framework impact counters
      activeFrameworks.forEach(fw => {
        frameworkImpacts[fw.code] = {
          framework_id: fw.id,
          framework_name: fw.name,
          total: 0,
          critical: 0,
          high: 0,
          medium: 0,
          low: 0,
          issues: []
        }
      })

      // Process each security issue
      for (const issue of issues) {
        const issueText = `${issue.title || ''} ${issue.description || ''} ${issue.category || ''}`.toLowerCase()
        
        // Check against each active framework
        for (const framework of activeFrameworks) {
          const mapping = COMPLIANCE_MAPPINGS[framework.code]
          if (!mapping) continue

          // Check if issue matches framework patterns
          const matchedPatterns = mapping.patterns.filter(p => p.pattern.test(issueText))
          
          if (matchedPatterns.length > 0) {
            // Determine compliance severity (use highest matched pattern severity)
            const complianceSeverity = this.getHighestSeverity(matchedPatterns.map(p => p.severity))
            
            // Create compliance issue
            const complianceIssue = {
              user_id: userId,
              framework_id: framework.id,
              title: `${framework.name} Compliance Issue: ${issue.title || issue.description}`,
              description: this.generateComplianceDescription(issue, framework, mapping),
              severity: complianceSeverity,
              status: 'open',
              issue_type: 'security_scan_finding',
              discovered_date: new Date().toISOString().split('T')[0],
              reported_by: 'Security Scanner',
              evidence: JSON.stringify({
                scan_id: scanId,
                original_issue: issue,
                matched_patterns: matchedPatterns.map(p => p.pattern.source)
              }),
              tags: [framework.code, 'automated_scan', issue.category || 'security'].filter(Boolean)
            }

            complianceIssues.push(complianceIssue)
            
            // Update framework impact counters
            frameworkImpacts[framework.code].total++
            frameworkImpacts[framework.code][complianceSeverity]++
            frameworkImpacts[framework.code].issues.push(complianceIssue)
          }
        }
      }

      // Insert compliance issues
      if (complianceIssues.length > 0) {
        for (const complianceIssue of complianceIssues) {
          await complianceIssuesApi.create(complianceIssue)
        }
      }

      // Update framework issue counts
      for (const [frameworkCode, impact] of Object.entries(frameworkImpacts)) {
        if (impact.total > 0) {
          const framework = activeFrameworks.find(fw => fw.code === frameworkCode)
          await complianceFrameworksApi.update(framework.id, {
            critical_issues: (framework.critical_issues || 0) + impact.critical,
            high_issues: (framework.high_issues || 0) + impact.high,
            medium_issues: (framework.medium_issues || 0) + impact.medium,
            low_issues: (framework.low_issues || 0) + impact.low
          })
        }
      }

      return {
        complianceIssues,
        frameworkImpacts: Object.fromEntries(
          Object.entries(frameworkImpacts).filter(([_, impact]) => impact.total > 0)
        )
      }
    } catch (error) {
      console.error('Error mapping issues to compliance:', error)
      throw error
    }
  }

  /**
   * Generate compliance-specific description for an issue
   */
  static generateComplianceDescription(issue, framework, mapping) {
    let description = `Security issue identified during automated scan that may impact ${framework.name} compliance.\n\n`
    
    description += `**Original Issue:** ${issue.description || issue.title}\n`
    description += `**Severity:** ${issue.severity}\n`
    description += `**Category:** ${issue.category || 'Security'}\n\n`
    
    if (issue.file_path) {
      description += `**Location:** ${issue.file_path}`
      if (issue.line_number) description += `:${issue.line_number}`
      description += '\n\n'
    }

    // Add framework-specific guidance
    switch (framework.code) {
      case 'gdpr':
        description += `**GDPR Relevance:** This issue may affect data protection requirements under GDPR Articles 25 (Data Protection by Design) and 32 (Security of Processing).\n\n`
        break
      case 'hipaa':
        description += `**HIPAA Relevance:** This security vulnerability may compromise Protected Health Information (PHI) and violate HIPAA Security Rule requirements.\n\n`
        break
      case 'soc2':
        description += `**SOC 2 Relevance:** This issue may impact the Security trust service criteria and affect system security controls.\n\n`
        break
      case 'iso27001':
        description += `**ISO 27001 Relevance:** This security issue may indicate non-compliance with information security management system (ISMS) requirements.\n\n`
        break
      case 'pci_dss':
        description += `**PCI DSS Relevance:** This vulnerability may affect cardholder data security and PCI DSS compliance requirements.\n\n`
        break
    }

    if (issue.recommendation) {
      description += `**Recommended Action:** ${issue.recommendation}\n\n`
    }

    description += `**Compliance Impact:** Review and remediate this issue to maintain ${framework.name} compliance posture.`

    return description
  }

  /**
   * Get the highest severity from a list of severities
   */
  static getHighestSeverity(severities) {
    const severityOrder = ['low', 'medium', 'high', 'critical']
    return severities.reduce((highest, current) => {
      return severityOrder.indexOf(current) > severityOrder.indexOf(highest) ? current : highest
    }, 'low')
  }

  /**
   * Generate compliance summary for scan results
   */
  static generateComplianceSummary(frameworkImpacts) {
    const summary = {}
    
    for (const [frameworkCode, impact] of Object.entries(frameworkImpacts)) {
      summary[frameworkCode] = {
        name: impact.framework_name,
        count: impact.total,
        critical: impact.critical,
        high: impact.high,
        medium: impact.medium,
        low: impact.low
      }
    }

    return summary
  }

  /**
   * Get compliance framework recommendations based on scan results
   */
  static getFrameworkRecommendations(issues) {
    const recommendations = []
    const issueText = issues.map(i => `${i.title || ''} ${i.description || ''} ${i.category || ''}`).join(' ').toLowerCase()

    // Analyze issues and recommend frameworks
    if (/personal.*data|privacy|gdpr|data.*protection/i.test(issueText)) {
      recommendations.push({
        framework: 'GDPR',
        code: 'gdpr',
        reason: 'Issues related to personal data protection detected',
        priority: 'high'
      })
    }

    if (/health.*information|medical.*data|phi|hipaa/i.test(issueText)) {
      recommendations.push({
        framework: 'HIPAA',
        code: 'hipaa',
        reason: 'Healthcare data security issues detected',
        priority: 'critical'
      })
    }

    if (/payment|credit.*card|financial|pci/i.test(issueText)) {
      recommendations.push({
        framework: 'PCI DSS',
        code: 'pci_dss',
        reason: 'Payment card data security issues detected',
        priority: 'critical'
      })
    }

    if (issues.length > 5) {
      recommendations.push({
        framework: 'ISO 27001',
        code: 'iso27001',
        reason: 'Multiple security issues suggest need for comprehensive ISMS',
        priority: 'medium'
      })
    }

    return recommendations
  }
}