# 🚀 VibeCodeAuditor - Quick Start Guide

## Step 1: Start the API Server

```bash
# From the project root directory
python start_server.py
```

You should see:
```
🚀 VibeCodeAuditor Server Startup
========================================
🧪 Testing imports...
✅ All imports successful
🌐 Starting server on http://localhost:8000
📚 API docs will be available at http://localhost:8000/api/docs
🔧 Press Ctrl+C to stop
```

**Keep this terminal open!** The API server needs to stay running.

## Step 2: Test the API (Optional but Recommended)

Open a new terminal and run:
```bash
python test_api.py
```

You should see all tests pass:
```
🧪 VibeCodeAuditor API Test Suite
========================================
✅ Health Check PASSED
✅ Rules Endpoint PASSED
✅ Config Endpoint PASSED
✅ File Upload PASSED
📊 Test Results: 4/4 tests passed
🎉 All API tests passed!
```

## Step 3: Start the Web App

Open another new terminal and run:
```bash
# Navigate to webapp directory
cd webapp

# Install dependencies (first time only)
npm install

# Start the React development server
npm start
```

The webapp will automatically open in your browser at `http://localhost:3000`.

## 🎯 What You Should See:

1. **API Server**: Running on http://localhost:8000
2. **Web App**: Running on http://localhost:3000
3. **API Docs**: Available at http://localhost:8000/api/docs

## 🔧 Troubleshooting:

### If npm install fails:
```bash
cd webapp
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

### If you get CORS errors:
Make sure both servers are running on the correct ports:
- API: http://localhost:8000
- Web App: http://localhost:3000

### If the web app can't connect to API:
Check that the API server is running and accessible at http://localhost:8000/api/health

## 🧪 Test the Full System:

1. Open http://localhost:3000
2. Click "Start New Scan"
3. Upload the sample file: `examples/sample_vulnerable_code.py`
4. Watch the real-time scan progress
5. View the detailed results with security issues found

## 🎉 You're Ready!

Your VibeCodeAuditor PWA is now fully functional with:
- ✅ Real-time code scanning
- ✅ Security vulnerability detection
- ✅ AI/ML specific checks
- ✅ Interactive web interface
- ✅ Detailed remediation guidance

---

**Need help?** Check the logs in both terminals for any error messages.