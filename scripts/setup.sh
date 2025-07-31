#!/bin/bash

# OAuth User Management System Setup Script
# This script prepares the environment and starts all services

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}🔧 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if .env file exists
check_env_file() {
    if [ ! -f .env ]; then
        print_error ".env file not found!"
        echo "Please create a .env file based on .env.example"
        exit 1
    fi
    print_success ".env file found"
}

# Check if required commands are available
check_dependencies() {
    print_status "Checking dependencies..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed or not in PATH"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed or not in PATH"
        exit 1
    fi
    
    if ! command -v envsubst &> /dev/null; then
        print_error "envsubst is not installed (usually part of gettext package)"
        exit 1
    fi
    
    print_success "All dependencies are available"
}

# Generate database init files
generate_db_init() {
    print_status "Generating database initialization files..."
    ./scripts/generate-db-init.sh
    print_success "Database init files generated"
}

# Clean up any existing containers
cleanup_containers() {
    print_status "Cleaning up existing containers..."
    docker-compose down --remove-orphans || true
    print_success "Cleanup completed"
}

# Start services in the correct order
start_services() {
    print_status "Starting OAuth User Management services..."
    
    # Start databases first
    print_status "Starting PostgreSQL databases..."
    docker-compose up -d postgres-hydra postgres-auth
    
    # Wait for databases to be healthy
    print_status "Waiting for databases to be ready..."
    sleep 10
    
    # Check database health
    until docker-compose exec -T postgres-hydra pg_isready -U postgres -d hydra_db; do
        print_status "Waiting for Hydra database..."
        sleep 2
    done
    print_success "Hydra database is ready"
    
    until docker-compose exec -T postgres-auth pg_isready -U postgres -d auth_db; do
        print_status "Waiting for Auth database..."
        sleep 2
    done
    print_success "Auth database is ready"
    
    # Start Hydra migration
    print_status "Running Hydra database migration..."
    docker-compose up hydra-migrate
    print_success "Hydra migration completed"
    
    # Start Hydra server
    print_status "Starting Hydra OAuth2 server..."
    docker-compose up -d hydra
    
    # Wait for Hydra to be ready
    print_status "Waiting for Hydra to be ready..."
    sleep 10
    
    # Start Auth Backend
    print_status "Starting Auth Backend..."
    docker-compose up -d auth-backend
    
    # Wait for Auth Backend to be ready
    print_status "Waiting for Auth Backend to be ready..."
    sleep 15
    
    # Start Management UI
    print_status "Starting Management UI..."
    docker-compose up -d management-ui
    
    print_success "All services started successfully!"
}

# Display service URLs
show_urls() {
    echo ""
    echo "🌐 Service URLs:"
    echo "   Management UI:    http://localhost:3000"
    echo "   Auth Backend:     http://localhost:8000"
    echo "   Hydra Public:     http://localhost:4444"
    echo "   Hydra Admin:      http://localhost:4445"
    echo ""
    echo "📊 Database Connections:"
    echo "   Hydra DB:         localhost:5433 (hydra_db)"
    echo "   Auth DB:          localhost:5434 (auth_db)"
    echo ""
}

# Test service health
test_services() {
    print_status "Testing service health..."
    
    # Test Auth Backend
    if curl -s http://localhost:8000/api/v1/health > /dev/null; then
        print_success "Auth Backend is responding"
    else
        print_warning "Auth Backend is not responding yet"
    fi
    
    # Test Hydra
    if curl -s http://localhost:4444/health/ready > /dev/null; then
        print_success "Hydra is responding"
    else
        print_warning "Hydra is not responding yet"
    fi
    
    # Test Management UI
    if curl -s http://localhost:3000 > /dev/null; then
        print_success "Management UI is responding"
    else
        print_warning "Management UI is not responding yet"
    fi
}

# Main execution
main() {
    echo "🚀 OAuth User Management System Setup"
    echo "======================================"
    
    check_env_file
    check_dependencies
    cleanup_containers
    generate_db_init
    start_services
    show_urls
    
    print_status "Waiting for services to fully start..."
    sleep 30
    
    test_services
    
    echo ""
    print_success "Setup completed! Your OAuth User Management system is ready."
    echo ""
    echo "📋 Next steps:"
    echo "   1. Open http://localhost:3000 to access the Management UI"
    echo "   2. Check the logs with: docker-compose logs -f"
    echo "   3. Stop services with: docker-compose down"
    echo ""
}

# Run main function
main "$@"
