#!/bin/bash

# Test runner script for auth-backend
# This script installs test dependencies and runs the test suite

set -e  # Exit on any error

echo "🧪 Setting up test environment for auth-backend..."

# Check if we're in the correct directory
if [ ! -f "requirements-test.txt" ]; then
    echo "❌ Error: requirements-test.txt not found. Please run this script from the auth-backend directory."
    exit 1
fi

# Install dependencies using pip
echo "📦 Installing dependencies with pip..."
if command -v python3 &> /dev/null; then
    python3 -m pip install -r requirements.txt
    python3 -m pip install -r requirements-test.txt
else
    echo "❌ Python3 not found. Please install Python3 first."
    exit 1
fi

# Run the test suite
echo "🚀 Running test suite..."
python3 -m pytest tests/ -v

# Generate coverage report
echo "📊 Generating coverage report..."
python3 -m pytest tests/ --cov=src --cov-report=html --cov-report=term

echo "✅ Test suite completed!"
echo "📝 Coverage report available in htmlcov/index.html"
