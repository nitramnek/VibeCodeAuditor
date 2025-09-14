#!/usr/bin/env python3
"""
Test Supabase connection and database functionality.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables
load_dotenv()

from vibeauditor.database.supabase_client import supabase_client
from vibeauditor.database.service import db_service

def test_environment_variables():
    """Test if environment variables are set correctly."""
    print("🔍 Testing Environment Variables")
    print("=" * 40)
    
    required_vars = [
        'SUPABASE_URL',
        'SUPABASE_ANON_KEY', 
        'SUPABASE_SERVICE_ROLE_KEY',
        'DATABASE_URL'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Mask sensitive keys
            if 'KEY' in var:
                display_value = f"{value[:20]}...{value[-10:]}" if len(value) > 30 else "***"
            else:
                display_value = value
            print(f"✅ {var}: {display_value}")
        else:
            print(f"❌ {var}: Not set")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n⚠️  Missing environment variables: {', '.join(missing_vars)}")
        return False
    
    print("✅ All environment variables are set!")
    return True

def test_supabase_client():
    """Test Supabase client initialization."""
    print("\n🔍 Testing Supabase Client")
    print("=" * 40)
    
    if not supabase_client.is_available():
        print("❌ Supabase client not available")
        return False
    
    print("✅ Supabase client initialized successfully")
    
    # Test connection
    if supabase_client.test_connection():
        print("✅ Database connection successful!")
        return True
    else:
        print("❌ Database connection failed")
        return False

def test_database_tables():
    """Test if required tables exist."""
    print("\n🔍 Testing Database Tables")
    print("=" * 40)
    
    if not supabase_client.is_available():
        print("❌ Supabase client not available")
        return False
    
    client = supabase_client.get_client()
    required_tables = [
        'profiles',
        'organizations', 
        'scans',
        'issues',
        'scan_files',
        'audit_logs',
        'compliance_frameworks'
    ]
    
    success_count = 0
    for table in required_tables:
        try:
            # Try to query the table (limit 0 to avoid returning data)
            result = client.table(table).select('*').limit(0).execute()
            print(f"✅ Table '{table}' exists and is accessible")
            success_count += 1
        except Exception as e:
            print(f"❌ Table '{table}' error: {e}")
    
    print(f"\n📊 Tables Status: {success_count}/{len(required_tables)} accessible")
    return success_count == len(required_tables)

def test_database_service():
    """Test database service functionality."""
    print("\n🔍 Testing Database Service")
    print("=" * 40)
    
    if not db_service.is_available():
        print("❌ Database service not available")
        return False
    
    print("✅ Database service is available")
    
    # Test creating a test scan (this will fail without a real user, but we can test the method)
    try:
        # This should fail gracefully since we don't have a real user_id
        scan_id = db_service.create_scan("test-user-id", "Test Scan")
        if scan_id:
            print(f"✅ Scan creation test successful (ID: {scan_id})")
        else:
            print("⚠️  Scan creation returned None (expected without valid user)")
    except Exception as e:
        print(f"⚠️  Scan creation test error (expected): {e}")
    
    return True

def test_compliance_frameworks():
    """Test compliance frameworks data."""
    print("\n🔍 Testing Compliance Frameworks")
    print("=" * 40)
    
    if not supabase_client.is_available():
        print("❌ Supabase client not available")
        return False
    
    try:
        client = supabase_client.get_client()
        result = client.table('compliance_frameworks').select('name, description').execute()
        
        if result.data:
            print(f"✅ Found {len(result.data)} compliance frameworks:")
            for framework in result.data:
                print(f"   - {framework['name']}: {framework.get('description', 'No description')}")
            return True
        else:
            print("⚠️  No compliance frameworks found")
            print("💡 Run the schema enhancements to add default frameworks")
            return False
            
    except Exception as e:
        print(f"❌ Error querying compliance frameworks: {e}")
        return False

def test_storage_bucket():
    """Test storage bucket access."""
    print("\n🔍 Testing Storage Bucket")
    print("=" * 40)
    
    if not supabase_client.is_available():
        print("❌ Supabase client not available")
        return False
    
    try:
        client = supabase_client.get_client()
        bucket_name = os.getenv('SUPABASE_STORAGE_BUCKET', 'vibeauditor-files')
        
        # Try to list files in the bucket (should work even if empty)
        result = client.storage.from_(bucket_name).list()
        
        if result:
            print(f"✅ Storage bucket '{bucket_name}' is accessible")
            return True
        else:
            print(f"⚠️  Storage bucket '{bucket_name}' exists but may be empty")
            return True
            
    except Exception as e:
        print(f"❌ Storage bucket error: {e}")
        print("💡 Make sure you created the 'vibeauditor-files' bucket in Supabase Storage")
        return False

def main():
    """Run all Supabase tests."""
    print("🚀 VibeCodeAuditor - Supabase Connection Test")
    print("=" * 60)
    
    tests = [
        ("Environment Variables", test_environment_variables),
        ("Supabase Client", test_supabase_client),
        ("Database Tables", test_database_tables),
        ("Database Service", test_database_service),
        ("Compliance Frameworks", test_compliance_frameworks),
        ("Storage Bucket", test_storage_bucket),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your Supabase integration is working perfectly!")
        print("\n🚀 Next Steps:")
        print("   1. Run schema enhancements: Copy supabase_schema_enhancements.sql to Supabase SQL Editor")
        print("   2. Update your API to use the database service")
        print("   3. Test the enhanced compliance UI with real data")
        print("   4. Set up authentication in your React app")
        return True
    else:
        print(f"\n⚠️  {total - passed} tests failed. Please check the issues above.")
        print("\n🔧 Common Solutions:")
        print("   - Verify environment variables in .env file")
        print("   - Check Supabase project is active and accessible")
        print("   - Run the database schema setup in Supabase SQL Editor")
        print("   - Create the 'vibeauditor-files' storage bucket")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)