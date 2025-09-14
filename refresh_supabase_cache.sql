-- Refresh Supabase Schema Cache
-- Run this in your Supabase SQL Editor to refresh the schema cache

-- This will force Supabase to refresh its internal schema cache
-- and recognize the 'description' column in the scans table

-- Method 1: Simple table comment update (forces cache refresh)
COMMENT ON TABLE public.scans IS 'Security scan records with enhanced schema - cache refreshed';

-- Method 2: Update table statistics (also helps with cache)
ANALYZE public.scans;

-- Method 3: If you have access to Supabase dashboard:
-- Go to Settings > API > Reset Schema Cache
-- Or restart your Supabase project

-- Verify the description column exists
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'scans'
AND table_schema = 'public'
AND column_name = 'description';
