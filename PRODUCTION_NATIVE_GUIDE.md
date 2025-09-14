# VibeCodeAuditor Native Production Setup

This guide helps you deploy VibeCodeAuditor in production without Docker.

## Quick Start

### 1. Prerequisites

Make sure you have:
- Ubuntu/Debian Linux system
- Python 3.8+
- Node.js 16+
- Supabase account with database setup

### 2. Automated Setup (Recommended)

Run the automated setup script:

```bash
# Make script executable
chmod +x setup_production_native.sh

# Run setup (will install all dependencies)
./setup_production_native.sh
```

This script will:
- Install all system dependencies
- Set up Python virtual environment
- Install security scanning tools (Bandit, Semgrep, ESLint, etc.)
- Configure nginx and systemd services
- Create production configuration files

### 3. Manual Configuration

After setup, update your environment variables:

```bash
# Edit the production environment file
nano .env.production

# Update these required values:
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

### 4. Start Production Services

```bash
# Start all services
./start_production.sh

# Or start manually
sudo systemctl start vibeauditor
sudo systemctl start nginx
```

## Alternative: Simple Python Runner

If you prefer a simpler setup without systemd/nginx:

### 1. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements-production.txt

# Install security tools
pip install bandit safety semgrep
npm install -g eslint eslint-plugin-security
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.template .env

# Edit with your Supabase credentials
nano .env
```

### 3. Run Simple Server

```bash
# Run the simple production server
python3 run_production.py
```

This will:
- Check all dependencies
- Install missing security tools
- Start the API server on http://localhost:8000

## Security Tools Included

The production setup includes these security scanners:

- **Bandit**: Python security linter
- **Semgrep**: Multi-language static analysis
- **ESLint Security**: JavaScript/TypeScript security rules
- **Safety**: Python dependency vulnerability scanner
- **Custom Rules**: Pattern-based security checks

## Production Features

✅ **Security Scanning**: Multi-tool integration for comprehensive analysis  
✅ **Database Integration**: Full Supabase integration with RLS  
✅ **File Upload**: Secure file handling with size/type validation  
✅ **Authentication**: JWT-based user authentication  
✅ **Rate Limiting**: API rate limiting for production use  
✅ **Logging**: Structured logging with rotation  
✅ **Error Handling**: Comprehensive error handling and reporting  
✅ **CORS**: Configurable CORS for web integration  

## API Endpoints

- `GET /health` - Health check
- `POST /scan` - Upload file and start scan
- `GET /scan/{scan_id}` - Get scan results
- `GET /scans?user_id={user_id}` - List user scans

## Monitoring & Logs

```bash
# View API server logs
journalctl -u vibeauditor -f

# View nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Check service status
sudo systemctl status vibeauditor
sudo systemctl status nginx
```

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Check what's using port 8000
   sudo lsof -i :8000
   
   # Change port in .env.production
   PORT=8001
   ```

2. **Permission denied**
   ```bash
   # Fix file permissions
   chmod +x *.sh
   sudo chown -R $USER:$USER ~/vibeauditor-prod
   ```

3. **Supabase connection failed**
   - Verify SUPABASE_URL and keys in .env
   - Check database schema is properly set up
   - Ensure RLS policies are configured

4. **Security tools not found**
   ```bash
   # Reinstall security tools
   pip install bandit safety semgrep
   npm install -g eslint eslint-plugin-security
   ```

### Performance Tuning

For high-traffic production:

1. **Increase workers**
   ```bash
   # In .env.production
   WORKERS=4
   ```

2. **Configure nginx caching**
   ```bash
   # Add to nginx config
   proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=api_cache:10m;
   ```

3. **Database connection pooling**
   ```bash
   # In .env.production
   DB_MAX_CONNECTIONS=50
   ```

## Security Considerations

- Change default JWT_SECRET in production
- Configure proper CORS origins
- Set up SSL/TLS certificates
- Enable firewall rules
- Regular security updates
- Database backups
- Log monitoring

## Support

For issues or questions:
1. Check the logs first
2. Verify environment configuration
3. Test with simple files
4. Check Supabase connectivity

The system is designed to be robust and provide detailed error messages to help with troubleshooting.