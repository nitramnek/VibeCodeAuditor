-- Fix the issues table constraint that's preventing multiple issues per scan

-- 1. Drop the problematic unique constraint on scan_id
ALTER TABLE public.issues 
DROP CONSTRAINT IF EXISTS issues_scan_id_tmp_key,
DROP CONSTRAINT IF EXISTS issues_scan_id_key,
DROP CONSTRAINT IF EXISTS issues_scan_id_unique;

-- 2. Also check for any other unique constraints on scan_id
DO $$ 
DECLARE 
    constraint_name text;
BEGIN
    -- Find and drop any unique constraints on scan_id column
    FOR constraint_name IN 
        SELECT conname 
        FROM pg_constraint 
        WHERE conrelid = 'public.issues'::regclass 
        AND contype = 'u' 
        AND 'scan_id' = ANY(
            SELECT attname 
            FROM pg_attribute 
            WHERE attrelid = conrelid 
            AND attnum = ANY(conkey)
        )
    LOOP
        EXECUTE 'ALTER TABLE public.issues DROP CONSTRAINT IF EXISTS ' || quote_ident(constraint_name);
        RAISE NOTICE 'Dropped constraint: %', constraint_name;
    END LOOP;
END $$;

-- 3. Ensure the foreign key constraint exists (but not unique)
ALTER TABLE public.issues 
DROP CONSTRAINT IF EXISTS issues_scan_id_fkey;

ALTER TABLE public.issues 
ADD CONSTRAINT issues_scan_id_fkey FOREIGN KEY (scan_id) REFERENCES public.scans(id);

-- 4. Create a proper index for performance (but not unique)
CREATE INDEX IF NOT EXISTS idx_issues_scan_id ON public.issues(scan_id);

-- 5. Verify the constraints
SELECT 
    conname as constraint_name,
    contype as constraint_type,
    pg_get_constraintdef(oid) as definition
FROM pg_constraint 
WHERE conrelid = 'public.issues'::regclass
ORDER BY contype, conname;