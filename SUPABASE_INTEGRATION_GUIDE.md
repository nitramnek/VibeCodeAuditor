# 🚀 VibeCodeAuditor - Supabase Integration Guide

## Overview

This guide shows how to integrate VibeCodeAuditor with Supabase for:
- **User Authentication & Authorization**
- **Scan Results Storage**
- **Compliance Data Persistence**
- **Real-time Updates**
- **File Storage for uploaded code**
- **Analytics & Reporting**

## 🏗️ Database Schema Design

### 1. Core Tables

```sql
-- Users table (extends Supabase auth.users)
CREATE TABLE public.profiles (
    id UUID REFERENCES auth.users(id) PRIMARY KEY,
    email TEXT,
    full_name TEXT,
    organization TEXT,
    role TEXT DEFAULT 'user',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Organizations table
CREATE TABLE public.organizations (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name TEXT NOT NULL,
    domain TEXT,
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Scans table
CREATE TABLE public.scans (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) NOT NULL,
    organization_id UUID REFERENCES organizations(id),
    name TEXT NOT NULL,
    status TEXT DEFAULT 'pending', -- pending, running, completed, failed
    config JSONB DEFAULT '{}',
    summary JSONB DEFAULT '{}',
    compliance_summary JSONB DEFAULT '{}',
    detected_frameworks JSONB DEFAULT '{}',
    file_count INTEGER DEFAULT 0,
    total_issues INTEGER DEFAULT 0,
    critical_issues INTEGER DEFAULT 0,
    high_issues INTEGER DEFAULT 0,
    medium_issues INTEGER DEFAULT 0,
    low_issues INTEGER DEFAULT 0,
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Issues table
CREATE TABLE public.issues (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    scan_id UUID REFERENCES scans(id) ON DELETE CASCADE NOT NULL,
    rule_id TEXT NOT NULL,
    severity TEXT NOT NULL,
    category TEXT NOT NULL,
    message TEXT NOT NULL,
    file_path TEXT NOT NULL,
    line_number INTEGER,
    column_number INTEGER,
    code_snippet TEXT,
    remediation TEXT,
    confidence DECIMAL(3,2) DEFAULT 1.0,
    metadata JSONB DEFAULT '{}',
    standards JSONB DEFAULT '[]',
    compliance_frameworks TEXT[] DEFAULT '{}',
    status TEXT DEFAULT 'open', -- open, acknowledged, resolved, false_positive
    assigned_to UUID REFERENCES auth.users(id),
    resolved_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Compliance frameworks reference table
CREATE TABLE public.compliance_frameworks (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    version TEXT,
    url TEXT,
    standards JSONB DEFAULT '[]',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Scan files table (for file storage references)
CREATE TABLE public.scan_files (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    scan_id UUID REFERENCES scans(id) ON DELETE CASCADE NOT NULL,
    file_name TEXT NOT NULL,
    file_path TEXT NOT NULL,
    file_size INTEGER,
    storage_path TEXT, -- Supabase storage path
    mime_type TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Audit logs table
CREATE TABLE public.audit_logs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id),
    action TEXT NOT NULL,
    resource_type TEXT NOT NULL,
    resource_id UUID,
    details JSONB DEFAULT '{}',
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### 2. Row Level Security (RLS) Policies

```sql
-- Enable RLS on all tables
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE organizations ENABLE ROW LEVEL SECURITY;
ALTER TABLE scans ENABLE ROW LEVEL SECURITY;
ALTER TABLE issues ENABLE ROW LEVEL SECURITY;
ALTER TABLE scan_files ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;

-- Profiles policies
CREATE POLICY "Users can view own profile" ON profiles
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON profiles
    FOR UPDATE USING (auth.uid() = id);

-- Scans policies
CREATE POLICY "Users can view own scans" ON scans
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create scans" ON scans
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own scans" ON scans
    FOR UPDATE USING (auth.uid() = user_id);

-- Issues policies
CREATE POLICY "Users can view issues from own scans" ON issues
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM scans 
            WHERE scans.id = issues.scan_id 
            AND scans.user_id = auth.uid()
        )
    );

-- Similar policies for other tables...
```

## 📦 Installation & Setup

### 1. Install Supabase Dependencies

```bash
# Backend dependencies
pip install supabase python-dotenv

# Frontend dependencies
cd webapp
npm install @supabase/supabase-js @supabase/auth-ui-react
```

### 2. Environment Configuration

Create `.env` file:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# Database
DATABASE_URL=postgresql://postgres:[password]@db.[project].supabase.co:5432/postgres

# Storage
SUPABASE_STORAGE_BUCKET=vibeauditor-files
```

Frontend `.env`:

```env
REACT_APP_SUPABASE_URL=https://your-project.supabase.co
REACT_APP_SUPABASE_ANON_KEY=your-anon-key
```

## 🔧 Backend Integration

### 1. Supabase Client Setup

```python
# vibeauditor/database/supabase_client.py
import os
from supabase import create_client, Client
from typing import Optional

class SupabaseClient:
    def __init__(self):
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        self.client: Client = create_client(url, key)
    
    def get_client(self) -> Client:
        return self.client

# Singleton instance
supabase_client = SupabaseClient()
```

### 2. Database Models

```python
# vibeauditor/database/models.py
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid

@dataclass
class ScanRecord:
    id: str
    user_id: str
    name: str
    status: str
    config: Dict[str, Any]
    summary: Dict[str, Any]
    compliance_summary: Dict[str, Any]
    detected_frameworks: Dict[str, Any]
    file_count: int = 0
    total_issues: int = 0
    critical_issues: int = 0
    high_issues: int = 0
    medium_issues: int = 0
    low_issues: int = 0
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class IssueRecord:
    id: str
    scan_id: str
    rule_id: str
    severity: str
    category: str
    message: str
    file_path: str
    line_number: Optional[int] = None
    column_number: Optional[int] = None
    code_snippet: Optional[str] = None
    remediation: Optional[str] = None
    confidence: float = 1.0
    metadata: Dict[str, Any] = None
    standards: List[Dict[str, Any]] = None
    compliance_frameworks: List[str] = None
    status: str = 'open'
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
```

### 3. Database Service

```python
# vibeauditor/database/service.py
from typing import List, Dict, Any, Optional
from .supabase_client import supabase_client
from .models import ScanRecord, IssueRecord
from ..core.results import AuditResults, Issue
import uuid
from datetime import datetime

class DatabaseService:
    def __init__(self):
        self.client = supabase_client.get_client()
    
    async def create_scan(self, user_id: str, name: str, config: Dict[str, Any]) -> str:
        """Create a new scan record."""
        scan_id = str(uuid.uuid4())
        
        scan_data = {
            'id': scan_id,
            'user_id': user_id,
            'name': name,
            'status': 'pending',
            'config': config,
            'started_at': datetime.utcnow().isoformat()
        }
        
        result = self.client.table('scans').insert(scan_data).execute()
        return scan_id
    
    async def update_scan_status(self, scan_id: str, status: str, 
                                summary: Optional[Dict] = None,
                                compliance_summary: Optional[Dict] = None,
                                detected_frameworks: Optional[Dict] = None):
        """Update scan status and results."""
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
        return result
    
    async def save_issues(self, scan_id: str, issues: List[Issue]):
        """Save scan issues to database."""
        issue_records = []
        
        for issue in issues:
            issue_data = {
                'id': str(uuid.uuid4()),
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
                'standards': [std.to_dict() if hasattr(std, 'to_dict') else std for std in (issue.standards or [])],
                'compliance_frameworks': issue.compliance_frameworks or []
            }
            issue_records.append(issue_data)
        
        if issue_records:
            result = self.client.table('issues').insert(issue_records).execute()
        
        return len(issue_records)
    
    async def get_scan_results(self, scan_id: str, user_id: str) -> Optional[Dict]:
        """Get scan results with issues."""
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
    
    async def get_user_scans(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Get user's scan history."""
        result = self.client.table('scans').select('*').eq('user_id', user_id).order('created_at', desc=True).limit(limit).execute()
        return result.data or []
    
    async def upload_file(self, scan_id: str, file_name: str, file_content: bytes) -> str:
        """Upload file to Supabase storage."""
        storage_path = f"scans/{scan_id}/{file_name}"
        
        # Upload to storage
        result = self.client.storage.from_('vibeauditor-files').upload(storage_path, file_content)
        
        if result.error:
            raise Exception(f"File upload failed: {result.error}")
        
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

# Singleton instance
db_service = DatabaseService()
```

### 4. Enhanced API Integration

```python
# vibeauditor/api/main.py (additions)
from ..database.service import db_service
from supabase import create_client
import os

# Add Supabase client for auth
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_ANON_KEY")
)

# Middleware for authentication
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token and get current user."""
    try:
        # Verify token with Supabase
        user = supabase.auth.get_user(credentials.credentials)
        if user.user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        return user.user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

# Enhanced endpoints
@app.post("/api/scan/upload", response_model=ScanResponse)
async def upload_and_scan(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...),
    config: Optional[str] = None,
    current_user = Depends(get_current_user)
):
    """Upload files and start scanning with user authentication."""
    
    # Create scan record in database
    scan_id = await db_service.create_scan(
        user_id=current_user.id,
        name=f"Scan {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}",
        config=json.loads(config) if config else {}
    )
    
    # Upload files to Supabase storage
    temp_dir = Path(tempfile.mkdtemp(prefix=f"vibeaudit_{scan_id}_"))
    
    for file in files:
        # Save to temp directory
        file_path = temp_dir / file.filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_content = await file.read()
        with open(file_path, "wb") as buffer:
            buffer.write(file_content)
        
        # Upload to Supabase storage
        await db_service.upload_file(scan_id, file.filename, file_content)
    
    # Start background scan
    background_tasks.add_task(run_scan_with_database, scan_id, temp_dir, current_user.id)
    
    return ScanResponse(
        scan_id=scan_id,
        status="started",
        message="Scan initiated successfully"
    )

async def run_scan_with_database(scan_id: str, target_path: Path, user_id: str):
    """Enhanced scan task with database integration."""
    try:
        # Update status to running
        await db_service.update_scan_status(scan_id, "running")
        
        # Run scan
        auditor = CodeAuditor(AuditorConfig())
        results = auditor.scan(target_path)
        
        # Save results to database
        await db_service.save_issues(scan_id, results.issues)
        
        # Update scan with results
        await db_service.update_scan_status(
            scan_id, 
            "completed",
            summary=results.get_summary(),
            compliance_summary=getattr(results, 'compliance_summary', {}),
            detected_frameworks=getattr(results, 'detected_frameworks', {})
        )
        
    except Exception as e:
        await db_service.update_scan_status(scan_id, "failed")
        raise e
    finally:
        # Cleanup temp directory
        shutil.rmtree(target_path, ignore_errors=True)

@app.get("/api/scan/{scan_id}/results", response_model=ScanResultsResponse)
async def get_scan_results(
    scan_id: str,
    current_user = Depends(get_current_user)
):
    """Get scan results from database."""
    results = await db_service.get_scan_results(scan_id, current_user.id)
    
    if not results:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    scan = results['scan']
    issues = results['issues']
    
    return ScanResultsResponse(
        scan_id=scan_id,
        summary=scan['summary'],
        issues=[IssueModel(**issue) for issue in issues],
        compliance_summary=scan.get('compliance_summary', {}),
        detected_frameworks=scan.get('detected_frameworks', {})
    )

@app.get("/api/scans", response_model=List[ScanResponse])
async def get_user_scans(
    current_user = Depends(get_current_user)
):
    """Get user's scan history."""
    scans = await db_service.get_user_scans(current_user.id)
    return [ScanResponse(**scan) for scan in scans]
```

## 🎨 Frontend Integration

### 1. Supabase Client Setup

```javascript
// webapp/src/lib/supabase.js
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL
const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY

export const supabase = createClient(supabaseUrl, supabaseAnonKey)
```

### 2. Authentication Context

```javascript
// webapp/src/contexts/AuthContext.js
import React, { createContext, useContext, useEffect, useState } from 'react'
import { supabase } from '../lib/supabase'

const AuthContext = createContext({})

export const useAuth = () => {
  return useContext(AuthContext)
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Get initial session
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null)
      setLoading(false)
    })

    // Listen for auth changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      async (event, session) => {
        setUser(session?.user ?? null)
        setLoading(false)
      }
    )

    return () => subscription.unsubscribe()
  }, [])

  const signIn = async (email, password) => {
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password,
    })
    return { data, error }
  }

  const signUp = async (email, password, metadata = {}) => {
    const { data, error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: metadata
      }
    })
    return { data, error }
  }

  const signOut = async () => {
    const { error } = await supabase.auth.signOut()
    return { error }
  }

  const value = {
    user,
    signIn,
    signUp,
    signOut,
    loading
  }

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  )
}
```

### 3. Enhanced API Service

```javascript
// webapp/src/services/api.js (enhanced)
import { supabase } from '../lib/supabase'

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000'

// Get auth token for API requests
const getAuthToken = async () => {
  const { data: { session } } = await supabase.auth.getSession()
  return session?.access_token
}

// Enhanced API client with auth
const apiClient = async (endpoint, options = {}) => {
  const token = await getAuthToken()
  
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers,
    },
    ...options,
  }

  const response = await fetch(`${API_BASE}${endpoint}`, config)
  
  if (!response.ok) {
    throw new Error(`API Error: ${response.statusText}`)
  }
  
  return response.json()
}

export const uploadAndScan = async (files, config = {}) => {
  const token = await getAuthToken()
  const formData = new FormData()
  
  files.forEach(file => {
    formData.append('files', file)
  })
  
  if (Object.keys(config).length > 0) {
    formData.append('config', JSON.stringify(config))
  }

  const response = await fetch(`${API_BASE}/api/scan/upload`, {
    method: 'POST',
    headers: {
      ...(token && { Authorization: `Bearer ${token}` }),
    },
    body: formData,
  })

  if (!response.ok) {
    throw new Error(`Upload failed: ${response.statusText}`)
  }

  return response.json()
}

export const getScanResults = async (scanId) => {
  return apiClient(`/api/scan/${scanId}/results`)
}

export const getUserScans = async () => {
  return apiClient('/api/scans')
}

export const getScanStatus = async (scanId) => {
  return apiClient(`/api/scan/${scanId}/status`)
}
```

### 4. Authentication Components

```javascript
// webapp/src/components/Auth/LoginForm.js
import React, { useState } from 'react'
import { useAuth } from '../../contexts/AuthContext'
import { useNavigate } from 'react-router-dom'

const LoginForm = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  
  const { signIn } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    const { error } = await signIn(email, password)
    
    if (error) {
      setError(error.message)
    } else {
      navigate('/dashboard')
    }
    
    setLoading(false)
  }

  return (
    <div className="max-w-md mx-auto bg-white p-8 rounded-lg shadow-sm border border-gray-200">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Sign In</h2>
      
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-md p-3 mb-4">
          <p className="text-sm text-red-700">{error}</p>
        </div>
      )}
      
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Email
          </label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            required
          />
        </div>
        
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Password
          </label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            required
          />
        </div>
        
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? 'Signing In...' : 'Sign In'}
        </button>
      </form>
    </div>
  )
}

export default LoginForm
```

### 5. Protected Routes

```javascript
// webapp/src/components/ProtectedRoute.js
import React from 'react'
import { Navigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth()

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return user ? children : <Navigate to="/login" />
}

export default ProtectedRoute
```

## 🚀 Deployment Steps

### 1. Supabase Project Setup

1. **Create Supabase Project**: Go to [supabase.com](https://supabase.com) and create a new project
2. **Run Database Migrations**: Execute the SQL schema in the Supabase SQL editor
3. **Configure Storage**: Create a bucket named `vibeauditor-files`
4. **Set up Authentication**: Configure email/password authentication
5. **Configure RLS**: Enable and test Row Level Security policies

### 2. Environment Variables

Update your deployment with the Supabase credentials:

```bash
# Production environment variables
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
DATABASE_URL=postgresql://postgres:[password]@db.[project].supabase.co:5432/postgres
```

### 3. Real-time Features

```javascript
// Real-time scan updates
useEffect(() => {
  if (!scanId) return

  const subscription = supabase
    .channel('scan-updates')
    .on('postgres_changes', 
      { 
        event: 'UPDATE', 
        schema: 'public', 
        table: 'scans',
        filter: `id=eq.${scanId}`
      }, 
      (payload) => {
        setScanStatus(payload.new.status)
        if (payload.new.status === 'completed') {
          // Refresh results
          refetch()
        }
      }
    )
    .subscribe()

  return () => {
    subscription.unsubscribe()
  }
}, [scanId])
```

## 🎯 Benefits of Supabase Integration

### ✅ **User Management**
- Secure authentication and authorization
- User profiles and organization management
- Role-based access control

### ✅ **Data Persistence**
- Scan history and results storage
- Compliance tracking over time
- Issue management and resolution tracking

### ✅ **Scalability**
- PostgreSQL database with automatic scaling
- File storage for uploaded code
- Real-time updates and notifications

### ✅ **Security**
- Row Level Security (RLS) policies
- JWT-based authentication
- Encrypted data storage

### ✅ **Analytics**
- Compliance trends and reporting
- User activity tracking
- Audit logs for compliance

This integration transforms VibeCodeAuditor into a full-featured, enterprise-ready security auditing platform with user management, data persistence, and scalable architecture! 🚀