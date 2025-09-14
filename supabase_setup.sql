-- VibeCodeAuditor Supabase Database Schema
-- Run this in your Supabase SQL editor

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table (extends Supabase auth.users)
CREATE TABLE IF NOT EXISTS public.profiles (
    user_id UUID NOT NULL,
    username TEXT UNIQUE,
    full_name TEXT,
    avatar_url TEXT,
    website TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()),
    role_id UUID NOT NULL,
    organization BIGINT,
    CONSTRAINT profiles_pkey PRIMARY KEY (user_id),
    CONSTRAINT profiles_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id),
    CONSTRAINT profiles_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id),
    CONSTRAINT profiles_organization_fkey FOREIGN KEY (organization) REFERENCES public.organizations(id)
);

-- Organizations table
CREATE TABLE IF NOT EXISTS public.organizations (
    id BIGINT GENERATED ALWAYS AS IDENTITY NOT NULL,
    name TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    CONSTRAINT organizations_pkey PRIMARY KEY (id)
);

-- Scans table
CREATE TABLE IF NOT EXISTS public.scans (
    user_id UUID,
    organization_id BIGINT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    config JSONB,
    name TEXT,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    status TEXT DEFAULT 'pending'::text CHECK (status = ANY (ARRAY['pending'::text, 'in_progress'::text, 'completed'::text, 'failed'::text])),
    compliance_summary JSONB DEFAULT '{}'::jsonb,
    summary JSONB DEFAULT '{}'::jsonb,
    detected_frameworks JSONB DEFAULT '{}'::jsonb,
    file_count INTEGER DEFAULT 0,
    total_issues INTEGER DEFAULT 0,
    critical_issues INTEGER DEFAULT 0,
    high_issues INTEGER DEFAULT 0,
    medium_issues INTEGER DEFAULT 0,
    low_issues INTEGER DEFAULT 0,
    id UUID NOT NULL DEFAULT gen_random_uuid() UNIQUE,
    CONSTRAINT scans_pkey PRIMARY KEY (id),
    CONSTRAINT scans_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organizations(id),
    CONSTRAINT scans_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id)
);

-- Issues table
CREATE TABLE IF NOT EXISTS public.issues (
    id BIGINT GENERATED ALWAYS AS IDENTITY NOT NULL,
    severity TEXT CHECK (severity = ANY (ARRAY['low'::text, 'medium'::text, 'high'::text, 'critical'::text])),
    status TEXT CHECK (status = ANY (ARRAY['open'::text, 'in_progress'::text, 'resolved'::text, 'closed'::text])),
    assigned_to UUID,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    title TEXT,
    description TEXT,
    file_path TEXT,
    line_number INTEGER,
    recommendation TEXT,
    scan_id UUID,
    CONSTRAINT issues_pkey PRIMARY KEY (id),
    CONSTRAINT issues_assigned_to_fkey FOREIGN KEY (assigned_to) REFERENCES auth.users(id),
    CONSTRAINT issues_scan_id_fkey FOREIGN KEY (scan_id) REFERENCES public.scans(id)
);

-- Compliance frameworks reference table
CREATE TABLE IF NOT EXISTS public.compliance_frameworks (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    version TEXT,
    url TEXT,
    standards JSONB DEFAULT '[]',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Scan files table (for file storage references)
CREATE TABLE IF NOT EXISTS public.scan_files (
    id BIGINT GENERATED ALWAYS AS IDENTITY NOT NULL,
    file_path TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    scan_id UUID UNIQUE,
    CONSTRAINT scan_files_pkey PRIMARY KEY (id),
    CONSTRAINT scan_files_scan_id_fkey FOREIGN KEY (scan_id) REFERENCES public.scans(id)
);

-- Audit logs table
CREATE TABLE IF NOT EXISTS public.audit_logs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
    action TEXT NOT NULL,
    resource_type TEXT NOT NULL,
    resource_id UUID,
    details JSONB DEFAULT '{}',
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_scans_user_id ON scans(user_id);
CREATE INDEX IF NOT EXISTS idx_scans_status ON scans(status);
CREATE INDEX IF NOT EXISTS idx_scans_created_at ON scans(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_issues_scan_id ON issues(scan_id);
CREATE INDEX IF NOT EXISTS idx_issues_severity ON issues(severity);
CREATE INDEX IF NOT EXISTS idx_issues_status ON issues(status);
CREATE INDEX IF NOT EXISTS idx_scan_files_scan_id ON scan_files(scan_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at ON audit_logs(created_at DESC);

-- Roles table
CREATE TABLE IF NOT EXISTS public.roles (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert default roles
INSERT INTO public.roles (id, name, description) VALUES
    ('ac4c17be-fdb2-4e45-bcc4-96fe27b3be64', 'user', 'Standard user role'),
    ('196154e0-ecd8-4dd3-ac3d-e5ab61d81245', 'admin', 'Administrator role'),
    ('9aed130e-b405-4b7c-943d-b2ac4e2e6f01', 'auditor', 'Auditor role')
ON CONFLICT (name) DO NOTHING;

-- Enable Row Level Security (RLS)
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE organizations ENABLE ROW LEVEL SECURITY;
ALTER TABLE scans ENABLE ROW LEVEL SECURITY;
ALTER TABLE issues ENABLE ROW LEVEL SECURITY;
ALTER TABLE scan_files ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;

-- RLS Policies

-- Profiles policies
CREATE POLICY "Users can view own profile" ON profiles
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can update own profile" ON profiles
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own profile" ON profiles
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Organizations policies
CREATE POLICY "Users can view own organization" ON organizations
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM profiles 
            WHERE profiles.id = auth.uid() 
            AND profiles.organization = organizations.name
        )
    );

-- Scans policies
CREATE POLICY "Users can view own scans" ON scans
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create scans" ON scans
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own scans" ON scans
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own scans" ON scans
    FOR DELETE USING (auth.uid() = user_id);

-- Issues policies
CREATE POLICY "Users can view issues from own scans" ON issues
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM scans 
            WHERE scans.id = issues.scan_id 
            AND scans.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can update issues from own scans" ON issues
    FOR UPDATE USING (
        EXISTS (
            SELECT 1 FROM scans 
            WHERE scans.id = issues.scan_id 
            AND scans.user_id = auth.uid()
        )
    );

-- Scan files policies
CREATE POLICY "Users can view files from own scans" ON scan_files
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM scans 
            WHERE scans.id = scan_files.scan_id 
            AND scans.user_id = auth.uid()
        )
    );

-- Audit logs policies
CREATE POLICY "Users can view own audit logs" ON audit_logs
    FOR SELECT USING (auth.uid() = user_id);

-- Compliance frameworks policies (public read)
CREATE POLICY "Anyone can view compliance frameworks" ON compliance_frameworks
    FOR SELECT USING (is_active = true);

-- Functions and triggers

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for updated_at
CREATE TRIGGER update_profiles_updated_at BEFORE UPDATE ON profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_organizations_updated_at BEFORE UPDATE ON organizations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_scans_updated_at BEFORE UPDATE ON scans
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_issues_updated_at BEFORE UPDATE ON issues
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function to create user profile on signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.profiles (user_id, username, full_name, role_id)
    VALUES (
        NEW.id,
        COALESCE(NEW.raw_user_meta_data->>'username', NEW.email),
        COALESCE(NEW.raw_user_meta_data->>'full_name', NEW.email),
        'ac4c17be-fdb2-4e45-bcc4-96fe27b3be64' -- Default to user role
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger to create profile on user signup
CREATE OR REPLACE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- Insert default compliance frameworks
INSERT INTO compliance_frameworks (name, description, version, url) VALUES
    ('ISO 27001', 'Information Security Management System', '2013', 'https://www.iso.org/standard/54534.html'),
    ('OWASP Top 10', 'Web Application Security Risks', '2021', 'https://owasp.org/www-project-top-ten/'),
    ('GDPR', 'General Data Protection Regulation', '2018', 'https://gdpr-info.eu/'),
    ('PCI DSS', 'Payment Card Industry Data Security Standard', '4.0', 'https://www.pcisecuritystandards.org/'),
    ('HIPAA', 'Health Insurance Portability and Accountability Act', '1996', 'https://www.hhs.gov/hipaa/'),
    ('NIST Cybersecurity Framework', 'Framework for Improving Critical Infrastructure Cybersecurity', '1.1', 'https://www.nist.gov/cyberframework')
ON CONFLICT (name) DO NOTHING;

-- Create storage bucket (run this in Supabase dashboard or via API)
-- INSERT INTO storage.buckets (id, name, public) VALUES ('vibeauditor-files', 'vibeauditor-files', false);

-- Storage policies (uncomment after creating bucket)
-- CREATE POLICY "Users can upload files to own scans" ON storage.objects
--     FOR INSERT WITH CHECK (
--         bucket_id = 'vibeauditor-files' AND
--         (storage.foldername(name))[1] = 'scans' AND
--         EXISTS (
--             SELECT 1 FROM scans 
--             WHERE scans.id::text = (storage.foldername(name))[2]
--             AND scans.user_id = auth.uid()
--         )
--     );

-- CREATE POLICY "Users can view files from own scans" ON storage.objects
--     FOR SELECT USING (
--         bucket_id = 'vibeauditor-files' AND
--         (storage.foldername(name))[1] = 'scans' AND
--         EXISTS (
--             SELECT 1 FROM scans 
--             WHERE scans.id::text = (storage.foldername(name))[2]
--             AND scans.user_id = auth.uid()
--         )
--     );