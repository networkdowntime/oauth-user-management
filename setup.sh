#!/bin/bash

# OAuth2 User Management System Setup Script
# This script sets up the complete development environment

set -e

echo "🚀 Setting up OAuth2 User Management System..."

# Check if required tools are installed
command -v docker >/dev/null 2>&1 || { echo "❌ Docker is required but not installed. Aborting." >&2; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo "❌ Docker Compose is required but not installed. Aborting." >&2; exit 1; }
command -v openssl >/dev/null 2>&1 || { echo "❌ OpenSSL is required but not installed. Aborting." >&2; exit 1; }

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📋 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and update the passwords and configuration before continuing!"
    echo "   Run: nano .env"
    echo ""
    read -p "Press Enter when you have updated the .env file..." 
fi

# Source the .env file
if [ -f .env ]; then
    echo "📖 Loading environment variables..."
    export $(cat .env | grep -v '^#' | xargs)
fi

# Generate JWT keys
echo "🔑 Generating JWT signing keys..."
./scripts/generate-keys.sh

# Update database init scripts with actual passwords from .env
echo "🔧 Updating database initialization scripts..."

# Update Hydra database init script
sed -i.bak "s/HYDRA_PASSWORD_PLACEHOLDER/${POSTGRES_HYDRA_PASSWORD}/g" database/hydra/init.sql
echo "✅ Updated Hydra database init script"

# Update Auth database init script  
sed -i.bak "s/AUTH_PASSWORD_PLACEHOLDER/${POSTGRES_AUTH_PASSWORD}/g" database/auth/init.sql
echo "✅ Updated Auth database init script"

# Update Hydra configuration
sed -i.bak "s/HYDRA_PASSWORD_PLACEHOLDER/${POSTGRES_HYDRA_PASSWORD}/g" hydra/hydra.yml
echo "✅ Updated Hydra configuration"

# Start the databases first
echo "🗄️  Starting PostgreSQL databases..."
docker-compose up -d postgres-hydra postgres-auth

# Wait for databases to be ready
echo "⏳ Waiting for databases to be ready..."
sleep 10

# Check database health
echo "🏥 Checking database health..."
docker-compose ps postgres-hydra postgres-auth

echo ""
echo "✅ Basic setup complete!"
echo ""
echo "Next steps:"
echo "1. Build and start all services: docker-compose up --build"
echo "2. Access the management UI at: http://localhost:3000"
echo "3. Access the API documentation at: http://localhost:8000/docs"
echo ""
echo "Default admin login:"
echo "  Email: ${DEFAULT_ADMIN_EMAIL}"
echo "  Password: ${DEFAULT_ADMIN_PASSWORD}"
echo ""
echo "⚠️  Remember to change all default passwords in production!"
