"""
Enhanced FastAPI application with Supabase integration.
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import tempfile
import shutil
from pathlib import Path
import uuid
import asyncio
from datetime import datetime
import json
import os

from ..core.auditor import CodeAuditor
from ..core.config import AuditorConfig
from ..core.results import AuditResults, Issue, Severity
from .models import *
from .websocket import websocket_manager
from ..database.service import db_service
from ..database.supabase_client import supabase_client

# Initialize FastAPI app
app = FastAPI(
    title="VibeCodeAuditor API",
    description="Enterprise security auditing API with Supabase integration",
    version="0.2.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware for PWA
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication setup
security = HTTPBearer(auto_error=False)

async def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)):
    """Verify JWT token and get current user."""
    if not credentials:
        return None
    
    if not supabase_client.is_available():
        # If Supabase is not configured, allow anonymous access for development
        return {"id": "anonymous", "email": "anonymous@example.com"}
    
    try:
        client = supabase_client.get_client()
        user_response = client.auth.get_user(credentials.credentials)
        
        if user_response.user:
            return user_response.user
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

async def get_authenticated_user(current_user = Depends(get_current_user)):
    """Require authentication."""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    return current_user

# Store active scan sessions (fallback if database not available)
active_scans: Dict[str, Dict[str, Any]] = {}

@app.get("/")
async def root():
    """Root endpoint - serves PWA."""
    return {
        "message": "VibeCodeAuditor API", 
        "version": "0.2.0",
        "database_available": db_service.is_available(),
        "supabase_configured": supabase_client.is_available()
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy", 
        "timestamp": datetime.utcnow(),
        "database": "connected" if db_service.is_available() else "unavailable",
        "supabase": "configured" if supabase_client.is_available() else "not_configured"
    }

@app.post("/api/scan/upload", response_model=ScanResponse)
async def upload_and_scan(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...),
    config: Optional[str] = None,
    current_user = Depends(get_current_user)
):
    """Upload files and start scanning with optional authentication."""
    
    # Generate scan ID
    if db_service.is_available() and current_user:
        # Create scan in database
        scan_id = db_service.create_scan(
            user_id=current_user.id,
            name=f"Scan {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}",
            config=json.loads(config) if config else {}
        )
        if not scan_id:
            raise HTTPException(status_code=500, detail="Failed to create scan in database")
        scan_id_str = str(scan_id)
    else:
        # Fallback to in-memory storage
        scan_id_str = str(uuid.uuid4())
    
    # Create temporary directory for uploaded files
    temp_dir = Path(tempfile.mkdtemp(prefix=f"vibeaudit_{scan_id_str}_"))
    
    try:
        # Save uploaded files
        for file in files:
            file_path = temp_dir / file.filename
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        
        # Parse config if provided
        auditor_config = AuditorConfig()
        if config:
            try:
                config_data = json.loads(config)
                # Apply config settings to auditor_config if needed
            except json.JSONDecodeError:
                pass
        
        # Store scan info
        scan_info = {
            "status": "started",
            "temp_dir": temp_dir,
            "start_time": datetime.utcnow(),
            "progress": 0,
            "user_id": current_user.id if current_user else "anonymous"
        }
        
        if db_service.is_available():
            # Update database
            db_service.update_scan_status(int(scan_id_str), "running")
        else:
            # Store in memory
            active_scans[scan_id_str] = scan_info
        
        # Start background scan
        background_tasks.add_task(run_enhanced_scan_task, scan_id_str, temp_dir, auditor_config, current_user)
        
        return ScanResponse(
            scan_id=scan_id_str,
            status="started",
            message="Scan initiated successfully"
        )
        
    except Exception as e:
        # Cleanup on error
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/scan/{scan_id}/status", response_model=ScanStatusResponse)
async def get_scan_status(scan_id: str, current_user = Depends(get_current_user)):
    """Get scan status and progress."""
    
    if db_service.is_available():
        # Get from database
        try:
            scan_id_int = int(scan_id)
            user_id = current_user.id if current_user else None
            results = db_service.get_scan_results(scan_id_int, user_id) if user_id else None
            
            if results:
                scan = results['scan']
                return ScanStatusResponse(
                    scan_id=scan_id,
                    status=scan['status'],
                    progress=scan.get('progress', 0),
                    start_time=datetime.fromisoformat(scan['started_at']) if scan.get('started_at') else datetime.utcnow(),
                    end_time=datetime.fromisoformat(scan['completed_at']) if scan.get('completed_at') else None,
                    message=scan.get('name', '')
                )
        except (ValueError, TypeError):
            pass
    
    # Fallback to in-memory storage
    if scan_id not in active_scans:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    scan_info = active_scans[scan_id]
    return ScanStatusResponse(
        scan_id=scan_id,
        status=scan_info["status"],
        progress=scan_info.get("progress", 0),
        start_time=scan_info["start_time"],
        end_time=scan_info.get("end_time"),
        message=scan_info.get("message", "")
    )

@app.get("/api/scan/{scan_id}/results", response_model=ScanResultsResponse)
async def get_scan_results(scan_id: str, current_user = Depends(get_current_user)):
    """Get scan results."""
    
    if db_service.is_available():
        # Get from database
        try:
            scan_id_int = int(scan_id)
            user_id = current_user.id if current_user else None
            results = db_service.get_scan_results(scan_id_int, user_id) if user_id else None
            
            if results:
                scan = results['scan']
                issues = results['issues']
                
                # Convert issues to IssueModel
                issue_models = []
                for issue_data in issues:
                    issue_models.append(IssueModel(
                        rule_id=issue_data['rule_id'],
                        severity=SeverityModel(issue_data['severity']),
                        message=issue_data['message'],
                        file_path=issue_data['file_path'],
                        line_number=issue_data.get('line_number'),
                        column_number=issue_data.get('column_number'),
                        code_snippet=issue_data.get('code_snippet'),
                        remediation=issue_data.get('remediation'),
                        category=issue_data.get('category', 'general'),
                        confidence=issue_data.get('confidence', 1.0),
                        metadata=issue_data.get('metadata', {}),
                        standards=[StandardModel(**std) if isinstance(std, dict) else StandardModel(id='', name=str(std), type='', url='') for std in issue_data.get('standards', [])],
                        compliance_frameworks=issue_data.get('compliance_frameworks', [])
                    ))
                
                return ScanResultsResponse(
                    scan_id=scan_id,
                    summary=scan.get('summary', {}),
                    issues=issue_models,
                    errors={},
                    detected_frameworks=scan.get('detected_frameworks', {}),
                    compliance_summary=scan.get('compliance_summary', {})
                )
        except (ValueError, TypeError):
            pass
    
    # Fallback to in-memory storage
    if scan_id not in active_scans:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    scan_info = active_scans[scan_id]
    if scan_info["status"] != "completed":
        raise HTTPException(status_code=400, detail="Scan not completed yet")
    
    results = scan_info.get("results")
    if not results:
        raise HTTPException(status_code=500, detail="Results not available")
    
    return ScanResultsResponse(
        scan_id=scan_id,
        summary=results.get_summary(),
        issues=[IssueModel.from_issue(issue) for issue in results.issues],
        errors={},
        detected_frameworks=getattr(results, 'detected_frameworks', {}),
        compliance_summary=getattr(results, 'compliance_summary', {})
    )

@app.get("/api/scans")
async def get_user_scans(current_user = Depends(get_authenticated_user)):
    """Get user's scan history."""
    if db_service.is_available():
        scans = db_service.get_user_scans(current_user.id)
        return scans
    else:
        # Return empty list if database not available
        return []

@app.delete("/api/scan/{scan_id}")
async def cleanup_scan(scan_id: str, current_user = Depends(get_current_user)):
    """Cleanup scan resources."""
    
    # Clean up from database if available
    if db_service.is_available():
        # Database cleanup would be handled by CASCADE DELETE
        pass
    
    # Clean up from memory
    if scan_id in active_scans:
        scan_info = active_scans[scan_id]
        temp_dir = scan_info.get("temp_dir")
        
        if temp_dir and temp_dir.exists():
            shutil.rmtree(temp_dir, ignore_errors=True)
        
        del active_scans[scan_id]
    
    return {"message": "Scan cleaned up successfully"}

async def run_enhanced_scan_task(scan_id: str, target_path: Path, config: AuditorConfig, current_user):
    """Enhanced background task to run the actual scan with database integration."""
    try:
        # Update status
        if db_service.is_available():
            db_service.update_scan_status(int(scan_id), "running")
        else:
            active_scans[scan_id]["status"] = "running"
        
        await websocket_manager.send_scan_update(scan_id, "running", 0)
        
        # Initialize auditor
        auditor = CodeAuditor(config)
        
        # Run scan with progress updates
        results = await run_scan_with_progress(auditor, target_path, scan_id)
        
        # Store results
        if db_service.is_available():
            # Save to database
            scan_id_int = int(scan_id)
            db_service.save_issues(scan_id_int, results.issues)
            db_service.update_scan_status(
                scan_id_int,
                "completed",
                summary=results.get_summary(),
                compliance_summary=getattr(results, 'compliance_summary', {}),
                detected_frameworks=getattr(results, 'detected_frameworks', {})
            )
            
            # Log audit event
            if current_user:
                db_service.log_audit_event(
                    user_id=current_user.id,
                    action="scan_completed",
                    resource_type="scan",
                    resource_id=scan_id_int,
                    details={"total_issues": len(results.issues)}
                )
        else:
            # Store in memory
            active_scans[scan_id].update({
                "status": "completed",
                "end_time": datetime.utcnow(),
                "results": results,
                "progress": 100
            })
        
        await websocket_manager.send_scan_update(scan_id, "completed", 100)
        
    except Exception as e:
        # Handle errors
        if db_service.is_available():
            db_service.update_scan_status(int(scan_id), "failed")
        else:
            active_scans[scan_id].update({
                "status": "failed",
                "end_time": datetime.utcnow(),
                "message": str(e),
                "progress": 0
            })
        
        await websocket_manager.send_scan_update(scan_id, "failed", 0, str(e))
    finally:
        # Cleanup temp directory
        shutil.rmtree(target_path, ignore_errors=True)

async def run_scan_with_progress(auditor: CodeAuditor, target_path: Path, scan_id: str) -> AuditResults:
    """Run scan with progress updates via WebSocket."""
    # Use the existing scan logic from your auditor
    results = auditor.scan(target_path)
    return results

# Include WebSocket endpoint
from .websocket import websocket_endpoint
app.add_websocket_route("/ws/{scan_id}", websocket_endpoint)