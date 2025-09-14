# 🚀 VibeCodeAuditor - Supabase Quick Start

## Step-by-Step Integration

### 1. **Create Supabase Project**

1. Go to [supabase.com](https://supabase.com) and create account
2. Click "New Project"
3. Choose organization and enter project details:
   - **Name**: `vibecodauditor`
   - **Database Password**: Generate strong password
   - **Region**: Choose closest to your users
4. Wait for project to be created (~2 minutes)

### 2. **Get Your Credentials**

From your Supabase dashboard:

1. Go to **Settings** → **API**
2. Copy these values:
   - **Project URL**: `https://your-project.supabase.co`
   - **anon public key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
   - **service_role secret key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

### 3. **Set Up Database Schema**

1. Go to **SQL Editor** in Supabase dashboard
2. Copy and paste the entire contents of `supabase_setup.sql`
3. Click **Run** to execute the schema
4. Verify tables were created in **Table Editor**

### 4. **Configure Environment Variables**

Create/update `.env` file in project root:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here

# Database URL (from Supabase Settings → Database)
DATABASE_URL=postgresql://postgres:[password]@db.[project].supabase.co:5432/postgres
```

Create/update `webapp/.env` file:

```env
REACT_APP_SUPABASE_URL=https://your-project.supabase.co
REACT_APP_SUPABASE_ANON_KEY=your-anon-key-here
```

### 5. **Set Up File Storage**

1. Go to **Storage** in Supabase dashboard
2. Click **Create Bucket**
3. Name: `vibeauditor-files`
4. Make it **Private** (not public)
5. Click **Create Bucket**

### 6. **Install Dependencies**

Backend:
```bash
pip install supabase python-dotenv
```

Frontend:
```bash
cd webapp
npm install @supabase/supabase-js @supabase/auth-ui-react
```

### 7. **Test the Integration**

Run this test script:

```python
# test_supabase_connection.py
import os
from dotenv import load_dotenv
from vibeauditor.database.supabase_client import supabase_client

load_dotenv()

def test_supabase():
    print("🔍 Testing Supabase Connection")
    print("=" * 40)
    
    # Check if client is available
    if not supabase_client.is_available():
        print("❌ Supabase client not available")
        print("💡 Check your environment variables:")
        print(f"   SUPABASE_URL: {os.getenv('SUPABASE_URL', 'Not set')}")
        print(f"   SUPABASE_SERVICE_ROLE_KEY: {'Set' if os.getenv('SUPABASE_SERVICE_ROLE_KEY') else 'Not set'}")
        return False
    
    # Test connection
    if supabase_client.test_connection():
        print("✅ Database connection successful!")
        return True
    else:
        print("❌ Database connection failed")
        return False

if __name__ == "__main__":
    test_supabase()
```

### 8. **Enable Authentication**

1. Go to **Authentication** → **Settings** in Supabase
2. Configure **Site URL**: `http://localhost:3000` (for development)
3. Add **Redirect URLs**: 
   - `http://localhost:3000/auth/callback`
   - `https://yourdomain.com/auth/callback` (for production)
4. Enable **Email** provider
5. Configure **SMTP** settings (or use Supabase's built-in email)

### 9. **Update Your App**

Wrap your React app with the AuthProvider:

```javascript
// webapp/src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { AuthProvider } from './contexts/AuthContext';
import Results from './pages/Results';
import LoginForm from './components/Auth/LoginForm';
import ProtectedRoute from './components/ProtectedRoute';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <Router>
          <div className="App">
            <Routes>
              <Route path="/login" element={<LoginForm />} />
              <Route 
                path="/results/:scanId" 
                element={
                  <ProtectedRoute>
                    <Results />
                  </ProtectedRoute>
                } 
              />
              {/* Add more routes */}
            </Routes>
          </div>
        </Router>
      </AuthProvider>
    </QueryClientProvider>
  );
}

export default App;
```

### 10. **Test Authentication**

1. Start your React app: `npm start`
2. Go to `/login`
3. Try signing up with an email
4. Check Supabase **Authentication** → **Users** to see the new user
5. Check **Table Editor** → **profiles** to see the profile was created

## 🎯 What You Get

### ✅ **User Management**
- Secure email/password authentication
- User profiles with organization info
- Password reset functionality

### ✅ **Data Persistence**
- All scan results stored in PostgreSQL
- Issue tracking and management
- Compliance history and trends

### ✅ **File Storage**
- Uploaded code files stored securely
- Automatic cleanup and organization
- Access control per user

### ✅ **Real-time Updates**
- Live scan progress updates
- Real-time notifications
- Collaborative issue management

### ✅ **Security**
- Row Level Security (RLS) policies
- JWT-based authentication
- Encrypted data storage

## 🚨 Common Issues & Solutions

### Issue: "Invalid JWT"
**Solution**: Check that your `SUPABASE_ANON_KEY` is correct and not the service role key

### Issue: "relation 'profiles' does not exist"
**Solution**: Make sure you ran the `supabase_setup.sql` script in the SQL Editor

### Issue: "Row Level Security policy violation"
**Solution**: Ensure RLS policies are set up correctly and user is authenticated

### Issue: "Storage bucket not found"
**Solution**: Create the `vibeauditor-files` bucket in Supabase Storage

## 🚀 Next Steps

1. **Deploy to Production**: Update environment variables for production
2. **Configure Custom Domain**: Set up custom domain in Supabase
3. **Set up Monitoring**: Enable logging and monitoring
4. **Add Team Features**: Implement organization-based access control
5. **Set up Backups**: Configure automated database backups

Your VibeCodeAuditor is now integrated with Supabase! 🎉

## 📞 Need Help?

- **Supabase Docs**: [supabase.com/docs](https://supabase.com/docs)
- **Discord**: [discord.supabase.com](https://discord.supabase.com)
- **GitHub Issues**: Create an issue in your repository

The integration provides enterprise-grade user management, data persistence, and scalability for your security auditing platform!