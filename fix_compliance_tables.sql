-- Fix missing compliance tables
-- Run this if some tables are missing after the initial migration

-- Create missing compliance_policies table
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
    last_reviewed DATE NOT NULL DEFAULT CURRENT_DATE,
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

-- Create missing compliance_issues table
CREATE TABLE IF NOT EXISTS public.compliance_issues (
    id uu