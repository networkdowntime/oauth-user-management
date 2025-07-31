#!/bin/bash

# Test runner script for auth-backend
# This script installs test dependencies and runs the test suite

set -e  # Exit on any error

echo "🧪 Setting up test environment for auth-backend..."

# Check if we're in the correct directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: pyproject.toml not found. Please run this script from the auth-backend directory."
    exit 1
fi

# Install dependencies using Poetry
echo "📦 Installing dependencies with Poetry..."
if command -v poetry &> /dev/null; then
    poetry install --with dev
else
    echo "❌ Poetry not found. Please install Poetry first:"
    echo "   curl -sSL https://install.python-poetry.org | python3 -"
    exit 1
fi

# Run the test suite
echo "🚀 Running test suite..."
poetry run pytest tests/ -v

# Generate coverage report
echo "📊 Generating coverage report..."
poetry run pytest tests/ --cov=src --cov-report=html --cov-report=term

echo "✅ Test suite completed!"
echo "📝 Coverage report available in htmlcov/index.html"
