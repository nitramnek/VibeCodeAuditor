#!/bin/bash
echo "🧪 Testing VibeCodeAuditor API with curl"
echo "========================================"

echo ""
echo "1. Testing health endpoint..."
curl -X GET http://localhost:8000/health -w "\nStatus: %{http_code}\n" -s

echo ""
echo "2. Testing upload endpoint (should require auth)..."
curl -X POST http://localhost:8000/scan \
  -F "file=@test_file.py" \
  -F "user_id=test-user" \
  -w "\nStatus: %{http_code}\n" -s

echo ""
echo "✅ Curl tests complete"