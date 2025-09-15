/**
 * Supabase client configuration for VibeCodeAuditor frontend.
 */

import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL
const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY

// Create a mock client for when Supabase is not configured
const createMockClient = () => ({
  auth: {
    getSession: () => Promise.resolve({ data: { session: null }, error: null }),
    getUser: () => Promise.resolve({ data: { user: null }, error: null }),
    signInWithPassword: () => Promise.resolve({ data: null, error: { message: 'Authentication not configured' } }),
    signUp: () => Promise.resolve({ data: null, error: { message: 'Authentication not configured' } }),
    signOut: () => Promise.resolve({ error: null }),
    resetPasswordForEmail: () => Promise.resolve({ error: null }),
    onAuthStateChange: () => ({ data: { subscription: { unsubscribe: () => {} } } })
  },
  from: () => ({
    select: () => ({
      eq: () => ({
        single: () => Promise.resolve({ data: null, error: { message: 'Database not configured' } }),
        order: () => Promise.resolve({ data: [], error: null })
      }),
      order: () => Promise.resolve({ data: [], error: null })
    }),
    insert: () => Promise.resolve({ data: null, error: { message: 'Database not configured' } }),
    upsert: () => Promise.resolve({ data: null, error: { message: 'Database not configured' } }),
    update: () => Promise.resolve({ data: null, error: { message: 'Database not configured' } }),
    delete: () => Promise.resolve({ data: null, error: { message: 'Database not configured' } })
  })
})

if (!supabaseUrl || !supabaseAnonKey) {
  console.warn('Supabase credentials not found. Authentication features will be disabled.')
}

export const supabase = (supabaseUrl && supabaseAnonKey)
  ? createClient(supabaseUrl, supabaseAnonKey)
  : createMockClient()

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
