-- Schema Alignment Fix for VibeCodeAuditor
-- This fixes the UUID generation and column alignment issues

-- 1. Fix the scans table to auto-generate UUIDs
ALTER TABLE public.scans 
ALTER COLUMN id SET DEFAULT gen_random_uuid();

-- 2. Clean up the issues table - remove old bigint column and fix scan_id
ALTER TABLE public.issues 
DROP COLUMN IF EXISTS scan_id_old_bigint,
ALTER COLUMN scan_id DROP CONSTRAINT IF EXISTS issues_scan_id_key,
DROP CONSTRAINT IF EXISTS issues_scan_id_fkey;

-- Re-add the foreign key constraint properly
ALTER TABLE public.issues 
ADD CONSTRAINT issues_scan_id_fkey FOREIGN KEY (scan_id) REFERENCES public.scans(id);

-- Remove the UNIQUE constraint on scan_id in issues (multiple issues can belong to one scan)
-- The UNIQUE constraint doesn't make sense here

-- 3. Clean up the scan_files table similarly
ALTER TABLE public.scan_files 
DROP COLUMN IF EXISTS scan_id_old_bigint,
ALTER COLUMN scan_id DROP CONSTRAINT IF EXISTS scan_files_scan_id_key,
DROP CONSTRAINT IF EXISTS scan_files_scan_id_fkey;

-- Re-add the foreign key constraint properly
ALTER TABLE public.scan_files 
ADD CONSTRAINT scan_files_scan_id_fkey FOREIGN KEY (scan_id) REFERENCES public.scans(id);

-- Remove the UNIQUE constraint on scan_id in scan_files (multiple files can belong to one scan)

-- 4. Create a demo scan with proper UUID for fallback
INSERT INTO public.scans (
    id,
    user_id,
    name,
    status,
    file_count,
    summary,
    compliance_summary,
    detected_frameworks,
    total_issues,
    critical_issues,
    high_issues,
    medium_issues,
    low_issues
) VALUES (
    'demo-scan-123e-4567-e89b-12d3a456426614'::uuid,
    '289c36cf-8779-4e49-bcfe-b829d0899472'::uuid, -- Your user ID
    'Demo Scan',
    'completed',
    1,
    '{"total_issues": 3, "files_scanned": 1}'::jsonb,
    '{"ISO 27001": {"name": "ISO 27001", "count": 2}}'::jsonb,
    '{"javascript": {"name": "JavaScript", "type": "language"}}'::jsonb,
    3,
    1,
    1,
    1,
    0
) ON CONFLICT (id) DO UPDATE SET
    name = EXCLUDED.name,
    status = EXCLUDED.status,
    summary = EXCLUDED.summary;

-- 5. Create demo issues for the demo scan
INSERT INTO public.issues (
    scan_id,
    title,
    description,
    severity,
    status,
    file_path,
    line_number,
    recommendation
) VALUES 
(
    'demo-scan-123e-4567-e89b-12d3a456426614'::uuid,
    'Hardcoded API Key',
    'A hardcoded API key was found in the source code',
    'critical',
    'open',
    'test.js',
    15,
    'Move API keys to environment variables'
),
(
    'demo-scan-123e-4567-e89b-12d3a456426614'::uuid,
    'SQL Injection Risk',
    'Potential SQL injection vulnerability detected',
    'high',
    'open',
    'test.js',
    42,
    'Use parameterized queries'
),
(
    'demo-scan-123e-4567-e89b-12d3a456426614'::uuid,
    'Missing Input Validation',
    'User input is not properly validated',
    'medium',
    'open',
    'test.js',
    28,
    'Implement input validation'
) ON CONFLICT DO NOTHING;

-- 6. Verify the schema is correct
SELECT 
    table_name,
    column_name,
    data_type,
    column_default,
    is_nullable
FROM information_schema.columns 
WHERE table_schema = 'public' 
AND table_name IN ('scans', 'issues', 'scan_files')
AND column_name LIKE '%id%'
ORDER BY table_name, ordinal_position;