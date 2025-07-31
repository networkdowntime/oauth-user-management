#!/bin/bash

# Development helper script for OAuth Auth Backend
# This script provides common development commands

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MAIN_PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
VENV_PYTHON="/Users/rwiles/workspace/oauth-user-management/.venv/bin/python"

case "$1" in
    "start"|"dev")
        echo "Starting FastAPI development server..."
        cd "$SCRIPT_DIR"
        $VENV_PYTHON run_dev.py
        ;;
    "db:start")
        echo "Starting PostgreSQL database for auth backend..."
        cd "$MAIN_PROJECT_DIR"
        docker-compose up -d postgres-auth
        echo "Waiting for database to be ready..."
        sleep 5
        docker-compose exec postgres-auth pg_isready -U auth_admin -d auth_db
        ;;
    "db:stop")
        echo "Stopping PostgreSQL database..."
        cd "$MAIN_PROJECT_DIR"
        docker-compose stop postgres-auth
        ;;
    "db:reset")
        echo "Resetting auth database (WARNING: This will delete all data)..."
        read -p "Are you sure? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            cd "$MAIN_PROJECT_DIR"
            docker-compose down postgres-auth
            docker volume rm oauth-user-management_auth-db-data 2>/dev/null || true
            docker-compose up -d postgres-auth
            echo "Auth database reset complete"
        else
            echo "Database reset cancelled"
        fi
        ;;
    "db:logs")
        echo "Showing auth database logs..."
        cd "$MAIN_PROJECT_DIR"
        docker-compose logs -f postgres-auth
        ;;
    "db:shell")
        echo "Connecting to auth database shell..."
        cd "$MAIN_PROJECT_DIR"
        docker-compose exec postgres-auth psql -U auth_admin -d auth_db
        ;;
    "full:start")
        echo "Starting full OAuth system (all services)..."
        cd "$MAIN_PROJECT_DIR"
        docker-compose up -d
        ;;
    "full:stop")
        echo "Stopping full OAuth system..."
        cd "$MAIN_PROJECT_DIR"
        docker-compose down
        ;;
    "test")
        echo "Running tests..."
        cd "$SCRIPT_DIR"
        $VENV_PYTHON -m pytest tests/ -v
        ;;
    "install")
        echo "Installing dependencies..."
        cd "$SCRIPT_DIR"
        $VENV_PYTHON -m pip install -r requirements.txt
        ;;
    "check")
        echo "Checking application import..."
        cd "$SCRIPT_DIR"
        $VENV_PYTHON -c "from src.main import app; print('✅ FastAPI app imports successfully!')"
        ;;
    "docs")
        echo "Opening API documentation..."
        open http://127.0.0.1:8000/docs
        ;;
    *)
        echo "OAuth Auth Backend Development Commands"
        echo ""
        echo "Usage: $0 {start|db:start|db:stop|db:reset|db:logs|db:shell|full:start|full:stop|test|install|check|docs}"
        echo ""
        echo "Application Commands:"
        echo "  start     Start the FastAPI development server"
        echo "  dev       Alias for start"
        echo "  test      Run the test suite"
        echo "  install   Install Python dependencies"
        echo "  check     Check if the application imports correctly"
        echo "  docs      Open API documentation in browser"
        echo ""
        echo "Database Commands:"
        echo "  db:start  Start PostgreSQL database for auth backend"
        echo "  db:stop   Stop PostgreSQL database"
        echo "  db:reset  Reset auth database (deletes all data)"
        echo "  db:logs   Show database logs"
        echo "  db:shell  Connect to auth database shell"
        echo ""
        echo "Full System Commands:"
        echo "  full:start Start all services (Hydra, Auth Backend, Management UI)"
        echo "  full:stop  Stop all services"
        echo ""
        exit 1
        ;;
esac
