"""
Database service for VibeCodeAuditor with Supabase integration.
"""

from typing import List, Dict, Any, Optional
from .supabase_client import supabase_client
from ..core.results import AuditResults, Issue
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DatabaseService:
    """Service for database operations with Supabase."""
    
    def __init__(self):
        self.client = supabase_client.get_client()
    
    def is_available(self) -> bool:
        """Check if database service is available."""
        return self.client is not None
    
    def create_scan(self, user_id: str, name: str, config: Dict[str, Any] = None) -> Optional[int]:
        """Create a new scan record."""
        if not self.is_available():
            logger.warning("Database not available, cannot create scan")
            return None
        
        try:
            scan_data = {
                'user_id': user_id,
                'name': name or f"Scan {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}",
                'status': 'pending',
                'config': config or {},
                'started_at': datetime.utcnow().isoformat()
            }
            
            result = self.client.table('scans').insert(scan_data).execute()
            if result.data and len(result.data) > 0:
                return result.data[0]['id']
            else:
                logger.error("Failed to create scan: no data returned")
                return None
                
        except Exception as e:
            logger.error(f"Error creating scan: {e}")
            return None
    
    def update_scan_status(self, scan_id: int, status: str, 
                          summary: Optional[Dict] = None,
                          compliance_summary: Optional[Dict] = None,
                          detected_frameworks: Optional[Dict] = None) -> bool:
        """Update scan status and results."""
        if not self.is_available():
            logger.warning("Database not available, cannot update scan")
            return False
        
        try:
            update_data = {
                'status': status,
                'updated_at': datetime.utcnow().isoformat()
            }
            
            if status == 'completed':
                update_data['completed_at'] = datetime.utcnow().isoformat()
            
            if summary:
                update_data.update({
                    'summary': summary,
                    'total_issues': summary.get('total_issues', 0),
                    'critical_issues': summary.get('critical', 0),
                    'high_issues': summary.get('high', 0),
                    'medium_issues': summary.get('medium', 0),
                    'low_issues': summary.get('low', 0)
                })
            
            if compliance_summary:
                update_data['compliance_summary'] = compliance_summary
            
            if detected_frameworks:
                update_data['detected_frameworks'] = detected_frameworks
            
            result = self.client.table('scans').update(update_data).eq('id', scan_id).execute()
            return result.data is not None
            
        except Exception as e:
            logger.error(f"Error updating scan {scan_id}: {e}")
            return False
    
    def save_issues(self, scan_id: int, issues: List[Issue]) -> int:
        """Save scan issues to database."""
        if not self.is_available():
            logger.warning("Database not available, cannot save issues")
            return 0
        
        try:
            issue_records = []
            
            for issue in issues:
                issue_data = {
                    'scan_id': scan_id,
                    'rule_id': issue.rule_id,
                    'severity': issue.severity.value,
                    'category': issue.category,
                    'message': issue.message,
                    'file_path': str(issue.file_path),
                    'line_number': issue.line_number,
                    'column_number': issue.column_number,
                    'code_snippet': issue.code_snippet,
                    'remediation': issue.remediation,
                    'confidence': issue.confidence,
                    'metadata': issue.metadata or {},
                    'standards': [self._serialize_standard(std) for std in (issue.standards or [])],
                    'compliance_frameworks': issue.compliance_frameworks or []
                }
                issue_records.append(issue_data)
            
            if issue_records:
                result = self.client.table('issues').insert(issue_records).execute()
                return len(result.data) if result.data else 0
            
            return 0
            
        except Exception as e:
            logger.error(f"Error saving issues for scan {scan_id}: {e}")
            return 0
    
    def _serialize_standard(self, standard) -> Dict[str, Any]:
        """Serialize a standard object for database storage."""
        if hasattr(standard, '__dict__'):
            return {
                'id': getattr(standard, 'id', ''),
                'name': getattr(standard, 'name', ''),
                'type': getattr(standard, 'type', {}).value if hasattr(getattr(standard, 'type', {}), 'value') else str(getattr(standard, 'type', '')),
                'url': getattr(standard, 'url', ''),
                'section': getattr(standard, 'section', ''),
                'description': getattr(standard, 'description', '')
            }
        elif isinstance(standard, dict):
            return standard
        else:
            return {'name': str(standard)}
    
    def get_scan_results(self, scan_id: int, user_id: str) -> Optional[Dict]:
        """Get scan results with issues."""
        if not self.is_available():
            logger.warning("Database not available, cannot get scan results")
            return None
        
        try:
            # Get scan info
            scan_result = self.client.table('scans').select('*').eq('id', scan_id).eq('user_id', user_id).execute()
            
            if not scan_result.data:
                return None
            
            scan = scan_result.data[0]
            
            # Get issues
            issues_result = self.client.table('issues').select('*').eq('scan_id', scan_id).execute()
            
            return {
                'scan': scan,
                'issues': issues_result.data or []
            }
            
        except Exception as e:
            logger.error(f"Error getting scan results for scan {scan_id}: {e}")
            return None
    
    def get_user_scans(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Get user's scan history."""
        if not self.is_available():
            logger.warning("Database not available, cannot get user scans")
            return []
        
        try:
            result = self.client.table('scans').select('*').eq('user_id', user_id).order('created_at', desc=True).limit(limit).execute()
            return result.data or []
            
        except Exception as e:
            logger.error(f"Error getting user scans for user {user_id}: {e}")
            return []
    
    def upload_file(self, scan_id: int, file_name: str, file_content: bytes) -> Optional[str]:
        """Upload file to Supabase storage."""
        if not self.is_available():
            logger.warning("Database not available, cannot upload file")
            return None
        
        try:
            storage_path = f"scans/{scan_id}/{file_name}"
            
            # Upload to storage
            result = self.client.storage.from_('vibeauditor-files').upload(storage_path, file_content)
            
            if result.error:
                logger.error(f"File upload failed: {result.error}")
                return None
            
            # Save file record
            file_data = {
                'scan_id': scan_id,
                'file_name': file_name,
                'file_path': file_name,
                'storage_path': storage_path,
                'file_size': len(file_content)
            }
            
            self.client.table('scan_files').insert(file_data).execute()
            
            return storage_path
            
        except Exception as e:
            logger.error(f"Error uploading file {file_name} for scan {scan_id}: {e}")
            return None
    
    def create_user_profile(self, user_id: str, email: str, full_name: str = None, organization: str = None, role_id: str = None) -> bool:
        """Create or update user profile."""
        if not self.is_available():
            logger.warning("Database not available, cannot create user profile")
            return False
        
        try:
            profile_data = {
                'id': user_id,  # Use user_id as the primary key to match auth.users
                'email': email,
                'full_name': full_name or email,
                'organization': organization,
                'role_id': role_id or 'user'  # Default to 'user' role if not specified
            }
            
            result = self.client.table('profiles').upsert(profile_data).execute()
            return result.data is not None
            
        except Exception as e:
            logger.error(f"Error creating user profile for {user_id}: {e}")
            return False
    
    def get_user_profile(self, user_id: str) -> Optional[Dict]:
        """Get user profile."""
        if not self.is_available():
            logger.warning("Database not available, cannot get user profile")
            return None
        
        try:
            result = self.client.table('profiles').select('*').eq('user_id', user_id).single().execute()
            return result.data
            
        except Exception as e:
            logger.error(f"Error getting user profile for {user_id}: {e}")
            return None
    
    def log_audit_event(self, user_id: str, action: str, resource_type: str, resource_id: int = None, details: Dict = None) -> bool:
        """Log an audit event."""
        if not self.is_available():
            return False
        
        try:
            audit_data = {
                'user_id': user_id,
                'action': action,
                'resource_type': resource_type,
                'resource_id': resource_id,
                'details': details or {}
            }
            
            result = self.client.table('audit_logs').insert(audit_data).execute()
            return result.data is not None
            
        except Exception as e:
            logger.error(f"Error logging audit event: {e}")
            return False

# Singleton instance
db_service = DatabaseService()