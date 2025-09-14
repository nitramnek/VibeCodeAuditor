// src/context/ProfileContext.js
import React, { createContext, useContext, useState, useEffect } from "react"
import { supabase } from "../supabaseClient"

const ProfileContext = createContext()

export const ProfileProvider = ({ children }) => {
  const [profile, setProfile] = useState(null)
  const [loading, setLoading] = useState(true)

  /**
   * Fetch profile + roles from Supabase
   */
  const fetchUserProfile = async (userId) => {
    try {
      // Get user email from auth
      const { data: { user }, error: userError } = await supabase.auth.getUser()
      const userEmail = user?.email || null

      // 1. Fetch profile with role information
      const { data: profileData, error: profileError } = await supabase
        .from("profiles")
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
        .eq("user_id", userId)
        .single()

      if (profileError) {
        if (profileError.code === "PGRST116") {
          // Profile doesn't exist, create it
          console.log("Profile not found, creating new profile...")

          // First, get the default role_id (assuming there's a 'user' role)
          const { data: defaultRole, error: roleError } = await supabase
            .from("roles")
            .select("id")
            .eq("name", "user")
            .single()

          if (roleError) {
            console.error("Error fetching default role:", roleError)
            return
          }

          const { data: newProfile, error: createError } = await supabase
            .from("profiles")
            .insert({
              user_id: userId,
              username: userEmail?.split('@')[0] || null,
              full_name: user?.user_metadata?.full_name || null,
              role_id: defaultRole.id
            })
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
            .single()

          if (createError) {
            console.error("Error creating profile:", createError)
            return
          }

          setProfile({
            ...newProfile,
            roles: newProfile.roles ? [newProfile.roles] : [{ name: 'user', description: 'Default user role' }],
          })
          return
        } else {
          console.error("Error fetching profile:", profileError)
          return
        }
      }

      // 2. Set profile with role information
      setProfile({
        ...profileData,
        roles: profileData.roles ? [profileData.roles] : [{ name: 'user', description: 'Default user role' }],
      })
    } catch (err) {
      console.error("Error in fetchUserProfile:", err)
    }
  }

  /**
   * Update profile details (not roles!)
   */
  const updateProfile = async (updates) => {
    try {
      const { error } = await supabase.from("profiles").upsert(updates)
      if (error) throw error
      setProfile((prev) => ({ ...prev, ...updates }))
    } catch (err) {
      console.error("Error updating profile:", err)
    }
  }

  /**
   * Role check helper
   */
  const hasRole = (roleName) => {
    return profile?.roles?.some((r) => r.name === roleName)
  }

  useEffect(() => {
    const loadProfile = async () => {
      const {
        data: { session },
      } = await supabase.auth.getSession()

      if (session?.user) {
        await fetchUserProfile(session.user.id)
      }
      setLoading(false)
    }

    loadProfile()

    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      if (session?.user) {
        fetchUserProfile(session.user.id)
      } else {
        setProfile(null)
      }
    })

    return () => subscription.unsubscribe()
  }, [])

  return (
    <ProfileContext.Provider
      value={{ profile, loading, updateProfile, hasRole }}
    >
      {children}
    </ProfileContext.Provider>
  )
}

export const useProfile = () => {
  return useContext(ProfileContext)
}
