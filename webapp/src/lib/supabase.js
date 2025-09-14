/**
 * Supabase client configuration for VibeCodeAuditor frontend.
 */

import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL
const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY

if (!supabaseUrl || !supabaseAnonKey) {
  console.warn('Supabase credentials not found. Authentication features will be disabled.')
}

export const supabase = createClient(supabaseUrl || '', supabaseAnonKey || '')

// Database type definitions for TypeScript support
export const Tables = {
  PROFILES: 'profiles',
  ORGANIZATIONS: 'organizations', 
  SCANS: 'scans',
  ISSUES: 'issues',
  COMPLIANCE_FRAMEWORKS: 'compliance_frameworks',
  SCAN_FILES: 'scan_files',
  AUDIT_LOGS: 'audit_logs'
}

// Helper functions
export const isSupabaseConfigured = () => {
  return !!(supabaseUrl && supabaseAnonKey)
}