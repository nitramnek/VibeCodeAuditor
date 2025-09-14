-- Fix for infinite recursion in profiles RLS policy
-- This issue occurs when the profiles table references itself in RLS policies

-- First, drop the problematic policies
DROP POLICY IF EXISTS "Users can view own profile" ON profiles;
DROP POLICY IF EXISTS "Users can update own profile" ON profiles;
DROP POLICY IF EXISTS "Users can insert own profile" ON profiles;

-- Recreate the policies with proper auth.uid() usage
CREATE POLICY "Users can view own profile" ON profiles
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON profiles
    FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Users can insert own profile" ON profiles
    FOR INSERT WITH CHECK (auth.uid() = id);

-- Fix the organizations policy to avoid recursion
DROP POLICY IF EXISTS "Users can view own organization" ON organizations;

-- Simplified organization policy - allow all authenticated users to view organizations
CREATE POLICY "Authenticated users can view organizations" ON organizations
    FOR SELECT USING (auth.uid() IS NOT NULL);

-- Fix the issues policy to avoid complex subqueries
DROP POLICY IF EXISTS "Users can view issues from own scans" ON issues;
DROP POLICY IF EXISTS "Users can update issues from own scans" ON issues;

-- Simplified issues policies
CREATE POLICY "Users can view issues from own scans" ON issues
    FOR SELECT USING (
        scan_id IN (
            SELECT id FROM scans WHERE user_id = auth.uid()
        )
    );

CREATE POLICY "Users can update issues from own scans" ON issues
    FOR UPDATE USING (
        scan_id IN (
            SELECT id FROM scans WHERE user_id = auth.uid()
        )
    );

-- Fix scan files policy
DROP POLICY IF EXISTS "Users can view files from own scans" ON scan_files;

CREATE POLICY "Users can view files from own scans" ON scan_files
    FOR SELECT USING (
        scan_id IN (
            SELECT id FROM scans WHERE user_id = auth.uid()
        )
    );

-- Fix audit logs policy
DROP POLICY IF EXISTS "Users can view own audit logs" ON audit_logs;

CREATE POLICY "Users can view own audit logs" ON audit_logs
    FOR SELECT USING (user_id = auth.uid());

-- Ensure auth.users is properly referenced
-- Grant necessary permissions
GRANT SELECT ON auth.users TO authenticated;
GRANT SELECT ON auth.users TO service_role;

-- Refresh the schema
-- Run this in your Supabase SQL editor to apply the fixes
