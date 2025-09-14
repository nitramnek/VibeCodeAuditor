#!/usr/bin/env python3
"""
Fix scan status for recent scans
"""
import sys
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def fix_scan_status():
    """Fix scan status for recent scans"""
    try:
        from vibeauditor.core.supabase_client import get_supabase_client
        
        supabase = get_supabase_client()
        
        print("🔧 Fixing scan status for recent scans...")
        
        # Get recent scans that are not completed
        scans_result = supabase.table("scans").select("*").neq("status", "completed").order("created_at", desc=True).limit(10).execute()
        
        print(f"📊 Found {len(scans_result.data)} scans to fix:")
        
        for scan in scans_result.data:
            scan_id = scan["id"]
            status = scan["status"]
            name = scan.get("name", "unknown")
            
            # Check if this scan has issues
            issues_result = supabase.table("issues").select("*").eq("scan_id", scan_id).execute()
            issue_count = len(issues_result.data)
            
            print(f"   Scan: {scan_id[:8]}... | {name} | {status} | Issues: {issue_count}")
            
            if issue_count > 0:
                # Update scan to completed
                try:
                    supabase.table("scans").update({
                        "status": "completed",
                        "total_issues": issue_count
                    }).eq("id", scan_id).execute()
                    print(f"     ✅ Updated to completed with {issue_count} issues")
                except Exception as e:
                    print(f"     ❌ Failed to update: {e}")
            else:
                print(f"     ⚠️ No issues found, leaving as {status}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error fixing scan status: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    fix_scan_status()