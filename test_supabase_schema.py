#!/usr/bin/env python3
"""
Test script to diagnose Supabase schema cache issues
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv()

def test_supabase_connection():
    """Test Supabase connection and schema cache"""
    try:
        from supabase import create_client, Client

        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_ANON_KEY')

        if not supabase_url or not supabase_key:
            print('❌ Missing Supabase credentials')
            return False

        print(f'🔗 Connecting to Supabase: {supabase_url[:30]}...')

        supabase: Client = create_client(supabase_url, supabase_key)
        print('✅ Supabase client created')

        # Test basic table access
        print('🔍 Testing scans table access...')
        result = supabase.table('scans').select('id, name').limit(1).execute()
        print('✅ Basic scans table query successful')

        # Test description column specifically
        print('🔍 Testing description column access...')
        result = supabase.table('scans').select('id, name, description').limit(1).execute()
        print('✅ Description column accessible')

        # Test insert with description
        print('🔍 Testing insert with description...')
        test_data = {
            "user_id": "test-user-123",
            "name": "Test Scan",
            "description": "Test description for schema cache",
            "status": "pending"
        }

        # Use upsert to avoid conflicts
        result = supabase.table('scans').upsert(test_data).execute()
        print('✅ Insert with description successful')

        # Clean up test data
        if result.data:
            scan_id = result.data[0]['id']
            supabase.table('scans').delete().eq('id', scan_id).execute()
            print('🧹 Test data cleaned up')

        return True

    except Exception as e:
        print(f'❌ Error: {e}')
        return False

if __name__ == '__main__':
    print('🧪 Testing Supabase Schema Cache')
    print('=' * 40)

    success = test_supabase_connection()

    if success:
        print('\n✅ All tests passed! Schema cache is working correctly.')
    else:
        print('\n❌ Tests failed. Schema cache issue detected.')
        print('\n💡 Possible solutions:')
        print('1. Refresh Supabase schema cache in dashboard')
        print('2. Restart Supabase services')
        print('3. Check Supabase project settings')
        print('4. Verify RLS policies allow the operations')
