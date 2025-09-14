#!/usr/bin/env python3
"""
Complete test of the frontend-backend alignment
"""

import subprocess
import sys
import time
import requests
import json
import os
from pathlib import Path

def start_mock_server():
    """Start the mock API server"""
    print("🚀 Starting mock API server...")
    try:
        # Kill any existing processes on port 8000
        try:
            subprocess.run(["pkill", "-f", "mock_api_server.py"], check=False)
        except:
            pass
        
        # Start server
        process = subprocess.Popen([
            sys.executable, "mock_api_server.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for server to start
        time.sleep(3)
        
        # Test health endpoint
        for attempt in range(5):
            try:
                response = requests.get("http://localhost:8000/health", timeout=2)
                if response.status_code == 200:
                    print("✅ Mock API server is running")
                    print(f"📊 Health check response: {response.json()}")
                    return process
            except:
                time.sleep(1)
        
        print("❌ Server health check failed")
        return None
            
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return None

def test_upload_endpoint():
    """Test the upload endpoint"""
    print("\n📤 Testing upload endpoint...")
    
    # Create test file content
    test_content = """
// Test JavaScript file with security issues
const express = require('express');
const app = express();

// Hardcoded secret (security issue)
const JWT_SECRET = 'supersecretkey123';

// SQL injection vulnerability
app.get('/user/:id', (req, res) => {
    const query = \`SELECT * FROM users WHERE id = \${req.params.id}\`;
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
        
        print("📤 Uploading test file...")
        response = requests.post(
            "http://localhost:8000/scan",
            files=files,
            data=data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Upload successful!")
            print(f"📊 Response structure:")
            print(f"   - scan_id: {result.get('scan_id')}")
            print(f"   - status: {result.get('status')}")
            print(f"   - message: {result.get('message')}")
            print(f"   - issues count: {len(result.get('issues', []))}")
            
            # Validate response structure
            required_fields = ['scan_id', 'status', 'issues']
            missing_fields = [field for field in required_fields if field not in result]
            
            if missing_fields:
                print(f"❌ Missing required fields: {missing_fields}")
                return None
            
            # Check issues structure
            issues = result.get('issues', [])
            if issues:
                print(f"\n🔍 Issues found ({len(issues)}):")
                for i, issue in enumerate(issues, 1):
                    print(f"   {i}. {issue.get('severity', 'unknown').upper()}: {issue.get('description', 'No description')}")
                    if 'line_number' in issue:
                        print(f"      Line {issue['line_number']}: {issue.get('code_snippet', 'No snippet')}")
                    if 'recommendation' in issue:
                        print(f"      Fix: {issue['recommendation']}")
                    print()
            
            return result
        else:
            print(f"❌ Upload failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error testing upload: {e}")
        return None

def check_frontend_build():
    """Check if frontend is built"""
    build_path = Path("webapp/build")
    if build_path.exists():
        print("✅ Frontend build exists")
        return True
    else:
        print("❌ Frontend build not found")
        print("Run: cd webapp && npm run build")
        return False

def main():
    """Main test function"""
    print("🧪 Complete Frontend-Backend Alignment Test")
    print("=" * 60)
    
    # Check frontend build
    if not check_frontend_build():
        print("\n🔧 Building frontend...")
        try:
            subprocess.run(["npm", "run", "build"], cwd="webapp", check=True)
            print("✅ Frontend built successfully")
        except:
            print("❌ Frontend build failed")
            return
    
    # Start mock server
    server_process = start_mock_server()
    if not server_process:
        print("❌ Cannot start server, exiting")
        return
    
    try:
        # Test upload endpoint
        upload_result = test_upload_endpoint()
        if not upload_result:
            print("❌ Upload test failed")
            return
        
        print("\n✅ All backend tests passed!")
        print("\n📋 Test Summary:")
        print(f"   ✅ Mock server: Running on http://localhost:8000")
        print(f"   ✅ Upload endpoint: Working (/scan)")
        print(f"   ✅ Response format: Valid")
        print(f"   ✅ Issues detected: {len(upload_result.get('issues', []))}")
        print(f"   ✅ Frontend build: Ready")
        
        print("\n🎯 Next Steps:")
        print("1. Start the React app:")
        print("   cd webapp && npm start")
        print("2. Go to http://localhost:3000")
        print("3. Upload a test file")
        print("4. Check console logs for:")
        print("   - 'Backend response: {scan_id: ..., issues: [...]}'")
        print("   - 'Inserted scan: {...}'")
        print("   - 'Inserted X issues for scan: ...'")
        print("5. Verify Results page shows the issues")
        
        print("\n🔍 Expected Console Output:")
        print("Backend response: {scan_id: 'abc-123', issues: [3 issues]}")
        print("Backend scan ID: abc-123")
        print("Number of issues: 3")
        print("Inserted scan: {id: 'def-456', total_issues: 3}")
        print("Inserted 3 issues for scan: def-456")
        
        print("\n📊 Expected Issues on Results Page:")
        for i, issue in enumerate(upload_result.get('issues', []), 1):
            severity = issue.get('severity', 'unknown').upper()
            desc = issue.get('description', 'No description')
            print(f"{i}. {severity}: {desc}")
        
        print(f"\n🌐 Keep this server running and test at:")
        print(f"   Frontend: http://localhost:3000")
        print(f"   Backend:  http://localhost:8000")
        print(f"\nPress Ctrl+C to stop the server...")
        
        # Keep server running
        server_process.wait()
        
    except KeyboardInterrupt:
        print("\n👋 Stopping server...")
    finally:
        if server_process:
            server_process.terminate()
            server_process.wait()
            print("✅ Server stopped")

if __name__ == "__main__":
    main()