#!/usr/bin/env python3
"""
Simple mock backend server for testing VibeCodeAuditor database fixes.
This will simulate the backend API responses while we test the database integration.
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uuid
from datetime import datetime

app = FastAPI(title="VibeCodeAuditor Mock API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@app.post("/api/scan/upload")
async def upload_and_scan(files: List[UploadFile] = File(...)):
    """Mock upload and scan endpoint."""
    print(f"📁 Received {len(files)} files for scanning")
    
    # Generate a unique scan ID
    scan_id = str(uuid.uuid4())
    
    # Mock scan results with realistic security issues
    mock_response = {
        "scan_id": scan_id,
        "status": "completed",
        "message": "Scan completed successfully",
        "summary": {
            "total_issues": 3,
            "critical": 1,
            "high": 1,
            "medium": 1,
            "low": 0,
            "files_scanned": len(files)
        },
        "compliance_summary": {
            "ISO 27001": {"name": "ISO 27001", "count": 2},
            "OWASP": {"name": "OWASP Top 10", "count": 2},
            "GDPR": {"name": "GDPR", "count": 1}
        },
        "detected_frameworks": {
            "javascript": {
                "name": "JavaScript",
                "type": "language",
                "confidence": 0.95,
                "files": [f.filename for f in files if f.filename.endswith('.js')]
            }
        },
        "issues": [
            {
                "title": "Hardcoded API Key Detected",
                "description": "A hardcoded API key was found in the source code. This poses a security risk.",
                "severity": "critical",
                "type": "security",
                "file": files[0].filename if files else "test.js",
                "line": 15,
                "recommendation": "Move API keys to environment variables or secure configuration files."
            },
            {
                "title": "SQL Injection Vulnerability",
                "description": "Potential SQL injection vulnerability detected in database query.",
                "severity": "high", 
                "type": "security",
                "file": files[0].filename if files else "test.js",
                "line": 42,
                "recommendation": "Use parameterized queries or prepared statements to prevent SQL injection."
            },
            {
                "title": "Missing Input Validation",
                "description": "User input is not properly validated before processing.",
                "severity": "medium",
                "type": "security", 
                "file": files[0].filename if files else "test.js",
                "line": 28,
                "recommendation": "Implement proper input validation and sanitization."
            }
        ]
    }
    
    print(f"✅ Mock scan completed for scan ID: {scan_id}")
    return mock_response

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Mock VibeCodeAuditor Backend")
    print("📍 Server will run on: http://localhost:8000")
    print("🔗 Frontend should connect automatically")
    print("📚 API docs available at: http://localhost:8000/docs")
    print()
    
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")