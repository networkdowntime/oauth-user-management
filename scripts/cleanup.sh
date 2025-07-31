#!/bin/bash

# Cleanup script for OAuth User Management System
# This script stops all services and optionally removes volumes

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}🔧 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Parse command line arguments
REMOVE_VOLUMES=false
if [ "$1" = "--volumes" ] || [ "$1" = "-v" ]; then
    REMOVE_VOLUMES=true
fi

echo "🧹 OAuth User Management System Cleanup"
echo "======================================"

# Stop all services
print_status "Stopping all services..."
docker-compose down --remove-orphans

if [ "$REMOVE_VOLUMES" = true ]; then
    print_warning "Removing all volumes (data will be lost)..."
    docker-compose down -v
    print_warning "All data has been removed"
else
    print_status "Keeping volumes (data preserved)"
    echo "   Use --volumes flag to remove all data"
fi

# Remove generated SQL files
print_status "Cleaning up generated files..."
rm -f database/hydra/init.sql
rm -f database/auth/init.sql
print_success "Generated files cleaned up"

# Clean up unused Docker resources
print_status "Cleaning up Docker resources..."
docker system prune -f || true

print_success "Cleanup completed!"
echo ""
echo "📋 Next steps:"
echo "   - To restart: ./scripts/setup.sh"
echo "   - To regenerate init files: ./scripts/generate-db-init.sh"
echo ""
