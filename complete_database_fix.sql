-- Complete Database Fix for VibeCodeAuditor
-- This will completely remove all problematic policies and create new ones

-- 1. DISABLE RLS temporarily to avoid conflicts
ALTER TABLE public.user_organizations DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.scans DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.profiles DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.issues DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.scan_files DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.audit_logs DISABLE ROW LEVEL SECURITY;

-- 2. DROP ALL EXISTING POLICIES (this removes any problematic ones)
DO $$ 
DECLARE 
    r RECORD;
BEGIN
    -- Drop all policies on user_organizations
    FOR r IN (SELECT policyname FROM pg_policies WHERE tablename = 'user_organizations' AND schemaname = 'public') LOOP
        EXECUTE 'DROP POLICY IF EXISTS ' || quote_ident(r.policyname) || ' ON public.user_organizations';
    END LOOP;
    
    -- Drop all policies on scans
    FOR r IN (SELECT policyname FROM pg_policies WHERE tablename = 'scans' AND schemaname = 'public') LOOP
        EXECUTE 'DROP POLICY IF EXISTS ' || quote_ident(r.policyname) || ' ON public.scans';
    END LOOP;
    
    -- Drop all policies on profiles
    FOR r IN (SELECT policyname FROM pg_policies WHERE tablename = 'profiles' AND schemaname = 'public') LOOP
        EXECUTE 'DROP POLICY IF EXISTS ' || quote_ident(r.policyname) || ' ON public.profiles';
    END LOOP;
    
    -- Drop all policies on issues
    FOR r IN (SELECT policyname FROM pg_policies WHERE tablename = 'issues' AND schemaname = 'public') LOOP
        EXECUTE 'DROP POLICY IF EXISTS ' || quote_ident(r.policyname) || ' ON public.issues';
    END LOOP;
    
    -- Drop all policies on scan_files
    FOR r IN (SELECT policyname FROM pg_policies WHERE tablename = 'scan_files' AND schemaname = 'public') LOOP
        EXECUTE 'DROP POLICY IF EXISTS ' || quote_ident(r.policyname) || ' ON public.scan_files';
    END LOOP;
    
    -- Drop all policies on audit_logs
    FOR r IN (SELECT policyname FROM pg_policies WHERE tablename = 'audit_logs' AND schemaname = 'public') LOOP
        EXECUTE 'DROP POLICY IF EXISTS ' || quote_ident(r.policyname) || ' ON public.audit_logs';
    END LOOP;
END $$;

-- 3. ADD MISSING COLUMNS to issues table if they don't exist
ALTER TABLE public.issues 
ADD COLUMN IF NOT EXISTS title text,
ADD COLUMN IF NOT EXISTS description text,
ADD COLUMN IF NOT EXISTS file_path text,
ADD COLUMN IF NOT EXISTS line_number integer,
ADD COLUMN IF NOT EXISTS recommendation text;

-- 4. CREATE SIMPLE, NON-RECURSIVE POLICIES

-- PROFILES TABLE
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "profiles_own_data" ON public.profiles
    FOR ALL USING (auth.uid() = user_id);

-- SCANS TABLE  
ALTER TABLE public.scans ENABLE ROW LEVEL SECURITY;

CREATE POLICY "scans_own_data" ON public.scans
    FOR ALL USING (auth.uid() = user_id);

-- ISSUES TABLE
ALTER TABLE public.issues ENABLE ROW LEVEL SECURITY;

CREATE POLICY "issues_own_scans" ON public.issues
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM public.scans 
            WHERE scans.id = issues.scan_id 
            AND scans.user_id = auth.uid()
        )
    );

-- SCAN_FILES TABLE
ALTER TABLE public.scan_files ENABLE ROW LEVEL SECURITY;

CREATE POLICY "scan_files_own_scans" ON public.scan_files
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM public.scans 
            WHERE scans.id = scan_files.scan_id 
            AND scans.user_id = auth.uid()
        )
    );

-- AUDIT_LOGS TABLE
ALTER TABLE public.audit_logs ENABLE ROW LEVEL SECURITY;

CREATE POLICY "audit_logs_own_data" ON public.audit_logs
    FOR ALL USING (auth.uid() = user_id);

-- USER_ORGANIZATIONS TABLE - SIMPLE POLICY WITHOUT RECURSION
ALTER TABLE public.user_organizations ENABLE ROW LEVEL SECURITY;

CREATE POLICY "user_organizations_own_data" ON public.user_organizations
    FOR ALL USING (auth.uid() = user_id);

-- 5. INSERT DEFAULT DATA if missing

-- Insert default roles
INSERT INTO public.roles (id, name, description) VALUES 
    ('ac4c17be-fdb2-4e45-bcc4-96fe27b3be64', 'user', 'Standard user role'),
    ('196154e0-ecd8-4dd3-ac3d-e5ab61d81245', 'admin', 'Administrator role'),
    ('9aed130e-b405-4b7c-943d-b2ac4e2e6f01', 'auditor', 'Auditor role')
ON CONFLICT (name) DO NOTHING;

-- Insert default organization
INSERT INTO public.organizations (name) VALUES ('Default Organization')
ON CONFLICT (name) DO NOTHING;

-- 6. CREATE INDEXES for better performance
CREATE INDEX IF NOT EXISTS idx_scans_user_id ON public.scans(user_id);
CREATE INDEX IF NOT EXISTS idx_scans_created_at ON public.scans(created_at);
CREATE INDEX IF NOT EXISTS idx_profiles_user_id ON public.profiles(user_id);
CREATE INDEX IF NOT EXISTS idx_user_organizations_user_id ON public.user_organizations(user_id);
CREATE INDEX IF NOT EXISTS idx_issues_scan_id ON public.issues(scan_id);
CREATE INDEX IF NOT EXISTS idx_issues_severity ON public.issues(severity);
CREATE INDEX IF NOT EXISTS idx_issues_status ON public.issues(status);

-- 7. VERIFY POLICIES (this will show what policies exist after our changes)
SELECT 
    schemaname,
    tablename,
    policyname,
    permissive,
    roles,
    cmd,
    qual,
    with_check
FROM pg_policies 
WHERE schemaname = 'public' 
ORDER BY tablename, policyname;