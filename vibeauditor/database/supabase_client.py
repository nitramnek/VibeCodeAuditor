"""
Supabase client configuration for VibeCodeAuditor.
"""

import os
from supabase import create_client, Client
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class SupabaseClient:
    """Singleton Supabase client for database operations."""
    
    def __init__(self):
        self._client: Optional[Client] = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Supabase client with environment variables."""
        try:
            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
            
            if not url or not key:
                logger.warning("Supabase credentials not found. Database features will be disabled.")
                return
            
            self._client = create_client(url, key)
            logger.info("Supabase client initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Supabase client: {e}")
            self._client = None
    
    def get_client(self) -> Optional[Client]:
        """Get the Supabase client instance."""
        return self._client
    
    def is_available(self) -> bool:
        """Check if Supabase client is available."""
        return self._client is not None
    
    def test_connection(self) -> bool:
        """Test database connection."""
        if not self.is_available():
            return False
        
        try:
            # Simple query to test connection
            result = self._client.table('profiles').select('id').limit(1).execute()
            return True
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return False

# Singleton instance
supabase_client = SupabaseClient()