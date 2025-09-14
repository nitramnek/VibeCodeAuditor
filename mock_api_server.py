#!/usr/bin/env python3
"""
Mock API server for testing frontend integration
"""
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import uuid
from datetime import datetime

app = FastAPI(title="Mock VibeCodeAuditor API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Mock data
mock_scans = {}
mock_issues = {}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "environment": "development",
        "version": "1.0.0",
        "scanners_available": ["bandit", "semgrep", "eslint"]
    }

@app.post("/scan")
async def upload_and_scan(
    file: UploadFile = File(...),
    user_id: str = Form(...)
):
    """Mock upload and scan endpoint"""
    try:
        # Generate a mock scan ID
        scan_id = str(uuid.uuid4())
        
        # Read file content
        content = await file.read()
        
        # Create mock scan record
        mock_scans[scan_id] = {
            "id": scan_id,
            "user_id": user_id,
            "filename": file.filename,
            "status": "completed",
            "file_size": len(content),
            "created_at": datetime.now().isoformat(),
            "completed_at": datetime.now().isoformat(),
            "issues_count": 3
        }
        
        # Create mock issues
        mock_issues[scan_id] = [
            {
                "id": str(uuid.uuid4()),
                "scan_id": scan_id,
                "severity": "high",
                "issue_type": "security",
                "description": "Potential SQL injection vulnerability detected",
                "file_path": file.filename,
                "line_number": 42,
                "code_snippet": "SELECT * FROM users WHERE id = user_input_placeholder",
                "recommendation": "Use parameterized queries to prevent SQL injection"
            },
            {
                "id": str(uuid.uuid4()),
                "scan_id": scan_id,
                "severity": "medium",
                "issue_type": "security",
                "description": "Hardcoded API key found",
                "file_path": file.filename,
                "line_number": 15,
                "code_snippet": "API_KEY = 'sk-1234567890abcdef'",
                "recommendation": "Store API keys in environment variables"
            },
            {
                "id": str(uuid.uuid4()),
                "scan_id": scan_id,
                "severity": "low",
                "issue_type": "code_quality",
                "description": "Unused variable detected",
                "file_path": file.filename,
                "line_number": 28,
                "code_snippet": "unused_var = calculate_something()",
                "recommendation": "Remove unused variables to improve code quality"
            }
        ]
        
        print(f"✅ Mock scan created: {scan_id} for file: {file.filename}")
        
        # Prepare response with issues and summary to match frontend expectations
        response = {
            "scan_id": scan_id,
            "status": "completed",
            "message": "File uploaded and scanned successfully",
            "issues": mock_issues[scan_id],
            "summary": {
                "total_issues": len(mock_issues[scan_id]),
                "severity_breakdown": {
                    "high": 1,
                    "medium": 1,
                    "low": 1
                }
            },
            "compliance_summary": {},
            "detected_frameworks": {}
        }
        return response
        
    except Exception as e:
        print(f"❌ Mock scan error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/scan/{scan_id}")
async def get_scan_results(scan_id: str):
    """Mock get scan results endpoint"""
    try:
        if scan_id not in mock_scans:
            raise HTTPException(status_code=404, detail="Scan not found")
        
        scan = mock_scans[scan_id]
        issues = mock_issues.get(scan_id, [])
        
        # Create summary
        severity_counts = {}
        for issue in issues:
            severity = issue["severity"]
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        summary = {
            "total_issues": len(issues),
            "severity_breakdown": severity_counts,
            "scan_duration": "2.3s",
            "file_name": scan["filename"]
        }
        
        return {
            "scan_id": scan_id,
            "status": scan["status"],
            "issues": issues,
            "summary": summary
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error getting scan results: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/scans")
async def list_user_scans(user_id: str):
    """Mock list user scans endpoint"""
    try:
        user_scans = [scan for scan in mock_scans.values() if scan["user_id"] == user_id]
        return {"scans": user_scans}
    except Exception as e:
        print(f"❌ Error listing scans: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("🚀 Starting Mock VibeCodeAuditor API Server")
    print("📍 Server will be available at: http://localhost:8000")
    print("📚 Health check: http://localhost:8000/health")
    print("🔧 Press Ctrl+C to stop")
    print()
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )