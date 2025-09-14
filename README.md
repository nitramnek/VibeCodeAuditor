# VibeCodeAuditor 🛡️

A comprehensive **Progressive Web App (PWA)** for code auditing designed to help AI developers build secure, maintainable, and high-quality applications. VibeCodeAuditor analyzes codebases for security vulnerabilities, code quality issues, and adherence to best practices with real-time feedback and modern web interface.

## ✨ Features

### 🔒 Security Analysis
- **Vulnerability Detection**: SQL injection, XSS, insecure dependencies
- **Secret Scanning**: Hardcoded API keys, passwords, tokens
- **AI/ML Security**: Model loading security, data privacy checks

### 📊 Code Quality
- **Quality Metrics**: Code complexity, function length, maintainability
- **Best Practices**: Industry standards compliance
- **Dead Code Detection**: Unreachable code identification

### 🤖 AI/ML Specialized Audits
- **Data Privacy**: GDPR, CCPA compliance checks
- **Bias Detection**: Fairness and discrimination analysis
- **Model Security**: Safe model loading and validation

### 🎯 Framework-Aware Analysis
- **Smart Detection**: Automatically detects 15+ frameworks (Django, Flask, React, PyTorch, etc.)
- **Targeted Rules**: Framework-specific security and best practice rules
- **Contextual Guidance**: Remediation advice tailored to your tech stack
- **Confidence Scoring**: Framework detection with confidence levels

### 🏛️ World-Class Standards Integration
- **OWASP Top 10 2021**: Complete mapping to latest OWASP vulnerabilities
- **NIST Frameworks**: Cybersecurity Framework & AI Risk Management Framework
- **Compliance Standards**: GDPR, HIPAA, PCI DSS, SOX, ISO 27001
- **Industry Best Practices**: Microsoft SDL, Google Security, AWS Security
- **Coding Standards**: PEP 8, Google Style Guides, Airbnb JavaScript
- **SANS Top 25**: Most dangerous software weaknesses
- **ASVS**: Application Security Verification Standard

### 🌐 Modern PWA Interface
- **Real-time Scanning**: Live progress updates via WebSocket
- **Offline Capable**: Works without internet connection
- **Responsive Design**: Desktop and mobile optimized
- **Interactive Reports**: Rich, searchable results

### 📈 Multiple Output Formats
- **Interactive Web Dashboard**: Real-time results
- **HTML Reports**: Shareable audit reports
- **JSON Export**: Integration with CI/CD pipelines
- **Console Output**: Terminal-friendly results

## 🚀 Quick Start

### Option 1: PWA Mode (Recommended)
```bash
# Install dependencies
pip install -r requirements.txt

# Start the web server
python run_server.py

# Open http://localhost:8000 in your browser
```

### Option 2: CLI Mode
```bash
# Install dependencies
pip install -r requirements.txt

# Run basic audit
python -m vibeauditor scan ./your-project

# Generate HTML report
python -m vibeauditor scan ./your-project --report-format html --output audit-report.html

# Start web server
python -m vibeauditor serve --host 0.0.0.0 --port 8000
```

## 🏗️ Architecture

### Backend (Python FastAPI)
```
vibeauditor/
├── api/                  # FastAPI web API
│   ├── main.py          # Main application
│   ├── models.py        # Pydantic models
│   └── websocket.py     # Real-time updates
├── core/                # Core auditing engine
│   ├── auditor.py       # Main auditor class
│   ├── config.py        # Configuration management
│   └── results.py       # Results handling
├── rules/               # Audit rules
│   ├── security_rules.py    # Security checks
│   ├── quality_rules.py     # Code quality
│   └── ai_ml_rules.py       # AI/ML specific
├── scanners/            # Language parsers
│   ├── python_scanner.py
│   └── javascript_scanner.py
└── reporters/           # Output generators
    ├── console_reporter.py
    ├── html_reporter.py
    └── json_reporter.py
```

### Frontend (React PWA)
```
webapp/
├── src/
│   ├── components/      # Reusable UI components
│   ├── pages/          # Main application pages
│   ├── services/       # API integration
│   └── context/        # State management
├── public/
│   └── manifest.json   # PWA configuration
└── package.json        # Dependencies
```

## 🔧 Development Setup

### Backend Development
```bash
# Install Python dependencies
pip install -r requirements.txt

# Run development server with auto-reload
python -m vibeauditor serve --reload

# Run tests
python -m pytest tests/

# Format code
black vibeauditor/
isort vibeauditor/
```

### Frontend Development
```bash
# Navigate to webapp directory
cd webapp

# Install Node.js dependencies
npm install

# Start development server
npm start

# Build for production
npm run build
```

## 📋 Usage Examples

### Web Interface
1. Open http://localhost:8000
2. Upload your code files or connect to GitHub
3. Configure scan settings
4. Watch real-time progress
5. Review interactive results

### API Integration
```python
import requests

# Start scan
response = requests.post('http://localhost:8000/api/scan/upload', 
                        files={'files': open('code.py', 'rb')})
scan_id = response.json()['scan_id']

# Get results
results = requests.get(f'http://localhost:8000/api/scan/{scan_id}/results')
print(results.json())
```

### CLI Usage
```bash
# Scan with custom config
python -m vibeauditor scan ./project --config config.yaml

# Filter by severity
python -m vibeauditor scan ./project --severity high

# Exclude patterns
python -m vibeauditor scan ./project --exclude "*.test.py" --exclude "node_modules"

# List available rules
python -m vibeauditor list-rules
```

## ⚙️ Configuration

### YAML Configuration
```yaml
# config.yaml
min_severity: "medium"
enabled_rules: []  # Empty = all rules
disabled_rules: ["quality.todo_comments"]

exclude_patterns:
  - "*.pyc"
  - "__pycache__"
  - ".git"
  - "node_modules"

include_patterns:
  - "*.py"
  - "*.js"
  - "*.ts"

# AI/ML specific settings
check_data_privacy: true
check_model_security: true
check_bias_detection: true

# Report settings
max_issues_per_file: 50
include_code_snippets: true
show_remediation: true
```

## 🔌 API Endpoints

### Core Endpoints
- `POST /api/scan/upload` - Upload files and start scan
- `GET /api/scan/{scan_id}/status` - Get scan progress
- `GET /api/scan/{scan_id}/results` - Get scan results
- `DELETE /api/scan/{scan_id}` - Cleanup scan resources

### Configuration
- `GET /api/rules` - List available rules
- `GET /api/config/default` - Get default configuration

### Real-time Updates
- `WS /ws/{scan_id}` - WebSocket for live progress

## 🧪 Testing

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=vibeauditor

# Test specific module
python -m pytest tests/test_auditor.py

# Test the example vulnerable code
python -m vibeauditor scan examples/sample_vulnerable_code.py
```

## 🚀 Deployment

### Docker Deployment
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "-m", "vibeauditor", "serve", "--host", "0.0.0.0"]
```

### Production Setup
```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn vibeauditor.api.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built for the AI developer community
- Inspired by industry-leading security tools
- Powered by modern web technologies

---

**Ready to audit your code?** 🚀 Start with `python run_server.py` and open http://localhost:8000