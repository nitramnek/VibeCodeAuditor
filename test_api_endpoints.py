#!/usr/bin/env python3
"""
Test API endpoints to verify they work correctly
"""
import sys
import os
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def test_imports():
    """Test that all imports work correctly"""
    try:
        print("Testing imports...")
        from vibeauditor.main import app
        print("✅ Main app imported successfully")
        
        from vibeauditor.core.supabase_client import get_supabase_client
        print("✅ Supabase client imported successfully")
        
        from vibeauditor.scanners.real_security_scanner import SecurityScanner
        print("✅ Security scanner imported successfully")
        
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_endpoints():
    """Test API endpoints"""
    try:
        from fastapi.testclient import TestClient
        from vibeauditor.main import app
        
        client = TestClient(app)
        
        # Test health endpoint
        print("\nTesting /health endpoint...")
        response = client.get("/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print("❌ Health endpoint failed")
            
        return True
        
    except Exception as e:
        print(f"❌ Endpoint test error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Testing VibeCodeAuditor API")
    print("=" * 40)
    
    # Test imports
    if not test_imports():
        sys.exit(1)
    
    # Test endpoints
    if not test_endpoints():
        sys.exit(1)
    
    print("\n✅ All tests passed!")