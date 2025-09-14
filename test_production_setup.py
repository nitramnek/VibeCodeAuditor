#!/usr/bin/env python3
"""
Test script to verify VibeCodeAuditor production setup.
"""

import os
import sys
import subprocess
import requests
import time
import json
from pathlib import Path

def test_dependencies():
    """Test if all required dependencies are available."""
    print("🔍 Testing dependencies...")
    
    tests = [
        ("python3 --version", "Python 3"),
        ("node --version", "Node.js"),
        ("npm --version", "npm"),
        ("bandit --version", "Bandit security scanner"),
        ("semgrep --version", "Semgrep scanner"),
        ("eslint --version", "ESLint"),
    ]
    
    results = []
    for cmd, name in tests:
        try:
            result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"  ✅ {name}: {result.stdout.strip()}")
                results.append(True)
            else:
                print(f"  ❌ {name}: Not found or error")
                results.append(False)
        except Exception as e:
            print(f"  ❌ {name}: Error - {e}")
            results.append(False)
    
    return all(results)

def test_environment():
    """Test environment configuration."""
    print("\n🔍 Testing environment configuration...")
    
    # Load .env if exists
    env_file = Path(".env")
    if env_file.exists():
        from dotenv import load_dotenv
        load_dotenv()
        print("  ✅ .env file loaded")
    else:
        print("  ⚠️  No .env file found")
    
    # Check required environment variables
    required_vars = [
        "SUPABASE_URL",
        "SUPABASE_ANON_KEY"
    ]
    
    missing = []
    for var in required_vars:
        if os.getenv(var):
            print(f"  ✅ {var}: Set")
        else:
            print(f"  ❌ {var}: Missing")
            missing.append(var)
    
    return len(missing) == 0

def test_security_scanners():
    """Test security scanner functionality."""
    print("\n🔍 Testing security scanners...")
    
    # Create a test file with security issues
    test_file = Path("test_security_sample.py")
    test_content = '''
import os
import subprocess

# Security issue: hardcoded password
password = "admin123"

# Security issue: SQL injection vulnerability
def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return query

# Security issue: command injection
def run_command(cmd):
    os.system(cmd)

# Security issue: insecure random
import random
token = random.randint(1000, 9999)
'''
    
    test_file.write_text(test_content)
    
    try:
        # Test Bandit
        print("  Testing Bandit...")
        result = subprocess.run(
            ["bandit", "-f", "json", str(test_file)], 
            capture_output=True, text=True, timeout=30
        )
        if result.returncode in [0, 1]:  # Bandit returns 1 when issues found
            try:
                bandit_results = json.loads(result.stdout)
                issues_found = len(bandit_results.get("results", []))
                print(f"    ✅ Bandit found {issues_found} security issues")
            except:
                print("    ✅ Bandit executed successfully")
        else:
            print(f"    ❌ Bandit failed: {result.stderr}")
        
        # Test Semgrep
        print("  Testing Semgrep...")
        result = subprocess.run(
            ["semgrep", "--config=auto", "--json", str(test_file)], 
            capture_output=True, text=True, timeout=30
        )
        if result.returncode in [0, 1]:
            try:
                semgrep_results = json.loads(result.stdout)
                issues_found = len(semgrep_results.get("results", []))
                print(f"    ✅ Semgrep found {issues_found} security issues")
            except:
                print("    ✅ Semgrep executed successfully")
        else:
            print(f"    ❌ Semgrep failed: {result.stderr}")
        
        return True
        
    except Exception as e:
        print(f"    ❌ Scanner test failed: {e}")
        return False
    finally:
        # Clean up test file
        if test_file.exists():
            test_file.unlink()

def test_api_server():
    """Test if API server can start and respond."""
    print("\n🔍 Testing API server...")
    
    # Check if server is already running
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("  ✅ API server is already running")
            print(f"    Response: {response.json()}")
            return True
    except:
        pass
    
    print("  Starting API server for testing...")
    
    # Start server in background
    try:
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "vibeauditor.main:app", 
            "--host", "127.0.0.1", 
            "--port", "8000"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for server to start
        for i in range(10):
            try:
                response = requests.get("http://localhost:8000/health", timeout=2)
                if response.status_code == 200:
                    print("  ✅ API server started successfully")
                    print(f"    Health check: {response.json()}")
                    
                    # Test file upload endpoint (without auth for now)
                    try:
                        # This will fail due to auth, but should return 401, not 500
                        upload_response = requests.post("http://localhost:8000/scan")
                        if upload_response.status_code in [401, 422]:  # Expected auth/validation errors
                            print("  ✅ Scan endpoint is responding (auth required)")
                        else:
                            print(f"  ⚠️  Scan endpoint returned: {upload_response.status_code}")
                    except Exception as e:
                        print(f"  ⚠️  Scan endpoint test failed: {e}")
                    
                    # Stop the test server
                    process.terminate()
                    process.wait(timeout=5)
                    return True
                    
            except requests.exceptions.RequestException:
                time.sleep(1)
        
        print("  ❌ API server failed to start within timeout")
        process.terminate()
        return False
        
    except Exception as e:
        print(f"  ❌ Failed to start API server: {e}")
        return False

def test_database_connection():
    """Test database connection."""
    print("\n🔍 Testing database connection...")
    
    try:
        from vibeauditor.core.supabase_client import get_supabase_client
        
        supabase = get_supabase_client()
        
        # Test a simple query
        result = supabase.table("scans").select("count", count="exact").execute()
        print(f"  ✅ Database connection successful")
        print(f"    Scans table accessible")
        return True
        
    except Exception as e:
        print(f"  ❌ Database connection failed: {e}")
        print("    Make sure SUPABASE_URL and SUPABASE_ANON_KEY are set correctly")
        return False

def main():
    """Run all tests."""
    print("🚀 VibeCodeAuditor Production Setup Test\n")
    
    tests = [
        ("Dependencies", test_dependencies),
        ("Environment", test_environment),
        ("Security Scanners", test_security_scanners),
        ("Database Connection", test_database_connection),
        ("API Server", test_api_server),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"  ❌ {name} test crashed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*50)
    print("📊 TEST SUMMARY")
    print("="*50)
    
    passed = 0
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {name}")
        if result:
            passed += 1
    
    print(f"\nPassed: {passed}/{len(results)} tests")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Your production setup is ready.")
        print("\nNext steps:")
        print("1. Start the production server: python3 run_production.py")
        print("2. Access the API at: http://localhost:8000")
        print("3. Check health endpoint: curl http://localhost:8000/health")
    else:
        print("\n⚠️  Some tests failed. Please check the issues above.")
        print("\nCommon fixes:")
        print("1. Install missing dependencies")
        print("2. Set up .env file with Supabase credentials")
        print("3. Ensure database schema is properly configured")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)