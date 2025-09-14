#!/usr/bin/env python3
"""
Check if issues are actually in the database
"""
import sys
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def check_database_issues():
    """Check if issues are in the database"""
    try:
        from vibeauditor.core.supabase_client import get_supabase_client
        
        supabase = get_supabase_client()
        
        print("🔍 Checking database for recent issues...")
        
        # Get recent scans
        scans_result = supabase.table("scans").select("*").order("created_at", desc=True).limit(5).execute()
        
        print(f"📊 Found {len(scans_result.data)} recent scans:")
        for scan in scans_result.data:
            scan_id = scan["id"]
            status = scan["status"]
            name = scan.get("name", "unknown")
            created_at = scan["created_at"]
            
            print(f"   Scan: {scan_id[:8]}... | {name} | {status} | {created_at}")
            
            # Check issues for this scan
            issues_result = supabase.table("issues").select("*").eq("scan_id", scan_id).execute()
            print(f"     Issues: {len(issues_result.data)}")
            
            if issues_result.data:
                for issue in issues_result.data[:3]:  # Show first 3 issues
                    print(f"       - {issue.get('severity', 'unknown')}: {issue.get('message', 'no message')}")
                if len(issues_result.data) > 3:
                    print(f"       ... and {len(issues_result.data) - 3} more")
            print()
        
        # Check if there are any issues at all
        all_issues = supabase.table("issues").select("*").limit(10).execute()
        print(f"📋 Total issues in database: {len(all_issues.data)}")
        
        if all_issues.data:
            print("Recent issues:")
            for issue in all_issues.data[:5]:
                print(f"   - {issue.get('rule_id', 'unknown')}: {issue.get('message', 'no message')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    check_database_issues()