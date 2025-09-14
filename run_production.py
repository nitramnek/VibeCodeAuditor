#!/usr/bin/env python3
"""
VibeCodeAuditor Production Runner
Simple production server without Docker dependency.
"""

import os
import sys
import subprocess
import signal
import time
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_dependencies():
    """Check if all required dependencies are installed."""
    required_commands = [
        ("python3", "Python 3 is required"),
        ("node", "Node.js is required for ESLint"),
        ("npm", "npm is required for JavaScript tools"),
    ]
    
    missing = []
    for cmd, desc in required_commands:
        if subprocess.run(["which", cmd], capture_output=True).returncode != 0:
            missing.append(desc)
    
    if missing:
        logger.error("Missing dependencies:")
        for dep in missing:
            logger.error(f"  - {dep}")
        return False
    
    return True

def install_security_tools():
    """Install security scanning tools."""
    logger.info("Installing security scanning tools...")
    
    # Install Python tools
    python_tools = [
        "bandit[toml]",
        "safety", 
        "semgrep"
    ]
    
    for tool in python_tools:
        logger.info(f"Installing {tool}...")
        result = subprocess.run([sys.executable, "-m", "pip", "install", tool], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            logger.warning(f"Failed to install {tool}: {result.stderr}")
    
    # Install Node.js tools globally
    node_tools = [
        "eslint",
        "eslint-plugin-security",
        "@typescript-eslint/parser",
        "@typescript-eslint/eslint-plugin"
    ]
    
    for tool in node_tools:
        logger.info(f"Installing {tool}...")
        result = subprocess.run(["npm", "install", "-g", tool], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            logger.warning(f"Failed to install {tool}: {result.stderr}")

def setup_environment():
    """Setup production environment."""
    logger.info("Setting up production environment...")
    
    # Create necessary directories
    dirs = ["logs", "uploads", "temp", "backups"]
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
        logger.info(f"Created directory: {dir_name}")
    
    # Check for .env file
    if not Path(".env").exists():
        logger.warning("No .env file found. Creating template...")
        create_env_template()

def create_env_template():
    """Create a template .env file."""
    template = """# VibeCodeAuditor Environment Configuration
# Copy this to .env and update with your actual values

# Environment
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# Server
HOST=0.0.0.0
PORT=8000

# Supabase Configuration (REQUIRED - Update these!)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here

# Security
JWT_SECRET=your-jwt-secret-change-this-in-production
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com

# Scanner Configuration
ENABLED_SCANNERS=bandit,semgrep,eslint_security,safety,custom_rules
TEMP_DIR=./temp
"""
    
    with open(".env.template", "w") as f:
        f.write(template)
    
    logger.info("Created .env.template - please copy to .env and update with your values")

def start_server():
    """Start the production server."""
    logger.info("Starting VibeCodeAuditor production server...")
    
    # Load environment variables
    if Path(".env").exists():
        from dotenv import load_dotenv
        load_dotenv()
    
    # Get configuration
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    workers = int(os.getenv("WORKERS", "1"))
    
    # Start server with uvicorn
    cmd = [
        sys.executable, "-m", "uvicorn",
        "vibeauditor.main:app",
        "--host", host,
        "--port", str(port),
        "--workers", str(workers),
        "--log-level", "info"
    ]
    
    logger.info(f"Starting server: {' '.join(cmd)}")
    logger.info(f"Server will be available at: http://{host}:{port}")
    
    try:
        # Start the server
        process = subprocess.Popen(cmd)
        
        # Handle shutdown gracefully
        def signal_handler(signum, frame):
            logger.info("Shutting down server...")
            process.terminate()
            process.wait()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Wait for the process
        process.wait()
        
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        return False
    
    return True

def main():
    """Main entry point."""
    logger.info("🚀 VibeCodeAuditor Production Setup")
    
    # Check dependencies
    if not check_dependencies():
        logger.error("❌ Dependency check failed")
        sys.exit(1)
    
    # Install security tools
    install_security_tools()
    
    # Setup environment
    setup_environment()
    
    # Check for required environment variables
    required_env = ["SUPABASE_URL", "SUPABASE_ANON_KEY"]
    missing_env = [var for var in required_env if not os.getenv(var)]
    
    if missing_env:
        logger.error("❌ Missing required environment variables:")
        for var in missing_env:
            logger.error(f"  - {var}")
        logger.error("Please update your .env file with the required values")
        sys.exit(1)
    
    # Start server
    logger.info("✅ All checks passed. Starting server...")
    if start_server():
        logger.info("✅ Server started successfully")
    else:
        logger.error("❌ Server failed to start")
        sys.exit(1)

if __name__ == "__main__":
    main()