"""
Production Configuration for VibeCodeAuditor
Handles environment variables, security settings, and deployment configurations.
"""

import os
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from pathlib import Path
import json

@dataclass
class DatabaseConfig:
    """Database configuration."""
    url: str
    max_connections: int = 20
    ssl_mode: str = "require"
    timeout: int = 30

@dataclass
class SecurityConfig:
    """Security configuration."""
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expiration: int = 3600  # 1 hour
    cors_origins: List[str] = field(default_factory=lambda: ["*"])
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_file_types: List[str] = field(default_factory=lambda: [
        '.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.go', '.rb', '.php',
        '.c', '.cpp', '.h', '.cs', '.swift', '.kt', '.json', '.yml', '.yaml'
    ])
    rate_limit_per_minute: int = 60

@dataclass
class ScannerConfig:
    """Scanner configuration."""
    enabled_scanners: List[str] = field(default_factory=lambda: [
        'bandit', 'semgrep', 'eslint_security', 'safety', 'custom_rules'
    ])
    timeout_per_file: int = 30  # seconds
    max_concurrent_scans: int = 5
    temp_dir: Optional[str] = None

@dataclass
class StorageConfig:
    """File storage configuration."""
    type: str = "local"  # local, s3, gcs
    local_path: str = "/tmp/vibeauditor"
    s3_bucket: Optional[str] = None
    s3_region: Optional[str] = None
    gcs_bucket: Optional[str] = None
    retention_days: int = 30

@dataclass
class NotificationConfig:
    """Notification configuration."""
    email_enabled: bool = False
    smtp_host: Optional[str] = None
    smtp_port: int = 587
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    webhook_url: Optional[str] = None

@dataclass
class ProductionConfig:
    """Main production configuration."""
    environment: str = "development"
    debug: bool = False
    log_level: str = "INFO"
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 1
    
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    scanner: ScannerConfig = field(default_factory=ScannerConfig)
    storage: StorageConfig = field(default_factory=StorageConfig)
    notifications: NotificationConfig = field(default_factory=NotificationConfig)
    
    @classmethod
    def from_env(cls) -> 'ProductionConfig':
        """Create configuration from environment variables."""
        
        # Database configuration
        database = DatabaseConfig(
            url=os.getenv('DATABASE_URL', 'postgresql://localhost/vibeauditor'),
            max_connections=int(os.getenv('DB_MAX_CONNECTIONS', '20')),
            ssl_mode=os.getenv('DB_SSL_MODE', 'require'),
            timeout=int(os.getenv('DB_TIMEOUT', '30'))
        )
        
        # Security configuration
        security = SecurityConfig(
            jwt_secret=os.getenv('JWT_SECRET', 'your-secret-key-change-in-production'),
            jwt_algorithm=os.getenv('JWT_ALGORITHM', 'HS256'),
            jwt_expiration=int(os.getenv('JWT_EXPIRATION', '3600')),
            cors_origins=os.getenv('CORS_ORIGINS', '*').split(','),
            max_file_size=int(os.getenv('MAX_FILE_SIZE', str(10 * 1024 * 1024))),
            rate_limit_per_minute=int(os.getenv('RATE_LIMIT_PER_MINUTE', '60'))
        )
        
        # Scanner configuration
        scanner = ScannerConfig(
            enabled_scanners=os.getenv('ENABLED_SCANNERS', 'bandit,semgrep,custom_rules').split(','),
            timeout_per_file=int(os.getenv('SCANNER_TIMEOUT', '30')),
            max_concurrent_scans=int(os.getenv('MAX_CONCURRENT_SCANS', '5')),
            temp_dir=os.getenv('TEMP_DIR')
        )
        
        # Storage configuration
        storage = StorageConfig(
            type=os.getenv('STORAGE_TYPE', 'local'),
            local_path=os.getenv('STORAGE_LOCAL_PATH', '/tmp/vibeauditor'),
            s3_bucket=os.getenv('S3_BUCKET'),
            s3_region=os.getenv('S3_REGION'),
            gcs_bucket=os.getenv('GCS_BUCKET'),
            retention_days=int(os.getenv('STORAGE_RETENTION_DAYS', '30'))
        )
        
        # Notification configuration
        notifications = NotificationConfig(
            email_enabled=os.getenv('EMAIL_ENABLED', 'false').lower() == 'true',
            smtp_host=os.getenv('SMTP_HOST'),
            smtp_port=int(os.getenv('SMTP_PORT', '587')),
            smtp_username=os.getenv('SMTP_USERNAME'),
            smtp_password=os.getenv('SMTP_PASSWORD'),
            webhook_url=os.getenv('WEBHOOK_URL')
        )
        
        return cls(
            environment=os.getenv('ENVIRONMENT', 'development'),
            debug=os.getenv('DEBUG', 'false').lower() == 'true',
            log_level=os.getenv('LOG_LEVEL', 'INFO'),
            host=os.getenv('HOST', '0.0.0.0'),
            port=int(os.getenv('PORT', '8000')),
            workers=int(os.getenv('WORKERS', '1')),
            database=database,
            security=security,
            scanner=scanner,
            storage=storage,
            notifications=notifications
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            'environment': self.environment,
            'debug': self.debug,
            'log_level': self.log_level,
            'host': self.host,
            'port': self.port,
            'workers': self.workers,
            'database': {
                'url': self.database.url,
                'max_connections': self.database.max_connections,
                'ssl_mode': self.database.ssl_mode,
                'timeout': self.database.timeout
            },
            'security': {
                'jwt_algorithm': self.security.jwt_algorithm,
                'jwt_expiration': self.security.jwt_expiration,
                'cors_origins': self.security.cors_origins,
                'max_file_size': self.security.max_file_size,
                'allowed_file_types': self.security.allowed_file_types,
                'rate_limit_per_minute': self.security.rate_limit_per_minute
            },
            'scanner': {
                'enabled_scanners': self.scanner.enabled_scanners,
                'timeout_per_file': self.scanner.timeout_per_file,
                'max_concurrent_scans': self.scanner.max_concurrent_scans,
                'temp_dir': self.scanner.temp_dir
            },
            'storage': {
                'type': self.storage.type,
                'local_path': self.storage.local_path,
                'retention_days': self.storage.retention_days
            },
            'notifications': {
                'email_enabled': self.notifications.email_enabled,
                'webhook_url': self.notifications.webhook_url
            }
        }
    
    def save_to_file(self, file_path: Path):
        """Save configuration to JSON file."""
        with open(file_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load_from_file(cls, file_path: Path) -> 'ProductionConfig':
        """Load configuration from JSON file."""
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # This is a simplified loader - in production you'd want more robust parsing
        config = cls()
        config.environment = data.get('environment', 'development')
        config.debug = data.get('debug', False)
        config.log_level = data.get('log_level', 'INFO')
        config.host = data.get('host', '0.0.0.0')
        config.port = data.get('port', 8000)
        config.workers = data.get('workers', 1)
        
        return config

# Global configuration instance
config = ProductionConfig.from_env()

def get_config() -> ProductionConfig:
    """Get the global configuration instance."""
    return config

def update_config(**kwargs):
    """Update configuration values."""
    global config
    for key, value in kwargs.items():
        if hasattr(config, key):
            setattr(config, key, value)