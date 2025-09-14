# Database Fixes for VibeCodeAuditor

## Issue Summary
The application was experiencing:
1. **Infinite recursion in RLS policies** - causing 500 errors
2. **Schema misalignment** - frontend expecting columns that don't exist
3. **ID generation conflicts** - trying to manually set auto-generated IDs

## How to Apply Fixes

### Option 1: Supabase Dashboard (Recommended)
1. Go to your Supabase project dashboard
2. Navigate to **SQL Editor**
3. Copy and paste the contents of `database_fixes.sql`
4. Click **Run** to execute all fixes

### Option 2: Command Line (if you have psql access)
```bash
psql -h your-supabase-host -U postgres -d postgres -f database_fixes.sql
```

## What These Fixes Do

### 1. Fix RLS Policies
- Removes problematic recursive policies on `user_organizations`
- Creates simple, non-recursive policies for all tables
- Ensures users can only access their own data

### 2. Schema Alignment
- Adds missing columns to `issues` table:
  - `title` - Issue title/name
  - `description` - Detailed description
  - `file_path` - Path to affected file
  - `line_number` - Line number of issue
  - `recommendation` - Fix recommendation

### 3. Performance Improvements
- Adds indexes on frequently queried columns
- Optimizes query performance for scans and issues

### 4. Data Integrity
- Ensures proper foreign key relationships
- Adds default roles and organization if missing

## Frontend Changes Made

### Scanner.js Updates
- Fixed scan creation to use database-generated IDs
- Added proper issue mapping with all required fields
- Enhanced error handling and logging

### Expected Results After Fixes
- ✅ No more "infinite recursion" errors
- ✅ Successful scan creation and retrieval
- ✅ Proper issue tracking and display
- ✅ Better performance and security

## Testing the Fixes
1. Apply the database fixes
2. Restart your application
3. Try uploading a file for scanning
4. Verify the scan appears in results
5. Check that issues are properly displayed

## Rollback Plan
If you need to rollback, you can:
1. Drop the new policies: `DROP POLICY IF EXISTS "policy_name" ON table_name;`
2. Remove added columns: `ALTER TABLE issues DROP COLUMN IF EXISTS title;`
3. Restore your previous RLS policies

## Support
If you encounter any issues after applying these fixes, check:
1. Supabase logs for any remaining policy errors
2. Browser console for frontend errors
3. Network tab for failed API calls