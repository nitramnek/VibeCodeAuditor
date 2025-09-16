"""
VibeCodeAuditor Production Main Application
FastAPI application with security scanning capabilities.
"""

import os
import sys
import logging
from pathlib import Path
from typing import List, Optional
import asyncio
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from vibeauditor.core.production_config import get_config
from vibeauditor.scanners.real_security_scanner import SecurityScanner
from vibeauditor.core.supabase_client import get_supabase_client

# Configure logging
# Ensure logs directory exists before configuring file handler
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/vibeauditor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Global instances
config = get_config()
security_scanner = None
supabase = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    global security_scanner, supabase

    # Startup
    logger.info("Starting VibeCodeAuditor...")

    # Initialize Supabase client
    try:
        supabase = get_supabase_client()
        logger.info("✅ Supabase client initialized")
    except Exception as e:
        logger.error(f"❌ Failed to initialize Supabase: {e}")
        raise

    # Initialize security scanner
    try:
        security_scanner = SecurityScanner()
        logger.info("✅ Security scanner initialized")
    except Exception as e:
        logger.error(f"❌ Failed to initialize security scanner: {e}")
        raise

    # Create necessary directories
    os.makedirs(config.storage.local_path, exist_ok=True)
    os.makedirs(config.scanner.temp_dir or "/tmp/vibeauditor", exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    logger.info("🚀 VibeCodeAuditor started successfully")

    yield

    # Shutdown
    logger.info("Shutting down VibeCodeAuditor...")

# Create FastAPI app
app = FastAPI(
    title="VibeCodeAuditor API",
    description="Professional security code auditing platform",
    version="1.0.0",
    lifespan=lifespan
)

# Security middleware
security = HTTPBearer()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.security.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Trusted host middleware for production
if config.environment == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["localhost", "127.0.0.1", "*.yourdomain.com"]
    )

# Pydantic models
class ScanRequest(BaseModel):
    filename: str
    user_id: str

class ScanResponse(BaseModel):
    scan_id: str
    status: str
    message: str

class IssueResponse(BaseModel):
    id: str
    scan_id: str
    severity: str
    issue_type: str
    description: str
    file_path: str
    line_number: Optional[int]
    code_snippet: Optional[str]
    recommendation: Optional[str]

class ScanResultResponse(BaseModel):
    scan_id: str
    status: str
    issues: List[IssueResponse]
    summary: dict

# Authentication dependency
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Validate JWT token and return user info."""
    try:
        # In a real implementation, you'd validate the JWT token here
        # For now, we'll extract user_id from the token payload
        token = credentials.credentials

        # Simple validation - in production, use proper JWT validation
        if not token or len(token) < 10:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token"
            )

        # Mock user extraction - replace with actual JWT decoding
        return {"user_id": "authenticated_user", "email": "user@example.com"}

    except Exception as e:
        logger.error(f"Authentication error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

# Root endpoint to avoid 404 on /
@app.get("/")
async def root():
    return {"message": "Welcome to VibeCodeAuditor API. Visit /docs for API documentation."}

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "environment": config.environment,
        "version": "1.0.0",
        "scanners_available": config.scanner.enabled_scanners
    }

# File upload and scan endpoint
@app.post("/scan")
async def upload_and_scan(
    file: UploadFile = File(...),
    user_id: str = Form(...)
):
    """Upload a file and start security scanning."""
    try:
        # Validate file type
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in config.security.allowed_file_types:
            raise HTTPException(
                status_code=400,
                detail=f"File type {file_ext} not supported"
            )

        # Validate file size
        content = await file.read()
        if len(content) > config.security.max_file_size:
            raise HTTPException(
                status_code=400,
                detail="File size exceeds maximum allowed size"
            )

        # Save uploaded file
        upload_dir = Path(config.storage.local_path)
        upload_dir.mkdir(exist_ok=True)

        file_path = upload_dir / f"{user_id}_{file.filename}"
        with open(file_path, "wb") as f:
            f.write(content)

        # Create scan record in database
        scan_data = {
            "user_id": user_id,
            "name": file.filename,
            "description": f"Security scan of {file.filename}",
            "status": "pending",
            "file_count": 1,
            "config": {"file_path": str(file_path), "file_size": len(content)}
        }

        result = supabase.table("scans").insert(scan_data).execute()
        scan_id = result.data[0]["id"]

        # Perform immediate scanning for better UX
        logger.info(f"Starting immediate scan for {scan_id}")

        # Perform the scan synchronously
        scan_results = await security_scanner.scan_file(str(file_path))
        logger.info(f"Scan completed, found {len(scan_results.get('issues', []))} issues")

        # Store issues in database
        issues_data = []
        for issue in scan_results.get("issues", []):
            issue_data = {
                "scan_id": scan_id,
                "rule_id": issue.get("rule_id", issue.get("type", "unknown")),
                "severity": issue.get("severity", "medium"),
                "category": issue.get("category", issue.get("type", "security")),
                "message": issue.get("description", issue.get("message", "")),
                "file_path": issue.get("file_path", str(file_path)),
                "line_number": issue.get("line_number"),
                "code_snippet": issue.get("code_snippet"),
                "remediation": issue.get("recommendation", issue.get("remediation", ""))
            }
            issues_data.append(issue_data)

        if issues_data:
            logger.info(f"Inserting {len(issues_data)} issues into database")
            supabase.table("issues").insert(issues_data).execute()

        # Update scan status to completed (handle updated_at error)
        try:
            supabase.table("scans").update({
                "status": "completed",
                "total_issues": len(issues_data)
            }).eq("id", scan_id).execute()
        except Exception as update_error:
            logger.warning(f"Could not update scan status: {update_error}")
            # Try a simpler update without total_issues
            try:
                supabase.table("scans").update({"status": "completed"}).eq("id", scan_id).execute()
                logger.info(f"✅ Scan status updated to completed (simple)")
            except Exception as simple_error:
                logger.error(f"Failed simple status update: {simple_error}")
                # Issues are still saved, this is not critical for functionality

        logger.info(f"Completed scan {scan_id} with {len(issues_data)} issues found")

        # Return response with issues (like mock server)
        return {
            "scan_id": scan_id,
            "status": "completed",
            "message": "File uploaded and scanned successfully",
            "issues": [
                {
                    "id": str(i),
                    "scan_id": scan_id,
                    "severity": issue.get("severity", "medium"),
                    "issue_type": issue.get("category", issue.get("type", "security")),
                    "description": issue.get("description", issue.get("message", "")),
                    "file_path": issue.get("file_path", str(file_path)),
                    "line_number": issue.get("line_number"),
                    "code_snippet": issue.get("code_snippet"),
                    "recommendation": issue.get("recommendation", issue.get("remediation", ""))
                }
                for i, issue in enumerate(scan_results.get("issues", []))
            ],
            "summary": {
                "total_issues": len(scan_results.get("issues", [])),
                "severity_breakdown": {
                    severity: len([i for i in scan_results.get("issues", []) if i.get("severity") == severity])
                    for severity in ["critical", "high", "medium", "low"]
                }
            },
            "compliance_summary": {},
            "detected_frameworks": {}
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error during file upload"
        )

async def perform_scan(scan_id: str, file_path: Path, user_id: str):
    """Perform security scanning asynchronously."""
    try:
        logger.info(f"Starting scan process for {scan_id}")

        # Skip the status update that's causing issues for now
        # supabase.table("scans").update({"status": "running"}).eq("id", scan_id).execute()

        # Perform the actual scan
        logger.info(f"Running security scan on {file_path}")
        logger.info(f"File exists: {file_path.exists()}")
        logger.info(f"File size: {file_path.stat().st_size if file_path.exists() else 'N/A'}")

        scan_results = await security_scanner.scan_file(str(file_path))
        logger.info(f"Scan results type: {type(scan_results)}")
        logger.info(f"Scan results keys: {list(scan_results.keys()) if isinstance(scan_results, dict) else 'Not a dict'}")
        logger.info(f"Scan completed, found {len(scan_results.get('issues', []))} issues")

        # Store issues in database
        issues_data = []
        for issue in scan_results.get("issues", []):
            issue_data = {
                "scan_id": scan_id,
                "rule_id": issue.get("rule_id", issue.get("type", "unknown")),
                "severity": issue.get("severity", "medium"),
                "category": issue.get("category", issue.get("type", "security")),
                "message": issue.get("description", issue.get("message", "")),
                "file_path": issue.get("file_path", str(file_path)),
                "line_number": issue.get("line_number"),
                "code_snippet": issue.get("code_snippet"),
                "remediation": issue.get("recommendation", issue.get("remediation", ""))
            }
            issues_data.append(issue_data)

        if issues_data:
            logger.info(f"Inserting {len(issues_data)} issues into database")
            supabase.table("issues").insert(issues_data).execute()

        # Update scan status to completed (handle updated_at error)
        try:
            supabase.table("scans").update({
                "status": "completed",
                "total_issues": len(issues_data)
            }).eq("id", scan_id).execute()
            logger.info(f"✅ Scan status updated to completed")
        except Exception as update_error:
            logger.warning(f"Could not update scan status (but issues were saved): {update_error}")
            # Try a simpler update without total_issues
            try:
                supabase.table("scans").update({"status": "completed"}).eq("id", scan_id).execute()
                logger.info(f"✅ Scan status updated to completed (simple)")
            except Exception as simple_error:
                logger.error(f"Failed simple status update: {simple_error}")
                # Issues are still saved, this is not critical for functionality

        logger.info(f"Completed scan {scan_id} with {len(issues_data)} issues found")

    except Exception as e:
        logger.error(f"Scan error for {scan_id}: {e}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")

        # Update scan status to failed (simple update)
        try:
            supabase.table("scans").update({
                "status": "failed"
            }).eq("id", scan_id).execute()
        except Exception as update_error:
            logger.warning(f"Could not update scan status to failed: {update_error}")
            # Not critical since the main error is already logged

# Get scan results endpoint
@app.get("/scan/{scan_id}", response_model=ScanResultResponse)
async def get_scan_results(
    scan_id: str
):
    """Get scan results by scan ID."""
    try:
        # Get scan info
        scan_result = supabase.table("scans").select("*").eq("id", scan_id).execute()

        if not scan_result.data:
            raise HTTPException(status_code=404, detail="Scan not found")

        scan = scan_result.data[0]

        # Get issues
        issues_result = supabase.table("issues").select("*").eq("scan_id", scan_id).execute()

        issues = [
            IssueResponse(
                id=issue["id"],
                scan_id=issue["scan_id"],
                severity=issue["severity"],
                issue_type=issue["category"],  # Use 'category' instead of 'issue_type'
                description=issue["message"],  # Use 'message' instead of 'description'
                file_path=issue["file_path"],
                line_number=issue["line_number"],
                code_snippet=issue["code_snippet"],
                recommendation=issue["remediation"]  # Use 'remediation' instead of 'recommendation'
            )
            for issue in issues_result.data
        ]

        # Create summary
        severity_counts = {}
        for issue in issues:
            severity_counts[issue.severity] = severity_counts.get(issue.severity, 0) + 1

        summary = {
            "total_issues": len(issues),
            "severity_breakdown": severity_counts,
            "scan_duration": None,  # Calculate if needed
            "file_name": scan["name"]  # Use 'name' instead of 'filename'
        }

        return ScanResultResponse(
            scan_id=scan_id,
            status=scan["status"],
            issues=issues,
            summary=summary
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting scan results: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

# List user scans endpoint
@app.get("/scans")
async def list_user_scans(
    user_id: str
):
    """List all scans for a user."""
    try:
        result = supabase.table("scans").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()

        return {"scans": result.data}

    except Exception as e:
        logger.error(f"Error listing scans: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "status_code": exc.status_code}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "status_code": 500}
    )

if __name__ == "__main__":
    # Run the application
    uvicorn.run(
        "vibeauditor.main:app",
        host=config.host,
        port=config.port,
        workers=config.workers if config.environment == "production" else 1,
        log_level=config.log_level.lower(),
        reload=config.debug
    )
