/**
 * Authentication + Role context for VibeCodeAuditor.
 * Handles auth state, profiles, and role-based access using Supabase.
 */

import React, { createContext, useContext, useEffect, useState, useCallback } from 'react'
import { supabase, isSupabaseConfigured } from '../lib/supabase'

const AuthContext = createContext({
  user: null,
  profile: null,
  loading: true,
  signIn: async () => ({ data: null, error: null }),
  signUp: async () => ({ data: null, error: null }),
  signOut: async () => ({ error: null }),
  resetPassword: async () => ({ error: null }),
  updateProfile: async () => ({ error: null }),
  isAuthenticated: false,
  isSupabaseEnabled: false,
  hasRole: () => false
})

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [profile, setProfile] = useState(null)
  const [loading, setLoading] = useState(true)

  const isSupabaseEnabled = isSupabaseConfigured()

  const createUserProfile = useCallback(async (userId) => {
    try {
      console.log('Creating profile for user ID:', userId);

      // Get user info from auth
      const { data: userData, error: userError } = await supabase.auth.getUser();

      if (userError) {
        console.error('Error getting user info:', userError);
        return;
      }

      const user = userData.user;
      const profileData = {
        user_id: userId,
        username: user.email,
        full_name: user.user_metadata?.full_name || user.email,
        organization: user.user_metadata?.organization || '',
        role_id: 'ac4c17be-fdb2-4e45-bcc4-96fe27b3be64', // Default to user role
        settings: {}
      };

      const { error: createError } = await supabase
        .from('profiles')
        .insert(profileData);

      if (createError) {
        console.error('Error creating profile:', createError);
      } else {
        console.log('Profile created successfully');
      }
    } catch (err) {
      console.error('Error in createUserProfile:', err);
    }
  }, [])

  const fetchUserProfile = useCallback(async (userId) => {
    try {
      console.log('Fetching profile for user ID:', userId);

      // Fetch profile with role information
      const { data: profileData, error: profileError } = await supabase
        .from('profiles')
        .select(`
          user_id,
          username,
          full_name,
          avatar_url,
          website,
          organization,
          roles (
            id,
            name,
            description
          )
        `)
        .eq('user_id', userId)
        .single()

      if (profileError) {
        console.error('Error fetching profile:', profileError);

        // If profile doesn't exist, create it automatically
        if (profileError.code === 'PGRST116') {
          console.log('Profile not found, creating new profile...');
          await createUserProfile(userId);

          // Try fetching again after creation
          const { data: newProfileData, error: newError } = await supabase
            .from('profiles')
            .select(`
              user_id,
              username,
              full_name,
              avatar_url,
              website,
              organization,
              roles (
                id,
                name,
                description
              )
            `)
            .eq('user_id', userId)
            .single();

          if (newError) {
            console.error('Error fetching new profile:', newError);
          } else {
            console.log('New profile fetched successfully:', newProfileData);
            setProfile({
              ...newProfileData,
              roles: newProfileData.roles ? [newProfileData.roles] : [{ name: 'user', description: 'Default user role' }],
            });
          }
        }
      } else {
        console.log('Profile fetched successfully:', profileData);
        setProfile({
          ...profileData,
          roles: profileData.roles ? [profileData.roles] : [{ name: 'user', description: 'Default user role' }],
        });
      }
    } catch (err) {
      console.error('Error in fetchUserProfile:', err)
    }
  }, [createUserProfile])

  useEffect(() => {
    if (!isSupabaseEnabled) {
      setLoading(false)
      return
    }

    const getInitialSession = async () => {
      try {
        const { data: { session }, error } = await supabase.auth.getSession()
        if (error) {
          console.error('Error getting session:', error)
        } else {
          setUser(session?.user ?? null)
          if (session?.user) {
            await fetchUserProfile(session.user.id)
          }
        }
      } catch (err) {
        console.error('Error in getInitialSession:', err)
      } finally {
        setLoading(false)
      }
    }

    getInitialSession()

    // Subscribe to auth changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      async (event, session) => {
        console.log('Auth state changed:', event, session?.user?.email)
        setUser(session?.user ?? null)
        if (session?.user) {
          console.log('Fetching profile for user:', session.user.id)
          await fetchUserProfile(session.user.id)
          console.log('Profile fetch completed')
        } else {
          setProfile(null)
        }
        console.log('Setting loading to false')
        setLoading(false)
      }
    )

    return () => {
      subscription.unsubscribe()
    }
  }, [isSupabaseEnabled, fetchUserProfile, createUserProfile])




  const signIn = async (email, password) => {
    if (!isSupabaseEnabled) {
      return { data: null, error: { message: 'Authentication not configured' } }
    }

    try {
      const { data, error } = await supabase.auth.signInWithPassword({ email, password })
      return { data, error }
    } catch (err) {
      return { data: null, error: err }
    }
  }

  const signUp = async (email, password, metadata = {}, roleId = null) => {
    if (!isSupabaseEnabled) {
      return { data: null, error: { message: 'Authentication not configured' } }
    }

    try {
      const { data, error } = await supabase.auth.signUp({
        email,
        password,
        options: {
          data: {
            full_name: metadata.fullName || '',
            organization: metadata.organization || '',
            ...metadata
          }
        }
      })

      if (data.user && data.user.id) {
        // Create user profile with role assignment
        const profileData = {
          user_id: data.user.id,
          username: email,
          full_name: metadata.fullName || '',
          organization: metadata.organization || '',
          role_id: roleId || 'user' // Default to 'user' role if not specified
        };

        // Insert profile data into the profiles table
        const { error: profileError } = await supabase
          .from('profiles')
          .upsert(profileData);

        if (profileError) {
          console.error('Error creating user profile:', profileError);
        }
      }

      return { data, error }
    } catch (err) {
      return { data: null, error: err }
    }
  }

  const signOut = async () => {
    if (!isSupabaseEnabled) {
      return { error: { message: 'Authentication not configured' } }
    }

    try {
      const { error } = await supabase.auth.signOut()
      return { error }
    } catch (err) {
      return { error: err }
    }
  }

  const resetPassword = async (email) => {
    if (!isSupabaseEnabled) {
      return { error: { message: 'Authentication not configured' } }
    }

    try {
      const { error } = await supabase.auth.resetPasswordForEmail(email, {
        redirectTo: `${window.location.origin}/reset-password`
      })
      return { error }
    } catch (err) {
      return { error: err }
    }
  }

  const updateProfile = async (updates) => {
    if (!isSupabaseEnabled || !user) {
      return { error: { message: 'Authentication not configured or user not logged in' } }
    }

    try {
      const { error } = await supabase
        .from('profiles')
        .upsert({
          user_id: user.id,
          ...updates,
          updated_at: new Date().toISOString()
        })

      if (!error) {
        setProfile(prev => ({ ...prev, ...updates }))
      }

      return { error }
    } catch (err) {
      return { error: err }
    }
  }

  /**
   * Role check helper
   */
  const hasRole = (roleName) => {
    // If we have role information from join
    if (profile?.roles?.name) {
      return profile.roles.name === roleName;
    }
    
    // If we only have role_id, we need to map it to role names
    // Based on the actual roles in the database
    const roleMappings = {
      'ac4c17be-fdb2-4e45-bcc4-96fe27b3be64': 'user',     // Standard user
      '196154e0-ecd8-4dd3-ac3d-e5ab61d81245': 'admin',    // Administrator
      '9aed130e-b405-4b7c-943d-b2ac4e2e6f01': 'auditor',  // Auditor
    };
    
    if (profile?.role_id && roleMappings[profile.role_id]) {
      return roleMappings[profile.role_id] === roleName;
    }
    
    return false;
  }

  const value = {
    user,
    profile,
    loading,
    signIn,
    signUp,
    signOut,
    resetPassword,
    updateProfile,
    isAuthenticated: !!user,
    isSupabaseEnabled,
    hasRole
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}
