-- Supabase Migration Script for Compliance Management System
-- This script creates the database schema and populates it with mock data

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create custom types
DO $$ BEGIN
    CREATE TYPE control_type_enum AS ENUM ('preventive', 'detective', 'corrective');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE control_status_enum AS ENUM ('not_implemented', 'partially_implemented', 'fully_implemented', 'not_applicable');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE implementation_status_enum AS ENUM ('not_started', 'in_progress', 'completed', 'cancelled');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE priority_enum AS ENUM ('low', 'medium', 'high', 'critical');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE audit_frequency_enum AS ENUM ('monthly', 'quarterly', 'semi-annual', 'annual');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE test_status_enum AS ENUM ('not_tested', 'passed', 'failed', 'in_progress');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE impact_enum AS ENUM ('low', 'medium', 'high', 'critical');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE severity_enum AS ENUM ('low', 'medium', 'high', 'critical');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE policy_status_enum AS ENUM ('draft', 'review', 'approved', 'published', 'archived');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE review_frequency_enum AS ENUM ('monthly', 'quarterly', 'semi-annual', 'annual');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE report_type_enum AS ENUM ('compliance', 'risk_assessment', 'audit', 'gap_analysis', 'remediation');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Create tables
CREATE TABLE IF NOT EXISTS public.audit_logs (
  id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  user_id uuid,
  resource_id bigint,
  action text NOT NULL,
  created_at timestamp with time zone DEFAULT now(),
  CONSTRAINT audit_logs_pkey PRIMARY KEY (id),
  CONSTRAINT audit_logs_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id)
);

CREATE TABLE IF NOT EXISTS public.compliance_frameworks (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  name text NOT NULL UNIQUE,
  description text,
  version text,
  url text,
  standards jsonb DEFAULT '[]'::jsonb,
  is_active boolean DEFAULT true,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  user_id uuid,
  code character varying UNIQUE,
  status character varying DEFAULT 'active'::character varying CHECK (status::text = ANY (ARRAY['active'::character varying, 'inactive'::character varying, 'deprecated'::character varying]::text[])),
  compliance_score integer DEFAULT 0 CHECK (compliance_score >= 0 AND compliance_score <= 100),
  total_controls integer DEFAULT 0,
  implemented_controls integer DEFAULT 0,
  critical_issues integer DEFAULT 0,
  high_issues integer DEFAULT 0,
  medium_issues integer DEFAULT 0,
  low_issues integer DEFAULT 0,
  last_audit_date date,
  next_audit_date date,
  auditor_name character varying,
  audit_frequency character varying DEFAULT 'annual'::character varying CHECK (audit_frequency::text = ANY (ARRAY['annual'::character varying, 'semi-annual'::character varying, 'quarterly'::character varying, 'monthly'::character varying]::text[])),
  framework_version character varying,
  regulatory_body character varying,
  website_url character varying,
  documentation_url character varying,
  CONSTRAINT compliance_frameworks_pkey PRIMARY KEY (id),
  CONSTRAINT compliance_frameworks_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id)
);

CREATE TABLE IF NOT EXISTS public.compliance_audits (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  user_id uuid,
  framework_id uuid,
  framework_name character varying NOT NULL,
  audit_type character varying NOT NULL CHECK (audit_type::text = ANY (ARRAY['internal'::character varying, 'external'::character varying, 'regulatory'::character varying, 'certification'::character varying]::text[])),
  audit_date date NOT NULL,
  completion_date date,
  status character varying DEFAULT 'scheduled'::character varying CHECK (status::text = ANY (ARRAY['scheduled'::character varying, 'in_progress'::character varying, 'completed'::character varying, 'cancelled'::character varying]::text[])),
  auditor_name character varying,
  auditor_company character varying,
  audit_scope text,
  total_findings integer DEFAULT 0,
  critical_findings integer DEFAULT 0,
  high_findings integer DEFAULT 0,
  medium_findings integer DEFAULT 0,
  low_findings integer DEFAULT 0,
  compliance_score integer CHECK (compliance_score >= 0 AND compliance_score <= 100),
  recommendations text,
  follow_up_required boolean DEFAULT false,
  follow_up_date date,
  report_url character varying,
  notes text,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT compliance_audits_pkey PRIMARY KEY (id),
  CONSTRAINT compliance_audits_framework_id_fkey FOREIGN KEY (framework_id) REFERENCES public.compliance_frameworks(id),
  CONSTRAINT compliance_audits_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id)
);

CREATE TABLE IF NOT EXISTS public.compliance_controls (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  user_id uuid,
  framework_id uuid NOT NULL,
  control_id text NOT NULL,
  title text NOT NULL,
  description text,
  category text,
  subcategory text,
  control_type control_type_enum DEFAULT 'preventive'::control_type_enum,
  status control_status_enum DEFAULT 'not_implemented'::control_status_enum,
  implementation_status implementation_status_enum DEFAULT 'not_started'::implementation_status_enum,
  priority priority_enum DEFAULT 'medium'::priority_enum,
  owner_name text,
  owner_email text,
  implementation_date date,
  last_tested date,
  next_test_date date,
  test_frequency audit_frequency_enum DEFAULT 'annual'::audit_frequency_enum,
  test_results text,
  test_status test_status_enum DEFAULT 'not_tested'::test_status_enum,
  evidence text,
  evidence_url text,
  compensating_controls text,
  risk_impact impact_enum DEFAULT 'medium'::impact_enum,
  cost_impact impact_enum DEFAULT 'medium'::impact_enum,
  notes text,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT compliance_controls_pkey PRIMARY KEY (id),
  CONSTRAINT compliance_controls_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id),
  CONSTRAINT compliance_controls_framework_id_fkey FOREIGN KEY (framework_id) REFERENCES public.compliance_frameworks(id)
);

CREATE TABLE IF NOT EXISTS public.compliance_issues (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL,
  framework_id uuid,
  control_id uuid,
  audit_id uuid,
  title text NOT NULL,
  description text,
  severity severity_enum DEFAULT 'medium'::severity_enum,
  status text DEFAULT 'open'::text,
  issue_type text NOT NULL,
  discovered_date date NOT NULL,
  reported_by text,
  assigned_to text,
  assigned_email text,
  due_date date,
  resolution_date date,
  resolution text,
  root_cause text,
  preventive_actions text,
  evidence text,
  evidence_url text,
  cost_impact numeric,
  risk_impact impact_enum DEFAULT 'medium'::impact_enum,
  priority_score smallint DEFAULT 0 CHECK (priority_score >= 0 AND priority_score <= 100),
  tags text[],
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT compliance_issues_pkey PRIMARY KEY (id),
  CONSTRAINT compliance_issues_control_id_fkey FOREIGN KEY (control_id) REFERENCES public.compliance_controls(id),
  CONSTRAINT compliance_issues_audit_id_fkey FOREIGN KEY (audit_id) REFERENCES public.compliance_audits(id),
  CONSTRAINT compliance_issues_framework_id_fkey FOREIGN KEY (framework_id) REFERENCES public.compliance_frameworks(id),
  CONSTRAINT compliance_issues_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id)
);

CREATE TABLE IF NOT EXISTS public.compliance_policies (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL,
  framework_id uuid NOT NULL,
  title text NOT NULL,
  description text,
  policy_number text,
  version text DEFAULT '1.0'::text,
  status policy_status_enum DEFAULT 'draft'::policy_status_enum,
  category text,
  owner_name text,
  owner_email text,
  reviewer_name text,
  reviewer_email text,
  approver_name text,
  approver_email text,
  effective_date date,
  last_reviewed date NOT NULL,
  next_review_date date,
  review_frequency review_frequency_enum DEFAULT 'annual'::review_frequency_enum,
  content text,
  objectives text,
  scope text,
  responsibilities text,
  procedures text,
  reference_text text,
  attachments jsonb DEFAULT '[]'::jsonb,
  document_url text,
  is_template boolean DEFAULT false,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  parent_policy_id uuid,
  CONSTRAINT compliance_policies_pkey PRIMARY KEY (id),
  CONSTRAINT fk_policies_user FOREIGN KEY (user_id) REFERENCES auth.users(id),
  CONSTRAINT fk_policies_framework FOREIGN KEY (framework_id) REFERENCES public.compliance_frameworks(id),
  CONSTRAINT fk_parent_policy FOREIGN KEY (parent_policy_id) REFERENCES public.compliance_policies(id)
);

CREATE TABLE IF NOT EXISTS public.compliance_reports (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL,
  title text NOT NULL,
  description text,
  report_type report_type_enum NOT NULL,
  framework_id uuid,
  date_range_start date,
  date_range_end date,
  status text DEFAULT 'draft'::text,
  generated_at timestamp with time zone,
  generated_by text,
  file_url text,
  file_size integer,
  parameters jsonb DEFAULT '{}'::jsonb,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT compliance_reports_pkey PRIMARY KEY (id),
  CONSTRAINT compliance_reports_framework_id_fkey FOREIGN KEY (framework_id) REFERENCES public.compliance_frameworks(id),
  CONSTRAINT compliance_reports_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id)
);

CREATE TABLE IF NOT EXISTS public.compliance_risk_assessments (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  user_id uuid,
  framework_id uuid,
  title character varying NOT NULL,
  description text,
  status character varying DEFAULT 'draft'::character varying CHECK (status::text = ANY (ARRAY['draft'::character varying, 'in_progress'::character varying, 'completed'::character varying, 'cancelled'::character varying]::text[])),
  risk_score integer DEFAULT 0 CHECK (risk_score >= 0 AND risk_score <= 100),
  risk_level character varying DEFAULT 'low'::character varying CHECK (risk_level::text = ANY (ARRAY['very_low'::character varying, 'low'::character varying, 'medium'::character varying, 'high'::character varying, 'very_high'::character varying, 'critical'::character varying]::text[])),
  assessment_type character varying NOT NULL,
  assessor_name character varying,
  review_frequency character varying DEFAULT 'annual'::character varying CHECK (review_frequency::text = ANY (ARRAY['annual'::character varying, 'semi-annual'::character varying, 'quarterly'::character varying, 'monthly'::character varying]::text[])),
  last_updated date NOT NULL,
  next_review_date date,
  methodology text,
  scope text,
  findings text,
  recommendations text,
  mitigation_plan text,
  residual_risk_score integer CHECK (residual_risk_score >= 0 AND residual_risk_score <= 100),
  approval_status character varying DEFAULT 'pending'::character varying CHECK (approval_status::text = ANY (ARRAY['pending'::character varying, 'approved'::character varying, 'rejected'::character varying]::text[])),
  approved_by character varying,
  approved_date date,
  document_url character varying,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT compliance_risk_assessments_pkey PRIMARY KEY (id),
  CONSTRAINT compliance_risk_assessments_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id),
  CONSTRAINT compliance_risk_assessments_framework_id_fkey FOREIGN KEY (framework_id) REFERENCES public.compliance_frameworks(id)
);

CREATE TABLE IF NOT EXISTS public.organizations (
  id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  name text NOT NULL UNIQUE,
  created_at timestamp with time zone DEFAULT now(),
  CONSTRAINT organizations_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.roles (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  name text NOT NULL UNIQUE CHECK (name = ANY (ARRAY['user'::text, 'admin'::text, 'auditor'::text])),
  description text,
  CONSTRAINT roles_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.permissions (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  name text NOT NULL UNIQUE,
  description text,
  created_at timestamp with time zone DEFAULT timezone('utc'::text, now()),
  updated_at timestamp with time zone DEFAULT timezone('utc'::text, now()),
  CONSTRAINT permissions_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.profiles (
  user_id uuid NOT NULL,
  username text UNIQUE,
  full_name text,
  avatar_url text,
  website text,
  created_at timestamp with time zone DEFAULT timezone('utc'::text, now()),
  updated_at timestamp with time zone DEFAULT timezone('utc'::text, now()),
  role_id uuid NOT NULL,
  organization bigint,
  CONSTRAINT profiles_pkey PRIMARY KEY (user_id),
  CONSTRAINT profiles_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id),
  CONSTRAINT profiles_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id),
  CONSTRAINT profiles_organization_fkey FOREIGN KEY (organization) REFERENCES public.organizations(id)
);

CREATE TABLE IF NOT EXISTS public.role_permissions (
  role_id uuid NOT NULL,
  permission_id uuid NOT NULL,
  created_at timestamp with time zone DEFAULT timezone('utc'::text, now()),
  CONSTRAINT role_permissions_pkey PRIMARY KEY (role_id, permission_id),
  CONSTRAINT role_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES public.permissions(id),
  CONSTRAINT role_permissions_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id)
);

CREATE TABLE IF NOT EXISTS public.scans (
  user_id uuid,
  organization_id bigint,
  created_at timestamp with time zone DEFAULT now(),
  config jsonb,
  name text,
  started_at timestamp with time zone DEFAULT now(),
  status text DEFAULT 'pending'::text CHECK (status = ANY (ARRAY['pending'::text, 'in_progress'::text, 'completed'::text, 'failed'::text])),
  compliance_summary jsonb DEFAULT '{}'::jsonb,
  summary jsonb DEFAULT '{}'::jsonb,
  detected_frameworks jsonb DEFAULT '{}'::jsonb,
  file_count integer DEFAULT 0,
  total_issues integer DEFAULT 0,
  critical_issues integer DEFAULT 0,
  high_issues integer DEFAULT 0,
  medium_issues integer DEFAULT 0,
  low_issues integer DEFAULT 0,
  id uuid NOT NULL DEFAULT gen_random_uuid() UNIQUE,
  description text,
  updated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT scans_pkey PRIMARY KEY (id),
  CONSTRAINT scans_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organizations(id),
  CONSTRAINT scans_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id)
);

CREATE TABLE IF NOT EXISTS public.issues (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  scan_id uuid NOT NULL,
  rule_id text,
  severity text NOT NULL CHECK (severity = ANY (ARRAY['low'::text, 'medium'::text, 'high'::text, 'critical'::text])),
  category text DEFAULT 'security'::text,
  message text,
  file_path text NOT NULL,
  line_number integer,
  column_number integer,
  code_snippet text,
  remediation text,
  confidence numeric DEFAULT 1.0 CHECK (confidence >= 0::numeric AND confidence <= 1::numeric),
  metadata jsonb DEFAULT '{}'::jsonb,
  standards jsonb DEFAULT '[]'::jsonb,
  compliance_frameworks text[] DEFAULT '{}'::text[],
  status text DEFAULT 'open'::text CHECK (status = ANY (ARRAY['open'::text, 'acknowledged'::text, 'resolved'::text, 'false_positive'::text, 'wont_fix'::text])),
  assigned_to uuid,
  resolved_at timestamp with time zone,
  resolution_notes text,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  title text,
  description text,
  recommendation text,
  CONSTRAINT issues_pkey PRIMARY KEY (id),
  CONSTRAINT issues_scan_id_fkey FOREIGN KEY (scan_id) REFERENCES public.scans(id),
  CONSTRAINT issues_assigned_to_fkey FOREIGN KEY (assigned_to) REFERENCES auth.users(id)
);

CREATE TABLE IF NOT EXISTS public.scan_files (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  scan_id uuid NOT NULL,
  file_name text NOT NULL,
  file_path text NOT NULL,
  file_size integer,
  storage_path text,
  mime_type text,
  checksum text,
  created_at timestamp with time zone DEFAULT now(),
  CONSTRAINT scan_files_pkey PRIMARY KEY (id),
  CONSTRAINT scan_files_scan_id_fkey FOREIGN KEY (scan_id) REFERENCES public.scans(id)
);

CREATE TABLE IF NOT EXISTS public.user_organizations (
  id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  user_id uuid NOT NULL,
  organization_id bigint NOT NULL,
  role text NOT NULL DEFAULT 'member'::text,
  status text NOT NULL DEFAULT 'active'::text CHECK (status = ANY (ARRAY['active'::text, 'pending'::text, 'inactive'::text])),
  joined_at timestamp with time zone DEFAULT now(),
  created_at timestamp with time zone DEFAULT now(),
  CONSTRAINT user_organizations_pkey PRIMARY KEY (id),
  CONSTRAINT user_organizations_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id),
  CONSTRAINT user_organizations_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organizations(id)
);

CREATE TABLE IF NOT EXISTS public.user_roles (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL,
  role_id uuid NOT NULL,
  CONSTRAINT user_roles_pkey PRIMARY KEY (id),
  CONSTRAINT user_roles_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id),
  CONSTRAINT user_roles_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id)
);

-- Insert mock data
-- Insert organizations
INSERT INTO public.organizations (name) VALUES
('TechCorp Inc.'),
('SecureDev Solutions'),
('ComplianceFirst Ltd.')
ON CONFLICT (name) DO NOTHING;

-- Insert roles
INSERT INTO public.roles (name, description) VALUES
('user', 'Standard user with basic access'),
('admin', 'Administrator with full access'),
('auditor', 'Auditor with compliance access')
ON CONFLICT (name) DO NOTHING;

-- Insert permissions
INSERT INTO public.permissions (name, description) VALUES
('read_scans', 'Can view scan results'),
('create_scans', 'Can initiate new scans'),
('manage_compliance', 'Can manage compliance frameworks'),
('view_reports', 'Can view compliance reports'),
('admin_access', 'Full administrative access')
ON CONFLICT (name) DO NOTHING;

-- Insert compliance frameworks
INSERT INTO public.compliance_frameworks (name, description, version, code, status, compliance_score, total_controls, implemented_controls, audit_frequency, regulatory_body) VALUES
('ISO 27001', 'Information Security Management Systems', '2022', 'ISO27001', 'active', 85, 114, 97, 'annual', 'ISO'),
('OWASP Top 10', 'Web Application Security', '2021', 'OWASP', 'active', 78, 10, 8, 'quarterly', 'OWASP'),
('GDPR', 'General Data Protection Regulation', '2018', 'GDPR', 'active', 92, 99, 91, 'annual', 'EU'),
('PCI DSS', 'Payment Card Industry Data Security Standard', '4.0', 'PCIDSS', 'active', 76, 12, 9, 'annual', 'PCI SSC'),
('NIST Cybersecurity Framework', 'NIST CSF', '2.0', 'NISTCSF', 'active', 88, 108, 95, 'annual', 'NIST')
ON CONFLICT (name) DO NOTHING;

-- Insert compliance controls
INSERT INTO public.compliance_controls (framework_id, control_id, title, description, category, control_type, status, priority, owner_name) 
SELECT 
  cf.id,
  'CTRL-' || cf.code || '-' || ROW_NUMBER() OVER (PARTITION BY cf.id ORDER BY cf.id),
  'Control ' || ROW_NUMBER() OVER (PARTITION BY cf.id ORDER BY cf.id),
  'Description for control ' || ROW_NUMBER() OVER (PARTITION BY cf.id ORDER BY cf.id),
  'Technical',
  'preventive',
  'fully_implemented',
  'medium',
  'John Doe'
FROM public.compliance_frameworks cf
CROSS JOIN generate_series(1, 5) AS gs(num)
ON CONFLICT DO NOTHING;

-- Insert scans
INSERT INTO public.scans (name, description, status, file_count, total_issues, critical_issues, high_issues, medium_issues, low_issues, compliance_summary, summary) VALUES
('Security Audit - Project Alpha', 'Comprehensive security scan of Project Alpha codebase', 'completed', 45, 23, 2, 5, 8, 8, '{"ISO 27001": 85, "OWASP": 78}', '{"scanned_files": 45, "vulnerabilities_found": 23}'),
('Compliance Check - API Gateway', 'Compliance verification for API Gateway services', 'completed', 12, 7, 0, 2, 3, 2, '{"GDPR": 92, "PCI DSS": 76}', '{"scanned_files": 12, "vulnerabilities_found": 7}'),
('Weekly Security Scan', 'Automated weekly security assessment', 'in_progress', 67, 0, 0, 0, 0, 0, '{}', '{"scanned_files": 67, "vulnerabilities_found": 0}'),
('Mobile App Security Review', 'Security audit of mobile application', 'completed', 23, 15, 1, 4, 6, 4, '{"OWASP": 82}', '{"scanned_files": 23, "vulnerabilities_found": 15}'),
('Database Security Assessment', 'Security assessment of database configurations', 'failed', 8, 0, 0, 0, 0, 0, '{}', '{"error": "Connection timeout"}')
ON CONFLICT (id) DO NOTHING;

-- Insert issues
INSERT INTO public.issues (scan_id, severity, category, title, description, file_path, line_number, status, recommendation) 
SELECT 
  s.id,
  CASE WHEN random() < 0.1 THEN 'critical' 
       WHEN random() < 0.3 THEN 'high' 
       WHEN random() < 0.6 THEN 'medium' 
       ELSE 'low' END,
  'security',
  'Security Issue ' || ROW_NUMBER() OVER (PARTITION BY s.id ORDER BY s.id),
  'Description of security issue ' || ROW_NUMBER() OVER (PARTITION BY s.id ORDER BY s.id),
  '/src/components/' || (ROW_NUMBER() OVER (PARTITION BY s.id ORDER BY s.id)) || '.js',
  floor(random() * 100 + 1)::int,
  CASE WHEN random() < 0.7 THEN 'open' ELSE 'resolved' END,
  'Implement proper input validation and sanitization'
FROM public.scans s
CROSS JOIN generate_series(1, 5) AS gs(num)
WHERE s.status = 'completed'
ON CONFLICT DO NOTHING;

-- Insert compliance audits
INSERT INTO public.compliance_audits (framework_id, framework_name, audit_type, audit_date, status, auditor_name, total_findings, critical_findings, high_findings, compliance_score) 
SELECT 
  cf.id,
  cf.name,
  'internal',
  CURRENT_DATE - INTERVAL '30 days',
  'completed',
  'Jane Smith',
  15,
  1,
  3,
  cf.compliance_score
FROM public.compliance_frameworks cf
ON CONFLICT DO NOTHING;

-- Insert compliance issues
INSERT INTO public.compliance_issues (user_id, framework_id, title, description, severity, status, issue_type, discovered_date, reported_by, priority_score) 
SELECT 
  '00000000-0000-0000-0000-000000000000'::uuid, -- Placeholder user_id
  cf.id,
  'Compliance Issue ' || ROW_NUMBER() OVER (PARTITION BY cf.id ORDER BY cf.id),
  'Description of compliance issue ' || ROW_NUMBER() OVER (PARTITION BY cf.id ORDER BY cf.id),
  'medium',
  'open',
  'technical',
  CURRENT_DATE - INTERVAL '15 days',
  'System Scanner',
  floor(random() * 100)::int
FROM public.compliance_frameworks cf
CROSS JOIN generate_series(1, 3) AS gs(num)
ON CONFLICT DO NOTHING;

-- Insert compliance reports
INSERT INTO public.compliance_reports (user_id, title, description, report_type, status, generated_by) VALUES
('00000000-0000-0000-0000-000000000000'::uuid, 'Monthly Compliance Report', 'Comprehensive compliance status report', 'compliance', 'generated', 'System'),
('00000000-0000-0000-0000-000000000000'::uuid, 'Risk Assessment Report', 'Annual risk assessment findings', 'risk_assessment', 'generated', 'System'),
('00000000-0000-0000-0000-000000000000'::uuid, 'Audit Findings Report', 'Internal audit results and recommendations', 'audit', 'draft', 'System')
ON CONFLICT DO NOTHING;

-- Insert audit logs
INSERT INTO public.audit_logs (user_id, action) VALUES
('00000000-0000-0000-0000-000000000000'::uuid, 'User logged in'),
('00000000-0000-0000-0000-000000000000'::uuid, 'Scan initiated'),
('00000000-0000-0000-0000-000000000000'::uuid, 'Compliance report generated'),
('00000000-0000-0000-0000-000000000000'::uuid, 'User profile updated')
ON CONFLICT DO NOTHING;

-- Enable Row Level Security (RLS) on tables
ALTER TABLE public.compliance_frameworks ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.compliance_audits ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.compliance_controls ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.compliance_issues ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.compliance_policies ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.compliance_reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.compliance_risk_assessments ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.scans ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.issues ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.scan_files ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.audit_logs ENABLE ROW LEVEL SECURITY;

-- Create basic RLS policies (these would need to be adjusted based on your auth setup)
CREATE POLICY "Users can view their own compliance frameworks" ON public.compliance_frameworks
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can view their own scans" ON public.scans
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can view issues from their scans" ON public.issues
  FOR SELECT USING (
    scan_id IN (
      SELECT id FROM public.scans WHERE user_id = auth.uid()
    )
  );

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_compliance_frameworks_user_id ON public.compliance_frameworks(user_id);
CREATE INDEX IF NOT EXISTS idx_compliance_audits_framework_id ON public.compliance_audits(framework_id);
CREATE INDEX IF NOT EXISTS idx_compliance_controls_framework_id ON public.compliance_controls(framework_id);
CREATE INDEX IF NOT EXISTS idx_compliance_issues_framework_id ON public.compliance_issues(framework_id);
CREATE INDEX IF NOT EXISTS idx_scans_user_id ON public.scans(user_id);
CREATE INDEX IF NOT EXISTS idx_issues_scan_id ON public.issues(scan_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_user_id ON public.audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at ON public.audit_logs(created_at);

-- Create views for analytics
CREATE OR REPLACE VIEW public.scan_analytics AS
SELECT
  DATE_TRUNC('day', created_at) as scan_date,
  COUNT(*) as total_scans,
  SUM(total_issues) as total_issues,
  SUM(critical_issues) as critical_issues,
  SUM(high_issues) as high_issues,
  SUM(medium_issues) as medium_issues,
  SUM(low_issues) as low_issues,
  AVG(total_issues) as avg_issues_per_scan
FROM public.scans
WHERE status = 'completed'
GROUP BY DATE_TRUNC('day', created_at)
ORDER BY scan_date DESC;

CREATE OR REPLACE VIEW public.compliance_analytics AS
SELECT
  cf.name as framework_name,
  cf.compliance_score,
  COUNT(ca.id) as total_audits,
  AVG(ca.compliance_score) as avg_audit_score,
  SUM(ca.total_findings) as total_findings,
  SUM(ca.critical_findings) as critical_findings
FROM public.compliance_frameworks cf
LEFT JOIN public.compliance_audits ca ON cf.id = ca.framework_id
GROUP BY cf.id, cf.name, cf.compliance_score;

-- Grant necessary permissions
GRANT USAGE ON SCHEMA public TO anon, authenticated;
GRANT ALL ON ALL TABLES IN SCHEMA public TO authenticated;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO authenticated;
