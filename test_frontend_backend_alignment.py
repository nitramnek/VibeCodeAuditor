#!/usr/bin/env python3
"""
Test script to verify frontend-backend alignment for scan results
"""

import requests
import json
import time
import subprocess
import sys
from pathlib import Path

def start_mock_server():
    """Start the mock API server"""
    print("🚀 Starting mock API server...")
    try:
        # Start server in background
        process = subprocess.Popen([
            sys.executable, "mock_api_server.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for server to start
        time.sleep(3)
        
        # Test health endpoint
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Mock API server is running")
            return process
        else:
            print("❌ Server health check failed")
            return None
            
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return None

def test_scan_endpoint():
    """Test the scan endpoint with a sample file"""
    print("\n📁 Testing scan endpoint...")
    
    # Create a test file
    test_content = """
// Test JavaScript file with security issues
const express = require('express');
const app = express();

// Hardcoded secret (security issue)
const JWT_SECRET = 'supersecretkey123';

// SQL injection vulnerability
app.get('/user/:id', (req, res) => {
    const query = `SELECT * FROM users WHERE id = ${req.params.id}`;
    // This is vulnerable to SQL injection
    db.query(query, (err, results) => {
        if (err) {
            res.status(500).json({ error: err.message, stack: err.stack });
        } else {
            res.json(results);
        }
    });
});

app.listen(3000);
"""
    
    try:
        # Prepare the file upload
        files = {
            'file': ('test.js', test_content, 'application/javascript')
        }
        data = {
            'user_id': 'test-user-123'
        }
        
        # Send request to scan endpoint
        print("📤 Uploading test file...")
        response = requests.post(
            "http://localhost:8000/scan",
            files=files,
            data=data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Scan completed successfully!")
            print(f"📊 Scan ID: {result.get('scan_id')}")
            print(f"📊 Status: {result.get('status')}")
            print(f"📊 Issues found: {len(result.get('issues', []))}")
            
            # Print issues details
            issues = result.get('issues', [])
            if issues:
                print("\n🔍 Issues found:")
                for i, issue in enumerate(issues, 1):
                    print(f"  {i}. {issue.get('severity', 'unknown').upper()}: {issue.get('description', 'No description')}")
                    print(f"     Line {issue.get('line_number', 'unknown')}: {issue.get('code_snippet', 'No snippet')}")
                    print(f"     Fix: {issue.get('recommendation', 'No recommendation')}")
                    print()
            
            return result
        else:
            print(f"❌ Scan failed: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error testing scan endpoint: {e}")
        return None

def test_get_results(scan_id):
    """Test getting scan results"""
    print(f"\n📋 Testing get results for scan: {scan_id}")
    
    try:
        response = requests.get(f"http://localhost:8000/scan/{scan_id}", timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Successfully retrieved scan results!")
            print(f"📊 Issues: {len(result.get('issues', []))}")
            return result
        else:
            print(f"❌ Failed to get results: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error getting results: {e}")
        return None

def main():
    """Main test function"""
    print("🧪 Testing Frontend-Backend Alignment")
    print("=" * 50)
    
    # Start mock server
    server_process = start_mock_server()
    if not server_process:
        print("❌ Cannot start server, exiting")
        return
    
    try:
        # Test scan endpoint
        scan_result = test_scan_endpoint()
        if not scan_result:
            print("❌ Scan test failed")
            return
        
        # Test get results
        scan_id = scan_result.get('scan_id')
        if scan_id:
            get_result = test_get_results(scan_id)
            if get_result:
                print("\n✅ All tests passed!")
                print("\n📋 Summary:")
                print(f"   - Mock server: Running on port 8000")
                print(f"   - Scan endpoint: Working (/scan)")
                print(f"   - Results endpoint: Working (/scan/{scan_id})")
                print(f"   - Issues detected: {len(get_result.get('issues', []))}")
                print("\n🎯 Frontend should now be able to:")
                print("   1. Upload files to /scan")
                print("   2. Receive scan_id and issues in response")
                print("   3. Store scan data in Supabase")
                print("   4. Display issues in Results page")
            else:
                print("❌ Get results test failed")
        else:
            print("❌ No scan ID returned")
            
    finally:
        # Cleanup
        if server_process:
            print("\n🧹 Cleaning up...")
            server_process.terminate()
            server_process.wait()
            print("✅ Server stopped")

if __name__ == "__main__":
    main()