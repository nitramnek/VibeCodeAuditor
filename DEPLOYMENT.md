# VibeCodeAuditor Deployment Guide 🚀

This guide covers various deployment options for VibeCodeAuditor, from local development to production cloud deployments.

## 🏠 Local Development

### Quick Start
```bash
# Clone and setup
git clone <repository-url>
cd VibeCodeAuditor

# Setup development environment
make dev-setup

# Test with sample code
make demo

# Start web interface
make serve
```

### Manual Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Test basic functionality
python test_basic_functionality.py

# Start development server
python run_server.py
```

## 🐳 Docker Deployment

### Basic Docker Setup
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Run application
CMD ["python", "-m", "vibeauditor", "serve", "--host", "0.0.0.0", "--port", "8000"]
```

### Build and Run
```bash
# Build image
docker build -t vibeauditor:latest .

# Run container
docker run -p 8000:8000 vibeauditor:latest

# Run with volume for persistent data
docker run -p 8000:8000 -v $(pwd)/data:/app/data vibeauditor:latest
```

### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  vibeauditor:
    build: .
    ports:
      - "8000:8000"
    environment:
      - PYTHONPATH=/app
    volumes:
      - ./data:/app/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - vibeauditor
    restart: unless-stopped
```

## ☁️ Cloud Deployments

### AWS Deployment

#### AWS ECS (Elastic Container Service)
```json
{
  "family": "vibeauditor",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::ACCOUNT:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "vibeauditor",
      "image": "your-account.dkr.ecr.region.amazonaws.com/vibeauditor:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "essential": true,
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/vibeauditor",
          "awslogs-region": "us-west-2",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

#### AWS Lambda (Serverless)
```python
# lambda_handler.py
import json
from mangum import Mangum
from vibeauditor.api.main import app

handler = Mangum(app)
```

### Google Cloud Platform

#### Cloud Run
```yaml
# cloudbuild.yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/vibeauditor', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/vibeauditor']
  - name: 'gcr.io/cloud-builders/gcloud'
    args:
      - 'run'
      - 'deploy'
      - 'vibeauditor'
      - '--image'
      - 'gcr.io/$PROJECT_ID/vibeauditor'
      - '--region'
      - 'us-central1'
      - '--platform'
      - 'managed'
      - '--allow-unauthenticated'
```

### Microsoft Azure

#### Azure Container Instances
```bash
# Deploy to Azure Container Instances
az container create \
  --resource-group myResourceGroup \
  --name vibeauditor \
  --image myregistry.azurecr.io/vibeauditor:latest \
  --cpu 1 \
  --memory 1 \
  --ports 8000 \
  --dns-name-label vibeauditor-app \
  --environment-variables PYTHONPATH=/app
```

## 🔧 Production Configuration

### Environment Variables
```bash
# Production environment variables
export PYTHONPATH=/app
export VIBEAUDITOR_ENV=production
export VIBEAUDITOR_LOG_LEVEL=info
export VIBEAUDITOR_MAX_UPLOAD_SIZE=100MB
export VIBEAUDITOR_CORS_ORIGINS="https://yourdomain.com"
export VIBEAUDITOR_SECRET_KEY="your-secret-key"
```

### Nginx Configuration
```nginx
# nginx.conf
upstream vibeauditor {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    client_max_body_size 100M;

    location / {
        proxy_pass http://vibeauditor;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /ws/ {
        proxy_pass http://vibeauditor;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Production Startup Script
```bash
#!/bin/bash
# start_production.sh

set -e

echo "🚀 Starting VibeCodeAuditor in production mode..."

# Set production environment
export PYTHONPATH=/app
export VIBEAUDITOR_ENV=production

# Start with Gunicorn for production
exec gunicorn vibeauditor.api.main:app \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    --timeout 120 \
    --keep-alive 2 \
    --max-requests 1000 \
    --max-requests-jitter 50
```

## 📊 Monitoring and Logging

### Health Checks
```python
# Add to vibeauditor/api/main.py
@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": "0.1.0"
    }

@app.get("/api/metrics")
async def metrics():
    return {
        "active_scans": len(active_scans),
        "total_scans": get_total_scans(),
        "uptime": get_uptime()
    }
```

### Logging Configuration
```python
# logging_config.py
import logging
import sys

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('/app/logs/vibeauditor.log')
        ]
    )
```

## 🔒 Security Considerations

### Production Security Checklist
- [ ] Use HTTPS in production
- [ ] Set secure CORS origins
- [ ] Implement rate limiting
- [ ] Use secure session management
- [ ] Regular security updates
- [ ] Monitor for vulnerabilities
- [ ] Implement proper authentication
- [ ] Use secrets management
- [ ] Enable audit logging
- [ ] Regular backups

### Rate Limiting
```python
# Add to requirements.txt
slowapi==0.1.9

# Add to vibeauditor/api/main.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/scan/upload")
@limiter.limit("5/minute")
async def upload_and_scan(request: Request, ...):
    # Implementation
```

## 🚀 CI/CD Pipeline

### GitHub Actions
```yaml
# .github/workflows/deploy.yml
name: Deploy VibeCodeAuditor

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: |
          python test_basic_functionality.py
          python tests/test_ai_ml_rules.py
          vibeauditor ai-scan --model-format ONNX --validation-tier production

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to production
        run: |
          # Your deployment script here
          echo "Deploying to production..."
```

## 📈 Scaling Considerations

### Horizontal Scaling
- Use load balancers (nginx, AWS ALB, etc.)
- Implement stateless design
- Use Redis for session storage
- Consider microservices architecture

### Performance Optimization
- Enable gzip compression
- Use CDN for static assets
- Implement caching strategies
- Optimize database queries
- Use async processing for large scans

### Resource Requirements
- **Minimum**: 1 CPU, 512MB RAM
- **Recommended**: 2 CPU, 2GB RAM
- **High Load**: 4+ CPU, 4GB+ RAM
- **Storage**: 10GB+ for logs and temporary files

## 🆘 Troubleshooting

### Common Issues
1. **Port already in use**: Change port with `--port` flag
2. **Permission denied**: Check file permissions
3. **Module not found**: Ensure PYTHONPATH is set
4. **Memory issues**: Increase container memory limits
5. **WebSocket connection failed**: Check firewall/proxy settings

### Debug Mode
```bash
# Enable debug logging
export VIBEAUDITOR_LOG_LEVEL=debug
python -m vibeauditor serve --reload
```

### Health Check Commands
```bash
# Check API health
curl http://localhost:8000/api/health

# Check WebSocket connection
wscat -c ws://localhost:8000/ws/test-scan-id

# Monitor logs
tail -f /app/logs/vibeauditor.log
```

---

For more deployment options and advanced configurations, check the [documentation](README.md) or open an issue on GitHub.