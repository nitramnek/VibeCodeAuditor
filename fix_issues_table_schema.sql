-- Fix issues table schema to ensure recommendation column exists
-- Run this in your Supabase SQL editor

-- Check if recommendation column exists, if not add it
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'issues' 
        AND column_name = 'recommendation'
        AND table_schema = 'public'
    ) THEN
        ALTER TABLE public.issues ADD COLUMN recommendation TEXT;
        RAISE NOTICE 'Added recommendation column to issues table';
    ELSE
        RAISE NOTICE 'Recommendation column already exists in issues table';
    END IF;
END $$;

-- Refresh the schema cache
NOTIFY pgrst, 'reload schema';

-- Verify the column exists
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'issues' 
AND table_schema = 'public'
ORDER BY ordinal_position;