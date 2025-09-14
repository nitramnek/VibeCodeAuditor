/**
 * Tests for useScan hook
 */

import { renderHook, act } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { useScan } from '../useScan'

// Mock dependencies
jest.mock('../../lib/supabase', () => ({
  supabase: {
    auth: {
      getUser: jest.fn()
    },
    from: jest.fn()
  }
}))

jest.mock('../../services/api', () => ({
  uploadAndScan: jest.fn()
}))

const wrapper = ({ children }) => (
  <BrowserRouter>{children}</BrowserRouter>
)

describe('useScan', () => {
  it('should initialize with loading false', () => {
    const { result } = renderHook(() => useScan(), { wrapper })
    
    expect(result.current.loading).toBe(false)
    expect(typeof result.current.performScan).toBe('function')
  })

  it('should set loading to true during scan', async () => {
    const { result } = renderHook(() => useScan(), { wrapper })
    
    // Mock successful response
    const mockFiles = [new File(['test'], 'test.js', { type: 'text/javascript' })]
    
    act(() => {
      result.current.performScan(mockFiles)
    })
    
    expect(result.current.loading).toBe(true)
  })
})