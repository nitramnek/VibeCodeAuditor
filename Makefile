# VibeCodeAuditor Makefile

.PHONY: help install test lint format clean run-example serve demo dev-setup

help:
	@echo "VibeCodeAuditor - Available Commands:"
	@echo "=================================="
	@echo "  install     Install Python dependencies"
	@echo "  dev-setup   Complete development setup"
	@echo "  test        Run functionality tests"
	@echo "  demo        Run demo scan on sample code"
	@echo "  serve       Start web server (PWA mode)"
	@echo "  run-example Run CLI scan on examples"
	@echo "  self-audit  Run audit on VibeCodeAuditor itself"
	@echo "  lint        Run code linting"
	@echo "  format      Format code with black/isort"
	@echo "  clean       Clean up temporary files"
	@echo ""
	@echo "Quick Start:"
	@echo "  make dev-setup  # Setup everything"
	@echo "  make demo       # Test with sample code"
	@echo "  make serve      # Start web interface"

# Install dependencies
install:
	@echo "📦 Installing Python dependencies..."
	pip install -r requirements.txt

# Complete development setup
dev-setup: install
	@echo "🔧 Setting up development environment..."
	@echo "✅ Python dependencies installed"
	@echo "🧪 Running basic functionality test..."
	python test_basic_functionality.py

# Run functionality tests
test:
	@echo "🧪 Running functionality tests..."
	python test_basic_functionality.py
	@echo "🧪 Running unit tests..."
	python -m pytest tests/ -v

# Demo with sample code
demo:
	@echo "🎯 Running demo scan on sample vulnerable code..."
	python -m vibeauditor scan examples/sample_vulnerable_code.py --verbose
	@echo ""
	@echo "🌐 For web interface demo, run: make serve"

# Start web server
serve:
	@echo "🚀 Starting VibeCodeAuditor web server..."
	@echo "🌐 Open http://localhost:8000 in your browser"
	python run_server.py

# Lint code
lint:
	flake8 vibeauditor/ --ignore=E501,W503
	pylint vibeauditor/ --disable=C0114,C0116
	mypy vibeauditor/ --ignore-missing-imports

# Format code
format:
	black vibeauditor/ tests/
	isort vibeauditor/ tests/

# Clean build artifacts
clean:
	@echo "🧹 Cleaning up temporary files..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete
	find . -name ".pytest_cache" -exec rm -rf {} +
	@echo "✅ Cleanup complete"

# Run example scan
run-example:
	@echo "🔍 Running CLI scan on examples..."
	python -m vibeauditor scan examples/ --report-format html --output example-report.html
	@echo "📄 Report saved to example-report.html"

# Run on self (dogfooding)
self-audit:
	@echo "🔍 Running VibeCodeAuditor on itself..."
	python -m vibeauditor scan vibeauditor/ --verbose

# Build package
build:
	python setup.py sdist bdist_wheel

# Install in development mode
dev-install:
	pip install -e .

# Web app development (if Node.js is available)
webapp-install:
	@echo "📦 Installing webapp dependencies..."
	cd webapp && npm install

webapp-dev:
	@echo "🌐 Starting webapp development server..."
	cd webapp && npm start

webapp-build:
	@echo "🏗️  Building webapp for production..."
	cd webapp && npm run build