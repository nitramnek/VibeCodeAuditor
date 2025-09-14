#!/bin/bash

# VibeCodeAuditor Native Production Setup
# This script sets up the production environment without Docker

set -e

echo "🚀 Setting up VibeCodeAuditor for native production deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root for security reasons"
   exit 1
fi

# Create production directories
print_status "Creating production directories..."
mkdir -p ~/vibeauditor-prod/{logs,uploads,temp,backups}
mkdir -p ~/.local/bin

# Update system packages
print_status "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install system dependencies
print_status "Installing system dependencies..."
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    nodejs \
    npm \
    git \
    curl \
    wget \
    unzip \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    nginx \
    supervisor \
    postgresql-client

# Install Node.js 18+ (required for modern tools)
print_status "Installing Node.js 18..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Create Python virtual environment
print_status "Creating Python virtual environment..."
cd ~/vibeauditor-prod
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install --upgrade pip
pip install \
    fastapi \
    uvicorn \
    supabase \
    python-multipart \
    python-jose[cryptography] \
    passlib[bcrypt] \
    aiofiles \
    pydantic \
    requests \
    asyncio \
    bandit \
    safety \
    semgrep

# Install security scanning tools
print_status "Installing security scanning tools..."

# Install Bandit (Python security scanner)
pip install bandit[toml]

# Install Safety (Python dependency scanner)
pip install safety

# Install Semgrep
pip install semgrep

# Install ESLint and security plugins globally
print_status "Installing ESLint security tools..."
sudo npm install -g \
    eslint \
    eslint-plugin-security \
    eslint-plugin-node \
    @typescript-eslint/parser \
    @typescript-eslint/eslint-plugin

# Install additional security tools
print_status "Installing additional security tools..."

# Install CodeQL CLI (optional but powerful)
if ! command -v codeql &> /dev/null; then
    print_status "Installing CodeQL CLI..."
    cd /tmp
    wget -q https://github.com/github/codeql-action/releases/latest/download/codeql-bundle-linux64.tar.gz
    tar -xzf codeql-bundle-linux64.tar.gz
    sudo mv codeql ~/.local/bin/
    export PATH="$HOME/.local/bin/codeql:$PATH"
fi

# Install Trivy (vulnerability scanner)
if ! command -v trivy &> /dev/null; then
    print_status "Installing Trivy..."
    sudo apt-get install wget apt-transport-https gnupg lsb-release
    wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
    echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | sudo tee -a /etc/apt/sources.list.d/trivy.list
    sudo apt-get update
    sudo apt-get install trivy
fi

# Copy project files
print_status "Copying project files..."
cd ~/vibeauditor-prod
if [ -d "$OLDPWD" ]; then
    cp -r "$OLDPWD"/* . 2>/dev/null || true
    cp -r "$OLDPWD"/.env . 2>/dev/null || true
fi

# Install project Python dependencies
if [ -f "requirements.txt" ]; then
    print_status "Installing project Python dependencies..."
    pip install -r requirements.txt
fi

# Install project Node.js dependencies
if [ -f "webapp/package.json" ]; then
    print_status "Installing webapp dependencies..."
    cd webapp
    npm install
    npm run build
    cd ..
fi

# Create production environment file
print_status "Creating production environment configuration..."
cat > .env.production << EOF
# Production Environment Configuration
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# Server Configuration
HOST=0.0.0.0
PORT=8000
WORKERS=4

# Database Configuration (Update with your Supabase details)
DATABASE_URL=postgresql://your-supabase-url
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# Security Configuration
JWT_SECRET=$(openssl rand -base64 32)
JWT_ALGORITHM=HS256
JWT_EXPIRATION=3600
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
MAX_FILE_SIZE=10485760
RATE_LIMIT_PER_MINUTE=60

# Scanner Configuration
ENABLED_SCANNERS=bandit,semgrep,eslint_security,safety,custom_rules
SCANNER_TIMEOUT=30
MAX_CONCURRENT_SCANS=5
TEMP_DIR=$HOME/vibeauditor-prod/temp

# Storage Configuration
STORAGE_TYPE=local
STORAGE_LOCAL_PATH=$HOME/vibeauditor-prod/uploads
STORAGE_RETENTION_DAYS=30

# Notification Configuration
EMAIL_ENABLED=false
WEBHOOK_URL=
EOF

# Create systemd service file
print_status "Creating systemd service..."
sudo tee /etc/systemd/system/vibeauditor.service > /dev/null << EOF
[Unit]
Description=VibeCodeAuditor API Server
After=network.target

[Service]
Type=exec
User=$USER
Group=$USER
WorkingDirectory=$HOME/vibeauditor-prod
Environment=PATH=$HOME/vibeauditor-prod/venv/bin
EnvironmentFile=$HOME/vibeauditor-prod/.env.production
ExecStart=$HOME/vibeauditor-prod/venv/bin/uvicorn vibeauditor.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Create nginx configuration
print_status "Creating nginx configuration..."
sudo tee /etc/nginx/sites-available/vibeauditor << EOF
server {
    listen 80;
    server_name localhost;  # Change to your domain

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

    # API proxy
    location /api/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
        
        # File upload size limit
        client_max_body_size 10M;
    }

    # Serve static files
    location / {
        root $HOME/vibeauditor-prod/webapp/build;
        try_files \$uri \$uri/ /index.html;
        
        # Cache static assets
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }

    # Security: deny access to sensitive files
    location ~ /\. {
        deny all;
    }
    
    location ~ /(\.env|config\.yaml|requirements\.txt)$ {
        deny all;
    }
}
EOF

# Enable nginx site
sudo ln -sf /etc/nginx/sites-available/vibeauditor /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Create startup script
print_status "Creating startup script..."
cat > start_production.sh << 'EOF'
#!/bin/bash

# VibeCodeAuditor Production Startup Script

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Starting VibeCodeAuditor Production Environment...${NC}"

# Load environment
source .env.production
export $(cat .env.production | grep -v '^#' | xargs)

# Activate virtual environment
source venv/bin/activate

# Start services
echo -e "${GREEN}Starting API server...${NC}"
sudo systemctl start vibeauditor
sudo systemctl enable vibeauditor

echo -e "${GREEN}Starting nginx...${NC}"
sudo systemctl start nginx
sudo systemctl enable nginx

# Check status
echo -e "${BLUE}Service Status:${NC}"
sudo systemctl status vibeauditor --no-pager -l
sudo systemctl status nginx --no-pager -l

echo -e "${GREEN}✅ VibeCodeAuditor is running!${NC}"
echo -e "${BLUE}API Server: http://localhost:8000${NC}"
echo -e "${BLUE}Web Interface: http://localhost${NC}"
echo -e "${BLUE}Logs: journalctl -u vibeauditor -f${NC}"
EOF

chmod +x start_production.sh

# Create stop script
cat > stop_production.sh << 'EOF'
#!/bin/bash

echo "Stopping VibeCodeAuditor Production Environment..."

sudo systemctl stop vibeauditor
sudo systemctl stop nginx

echo "✅ Services stopped"
EOF

chmod +x stop_production.sh

# Create log rotation
print_status "Setting up log rotation..."
sudo tee /etc/logrotate.d/vibeauditor << EOF
$HOME/vibeauditor-prod/logs/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 $USER $USER
}
EOF

# Test nginx configuration
print_status "Testing nginx configuration..."
sudo nginx -t

print_success "✅ Native production setup completed!"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "1. Update .env.production with your actual Supabase credentials"
echo "2. Run: ./start_production.sh"
echo "3. Access your application at http://localhost"
echo ""
echo -e "${BLUE}Useful commands:${NC}"
echo "• Start: ./start_production.sh"
echo "• Stop: ./stop_production.sh"
echo "• Logs: journalctl -u vibeauditor -f"
echo "• Status: sudo systemctl status vibeauditor"
echo ""
echo -e "${YELLOW}Remember to:${NC}"
echo "• Configure your firewall"
echo "• Set up SSL/TLS certificates for production"
echo "• Update CORS_ORIGINS in .env.production"
echo "• Backup your database regularly"