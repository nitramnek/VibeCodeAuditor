"""
Framework detection for more targeted analysis.
"""

import re
from pathlib import Path
from typing import Dict, List, Set, Optional
from dataclasses import dataclass
from enum import Enum

class FrameworkType(Enum):
    """Types of frameworks we can detect."""
    WEB_FRAMEWORK = "web"
    ML_FRAMEWORK = "ml"
    DATABASE = "database"
    CLOUD = "cloud"
    TESTING = "testing"
    SECURITY = "security"
    FRONTEND = "frontend"
    MOBILE = "mobile"

@dataclass
class Framework:
    """Represents a detected framework."""
    name: str
    type: FrameworkType
    version: Optional[str] = None
    confidence: float = 1.0
    files: List[Path] = None
    
    def __post_init__(self):
        if self.files is None:
            self.files = []

class FrameworkDetector:
    """Detects frameworks and technologies used in a codebase."""
    
    def __init__(self):
        self.framework_patterns = {
            # Python Web Frameworks
            'django': {
                'type': FrameworkType.WEB_FRAMEWORK,
                'patterns': [
                    r'from django',
                    r'import django',
                    r'DJANGO_SETTINGS_MODULE',
                    r'django\.conf',
                ],
                'files': ['manage.py', 'settings.py', 'wsgi.py'],
                'directories': ['migrations/']
            },
            'flask': {
                'type': FrameworkType.WEB_FRAMEWORK,
                'patterns': [
                    r'from flask',
                    r'import flask',
                    r'Flask\(__name__\)',
                    r'@app\.route',
                ],
                'files': ['app.py', 'wsgi.py'],
                'directories': ['templates/', 'static/']
            },
            'fastapi': {
                'type': FrameworkType.WEB_FRAMEWORK,
                'patterns': [
                    r'from fastapi',
                    r'import fastapi',
                    r'FastAPI\(',
                    r'@app\.(get|post|put|delete)',
                ],
                'files': ['main.py'],
                'directories': []
            },
            
            # ML/AI Frameworks
            'tensorflow': {
                'type': FrameworkType.ML_FRAMEWORK,
                'patterns': [
                    r'import tensorflow',
                    r'from tensorflow',
                    r'tf\.',
                    r'keras\.',
                ],
                'files': [],
                'directories': ['models/', 'checkpoints/']
            },
            'pytorch': {
                'type': FrameworkType.ML_FRAMEWORK,
                'patterns': [
                    r'import torch',
                    r'from torch',
                    r'torch\.',
                    r'nn\.Module',
                ],
                'files': [],
                'directories': ['models/', 'checkpoints/']
            },
            'scikit-learn': {
                'type': FrameworkType.ML_FRAMEWORK,
                'patterns': [
                    r'from sklearn',
                    r'import sklearn',
                    r'sklearn\.',
                ],
                'files': [],
                'directories': []
            },
            'pandas': {
                'type': FrameworkType.ML_FRAMEWORK,
                'patterns': [
                    r'import pandas',
                    r'pd\.',
                    r'DataFrame',
                ],
                'files': [],
                'directories': ['data/']
            },
            'numpy': {
                'type': FrameworkType.ML_FRAMEWORK,
                'patterns': [
                    r'import numpy',
                    r'np\.',
                    r'ndarray',
                ],
                'files': [],
                'directories': []
            },
            
            # JavaScript/Node.js Frameworks
            'react': {
                'type': FrameworkType.FRONTEND,
                'patterns': [
                    r'import.*react',
                    r'from.*react',
                    r'React\.',
                    r'useState',
                    r'useEffect',
                ],
                'files': ['package.json'],
                'directories': ['src/', 'public/']
            },
            'vue': {
                'type': FrameworkType.FRONTEND,
                'patterns': [
                    r'import.*vue',
                    r'from.*vue',
                    r'Vue\.',
                    r'<template>',
                ],
                'files': ['vue.config.js'],
                'directories': ['src/']
            },
            'angular': {
                'type': FrameworkType.FRONTEND,
                'patterns': [
                    r'@angular',
                    r'import.*@angular',
                    r'@Component',
                    r'@Injectable',
                ],
                'files': ['angular.json'],
                'directories': ['src/app/']
            },
            'express': {
                'type': FrameworkType.WEB_FRAMEWORK,
                'patterns': [
                    r'require\([\'"]express[\'"]\)',
                    r'import.*express',
                    r'app\.get\(',
                    r'app\.post\(',
                    r'app\.use\(',
                    r'express\(\)',
                ],
                'files': ['server.js', 'app.js', 'index.js'],
                'directories': ['routes/', 'middleware/']
            },
            'nodejs': {
                'type': FrameworkType.WEB_FRAMEWORK,
                'patterns': [
                    r'require\([\'"]',
                    r'module\.exports',
                    r'process\.env',
                    r'__dirname',
                    r'console\.log',
                ],
                'files': ['package.json', 'server.js', 'app.js', 'index.js'],
                'directories': ['node_modules/']
            },
            
            # Database Frameworks
            'sqlalchemy': {
                'type': FrameworkType.DATABASE,
                'patterns': [
                    r'from sqlalchemy',
                    r'import sqlalchemy',
                    r'declarative_base',
                    r'Column',
                ],
                'files': [],
                'directories': ['migrations/']
            },
            'mongoose': {
                'type': FrameworkType.DATABASE,
                'patterns': [
                    r'require\([\'"]mongoose[\'"]\)',
                    r'import.*mongoose',
                    r'mongoose\.',
                    r'Schema\(',
                ],
                'files': [],
                'directories': ['models/']
            },
            
            # Cloud Frameworks
            'aws-sdk': {
                'type': FrameworkType.CLOUD,
                'patterns': [
                    r'import boto3',
                    r'from boto3',
                    r'aws-sdk',
                    r'AWS\.',
                ],
                'files': [],
                'directories': []
            },
            'google-cloud': {
                'type': FrameworkType.CLOUD,
                'patterns': [
                    r'from google\.cloud',
                    r'import.*google\.cloud',
                    r'gcp',
                ],
                'files': [],
                'directories': []
            },
            
            # Testing Frameworks
            'pytest': {
                'type': FrameworkType.TESTING,
                'patterns': [
                    r'import pytest',
                    r'@pytest\.',
                    r'def test_',
                ],
                'files': ['pytest.ini', 'conftest.py'],
                'directories': ['tests/']
            },
            'jest': {
                'type': FrameworkType.TESTING,
                'patterns': [
                    r'describe\(',
                    r'it\(',
                    r'test\(',
                    r'expect\(',
                ],
                'files': ['jest.config.js'],
                'directories': ['__tests__/']
            },
            
            # Security Frameworks
            'oauth': {
                'type': FrameworkType.SECURITY,
                'patterns': [
                    r'oauth',
                    r'OAuth',
                    r'access_token',
                    r'refresh_token',
                ],
                'files': [],
                'directories': []
            },
            'jwt': {
                'type': FrameworkType.SECURITY,
                'patterns': [
                    r'import jwt',
                    r'jsonwebtoken',
                    r'JWT',
                    r'token',
                ],
                'files': [],
                'directories': []
            },
        }
    
    def detect_frameworks(self, target_path: Path) -> Dict[str, Framework]:
        """Detect frameworks in the given codebase."""
        detected = {}
        
        if target_path.is_file():
            files_to_scan = [target_path]
        else:
            files_to_scan = list(target_path.rglob("*"))
            files_to_scan = [f for f in files_to_scan if f.is_file()]
        
        # Check package files first for quick detection
        self._check_package_files(target_path, detected)
        
        # Scan code files for framework patterns
        for file_path in files_to_scan:
            if self._should_scan_file(file_path):
                self._scan_file_for_frameworks(file_path, detected)
        
        # Check directory structure
        self._check_directory_structure(target_path, detected)
        
        return detected
    
    def _check_package_files(self, target_path: Path, detected: Dict[str, Framework]):
        """Check package files for framework dependencies."""
        
        # Python requirements.txt
        req_file = target_path / "requirements.txt"
        if req_file.exists():
            self._scan_requirements_file(req_file, detected)
        
        # Python setup.py
        setup_file = target_path / "setup.py"
        if setup_file.exists():
            self._scan_setup_file(setup_file, detected)
        
        # Node.js package.json
        package_file = target_path / "package.json"
        if package_file.exists():
            self._scan_package_json(package_file, detected)
    
    def _scan_requirements_file(self, req_file: Path, detected: Dict[str, Framework]):
        """Scan Python requirements.txt for frameworks."""
        try:
            with open(req_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read().lower()
                
                framework_mappings = {
                    'django': 'django',
                    'flask': 'flask',
                    'fastapi': 'fastapi',
                    'tensorflow': 'tensorflow',
                    'torch': 'pytorch',
                    'sklearn': 'scikit-learn',
                    'pandas': 'pandas',
                    'numpy': 'numpy',
                    'sqlalchemy': 'sqlalchemy',
                    'boto3': 'aws-sdk',
                    'pytest': 'pytest',
                }
                
                for package, framework in framework_mappings.items():
                    if package in content:
                        if framework not in detected:
                            detected[framework] = Framework(
                                name=framework,
                                type=self.framework_patterns[framework]['type'],
                                confidence=0.9,
                                files=[req_file]
                            )
        except Exception:
            pass
    
    def _scan_package_json(self, package_file: Path, detected: Dict[str, Framework]):
        """Scan Node.js package.json for frameworks."""
        try:
            import json
            with open(package_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                dependencies = {}
                dependencies.update(data.get('dependencies', {}))
                dependencies.update(data.get('devDependencies', {}))
                
                framework_mappings = {
                    'react': 'react',
                    'vue': 'vue',
                    '@angular/core': 'angular',
                    'express': 'express',
                    'mongoose': 'mongoose',
                    'jest': 'jest',
                }
                
                for package, framework in framework_mappings.items():
                    if package in dependencies:
                        if framework not in detected:
                            detected[framework] = Framework(
                                name=framework,
                                type=self.framework_patterns[framework]['type'],
                                confidence=0.9,
                                files=[package_file]
                            )
        except Exception:
            pass
    
    def _scan_setup_file(self, setup_file: Path, detected: Dict[str, Framework]):
        """Scan Python setup.py for frameworks."""
        try:
            with open(setup_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read().lower()
                
                # Look for install_requires
                if 'install_requires' in content:
                    # Simple pattern matching for common frameworks
                    for framework_name, framework_info in self.framework_patterns.items():
                        if framework_name in content:
                            if framework_name not in detected:
                                detected[framework_name] = Framework(
                                    name=framework_name,
                                    type=framework_info['type'],
                                    confidence=0.8,
                                    files=[setup_file]
                                )
        except Exception:
            pass
    
    def _scan_file_for_frameworks(self, file_path: Path, detected: Dict[str, Framework]):
        """Scan individual file for framework patterns."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                for framework_name, framework_info in self.framework_patterns.items():
                    for pattern in framework_info['patterns']:
                        if re.search(pattern, content, re.IGNORECASE):
                            if framework_name not in detected:
                                detected[framework_name] = Framework(
                                    name=framework_name,
                                    type=framework_info['type'],
                                    confidence=0.7,
                                    files=[file_path]
                                )
                            else:
                                # Increase confidence and add file
                                detected[framework_name].confidence = min(1.0, detected[framework_name].confidence + 0.1)
                                if file_path not in detected[framework_name].files:
                                    detected[framework_name].files.append(file_path)
        except Exception:
            pass
    
    def _check_directory_structure(self, target_path: Path, detected: Dict[str, Framework]):
        """Check directory structure for framework indicators."""
        if not target_path.is_dir():
            return
        
        for framework_name, framework_info in self.framework_patterns.items():
            for dir_name in framework_info['directories']:
                if (target_path / dir_name).exists():
                    if framework_name not in detected:
                        detected[framework_name] = Framework(
                            name=framework_name,
                            type=framework_info['type'],
                            confidence=0.6
                        )
                    else:
                        detected[framework_name].confidence = min(1.0, detected[framework_name].confidence + 0.1)
            
            for file_name in framework_info['files']:
                if (target_path / file_name).exists():
                    if framework_name not in detected:
                        detected[framework_name] = Framework(
                            name=framework_name,
                            type=framework_info['type'],
                            confidence=0.8,
                            files=[target_path / file_name]
                        )
                    else:
                        detected[framework_name].confidence = min(1.0, detected[framework_name].confidence + 0.2)
                        if (target_path / file_name) not in detected[framework_name].files:
                            detected[framework_name].files.append(target_path / file_name)
    
    def _should_scan_file(self, file_path: Path) -> bool:
        """Check if file should be scanned for framework patterns."""
        scannable_extensions = {
            '.py', '.js', '.ts', '.jsx', '.tsx', '.vue', '.java', '.go', 
            '.rs', '.cpp', '.c', '.h', '.php', '.rb', '.cs', '.swift',
            '.kt', '.scala', '.clj', '.hs', '.ml', '.fs', '.dart'
        }
        
        return file_path.suffix.lower() in scannable_extensions
    
    def get_framework_specific_context(self, framework_name: str) -> Dict:
        """Get framework-specific context for better rule targeting."""
        contexts = {
            'django': {
                'security_concerns': ['CSRF', 'SQL injection', 'XSS', 'Authentication'],
                'best_practices': ['Use Django ORM', 'Validate forms', 'Use HTTPS'],
                'common_vulnerabilities': ['Debug mode in production', 'Weak SECRET_KEY'],
                'documentation': 'https://docs.djangoproject.com/en/stable/topics/security/'
            },
            'flask': {
                'security_concerns': ['Session management', 'CSRF', 'Input validation'],
                'best_practices': ['Use Flask-WTF', 'Validate inputs', 'Secure sessions'],
                'common_vulnerabilities': ['Debug mode', 'Weak session keys'],
                'documentation': 'https://flask.palletsprojects.com/en/2.3.x/security/'
            },
            'tensorflow': {
                'security_concerns': ['Model poisoning', 'Data privacy', 'Model stealing'],
                'best_practices': ['Validate inputs', 'Secure model storage', 'Monitor predictions'],
                'common_vulnerabilities': ['Unsafe model loading', 'Data leakage'],
                'documentation': 'https://www.tensorflow.org/responsible_ai/fairness_indicators/guide'
            },
            'pytorch': {
                'security_concerns': ['Unsafe model loading', 'Data privacy', 'Model attacks'],
                'best_practices': ['Use safe loading', 'Validate data', 'Monitor models'],
                'common_vulnerabilities': ['torch.load without map_location', 'Pickle vulnerabilities'],
                'documentation': 'https://pytorch.org/docs/stable/notes/serialization.html'
            },
            'react': {
                'security_concerns': ['XSS', 'CSRF', 'Dependency vulnerabilities'],
                'best_practices': ['Sanitize inputs', 'Use HTTPS', 'Update dependencies'],
                'common_vulnerabilities': ['dangerouslySetInnerHTML', 'Outdated packages'],
                'documentation': 'https://reactjs.org/docs/dom-elements.html#dangerouslysetinnerhtml'
            }
        }
        
        return contexts.get(framework_name, {})