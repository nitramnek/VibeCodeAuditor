-- VibeCodeAuditor Schema Enhancements
-- Run these additions to support full compliance features

-- Add missing columns to existing tables

-- Enhance scans table with compliance data
ALTER TABLE scans ADD COLUMN IF NOT EXISTS name TEXT;
ALTER TABLE scans ADD COLUMN IF NOT EXISTS description TEXT;
ALTER TABLE scans ADD COLUMN IF NOT EXISTS status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'running', 'completed', 'failed', 'cancelled'));
ALTER TABLE scans ADD COLUMN IF NOT EXISTS config JSONB DEFAULT '{}';
ALTER TABLE scans ADD COLUMN IF NOT EXISTS summary JSONB DEFAULT '{}';
ALTER TABLE scans ADD COLUMN IF NOT EXISTS compliance_summary JSONB DEFAULT '{}';
ALTER TABLE scans ADD COLUMN IF NOT EXISTS detected_frameworks JSONB DEFAULT '{}';
ALTER TABLE scans ADD COLUMN IF NOT EXISTS file_count INTEGER DEFAULT 0;
ALTER TABLE scans ADD COLUMN IF NOT EXISTS total_issues INTEGER DEFAULT 0;
ALTER TABLE scans ADD COLUMN IF NOT EXISTS critical_issues INTEGER DEFAULT 0;
ALTER TABLE scans ADD COLUMN IF NOT EXISTS high_issues INTEGER DEFAULT 0;
ALTER TABLE scans ADD COLUMN IF NOT EXISTS medium_issues INTEGER DEFAULT 0;
ALTER TABLE scans ADD COLUMN IF NOT EXISTS low_issues INTEGER DEFAULT 0;
ALTER TABLE scans ADD COLUMN IF NOT EXISTS progress INTEGER DEFAULT 0 CHECK (progress >= 0 AND progress <= 100);
ALTER TABLE scans ADD COLUMN IF NOT EXISTS started_at TIMESTAMP WITH TIME ZONE;
ALTER TABLE scans ADD COLUMN IF NOT EXISTS completed_at TIMESTAMP WITH TIME ZONE;
ALTER TABLE scans ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();

-- Enhance issues table with compliance data
ALTER TABLE issues ADD COLUMN IF NOT EXISTS rule_id TEXT;
ALTER TABLE issues ADD COLUMN IF NOT EXISTS category TEXT;
ALTER TABLE issues ADD COLUMN IF NOT EXISTS message TEXT;
ALTER TABLE issues ADD COLUMN IF NOT EXISTS file_path TEXT;
ALTER TABLE issues ADD COLUMN IF NOT EXISTS line_number INTEGER;
ALTER TABLE issues ADD COLUMN IF NOT EXISTS column_number INTEGER;
ALTER TABLE issues ADD COLUMN IF NOT EXISTS code_snippet TEXT;
ALTER TABLE issues ADD COLUMN IF NOT EXISTS remediation TEXT;
ALTER TABLE issues ADD COLUMN IF NOT EXISTS confidence DECIMAL(3,2) DEFAULT 1.0 CHECK (confidence >= 0 AND confidence <= 1);
ALTER TABLE issues ADD COLUMN IF NOT EXISTS metadata JSONB DEFAULT '{}';
ALTER TABLE issues ADD COLUMN IF NOT EXISTS standards JSONB DEFAULT '[]';
ALTER TABLE issues ADD COLUMN IF NOT EXISTS compliance_frameworks TEXT[] DEFAULT '{}';
ALTER TABLE issues ADD COLUMN IF NOT EXISTS resolved_at TIMESTAMP WITH TIME ZONE;
ALTER TABLE issues ADD COLUMN IF NOT EXISTS resolution_notes TEXT;
ALTER TABLE issues ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();

-- Enhance profiles table
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS full_name TEXT;
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS organization TEXT;
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS role TEXT DEFAULT 'user' CHECK (role IN ('user', 'admin', 'auditor'));
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS avatar_url TEXT;
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS settings JSONB DEFAULT '{}';
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();

-- Enhance organizations table
ALTER TABLE organizations ADD COLUMN IF NOT EXISTS domain TEXT;
ALTER TABLE organizations ADD COLUMN IF NOT EXISTS settings JSONB DEFAULT '{}';
ALTER TABLE organizations ADD COLUMN IF NOT EXISTS compliance_frameworks TEXT[] DEFAULT '{}';
ALTER TABLE organizations ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();

-- Enhance scan_files table
ALTER TABLE scan_files ADD COLUMN IF NOT EXISTS file_name TEXT;
ALTER TABLE scan_files ADD COLUMN IF NOT EXISTS file_size INTEGER;
ALTER TABLE scan_files ADD COLUMN IF NOT EXISTS storage_path TEXT;
ALTER TABLE scan_files ADD COLUMN IF NOT EXISTS mime_type TEXT;
ALTER TABLE scan_files ADD COLUMN IF NOT EXISTS checksum TEXT;

-- Enhance audit_logs table
ALTER TABLE audit_logs ADD COLUMN IF NOT EXISTS resource_type TEXT;
ALTER TABLE audit_logs ADD COLUMN IF NOT EXISTS details JSONB DEFAULT '{}';
ALTER TABLE audit_logs ADD COLUMN IF NOT EXISTS ip_address INET;
ALTER TABLE audit_logs ADD COLUMN IF NOT EXISTS user_agent TEXT;

-- Enhance compliance_frameworks table
ALTER TABLE compliance_frameworks ADD COLUMN IF NOT EXISTS description TEXT;
ALTER TABLE compliance_frameworks ADD COLUMN IF NOT EXISTS version TEXT;
ALTER TABLE compliance_frameworks ADD COLUMN IF NOT EXISTS url TEXT;
ALTER TABLE compliance_frameworks ADD COLUMN IF NOT EXISTS standards JSONB DEFAULT '[]';
ALTER TABLE compliance_frameworks ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT true;
ALTER TABLE compliance_frameworks ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();

-- Add new indexes for enhanced columns
CREATE INDEX IF NOT EXISTS idx_scans_status ON scans(status);
CREATE INDEX IF NOT EXISTS idx_scans_created_at ON scans(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_issues_rule_id ON issues(rule_id);
CREATE INDEX IF NOT EXISTS idx_issues_category ON issues(category);
CREATE INDEX IF NOT EXISTS idx_compliance_frameworks_is_active ON compliance_frameworks(is_active);

-- Update existing status check constraint for issues
ALTER TABLE issues DROP CONSTRAINT IF EXISTS issues_status_check;
ALTER TABLE issues ADD CONSTRAINT issues_status_check CHECK (status IN ('open', 'acknowledged', 'resolved', 'false_positive', 'wont_fix'));

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for updated_at
DROP TRIGGER IF EXISTS update_profiles_updated_at ON profiles;
CREATE TRIGGER update_profiles_updated_at BEFORE UPDATE ON profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_organizations_updated_at ON organizations;
CREATE TRIGGER update_organizations_updated_at BEFORE UPDATE ON organizations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_scans_updated_at ON scans;
CREATE TRIGGER update_scans_updated_at BEFORE UPDATE ON scans
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_issues_updated_at ON issues;
CREATE TRIGGER update_issues_updated_at BEFORE UPDATE ON issues
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_compliance_frameworks_updated_at ON compliance_frameworks;
CREATE TRIGGER update_compliance_frameworks_updated_at BEFORE UPDATE ON compliance_frameworks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function to create user profile on signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.profiles (user_id, email, full_name)
    VALUES (
        NEW.id,
        NEW.email,
        COALESCE(NEW.raw_user_meta_data->>'full_name', NEW.email)
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger to create profile on user signup
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- Insert default compliance frameworks
INSERT INTO compliance_frameworks (name, description, version, url, is_active) VALUES
    ('ISO 27001', 'Information Security Management System', '2013', 'https://www.iso.org/standard/54534.html', true),
    ('OWASP Top 10', 'Web Application Security Risks', '2021', 'https://owasp.org/www-project-top-ten/', true),
    ('GDPR', 'General Data Protection Regulation', '2018', 'https://gdpr-info.eu/', true),
    ('PCI DSS', 'Payment Card Industry Data Security Standard', '4.0', 'https://www.pcisecuritystandards.org/', true),
    ('HIPAA', 'Health Insurance Portability and Accountability Act', '1996', 'https://www.hhs.gov/hipaa/', true),
    ('NIST Cybersecurity Framework', 'Framework for Improving Critical Infrastructure Cybersecurity', '1.1', 'https://www.nist.gov/cyberframework', true)
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    version = EXCLUDED.version,
    url = EXCLUDED.url,
    is_active = EXCLUDED.is_active,
    updated_at = NOW();

-- RLS Policies (enhanced)

-- Profiles policies
DROP POLICY IF EXISTS "Users can view own profile" ON profiles;
CREATE POLICY "Users can view own profile" ON profiles
    FOR SELECT USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can update own profile" ON profiles;
CREATE POLICY "Users can update own profile" ON profiles
    FOR UPDATE USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can insert own profile" ON profiles;
CREATE POLICY "Users can insert own profile" ON profiles
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Organizations policies
DROP POLICY IF EXISTS "Users can view own organization" ON organizations;
CREATE POLICY "Users can view own organization" ON organizations
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM profiles 
            WHERE profiles.user_id = auth.uid() 
            AND profiles.organization = organizations.name
        )
    );

-- Scans policies
DROP POLICY IF EXISTS "Users can view own scans" ON scans;
CREATE POLICY "Users can view own scans" ON scans
    FOR SELECT USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can create scans" ON scans;
CREATE POLICY "Users can create scans" ON scans
    FOR INSERT WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can update own scans" ON scans;
CREATE POLICY "Users can update own scans" ON scans
    FOR UPDATE USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can delete own scans" ON scans;
CREATE POLICY "Users can delete own scans" ON scans
    FOR DELETE USING (auth.uid() = user_id);

-- Issues policies
DROP POLICY IF EXISTS "Users can view issues from own scans" ON issues;
CREATE POLICY "Users can view issues from own scans" ON issues
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM scans 
            WHERE scans.id = issues.scan_id 
            AND scans.user_id = auth.uid()
        )
    );

DROP POLICY IF EXISTS "Users can update issues from own scans" ON issues;
CREATE POLICY "Users can update issues from own scans" ON issues
    FOR UPDATE USING (
        EXISTS (
            SELECT 1 FROM scans 
            WHERE scans.id = issues.scan_id 
            AND scans.user_id = auth.uid()
        )
    );

-- Scan files policies
DROP POLICY IF EXISTS "Users can view files from own scans" ON scan_files;
CREATE POLICY "Users can view files from own scans" ON scan_files
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM scans 
            WHERE scans.id = scan_files.scan_id 
            AND scans.user_id = auth.uid()
        )
    );

-- Audit logs policies
DROP POLICY IF EXISTS "Users can view own audit logs" ON audit_logs;
CREATE POLICY "Users can view own audit logs" ON audit_logs
    FOR SELECT USING (auth.uid() = user_id);

-- Compliance frameworks policies (public read)
DROP POLICY IF EXISTS "Anyone can view compliance frameworks" ON compliance_frameworks;
CREATE POLICY "Anyone can view compliance frameworks" ON compliance_frameworks
    FOR SELECT USING (is_active = true);