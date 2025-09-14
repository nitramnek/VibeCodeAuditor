/**
 * Compliance API service for VibeCodeAuditor
 * Handles all compliance-related API operations
 */

import { supabase } from '../lib/supabase'

// Compliance Frameworks API
export const complianceFrameworksApi = {
  // Get all frameworks for user
  async getAll(userId) {
    const { data, error } = await supabase
      .from('compliance_frameworks')
      .select('*')
      .eq('user_id', userId)
      .order('created_at', { ascending: false })
    
    if (error) throw error
    return data
  },

  // Get framework by ID
  async getById(id) {
    const { data, error } = await supabase
      .from('compliance_frameworks')
      .select('*')
      .eq('id', id)
      .single()
    
    if (error) throw error
    return data
  },

  // Create new framework
  async create(frameworkData) {
    const { data, error } = await supabase
      .from('compliance_frameworks')
      .insert(frameworkData)
      .select()
      .single()
    
    if (error) throw error
    return data
  },

  // Update framework
  async update(id, updates) {
    const { data, error } = await supabase
      .from('compliance_frameworks')
      .update(updates)
      .eq('id', id)
      .select()
      .single()
    
    if (error) throw error
    return data
  },

  // Delete framework
  async delete(id) {
    const { error } = await supabase
      .from('compliance_frameworks')
      .delete()
      .eq('id', id)
    
    if (error) throw error
  }
}

// Compliance Audits API
export const complianceAuditsApi = {
  // Get all audits for user
  async getAll(userId, limit = 50) {
    const { data, error } = await supabase
      .from('compliance_audits')
      .select('*')
      .eq('user_id', userId)
      .order('audit_date', { ascending: false })
      .limit(limit)
    
    if (error) throw error
    return data
  },

  // Get audits by framework
  async getByFramework(frameworkId) {
    const { data, error } = await supabase
      .from('compliance_audits')
      .select('*')
      .eq('framework_id', frameworkId)
      .order('audit_date', { ascending: false })
    
    if (error) throw error
    return data
  },

  // Create new audit
  async create(auditData) {
    const { data, error } = await supabase
      .from('compliance_audits')
      .insert(auditData)
      .select()
      .single()
    
    if (error) throw error
    return data
  },

  // Update audit
  async update(id, updates) {
    const { data, error } = await supabase
      .from('compliance_audits')
      .update(updates)
      .eq('id', id)
      .select()
      .single()
    
    if (error) throw error
    return data
  }
}

// Compliance Controls API
export const complianceControlsApi = {
  // Get controls by framework
  async getByFramework(frameworkId) {
    const { data, error } = await supabase
      .from('compliance_controls')
      .select('*')
      .eq('framework_id', frameworkId)
      .order('control_id')
    
    if (error) throw error
    return data
  },

  // Create new control
  async create(controlData) {
    const { data, error } = await supabase
      .from('compliance_controls')
      .insert(controlData)
      .select()
      .single()
    
    if (error) throw error
    return data
  },

  // Update control
  async update(id, updates) {
    const { data, error } = await supabase
      .from('compliance_controls')
      .update(updates)
      .eq('id', id)
      .select()
      .single()
    
    if (error) throw error
    return data
  },

  // Bulk update control statuses
  async bulkUpdateStatus(controlIds, status) {
    const { data, error } = await supabase
      .from('compliance_controls')
      .update({ status, updated_at: new Date().toISOString() })
      .in('id', controlIds)
      .select()
    
    if (error) throw error
    return data
  }
}

// Compliance Issues API
export const complianceIssuesApi = {
  // Get issues by framework
  async getByFramework(frameworkId) {
    const { data, error } = await supabase
      .from('compliance_issues')
      .select('*')
      .eq('framework_id', frameworkId)
      .order('discovered_date', { ascending: false })
    
    if (error) throw error
    return data
  },

  // Get issues by severity
  async getBySeverity(severity, userId) {
    const { data, error } = await supabase
      .from('compliance_issues')
      .select('*')
      .eq('user_id', userId)
      .eq('severity', severity)
      .order('discovered_date', { ascending: false })
    
    if (error) throw error
    return data
  },

  // Create new issue
  async create(issueData) {
    const { data, error } = await supabase
      .from('compliance_issues')
      .insert(issueData)
      .select()
      .single()
    
    if (error) throw error
    return data
  },

  // Update issue
  async update(id, updates) {
    const { data, error } = await supabase
      .from('compliance_issues')
      .update(updates)
      .eq('id', id)
      .select()
      .single()
    
    if (error) throw error
    return data
  },

  // Resolve issue
  async resolve(id, resolution) {
    const { data, error } = await supabase
      .from('compliance_issues')
      .update({
        status: 'resolved',
        resolution_date: new Date().toISOString(),
        resolution,
        updated_at: new Date().toISOString()
      })
      .eq('id', id)
      .select()
      .single()
    
    if (error) throw error
    return data
  }
}

// Risk Assessments API
export const riskAssessmentsApi = {
  // Get all risk assessments for user
  async getAll(userId) {
    const { data, error } = await supabase
      .from('compliance_risk_assessments')
      .select('*')
      .eq('user_id', userId)
      .order('last_updated', { ascending: false })
    
    if (error) throw error
    return data
  },

  // Create new risk assessment
  async create(assessmentData) {
    const { data, error } = await supabase
      .from('compliance_risk_assessments')
      .insert(assessmentData)
      .select()
      .single()
    
    if (error) throw error
    return data
  },

  // Update risk assessment
  async update(id, updates) {
    const { data, error } = await supabase
      .from('compliance_risk_assessments')
      .update(updates)
      .eq('id', id)
      .select()
      .single()
    
    if (error) throw error
    return data
  }
}

// Policies API
export const policiesApi = {
  // Get all policies for user
  async getAll(userId) {
    const { data, error } = await supabase
      .from('compliance_policies')
      .select('*')
      .eq('user_id', userId)
      .order('last_reviewed', { ascending: false })
    
    if (error) throw error
    return data
  },

  // Get policies by framework
  async getByFramework(frameworkId) {
    const { data, error } = await supabase
      .from('compliance_policies')
      .select('*')
      .eq('framework_id', frameworkId)
      .order('last_reviewed', { ascending: false })
    
    if (error) throw error
    return data
  },

  // Create new policy
  async create(policyData) {
    const { data, error } = await supabase
      .from('compliance_policies')
      .insert(policyData)
      .select()
      .single()
    
    if (error) throw error
    return data
  },

  // Update policy
  async update(id, updates) {
    const { data, error } = await supabase
      .from('compliance_policies')
      .update(updates)
      .eq('id', id)
      .select()
      .single()
    
    if (error) throw error
    return data
  }
}

// Reports API
export const reportsApi = {
  // Get all reports for user
  async getAll(userId) {
    const { data, error } = await supabase
      .from('compliance_reports')
      .select('*')
      .eq('user_id', userId)
      .order('created_at', { ascending: false })
    
    if (error) throw error
    return data
  },

  // Create new report
  async create(reportData) {
    const { data, error } = await supabase
      .from('compliance_reports')
      .insert(reportData)
      .select()
      .single()
    
    if (error) throw error
    return data
  },

  // Update report status
  async updateStatus(id, status, fileUrl = null) {
    const updates = {
      status,
      updated_at: new Date().toISOString()
    }
    
    if (status === 'completed') {
      updates.generated_at = new Date().toISOString()
      if (fileUrl) updates.file_url = fileUrl
    }
    
    const { data, error } = await supabase
      .from('compliance_reports')
      .update(updates)
      .eq('id', id)
      .select()
      .single()
    
    if (error) throw error
    return data
  }
}

// Compliance Analytics API
export const complianceAnalyticsApi = {
  // Get compliance dashboard data
  async getDashboardData(userId) {
    try {
      // Fetch all data in parallel
      const [frameworks, audits, riskAssessments, policies, issues] = await Promise.all([
        complianceFrameworksApi.getAll(userId),
        complianceAuditsApi.getAll(userId, 10),
        riskAssessmentsApi.getAll(userId),
        policiesApi.getAll(userId),
        supabase
          .from('compliance_issues')
          .select('severity, status, framework_id')
          .eq('user_id', userId)
          .then(({ data, error }) => {
            if (error) throw error
            return data
          })
      ])

      // Calculate overall compliance score
      const overallScore = frameworks.length > 0
        ? Math.round(frameworks.reduce((sum, fw) => sum + (fw.compliance_score || 0), 0) / frameworks.length)
        : 0

      // Calculate issue statistics
      const issueStats = issues.reduce((stats, issue) => {
        stats.total++
        stats[issue.severity] = (stats[issue.severity] || 0) + 1
        if (issue.status === 'open') stats.open++
        return stats
      }, { total: 0, critical: 0, high: 0, medium: 0, low: 0, open: 0 })

      return {
        overallScore,
        frameworks: frameworks.map(fw => ({
          ...fw,
          // Map database fields to UI expected fields
          score: fw.compliance_score,
          controls: fw.total_controls,
          implemented: fw.implemented_controls,
          criticalIssues: fw.critical_issues,
          highIssues: fw.high_issues,
          mediumIssues: fw.medium_issues,
          lowIssues: fw.low_issues,
          lastAudit: fw.last_audit_date,
          nextAudit: fw.next_audit_date
        })),
        recentAudits: audits.map(audit => ({
          ...audit,
          // Map database fields to UI expected fields
          framework: audit.framework_name,
          type: audit.audit_type,
          date: audit.audit_date,
          findings: audit.total_findings,
          critical: audit.critical_findings,
          status: audit.status === 'completed' ? 
            (audit.critical_findings > 0 ? 'failed' : 
             audit.high_findings > 0 ? 'needs_attention' : 'passed') : 
            audit.status
        })),
        riskAssessments: riskAssessments.map(assessment => ({
          ...assessment,
          // Map database fields to UI expected fields
          score: assessment.risk_score,
          lastUpdated: assessment.last_updated,
          nextReview: assessment.next_review_date
        })),
        policies: policies.map(policy => ({
          ...policy,
          // Map database fields to UI expected fields
          lastReviewed: policy.last_reviewed,
          nextReview: policy.next_review_date
        })),
        issueStats
      }
    } catch (error) {
      console.error('Error fetching compliance dashboard data:', error)
      throw error
    }
  }
}