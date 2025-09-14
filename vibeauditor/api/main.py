"""
Main FastAPI application for VibeCodeAuditor PWA.
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import tempfile
import shutil
from pathlib import Path
import uuid
import asyncio
from datetime import datetime

from ..core.auditor import CodeAuditor
from ..core.config import AuditorConfig
from ..core.results import AuditResults, Issue, Severity
from ..scanners.real_security_scanner import SecurityScanner
from .models import *
from .websocket import websocket_manager

# Initialize FastAPI app
app = FastAPI(
    title="VibeCodeAuditor API",
    description="Comprehensive code auditing API for AI developers",
    version="0.1.0",
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

# Store active scan sessions
active_scans: Dict[str, Dict[str, Any]] = {}

@app.get("/")
async def root():
    """Root endpoint - serves PWA."""
    return {"message": "VibeCodeAuditor API", "version": "0.1.0"}

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@app.post("/api/scan/upload", response_model=ScanResponse)
async def upload_and_scan(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...),
    config: Optional[str] = None
):
    """Upload files and start scanning."""
    scan_id = str(uuid.uuid4())
    
    # Create temporary directory for uploaded files
    temp_dir = Path(tempfile.mkdtemp(prefix=f"vibeaudit_{scan_id}_"))
    
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
            # Parse JSON config from request
            import json
            config_data = json.loads(config)
            auditor_config = AuditorConfig(**config_data)
        
        # Start background scan
        active_scans[scan_id] = {
            "status": "started",
            "temp_dir": temp_dir,
            "start_time": datetime.utcnow(),
            "progress": 0
        }
        
        background_tasks.add_task(run_scan_task, scan_id, temp_dir, auditor_config)
        
        return ScanResponse(
            scan_id=scan_id,
            status="started",
            message="Scan initiated successfully"
        )
        
    except Exception as e:
        # Cleanup on error
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/scan/{scan_id}/status", response_model=ScanStatusResponse)
async def get_scan_status(scan_id: str):
    """Get scan status and progress."""
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
async def get_scan_results(scan_id: str):
    """Get scan results."""
    if scan_id not in active_scans:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    scan_info = active_scans[scan_id]
    if scan_info["status"] != "completed":
        raise HTTPException(status_code=400, detail="Scan not completed yet")
    
    results = scan_info.get("results")
    if not results:
        raise HTTPException(status_code=500, detail="Results not available")
    
    # Convert framework information
    frameworks = {}
    if hasattr(results, 'detected_frameworks'):
        for name, framework in results.detected_frameworks.items():
            frameworks[name] = FrameworkModel(
                name=framework.name,
                type=framework.type.value if hasattr(framework.type, 'value') else str(framework.type),
                confidence=framework.confidence,
                files=[str(f) for f in framework.files]
            )
    
    return ScanResultsResponse(
        scan_id=scan_id,
        summary=results.get_summary(),
        issues=[IssueModel.from_issue(issue) for issue in results.issues],
        errors=results.errors,
        detected_frameworks=frameworks,
        compliance_summary=getattr(results, 'compliance_summary', {})
    )

@app.get("/api/scan/demo-scan-123/results")
async def get_demo_scan_results():
    """Return demo scan results for testing the enhanced UI."""
    
    demo_results = {
        "scan_id": "demo-scan-123",
        "summary": {
            "total_issues": 5,
            "critical": 2,
            "high": 2,
            "medium": 1,
            "low": 0,
            "files_scanned": 3,
            "files_with_errors": 0
        },
        "compliance_summary": {
            "ISO 27001": {"name": "ISO 27001", "count": 4},
            "OWASP": {"name": "OWASP Top 10", "count": 3},
            "GDPR": {"name": "GDPR", "count": 2},
            "PCI DSS": {"name": "PCI DSS", "count": 2},
            "HIPAA": {"name": "HIPAA", "count": 1}
        },
        "detected_frameworks": {
            "nodejs": {
                "name": "Node.js",
                "type": "runtime",
                "confidence": 0.95,
                "files": ["test.js", "package.json"]
            },
            "express": {
                "name": "Express.js",
                "type": "web_framework", 
                "confidence": 0.88,
                "files": ["test.js"]
            }
        },
        "issues": [
            {
                "rule_id": "nodejs.hardcoded_secrets",
                "severity": "critical",
                "category": "security",
                "message": "Node.js Security: Hardcoded JWT secret",
                "file_path": "/tmp/vibeaudit_demo/test.js",
                "line_number": 20,
                "code_snippet": "const JWT_SECRET = 'supersecretjwtkey'; // <-- hard-coded secret",
                "remediation": "Use environment variables or secure configuration management. Never commit secrets to source code.",
                "confidence": 0.9,
                "metadata": {
                    "framework": "nodejs",
                    "cwe": "CWE-798",
                    "iso27001": "A.9.4.3, A.10.1.2",
                    "owasp": "A02-2021",
                    "gdpr": "Art. 32"
                },
                "standards": [
                    {
                        "id": "iso27001_a943",
                        "name": "ISO 27001",
                        "type": "security",
                        "url": "https://www.iso.org/standard/54534.html",
                        "section": "A.9.4.3 - Access Control"
                    },
                    {
                        "id": "owasp_a02_2021",
                        "name": "OWASP Top 10 2021",
                        "type": "security",
                        "url": "https://owasp.org/Top10/A02_2021-Cryptographic_Failures/",
                        "section": "A02-2021 - Cryptographic Failures"
                    },
                    {
                        "id": "cwe_798",
                        "name": "CWE",
                        "type": "security",
                        "url": "https://cwe.mitre.org/data/definitions/798.html",
                        "section": "CWE-798 - Use of Hard-coded Credentials"
                    }
                ],
                "compliance_frameworks": ["ISO 27001", "OWASP", "GDPR", "PCI DSS"]
            },
            {
                "rule_id": "express.security_misconfiguration",
                "severity": "high",
                "category": "security",
                "message": "Express Security: Permissive CORS configuration allows any origin",
                "file_path": "/tmp/vibeaudit_demo/test.js",
                "line_number": 12,
                "code_snippet": "app.use(cors());",
                "remediation": "Configure CORS with specific origins. Use: cors({origin: ['https://yourdomain.com']})",
                "confidence": 0.8,
                "metadata": {
                    "framework": "express",
                    "cwe": "CWE-346",
                    "iso27001": "A.13.1.3",
                    "owasp": "A05-2021"
                },
                "standards": [
                    {
                        "id": "iso27001_a1313",
                        "name": "ISO 27001",
                        "type": "security",
                        "url": "https://www.iso.org/standard/54534.html",
                        "section": "A.13.1.3 - Network Controls"
                    },
                    {
                        "id": "owasp_a05_2021",
                        "name": "OWASP Top 10 2021",
                        "type": "security",
                        "url": "https://owasp.org/Top10/A05_2021-Security_Misconfiguration/",
                        "section": "A05-2021 - Security Misconfiguration"
                    }
                ],
                "compliance_frameworks": ["ISO 27001", "OWASP", "PCI DSS"]
            },
            {
                "rule_id": "nodejs.information_disclosure",
                "severity": "high",
                "category": "security",
                "message": "Node.js Logging: Error stack trace returned to client",
                "file_path": "/tmp/vibeaudit_demo/test.js",
                "line_number": 18,
                "code_snippet": "res.status(500).json({ error: err.message, stack: err.stack });",
                "remediation": "Never return stack traces to clients in production",
                "confidence": 0.8,
                "metadata": {
                    "framework": "nodejs",
                    "cwe": "CWE-209",
                    "iso27001": "A.12.4.1",
                    "owasp": "A09-2021"
                },
                "standards": [
                    {
                        "id": "iso27001_a1241",
                        "name": "ISO 27001",
                        "type": "security",
                        "url": "https://www.iso.org/standard/54534.html",
                        "section": "A.12.4.1 - Event Logging"
                    }
                ],
                "compliance_frameworks": ["ISO 27001", "OWASP"]
            },
            {
                "rule_id": "nodejs.authentication",
                "severity": "critical",
                "category": "security",
                "message": "Node.js Authentication: Admin endpoint without authentication middleware",
                "file_path": "/tmp/vibeaudit_demo/test.js",
                "line_number": 25,
                "code_snippet": "app.get('/admin/config', (req, res) => {",
                "remediation": "Implement authentication middleware for all admin endpoints",
                "confidence": 0.8,
                "metadata": {
                    "framework": "nodejs",
                    "cwe": "CWE-306",
                    "iso27001": "A.9.1.2",
                    "owasp": "A07-2021"
                },
                "standards": [
                    {
                        "id": "iso27001_a912",
                        "name": "ISO 27001",
                        "type": "security",
                        "url": "https://www.iso.org/standard/54534.html",
                        "section": "A.9.1.2 - Access to Networks and Network Services"
                    }
                ],
                "compliance_frameworks": ["ISO 27001", "OWASP", "PCI DSS"]
            },
            {
                "rule_id": "nodejs.logging_security",
                "severity": "medium",
                "category": "security",
                "message": "Node.js Logging: Request body logged to file without encryption",
                "file_path": "/tmp/vibeaudit_demo/test.js",
                "line_number": 42,
                "code_snippet": "fs.appendFileSync('./app_logs.txt', JSON.stringify(req.body));",
                "remediation": "Encrypt sensitive data before logging and implement access controls",
                "confidence": 0.8,
                "metadata": {
                    "framework": "nodejs",
                    "cwe": "CWE-532",
                    "iso27001": "A.8.2.3",
                    "gdpr": "Art.32"
                },
                "standards": [
                    {
                        "id": "gdpr_art32",
                        "name": "GDPR",
                        "type": "compliance",
                        "url": "https://gdpr-info.eu/art-32-gdpr/",
                        "section": "Art. 32 - Security of Processing"
                    }
                ],
                "compliance_frameworks": ["GDPR", "HIPAA"]
            }
        ],
        "errors": {}
    }
    
    return demo_results

@app.delete("/api/scan/{scan_id}")
async def cleanup_scan(scan_id: str):
    """Cleanup scan resources."""
    if scan_id not in active_scans:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    scan_info = active_scans[scan_id]
    temp_dir = scan_info.get("temp_dir")
    
    if temp_dir and temp_dir.exists():
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    del active_scans[scan_id]
    return {"message": "Scan cleaned up successfully"}

@app.get("/api/rules", response_model=List[RuleModel])
async def get_available_rules():
    """Get all available audit rules."""
    from ..rules import get_all_rules
    
    rules = get_all_rules()
    return [RuleModel.from_rule(rule) for rule in rules]

@app.get("/api/config/default", response_model=ConfigModel)
async def get_default_config():
    """Get default configuration."""
    config = AuditorConfig()
    return ConfigModel.from_config(config)

async def run_scan_task(scan_id: str, target_path: Path, config: AuditorConfig):
    """Background task to run the actual scan."""
    try:
        # Update status
        active_scans[scan_id]["status"] = "scanning"
        await websocket_manager.send_scan_update(scan_id, "scanning", 0)
        
        # Initialize auditor
        auditor = CodeAuditor(config)
        
        # Run scan with progress updates
        results = await run_scan_with_progress(auditor, target_path, scan_id)
        
        # Store results
        active_scans[scan_id].update({
            "status": "completed",
            "end_time": datetime.utcnow(),
            "results": results,
            "progress": 100
        })
        
        await websocket_manager.send_scan_update(scan_id, "completed", 100)
        
    except Exception as e:
        active_scans[scan_id].update({
            "status": "failed",
            "end_time": datetime.utcnow(),
            "message": str(e),
            "progress": 0
        })
        
        await websocket_manager.send_scan_update(scan_id, "failed", 0, str(e))

async def run_scan_with_progress(auditor: CodeAuditor, target_path: Path, scan_id: str) -> AuditResults:
    """Run scan with progress updates via WebSocket."""
    # Use the real security scanner
    security_scanner = SecurityScanner()
    
    if target_path.is_file():
        files_to_scan = [target_path]
    else:
        files_to_scan = list(target_path.rglob('*'))
        files_to_scan = [f for f in files_to_scan if f.is_file()]
    
    # Filter out non-code files
    code_extensions = {'.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.go', '.rb', '.php', '.c', '.cpp', '.h', '.cs', '.swift', '.kt'}
    files_to_scan = [f for f in files_to_scan if f.suffix.lower() in code_extensions or f.name in ['requirements.txt', 'package.json', 'Pipfile']]
    
    total_files = len(files_to_scan)
    
    # Update progress to 10%
    active_scans[scan_id]["progress"] = 10
    await websocket_manager.send_scan_update(scan_id, "scanning", 10)
    
    # Run the real security scanner
    try:
        results = await security_scanner.scan_files(files_to_scan)
        
        # Update progress to 90%
        active_scans[scan_id]["progress"] = 90
        await websocket_manager.send_scan_update(scan_id, "scanning", 90)
        
        # Add some metadata
        results.metadata = {
            'files_scanned': len(files_to_scan),
            'scanners_used': list(security_scanner.scanners.keys()),
            'scan_duration': 'real-time'
        }
        
    except Exception as e:
        # Fallback to mock results if real scanner fails
        results = AuditResults()
        results.add_error('scanner', f"Real scanner failed: {e}")
        
        # Add some mock issues for demonstration
        mock_issues = [
            Issue(
                rule_id="fallback_demo",
                severity=Severity.HIGH,
                category="security",
                message="Demo security issue (real scanner unavailable)",
                file_path=files_to_scan[0] if files_to_scan else Path("demo.py"),
                line_number=1,
                code_snippet="# Demo code",
                remediation="This is a fallback demo issue",
                confidence=0.5,
                metadata={'demo': True}
            )
        ]
        
        for issue in mock_issues:
            results.add_issue(issue)
    
    return results

# Include WebSocket endpoint
from .websocket import websocket_endpoint
app.add_websocket_route("/ws/{scan_id}", websocket_endpoint)

# Serve static files for PWA (in production, use nginx or similar)
# app.mount("/", StaticFiles(directory="static", html=True), name="static")