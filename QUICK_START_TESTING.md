# VibeCodeAuditor - Quick Start Testing

Get VibeCodeAuditor running in under 5 minutes for immediate testing!

## 🚀 Super Quick Start

### 1. Install Everything
```bash
# One command to install all dependencies
python3 quick_install.py
```

### 2. Configure Environment
```bash
# Edit the .env file with your Supabase credentials
nano .env

# Required: Update these lines
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here
```

### 3. Start Server
```bash
# Start the API server
python3 run_production.py
```

### 4. Test Everything
```bash
# In another terminal, test the API
python3 test_api_client.py
```

## 🧪 What Gets Tested

The quick install creates:
- **API Server**: FastAPI with security scanning endpoints
- **Security Scanners**: Bandit, Safety, Custom rules
- **Test Files**: Sample Python/JavaScript files with security issues
- **Database Integration**: Supabase connection for storing results

## 📋 Test Results

After running the tests, you should see:

✅ **Health Check**: API server responds  
✅ **File Upload**: Can upload files for scanning  
✅ **Security Scanning**: Detects hardcoded passwords, SQL injection, etc.  
✅ **Results Storage**: Issues saved to Supabase database  

## 🔧 Troubleshooting

### Server Won't Start
```bash
# Check Python version (need 3.8+)
python3 --version

# Install missing dependencies
pip install fastapi uvicorn supabase

# Check port availability
lsof -i :8000
```

### Database Connection Failed
```bash
# Verify Supabase credentials in .env
cat .env | grep SUPABASE

# Test connection manually
python3 -c "from vibeauditor.core.supabase_client import get_supabase_client; print('✅ Connected')"
```

### Security Tools Missing
```bash
# Install security scanners
pip install bandit safety
npm install -g eslint eslint-plugin-security

# Test tools
bandit --version
safety --version
```

## 📊 Example API Usage

### Health Check
```bash
curl http://localhost:8000/health
```

### Upload File for Scanning
```bash
curl -X POST "http://localhost:8000/scan" \
  -H "Authorization: Bearer your-token" \
  -F "file=@test_sample.py" \
  -F "user_id=test_user"
```

### Get Scan Results
```bash
curl "http://localhost:8000/scan/{scan_id}" \
  -H "Authorization: Bearer your-token"
```

## 🎯 What You'll See

The system will detect security issues like:

- **Hardcoded Passwords**: `password = "admin123"`
- **API Keys**: `api_key = "sk-1234567890"`
- **SQL Injection**: `f"SELECT * FROM users WHERE id = {user_id}"`
- **Command Injection**: `os.system(cmd)`
- **XSS Vulnerabilities**: `innerHTML = userInput`

## 🔄 Development Workflow

1. **Make Changes**: Edit code in `vibeauditor/`
2. **Test Changes**: Run `python3 test_production_setup.py`
3. **Restart Server**: Ctrl+C and `python3 run_production.py`
4. **Test API**: Run `python3 test_api_client.py`

## 📁 Project Structure

```
VibeCodeAuditor/
├── vibeauditor/           # Main application
│   ├── main.py           # FastAPI server
│   ├── core/             # Core modules
│   └── scanners/         # Security scanners
├── webapp/               # Frontend (React)
├── quick_install.py      # Quick setup script
├── run_production.py     # Simple server runner
├── test_api_client.py    # API testing
└── .env                  # Configuration
```

## 🚀 Next Steps

Once testing works:

1. **Frontend**: Set up the React webapp
2. **Production**: Use the full production setup
3. **Security**: Configure proper authentication
4. **Scaling**: Add more security scanners
5. **Deployment**: Deploy to your server

## 💡 Tips

- **Start Simple**: Use `run_production.py` for development
- **Test Often**: Run tests after each change  
- **Check Logs**: Look at console output for errors
- **Mock Mode**: Tests work even without Supabase
- **Sample Files**: Use provided test files to verify scanning

The system is designed to work out of the box with minimal configuration!