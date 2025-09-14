#!/usr/bin/env python3
"""
Quick import test to verify the Pydantic fix.
"""

try:
    print("Testing imports...")
    
    # Test core imports
    from vibeauditor.core.auditor import CodeAuditor
    from vibeauditor.core.config import AuditorConfig
    print("✅ Core imports successful")
    
    # Test API imports (this was failing before)
    from vibeauditor.api.models import ReportRequest, ScanResponse
    print("✅ API models import successful")
    
    from vibeauditor.api.main import app
    print("✅ FastAPI app import successful")
    
    # Test creating a ReportRequest to verify the Field fix
    report_req = ReportRequest(
        scan_id="test-123",
        format="html",
        include_remediation=True
    )
    print(f"✅ ReportRequest creation successful: {report_req.format}")
    
    print("\n🎉 All imports successful! The Pydantic fix worked.")
    print("You can now run: gunicorn vibeauditor.api.main:app -w 4 -k uvicorn.workers.UvicornWorker")
    
except Exception as e:
    print(f"❌ Import failed: {e}")
    import traceback
    traceback.print_exc()