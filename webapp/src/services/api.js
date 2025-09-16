/**
 * API service for VibeCodeAuditor with Supabase integration.
 */

import { supabase, isSupabaseConfigured } from '../lib/supabase'

const API_BASE = process.env.REACT_APP_API_URL || 'https://vibecodeauditor.onrender.com'

// Get auth token for API requests
const getAuthToken = async () => {
  if (!isSupabaseConfigured()) {
    return null
  }
  
  try {
    const { data: { session } } = await supabase.auth.getSession()
    return session?.access_token
  } catch (error) {
    console.error('Error getting auth token:', error)
    return null
  }
}

// Enhanced API client with auth
const apiClient = async (endpoint, options = {}) => {
  const token = await getAuthToken()
  
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers,
    },
    ...options,
  }

  const response = await fetch(`${API_BASE}${endpoint}`, config)
  
  if (!response.ok) {
    throw new Error(`API Error: ${response.statusText}`)
  }
  
  return response.json()
}

export const uploadAndScan = async (files, userId, config = {}) => {
  const token = await getAuthToken()
  const formData = new FormData()
  
  // Backend expects single file and user_id
  if (files.length > 0) {
    formData.append('file', files[0]) // Take first file
    formData.append('user_id', userId)
  }
  
  if (Object.keys(config).length > 0) {
    formData.append('config', JSON.stringify(config))
  }

  const response = await fetch(`${API_BASE}/scan`, {
    method: 'POST',
    headers: {
      ...(token && { Authorization: `Bearer ${token}` }),
    },
    body: formData,
  })

  if (!response.ok) {
    throw new Error(`Upload failed: ${response.statusText}`)
  }

  return response.json()
}

export const getScanResults = async (scanId) => {
  return apiClient(`/scan/${scanId}`)
}

export const getUserScans = async (userId) => {
  return apiClient(`/scans?user_id=${userId}`)
}

export const getScanStatus = async (scanId) => {
  return apiClient(`/api/scan/${scanId}/status`)
}

export const healthCheck = async () => {
  try {
    const response = await fetch(`${API_BASE}/health`)
    if (response.ok) {
      return response.json()
    }
    return { status: 'unavailable' }
  } catch (error) {
    return { status: 'unavailable', error: error.message }
  }
}