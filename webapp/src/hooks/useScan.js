/**
 * Custom hook for handling file scanning operations
 * Provides reusable scanning logic for Dashboard and Scanner components
 */

import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { supabase, isSupabaseConfigured } from '../lib/supabase'
import { uploadAndScan } from '../services/api'
import { ComplianceIntegrationService } from '../services/complianceIntegration'

export const useScan = () => {
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const performScan = async (files, scanName = null) => {
    try {
      setLoading(true)

      const fileList = Array.from(files)
      console.log(`Starting scan of ${fileList.length} file(s)...`)

      // In demo mode, skip authentication check
      const mockUserId = 'demo-user-123'
      const userId = isSupabaseConfigured() ? (await supabase.auth.getUser()).data?.user?.id : mockUserId

      if (isSupabaseConfigured() && !userId) {
        throw new Error("No authenticated user found!")
      }

      // Upload and start scan
      const response = await uploadAndScan(fileList, userId || mockUserId)
      console.log("Backend response:", response)
      console.log("Issues from backend:", response.issues)

      // Extract scan data
      const backendScanId = response.scan_id
      const issues = response.issues || []

      console.log("Backend scan ID:", backendScanId)
      console.log("Number of issues:", issues.length)

      if (!backendScanId) {
        throw new Error("No scan ID returned from backend")
      }

      let databaseScanId = `demo-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
      let scanData = null

      // Only save to database if Supabase is configured
      if (isSupabaseConfigured() && userId) {
        // Insert scan record in database
        const { data: dbScanData, error: scanError } = await supabase
          .from('scans')
          .insert([
            {
              user_id: userId,
              name: scanName || fileList[0].name || 'Scan',
              status: 'completed',
              file_count: fileList.length,
              summary: response.summary || {},
              compliance_summary: response.compliance_summary || {},
              detected_frameworks: response.detected_frameworks || {},
              total_issues: issues.length,
              critical_issues: issues.filter(i => i.severity === 'critical').length,
              high_issues: issues.filter(i => i.severity === 'high').length,
              medium_issues: issues.filter(i => i.severity === 'medium').length,
              low_issues: issues.filter(i => i.severity === 'low').length
            }
          ])
          .select()
          .single()

        if (scanError) {
          console.error("Error inserting scan:", scanError)
          throw new Error("Failed to save scan to database")
        }

        console.log("Inserted scan:", dbScanData)
        databaseScanId = dbScanData.id
        scanData = dbScanData

        // Insert issues if any
        if (issues.length > 0) {
          await insertIssues(issues, databaseScanId)

          // Map issues to compliance frameworks
          try {
            const complianceMapping = await ComplianceIntegrationService.mapIssuesToCompliance(
              databaseScanId,
              issues,
              userId
            )

            // Add compliance summary to scan data
            if (complianceMapping.frameworkImpacts && Object.keys(complianceMapping.frameworkImpacts).length > 0) {
              const complianceSummary = ComplianceIntegrationService.generateComplianceSummary(
                complianceMapping.frameworkImpacts
              )

              // Update scan with compliance summary
              await supabase
                .from('scans')
                .update({
                  compliance_summary: complianceSummary,
                  updated_at: new Date().toISOString()
                })
                .eq('id', databaseScanId)
            }
          } catch (complianceError) {
            console.error('Error mapping to compliance frameworks:', complianceError)
            // Don't fail the scan if compliance mapping fails
          }
        }
      } else {
        // Demo mode: create mock scan data
        scanData = {
          id: databaseScanId,
          name: scanName || fileList[0].name || 'Demo Scan',
          status: 'completed',
          file_count: fileList.length,
          summary: response.summary || {},
          compliance_summary: response.compliance_summary || {},
          detected_frameworks: response.detected_frameworks || {},
          total_issues: issues.length,
          critical_issues: issues.filter(i => i.severity === 'critical').length,
          high_issues: issues.filter(i => i.severity === 'high').length,
          medium_issues: issues.filter(i => i.severity === 'medium').length,
          low_issues: issues.filter(i => i.severity === 'low').length,
          created_at: new Date().toISOString()
        }
        console.log("Demo mode: Created mock scan data")
      }

      // Navigate to results with fallback data
      navigate(`/results/${databaseScanId}`, {
        state: {
          fallbackIssues: issues,
          scanData: scanData
        }
      })

      return { success: true, scanId: databaseScanId, issues }
    } catch (error) {
      console.error('Scan error:', error)
      // For demo purposes, still navigate to show the UI with proper UUID
      navigate('/results/123e4567-e89b-12d3-a456-426614174000')
      return { success: false, error: error.message }
    } finally {
      setLoading(false)
    }
  }

  const insertIssues = async (issues, scanId) => {
    // Skip database operations in demo mode
    if (!isSupabaseConfigured()) {
      console.log("Demo mode: Skipping issue insertion to database")
      return
    }

    // Try to insert with recommendation field first, fallback without it
    let issueError = null
    try {
      const { error } = await supabase
        .from('issues')
        .insert(
          issues.map(issue => ({
            scan_id: scanId,
            title: issue.description || issue.message || 'Security Issue',
            message: issue.description || issue.message || 'Security issue detected',
            description: issue.recommendation || issue.description || 'No description available',
            severity: issue.severity || 'medium',
            category: issue.issue_type || 'security',
            status: 'open',
            file_path: issue.file_path || null,
            line_number: issue.line_number || null,
            recommendation: issue.recommendation || 'Review and address this issue'
          }))
        )
      issueError = error
    } catch (error) {
      console.log("Trying without recommendation field...")
      // Fallback: insert without recommendation field
      const { error: fallbackError } = await supabase
        .from('issues')
        .insert(
          issues.map(issue => ({
            scan_id: scanId,
            title: issue.description || issue.message || 'Security Issue',
            message: issue.description || issue.message || 'Security issue detected',
            description: `${issue.recommendation || issue.description || 'No description available'}\n\nRecommendation: ${issue.recommendation || 'Review and address this issue'}`,
            severity: issue.severity || 'medium',
            category: issue.issue_type || 'security',
            status: 'open',
            file_path: issue.file_path || null,
            line_number: issue.line_number || null
          }))
        )
      issueError = fallbackError
    }

    if (issueError) {
      console.error("Error inserting issues:", issueError)
    } else {
      console.log("Inserted", issues.length, "issues for scan:", scanId)
    }
  }

  return {
    loading,
    performScan
  }
}