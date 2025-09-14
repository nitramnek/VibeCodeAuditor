#!/usr/bin/env python3
"""
Reproduce the upload error to test the fix
"""

import os
import sys
import requests
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv()

def test_upload_endpoint():
    """Test the /scan endpoint that was failing"""

    # Create a simple test file
    test_file_path = "test_sample.py"
    with open(test_file_path, 'w') as f:
        f.write("# Test Python file\nprint('Hello World')\n")

    try:
        # Prepare the upload request
        url = "http://localhost:8000/scan"

        with open(test_file_path, 'rb') as f:
            files = {'file': ('test_sample.py', f, 'text/plain')}
            data = {'user_id': 'test-user-123'}

            print("📤 Sending upload request...")
            response = requests.post(url, files=files, data=data, timeout=30)

            print(f"📊 Response Status: {response.status_code}")
            print(f"📝 Response: {response.text}")

            if response.status_code == 200:
                print("✅ Upload successful!")
                return True
            else:
                print("❌ Upload failed!")
                return False

    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")
        return False
    finally:
        # Clean up test file
        if os.path.exists(test_file_path):
            os.remove(test_file_path)

if __name__ == '__main__':
    print('🧪 Testing Upload Endpoint')
    print('=' * 30)

    success = test_upload_endpoint()

    if success:
        print('\n✅ Upload test passed!')
    else:
        print('\n❌ Upload test failed - issue persists')
