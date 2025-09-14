#!/usr/bin/env python3
"""
Complete fix for Supabase schema cache issue
"""

import os
import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv()

def wait_for_user_confirmation():
    """Wait for user to refresh schema cache in Supabase dashboard"""
    print("\n" + "="*60)
    print("🔧 SUPABASE SCHEMA CACHE REFRESH REQUIRED")
    print("="*60)
    print()
    print("Please follow these steps in your Supabase dashboard:")
    print()
    print("1. Go to: https://supabase.com/dashboard/project/YOUR_PROJECT")
    print("2. Navigate to: Settings > API")
    print("3. Click: 'Reset Schema Cache' button")
    print("4. Or alternatively: Restart your Supabase project")
    print()
    print("After refreshing the cache, press Enter to continue...")
    input()

def test_fix():
    """Test that the schema cache fix worked"""
    print("\n🧪 Testing Schema Cache Fix")
    print("-" * 30)

    try:
        from supabase import create_client, Client

        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_ANON_KEY')

        if not supabase_url or not supabase_key:
            print('❌ Missing Supabase credentials')
            return False

        supabase: Client = create_client(supabase_url, supabase_key)

        # Test the exact insert that was failing
        test_data = {
            "user_id": "00000000-0000-0000-0000-000000000000",
            "name": "Schema Cache Test",
            "description": "Testing if description column is now recognized",
            "status": "pending",
            "file_count": 1
        }

        print("📤 Testing insert with description column...")
        result = supabase.table('scans').insert(test_data).execute()

        if result.data:
            scan_id = result.data[0]['id']
            print(f"✅ Insert successful! Scan ID: {scan_id}")

            # Clean up
            supabase.table('scans').delete().eq('id', scan_id).execute()
            print("🧹 Test data cleaned up")

            return True
        else:
            print("❌ Insert returned no data")
            return False

    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_full_upload_flow():
    """Test the complete upload flow"""
    print("\n🚀 Testing Complete Upload Flow")
    print("-" * 35)

    import requests

    # Create test file
    test_file_path = "test_upload.py"
    with open(test_file_path, 'w') as f:
        f.write("# Test file for upload\ndef test():\n    return 'success'\n")

    try:
        url = "http://localhost:8000/scan"

        with open(test_file_path, 'rb') as f:
            files = {'file': ('test_upload.py', f, 'text/plain')}
            data = {'user_id': 'test-user-123'}

            print("📤 Sending upload request...")
            response = requests.post(url, files=files, data=data, timeout=30)

            print(f"📊 Status: {response.status_code}")

            if response.status_code == 200:
                print("✅ Upload successful!")
                return True
            else:
                print(f"❌ Upload failed: {response.text}")
                return False

    except Exception as e:
        print(f"❌ Request error: {e}")
        return False
    finally:
        # Clean up
        if os.path.exists(test_file_path):
            os.remove(test_file_path)

def main():
    print("🔧 VibeCodeAuditor - Supabase Schema Cache Fix")
    print("=" * 50)

    # Step 1: Wait for user to refresh cache
    wait_for_user_confirmation()

    # Step 2: Test the fix
    cache_test = test_fix()

    if cache_test:
        print("\n✅ Schema cache fix verified!")

        # Step 3: Test full upload flow
        upload_test = test_full_upload_flow()

        if upload_test:
            print("\n🎉 ALL TESTS PASSED!")
            print("The upload functionality should now work correctly.")
        else:
            print("\n⚠️  Schema cache fixed, but upload still failing.")
            print("Check server logs for additional issues.")
    else:
        print("\n❌ Schema cache fix did not work.")
        print("Please try refreshing the cache again or contact Supabase support.")

if __name__ == '__main__':
    main()
