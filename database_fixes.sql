-- Fix for VibeCodeAuditor Database Schema Issues
-- This addresses the infinite recursion and aligns the schema with frontend expectations

-- 1. Drop problematic policies that cause infinite recursion
DROP POLICY IF EXISTS "user_organizations_policy" ON public.user_organizations;
DROP POLICY IF EXISTS "Users can view their own organization memberships" ON public.user_organizations;
DROP POLICY IF EXISTS "Users can manage their organization memberships" ON public.user_organizations;

-- 2. Create simple, non-recursive RLS policies
ALTER TABLE public.user_organizations ENABLE ROW LEVEL SECURITY;

-- Simple policy: users can only see their own organization memberships
CREATE POLICY "user_organizations_select_policy" ON public.user_organizations
    FOR SELECT USING (auth.uid() = user_id);

-- Users can insert their own memberships (for joining organizations)
CREATE POLICY "user_organizations_insert_policy" ON public.user_organizations
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Users can update their own memberships
CREATE POLICY "user_organizations_update_policy" ON public.user_organizations
    FOR UPDATE USING (auth.uid() = user_id);

-- 3. Fix scans table policies
ALTER TABLE public.scans ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "scans_policy" ON public.scans;

-- Users can view their own scans
CREATE POLICY "scans_select_policy" ON public.scans
    FOR SELECT USING (auth.uid() = user_id);

-- Users can create their own scans
CREATE POLICY "scans_insert_policy" ON public.scans
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Users can update their own scans
CREATE POLICY "scans_update_policy" ON public.scans
    FOR UPDATE USING (auth.uid() = user_id);

-- 4. Fix profiles table policies
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "profiles_policy" ON public.profiles;

-- Users can view their own profile
CREATE POLICY "profiles_select_policy" ON public.profiles
    FOR SELECT USING (auth.uid() = user_id);

-- Users can insert their own profile
CREATE POLICY "profiles_insert_policy" ON public.profiles
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Users can update their own profile
CREATE POLICY "profiles_update_policy" ON public.profiles
    FOR UPDATE USING (auth.uid() = user_id);

-- 5. Add missing indexes for performance
CREATE INDEX IF NOT EXISTS idx_scans_user_id ON public.scans(user_id);
CREATE INDEX IF NOT EXISTS idx_scans_created_at ON public.scans(created_at);
CREATE INDEX IF NOT EXISTS idx_profiles_user_id ON public.profiles(user_id);
CREATE INDEX IF NOT EXISTS idx_user_organizations_user_id ON public.user_organizations(user_id);

-- 6. Insert default roles if they don't exist
INSERT INTO public.roles (id, name, description) VALUES 
    ('ac4c17be-fdb2-4e45-bcc4-96fe27b3be64', 'user', 'Standard user role'),
    ('196154e0-ecd8-4dd3-ac3d-e5ab61d81245', 'admin', 'Administrator role'),
    ('9aed130e-b405-4b7c-943d-b2ac4e2e6f01', 'auditor', 'Auditor role')
ON CONFLICT (name) DO NOTHING;

-- 7. Create a default organization if none exists
INSERT INTO public.organizations (name) VALUES ('Default Organization')
ON CONFLICT (name) DO NOTHING;
-- 8. Add 
missing columns to issues table for better issue tracking
ALTER TABLE public.issues 
ADD COLUMN IF NOT EXISTS title text,
ADD COLUMN IF NOT EXISTS description text,
ADD COLUMN IF NOT EXISTS file_path text,
ADD COLUMN IF NOT EXISTS line_number integer,
ADD COLUMN IF NOT EXISTS recommendation text;

-- 9. Enable RLS on issues table
ALTER TABLE public.issues ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "issues_policy" ON public.issues;

-- Users can view issues from their own scans
CREATE POLICY "issues_select_policy" ON public.issues
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM public.scans 
            WHERE scans.id = issues.scan_id 
            AND scans.user_id = auth.uid()
        )
    );

-- Users can insert issues for their own scans
CREATE POLICY "issues_insert_policy" ON public.issues
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.scans 
            WHERE scans.id = issues.scan_id 
            AND scans.user_id = auth.uid()
        )
    );

-- Users can update issues from their own scans
CREATE POLICY "issues_update_policy" ON public.issues
    FOR UPDATE USING (
        EXISTS (
            SELECT 1 FROM public.scans 
            WHERE scans.id = issues.scan_id 
            AND scans.user_id = auth.uid()
        )
    );

-- 10. Add indexes for better performance
CREATE INDEX IF NOT EXISTS idx_issues_scan_id ON public.issues(scan_id);
CREATE INDEX IF NOT EXISTS idx_issues_severity ON public.issues(severity);
CREATE INDEX IF NOT EXISTS idx_issues_status ON public.issues(status);

-- 11. Enable RLS on other tables
ALTER TABLE public.scan_files ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.audit_logs ENABLE ROW LEVEL SECURITY;

-- Scan files policies
CREATE POLICY "scan_files_select_policy" ON public.scan_files
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM public.scans 
            WHERE scans.id = scan_files.scan_id 
            AND scans.user_id = auth.uid()
        )
    );

CREATE POLICY "scan_files_insert_policy" ON public.scan_files
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.scans 
            WHERE scans.id = scan_files.scan_id 
            AND scans.user_id = auth.uid()
        )
    );

-- Audit logs policies
CREATE POLICY "audit_logs_select_policy" ON public.audit_logs
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "audit_logs_insert_policy" ON public.audit_logs
    FOR INSERT WITH CHECK (auth.uid() = user_id);