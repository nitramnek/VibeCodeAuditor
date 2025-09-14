-- Supabase Compliance Center Migration
-- This migration extends the existing schema for the compliance management system
-- Run this in your Supabase SQL editor

-- Step 1: Extend existing compliance_frameworks table
ALTER TABLE public.compliance_frameworks
ADD COLUMN IF NOT EXISTS user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE,
ADD COLUMN IF NOT EXISTS code VARCHAR(50),
ADD COLUMN IF NOT EXISTS status VARCHAR(50) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'deprecated')),
ADD COLUMN IF NOT EXISTS compliance_score INTEGER DEFAULT 0 CHECK (compliance_score >= 0 AND compliance_score <= 100),
ADD COLUMN IF NOT EXISTS total_controls INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS implemented_controls INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS critical_issues INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS high_issues INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS medium_issues INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS low_issues INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS last_audit_date DATE,
ADD COLUMN IF NOT EXISTS next_audit_date DATE,
ADD COLUMN IF NOT EXISTS auditor_name VARCHAR(255),
ADD COLUMN IF NOT EXISTS audit_frequency VARCHAR(50) DEFAULT 'annual' CHECK (audit_frequency IN ('annual', 'semi-annual', 'quarterly', 'monthly')),
ADD COLUMN IF NOT EXISTS framework_version VARCHAR(50),
ADD COLUMN IF NOT EXISTS regulatory_body VARCHAR(255),
ADD COLUMN IF NOT EXISTS website_url VARCHAR(500),
ADD COLUMN IF NOT EXISTS documentation_url VARCHAR(500);

-- Add unique constraint on code (if not exists)
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint 
        WHERE conname = 'compliance_frameworks_code_key'
    ) THEN
        ALTER TABLE public.compliance_frameworks 
        ADD CONSTRAINT compliance_frameworks_code_key UNIQUE (code);
    END IF;
END $$;

-- Step 2: Create new compliance tables

-- Compliance Audits Table
CREATE TABLE IF NOT EXISTS public.compliance_audits (
    id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE,
    framework_id uuid REFERENCES public.compliance_frameworks(id) ON DELETE CASCADE,
    framework_name VARCHAR(255) NOT NULL,
    audit_type VARCHAR(100) NOT NULL CHECK (audit_type IN ('internal', 'external', 'regulatory', 'certification')),
    audit_date DATE NOT NULL,
    completion_date DATE,
    status VARCHAR(50) DEFAULT 'scheduled' CHECK (status IN ('scheduled', 'in_progress', 'completed', 'cancelled')),
    auditor_name VARCHAR(255),
    auditor_company VARCHAR(255),
    audit_scope TEXT,
    total_findings INTEGER DEFAULT 0,
    critical_findings INTEGER DEFAULT 0,
    high_findings INTEGER DEFAULT 0,
    medium_findings INTEGER DEFAULT 0,
    low_findings INTEGER DEFAULT 0,
    compliance_score INTEGER CHECK (compliance_score >= 0 AND compliance_score <= 100),
    recommendations TEXT,
    follow_up_required BOOLEAN DEFAULT FALSE,
    follow_up_date DATE,
    report_url VARCHAR(500),
    notes TEXT,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);

-- Compliance Risk Assessments Table
CREATE TABLE IF NOT EXISTS public.compliance_risk_assessments (
    id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE,
    framework_id uuid REFERENCES public.compliance_frameworks(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'draft' CHECK (status IN ('draft', 'in_progress', 'completed', 'cancelled')),
    risk_score INTEGER DEFAULT 0 CHECK (risk_score >= 0 AND risk_score <= 100),
    risk_level VARCHAR(50) DEFAULT 'low' CHECK (risk_level IN ('very_low', 'low', 'medium', 'high', 'very_high', 'critical')),
    assessment_type VARCHAR(100) NOT NULL,
    assessor_name VARCHAR(255),
    review_frequency VARCHAR(50) DEFAULT 'annual' CHECK (review_frequency IN ('annual', 'semi-annual', 'quarterly', 'monthly')),
    last_updated DATE NOT NULL,
    next_review_date DATE,
    methodology TEXT,
    scope TEXT,
    findings TEXT,
    recommendations TEXT,
    mitigation_plan TEXT,
    residual_risk_score INTEGER CHECK (residual_risk_score >= 0 AND residual_risk_score <= 100),
    approval_status VARCHAR(50) DEFAULT 'pending' CHECK (approval_status IN ('pending', 'approved', 'rejected')),
    approved_by VARCHAR(255),
    approved_date DATE,
    document_url VARCHAR(500),
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);

-- Compliance Policies Table
CREATE TABLE IF NOT EXISTS public.compliance_policies (
    id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE,
    framework_id uuid REFERENCES public.compliance_frameworks(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    policy_number VARCHAR(100),
    version VARCHAR(50) DEFAULT '1.0',
    status VARCHAR(50) DEFAULT 'draft' CHECK (status IN ('draft', 'review', 'approved', 'archived')),
    category VARCHAR(100),
    owner_name VARCHAR(255),
    owner_email VARCHAR(255),
    reviewer_name VARCHAR(255),
    reviewer_email VARCHAR(255),
    approver_name VARCHAR(255),
    approver_email VARCHAR(255),
    effective_date DATE,
    last_reviewed DATE NOT NULL,
    next_review_date DATE,
    review_frequency VARCHAR(50) DEFAULT 'annual' CHECK (review_frequency IN ('annual', 'semi-annual', 'quarterly', 'monthly')),
    content TEXT,
    objectives TEXT,
    scope TEXT,
    responsibilities TEXT,
    procedures TEXT,
    references TEXT,
    attachments JSONB DEFAULT '[]',
    document_url VARCHAR(500),
    is_template BOOLEAN DEFAULT FALSE,
    parent_policy_id uuid REFERENCES public.compliance_policies(id),
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);

-- Compliance Controls Table
CREATE TABLE IF NOT EXISTS public.compliance_controls (
    id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE,
    framework_id uuid REFERENCES public.compliance_frameworks(id) ON DELETE CASCADE NOT NULL,
    control_id VARCHAR(100) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    subcategory VARCHAR(100),
    control_type VARCHAR(50) DEFAULT 'preventive' CHECK (control_type IN ('preventive', 'detective', 'corrective')),
    status VARCHAR(50) DEFAULT 'not_implemented' CHECK (status IN ('not_implemented', 'planned', 'implemented', 'tested', 'automated')),
    implementation_status VARCHAR(50) DEFAULT 'not_started' CHECK (implementation_status IN ('not_started', 'in_progress', 'completed', 'cancelled')),
    priority VARCHAR(50) DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high', 'critical')),
    owner_name VARCHAR(255),
    owner_email VARCHAR(255),
    implementation_date DATE,
    last_tested DATE,
    next_test_date DATE,
    test_frequency VARCHAR(50) DEFAULT 'annual' CHECK (test_frequency IN ('annual', 'semi-annual', 'quarterly', 'monthly')),
    test_results TEXT,
    test_status VARCHAR(50) DEFAULT 'not_tested' CHECK (test_status IN ('not_tested', 'passed', 'failed', 'compensating_control')),
    evidence TEXT,
    evidence_url VARCHAR(500),
    compensating_controls TEXT,
    risk_impact VARCHAR(50) DEFAULT 'medium' CHECK (risk_impact IN ('low', 'medium', 'high', 'critical')),
    cost_impact VARCHAR(50) DEFAULT 'medium' CHECK (cost_impact IN ('low', 'medium', 'high', 'critical')),
    notes TEXT,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    UNIQUE(framework_id, control_id)
);

-- Compliance Issues Table (extends existing issues functionality)
CREATE TABLE IF NOT EXISTS public.compliance_issues (
    id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    framework_id uuid REFERENCES public.compliance_frameworks(id) ON DELETE CASCADE,
    control_id uuid REFERENCES public.compliance_controls(id) ON DELETE CASCADE,
    audit_id uuid REFERENCES public.compliance_audits(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    severity VARCHAR(50) DEFAULT 'medium' CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    status VARCHAR(50) DEFAULT 'open' CHECK (status IN ('open', 'in_progress', 'resolved', 'accepted_risk', 'false_positive')),
    issue_type VARCHAR(100) NOT NULL,
    discovered_date DATE NOT NULL,
    reported_by VARCHAR(255),
    assigned_to VARCHAR(255),
    assigned_email VARCHAR(255),
    due_date DATE,
    resolution_date DATE,
    resolution TEXT,
    root_cause TEXT,
    preventive_actions TEXT,
    evidence TEXT,
    evidence_url VARCHAR(500),
    cost_impact DECIMAL(10,2),
    risk_impact VARCHAR(50) DEFAULT 'medium' CHECK (risk_impact IN ('low', 'medium', 'high', 'critical')),
    priority_score INTEGER DEFAULT 0 CHECK (priority_score >= 0 AND priority_score <= 100),
    tags TEXT[],
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);

-- Compliance Reports Table
CREATE TABLE IF NOT EXISTS public.compliance_reports (
    id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    report_type VARCHAR(100) NOT NULL CHECK (report_type IN ('compliance_overview', 'audit_report', 'risk_assessment', 'control_effectiveness', 'gap_analysis', 'custom')),
    framework_id uuid REFERENCES public.compliance_frameworks(id),
    date_range_start DATE,
    date_range_end DATE,
    status VARCHAR(50) DEFAULT 'draft' CHECK (status IN ('draft', 'generating', 'completed', 'failed')),
    generated_at timestamp with time zone,
    generated_by VARCHAR(255),
    file_url VARCHAR(500),
    file_size INTEGER,
    parameters JSONB DEFAULT '{}',
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);

-- Step 3: Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_compliance_frameworks_user_id ON public.compliance_frameworks(user_id);
CREATE INDEX IF NOT EXISTS idx_compliance_frameworks_code ON public.compliance_frameworks(code);
CREATE INDEX IF NOT EXISTS idx_compliance_frameworks_status ON public.compliance_frameworks(status);

CREATE INDEX IF NOT EXISTS idx_compliance_audits_user_id ON public.compliance_audits(user_id);
CREATE INDEX IF NOT EXISTS idx_compliance_audits_framework_id ON public.compliance_audits(framework_id);
CREATE INDEX IF NOT EXISTS idx_compliance_audits_date ON public.compliance_audits(audit_date);
CREATE INDEX IF NOT EXISTS idx_compliance_audits_status ON public.compliance_audits(status);

CREATE INDEX IF NOT EXISTS idx_compliance_risk_assessments_user_id ON public.compliance_risk_assessments(user_id);
CREATE INDEX IF NOT EXISTS idx_compliance_risk_assessments_framework_id ON public.compliance_risk_assessments(framework_id);
CREATE INDEX IF NOT EXISTS idx_compliance_risk_assessments_status ON public.compliance_risk_assessments(status);

CREATE INDEX IF NOT EXISTS idx_compliance_policies_user_id ON public.compliance_policies(user_id);
CREATE INDEX IF NOT EXISTS idx_compliance_policies_framework_id ON public.compliance_policies(framework_id);
CREATE INDEX IF NOT EXISTS idx_compliance_policies_status ON public.compliance_policies(status);

CREATE INDEX IF NOT EXISTS idx_compliance_controls_user_id ON public.compliance_controls(user_id);
CREATE INDEX IF NOT EXISTS idx_compliance_controls_framework_id ON public.compliance_controls(framework_id);
CREATE INDEX IF NOT EXISTS idx_compliance_controls_status ON public.compliance_controls(status);

CREATE INDEX IF NOT EXISTS idx_compliance_issues_user_id ON public.compliance_issues(user_id);
CREATE INDEX IF NOT EXISTS idx_compliance_issues_framework_id ON public.compliance_issues(framework_id);
CREATE INDEX IF NOT EXISTS idx_compliance_issues_status ON public.compliance_issues(status);
CREATE INDEX IF NOT EXISTS idx_compliance_issues_severity ON public.compliance_issues(severity);

CREATE INDEX IF NOT EXISTS idx_compliance_reports_user_id ON public.compliance_reports(user_id);
CREATE INDEX IF NOT EXISTS idx_compliance_reports_type ON public.compliance_reports(report_type);

-- Step 4: Enable Row Level Security
ALTER TABLE public.compliance_frameworks ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.compliance_audits ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.compliance_risk_assessments ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.compliance_policies ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.compliance_controls ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.compliance_issues ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.compliance_reports ENABLE ROW LEVEL SECURITY;

-- Step 5: Create RLS policies
-- Compliance Frameworks policies
CREATE POLICY IF NOT EXISTS "Users can view their own compliance frameworks" ON public.compliance_frameworks
    FOR SELECT USING (auth.uid() = user_id OR user_id IS NULL);
CREATE POLICY IF NOT EXISTS "Users can insert their own compliance frameworks" ON public.compliance_frameworks
    FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY IF NOT EXISTS "Users can update their own compliance frameworks" ON public.compliance_frameworks
    FOR UPDATE USING (auth.uid() = user_id OR user_id IS NULL);
CREATE POLICY IF NOT EXISTS "Users can delete their own compliance frameworks" ON public.compliance_frameworks
    FOR DELETE USING (auth.uid() = user_id);

-- Compliance Audits policies
CREATE POLICY IF NOT EXISTS "Users can view their own compliance audits" ON public.compliance_audits
    FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY IF NOT EXISTS "Users can insert their own compliance audits" ON public.compliance_audits
    FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY IF NOT EXISTS "Users can update their own compliance audits" ON public.compliance_audits
    FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY IF NOT EXISTS "Users can delete their own compliance audits" ON public.compliance_audits
    FOR DELETE USING (auth.uid() = user_id);

-- Risk Assessments policies
CREATE POLICY IF NOT EXISTS "Users can view their own risk assessments" ON public.compliance_risk_assessments
    FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY IF NOT EXISTS "Users can insert their own risk assessments" ON public.compliance_risk_assessments
    FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY IF NOT EXISTS "Users can update their own risk assessments" ON public.compliance_risk_assessments
    FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY IF NOT EXISTS "Users can delete their own risk assessments" ON public.compliance_risk_assessments
    FOR DELETE USING (auth.uid() = user_id);

-- Policies policies
CREATE POLICY IF NOT EXISTS "Users can view their own policies" ON public.compliance_policies
    FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY IF NOT EXISTS "Users can insert their own policies" ON public.compliance_policies
    FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY IF NOT EXISTS "Users can update their own policies" ON public.compliance_policies
    FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY IF NOT EXISTS "Users can delete their own policies" ON public.compliance_policies
    FOR DELETE USING (auth.uid() = user_id);

-- Controls policies
CREATE POLICY IF NOT EXISTS "Users can view their own controls" ON public.compliance_controls
    FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY IF NOT EXISTS "Users can insert their own controls" ON public.compliance_controls
    FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY IF NOT EXISTS "Users can update their own controls" ON public.compliance_controls
    FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY IF NOT EXISTS "Users can delete their own controls" ON public.compliance_controls
    FOR DELETE USING (auth.uid() = user_id);

-- Issues policies
CREATE POLICY IF NOT EXISTS "Users can view their own compliance issues" ON public.compliance_issues
    FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY IF NOT EXISTS "Users can insert their own compliance issues" ON public.compliance_issues
    FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY IF NOT EXISTS "Users can update their own compliance issues" ON public.compliance_issues
    FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY IF NOT EXISTS "Users can delete their own compliance issues" ON public.compliance_issues
    FOR DELETE USING (auth.uid() = user_id);

-- Reports policies
CREATE POLICY IF NOT EXISTS "Users can view their own reports" ON public.compliance_reports
    FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY IF NOT EXISTS "Users can insert their own reports" ON public.compliance_reports
    FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY IF NOT EXISTS "Users can update their own reports" ON public.compliance_reports
    FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY IF NOT EXISTS "Users can delete their own reports" ON public.compliance_reports
    FOR DELETE USING (auth.uid() = user_id);

-- Step 6: Create functions for updating timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Step 7: Create triggers for updating timestamps
CREATE TRIGGER IF NOT EXISTS update_compliance_frameworks_updated_at
    BEFORE UPDATE ON public.compliance_frameworks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER IF NOT EXISTS update_compliance_audits_updated_at
    BEFORE UPDATE ON public.compliance_audits
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER IF NOT EXISTS update_compliance_risk_assessments_updated_at
    BEFORE UPDATE ON public.compliance_risk_assessments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER IF NOT EXISTS update_compliance_policies_updated_at
    BEFORE UPDATE ON public.compliance_policies
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER IF NOT EXISTS update_compliance_controls_updated_at
    BEFORE UPDATE ON public.compliance_controls
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER IF NOT EXISTS update_compliance_issues_updated_at
    BEFORE UPDATE ON public.compliance_issues
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER IF NOT EXISTS update_compliance_reports_updated_at
    BEFORE UPDATE ON public.compliance_reports
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Step 8: Insert sample compliance frameworks (only if none exist)
INSERT INTO public.compliance_frameworks (name, code, description, status, compliance_score, total_controls, implemented_controls, critical_issues, high_issues, medium_issues, low_issues, last_audit_date, next_audit_date, auditor_name, audit_frequency, framework_version, regulatory_body, is_active)
SELECT 
    'General Data Protection Regulation',
    'gdpr',
    'EU data protection regulation for personal data handling',
    'active',
    92,
    45,
    42,
    0,
    2,
    5,
    8,
    '2024-01-15'::date,
    '2024-07-15'::date,
    'Internal Security Team',
    'annual',
    'GDPR 2018',
    'European Commission',
    true
WHERE NOT EXISTS (SELECT 1 FROM public.compliance_frameworks WHERE code = 'gdpr')

UNION ALL

SELECT 
    'Health Insurance Portability and Accountability Act',
    'hipaa',
    'US healthcare data protection requirements',
    'active',
    78,
    38,
    29,
    1,
    3,
    8,
    12,
    '2024-01-10'::date,
    '2024-07-10'::date,
    'Compliance Team',
    'annual',
    'HIPAA 1996',
    'US Department of Health and Human Services',
    true
WHERE NOT EXISTS (SELECT 1 FROM public.compliance_frameworks WHERE code = 'hipaa')

UNION ALL

SELECT 
    'Service Organization Control 2',
    'soc2',
    'Trust services criteria for service organizations',
    'active',
    95,
    52,
    50,
    0,
    0,
    2,
    5,
    '2024-01-20'::date,
    '2024-07-20'::date,
    'Deloitte',
    'annual',
    'SOC 2 Type II',
    'American Institute of CPAs',
    true
WHERE NOT EXISTS (SELECT 1 FROM public.compliance_frameworks WHERE code = 'soc2')

UNION ALL

SELECT 
    'ISO 27001',
    'iso27001',
    'International information security management standard',
    'active',
    82,
    48,
    39,
    2,
    4,
    6,
    9,
    '2024-01-05'::date,
    '2024-07-05'::date,
    'ISO Auditors',
    'annual',
    'ISO 27001:2022',
    'International Organization for Standardization',
    true
WHERE NOT EXISTS (SELECT 1 FROM public.compliance_frameworks WHERE code = 'iso27001');

-- Step 9: Insert sample audit data
INSERT INTO public.compliance_audits (framework_name, audit_type, audit_date, status, auditor_name, auditor_company, total_findings, critical_findings, high_findings, medium_findings, low_findings, compliance_score, recommendations)
SELECT 
    'GDPR',
    'internal',
    '2024-01-15'::date,
    'completed',
    'Internal Security Team',
    'Internal',
    7,
    0,
    2,
    3,
    2,
    92,
    'Implement additional encryption measures'
WHERE NOT EXISTS (SELECT 1 FROM public.compliance_audits WHERE framework_name = 'GDPR' AND audit_date = '2024-01-15'::date)

UNION ALL

SELECT 
    'SOC 2',
    'external',
    '2024-01-20'::date,
    'completed',
    'John Smith',
    'Deloitte',
    2,
    0,
    0,
    1,
    1,
    95,
    'Minor documentation improvements needed'
WHERE NOT EXISTS (SELECT 1 FROM public.compliance_audits WHERE framework_name = 'SOC 2' AND audit_date = '2024-01-20'::date)

UNION ALL

SELECT 
    'HIPAA',
    'internal',
    '2024-01-10'::date,
    'completed',
    'Compliance Team',
    'Internal',
    12,
    1,
    2,
    4,
    5,
    78,
    'Address critical PHI handling issue'
WHERE NOT EXISTS (SELECT 1 FROM public.compliance_audits WHERE framework_name = 'HIPAA' AND audit_date = '2024-01-10'::date);

-- Step 10: Insert sample risk assessment data
INSERT INTO public.compliance_risk_assessments (title, description, status, risk_score, risk_level, assessment_type, assessor_name, last_updated, next_review_date, methodology)
SELECT 
    'Data Privacy Risk Assessment',
    'Comprehensive assessment of data privacy risks',
    'completed',
    85,
    'medium',
    'privacy_impact',
    'Data Protection Officer',
    '2024-01-12'::date,
    '2024-07-12'::date,
    'NIST Risk Management Framework'
WHERE NOT EXISTS (SELECT 1 FROM public.compliance_risk_assessments WHERE title = 'Data Privacy Risk Assessment')

UNION ALL

SELECT 
    'Security Controls Assessment',
    'Evaluation of information security controls',
    'in_progress',
    72,
    'high',
    'security_assessment',
    'CISO',
    '2024-01-08'::date,
    '2024-04-08'::date,
    'ISO 27001 Risk Assessment'
WHERE NOT EXISTS (SELECT 1 FROM public.compliance_risk_assessments WHERE title = 'Security Controls Assessment');

-- Step 11: Insert sample policy data
INSERT INTO public.compliance_policies (title, description, status, category, owner_name, last_reviewed, next_review_date, version)
SELECT 
    'Data Protection Policy',
    'Policy for handling personal data in compliance with GDPR',
    'approved',
    'privacy',
    'Data Protection Officer',
    '2024-01-10'::date,
    '2024-07-10'::date,
    '2.1'
WHERE NOT EXISTS (SELECT 1 FROM public.compliance_policies WHERE title = 'Data Protection Policy')

UNION ALL

SELECT 
    'Incident Response Plan',
    'Procedures for responding to security incidents',
    'draft',
    'security',
    'CISO',
    '2024-01-05'::date,
    '2024-04-05'::date,
    '1.3'
WHERE NOT EXISTS (SELECT 1 FROM public.compliance_policies WHERE title = 'Incident Response Plan');

-- Migration completed successfully
-- You can now use the compliance management system