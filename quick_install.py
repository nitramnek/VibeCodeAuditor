#!/usr/bin/env python3
"""
Quick installation script for VibeCodeAuditor testing.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, description=""):
    """Run a command and handle errors."""
    print(f"🔧 {description}")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"   ✅ Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ⚠️  Warning: {e}")
        print(f"   Output: {e.stdout}")
        print(f"   Error: {e.stderr}")
        return False

def check_python_version():
    """Check Python version."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def install_python_deps():
    """Install Python dependencies."""
    print("📦 Installing Python dependencies...")
    
    # Core dependencies
    deps = [
        "fastapi==0.104.1",
        "uvicorn[standard]==0.24.0", 
        "supabase==2.0.2",
        "python-multipart==0.0.6",
        "python-jose[cryptography]==3.3.0",
        "passlib[bcrypt]==1.7.4",
        "aiofiles==23.2.1",
        "python-dotenv==1.0.0",
        "pydantic==2.5.0"
    ]
    
    for dep in deps:
        run_command(f"pip install {dep}", f"Installing {dep.split('==')[0]}")
    
    # Security tools
    security_tools = ["bandit", "safety"]
    for tool in security_tools:
        run_command(f"pip install {tool}", f"Installing {tool}")

def install_node_deps():
    """Install Node.js dependencies if available."""
    if shutil.which("npm"):
        print("📦 Installing Node.js security tools...")
        tools = ["eslint", "eslint-plugin-security"]
        for tool in tools:
            run_command(f"npm install -g {tool}", f"Installing {tool}")
    else:
        print("⚠️  npm not found, skipping JavaScript tools")

def setup_directories():
    """Create necessary directories."""
    print("📁 Creating directories...")
    dirs = ["logs", "uploads", "temp", "backups"]
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"   ✅ Created {dir_name}/")

def setup_env_file():
    """Set up environment file."""
    print("⚙️  Setting up environment...")
    
    if not Path(".env").exists():
        if Path(".env.template").exists():
            shutil.copy(".env.template", ".env")
            print("   ✅ Created .env from template")
            print("   ⚠️  Please update .env with your Supabase credentials!")
        else:
            print("   ❌ No .env.template found")
    else:
        print("   ✅ .env already exists")

def create_test_files():
    """Create test files for scanning."""
    print("📝 Creating test files...")
    
    # Python test file with security issues
    test_py = Path("test_sample.py")
    test_py.write_text('''
# Test file with security issues for VibeCodeAuditor

import os
import subprocess

# Security issue: hardcoded password
password = "admin123"
api_key = "sk-1234567890abcdef"

# Security issue: SQL injection vulnerability  
def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return query

# Security issue: command injection
def run_command(cmd):
    os.system(cmd)

# Security issue: insecure random
import random
token = random.randint(1000, 9999)

print("This is a test file for security scanning")
''')
    print("   ✅ Created test_sample.py")
    
    # JavaScript test file
    test_js = Path("test_sample.js")
    test_js.write_text('''
// Test JavaScript file with security issues

const password = "secret123";
const apiKey = "abc-def-123";

// XSS vulnerability
function updateContent(userInput) {
    document.getElementById("content").innerHTML = userInput;
}

// Eval usage
function executeCode(code) {
    eval(code);
}

console.log("Test JavaScript file");
''')
    print("   ✅ Created test_sample.js")

def main():
    """Main installation process."""
    print("🚀 VibeCodeAuditor Quick Installation\n")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    install_python_deps()
    install_node_deps()
    
    # Setup environment
    setup_directories()
    setup_env_file()
    create_test_files()
    
    print("\n" + "="*50)
    print("✅ Installation Complete!")
    print("="*50)
    print("\nNext steps:")
    print("1. Update .env with your Supabase credentials")
    print("2. Test the setup: python3 test_production_setup.py")
    print("3. Start the server: python3 run_production.py")
    print("4. Test with sample files: test_sample.py, test_sample.js")
    print("\nAPI will be available at: http://localhost:8000")
    print("Health check: curl http://localhost:8000/health")

if __name__ == "__main__":
    main()