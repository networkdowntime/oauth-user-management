# OAuth User Management System Scripts

This directory contains utility scripts for setting up and managing the OAuth User Management System.

## Available Scripts

### 🚀 `setup.sh`
**Main setup script** - Sets up the entire system from scratch.

```bash
./scripts/setup.sh
```

**What it does:**
- Checks dependencies (Docker, Docker Compose, envsubst)
- Generates database init files from templates
- Starts all services in the correct order
- Waits for services to be healthy
- Tests service connectivity
- Displays service URLs and connection info

### 🔧 `generate-db-init.sh`
**Database initialization generator** - Creates SQL init files from templates using environment variables.

```bash
./scripts/generate-db-init.sh
```

**What it does:**
- Reads values from `.env` file
- Processes `*.sql.template` files
- Generates `init.sql` files with actual credentials
- Ensures database users match application credentials

### 🧹 `cleanup.sh`
**System cleanup script** - Stops services and optionally removes data.

```bash
# Stop services, keep data
./scripts/cleanup.sh

# Stop services and remove all data
./scripts/cleanup.sh --volumes
```

**What it does:**
- Stops all Docker containers
- Removes generated SQL files
- Optionally removes Docker volumes (data)
- Cleans up Docker resources

## Prerequisites

Before running any scripts, ensure you have:

1. **Docker** and **Docker Compose** installed
2. **gettext** package (for `envsubst` command)
3. A `.env` file with required environment variables

### Installing gettext (for envsubst)

**macOS:**
```bash
brew install gettext
```

**Ubuntu/Debian:**
```bash
sudo apt-get install gettext-base
```

**CentOS/RHEL:**
```bash
sudo yum install gettext
```

## Environment Variables

The scripts require these environment variables in your `.env` file:

```env
# Hydra Database
POSTGRES_HYDRA_DB=hydra_db
POSTGRES_HYDRA_ADMIN_USER=postgres
POSTGRES_HYDRA_ADMIN_PASSWORD=postgres_admin_password_change_me
POSTGRES_HYDRA_USER=hydra_user
POSTGRES_HYDRA_PASSWORD=hydra_user_password_change_me

# Auth Database
POSTGRES_AUTH_DB=auth_db
POSTGRES_AUTH_ADMIN_USER=postgres
POSTGRES_AUTH_ADMIN_PASSWORD=postgres_admin_password_change_me
POSTGRES_AUTH_USER=auth_user
POSTGRES_AUTH_PASSWORD=auth_user_password_change_me

# Other required variables...
```

## Typical Workflow

### First Time Setup
```bash
# 1. Copy and configure environment variables
cp .env.example .env
# Edit .env with your values

# 2. Run full setup
./scripts/setup.sh
```

### Development Workflow
```bash
# Start system
./scripts/setup.sh

# Make changes to code...

# Restart specific service
docker-compose restart auth-backend

# View logs
docker-compose logs -f auth-backend

# Clean shutdown
./scripts/cleanup.sh
```

### Complete Reset
```bash
# Stop everything and remove all data
./scripts/cleanup.sh --volumes

# Start fresh
./scripts/setup.sh
```

## Troubleshooting

### Database Connection Issues
If you get database connection errors:

1. **Check credentials match**: Ensure `.env` values match generated SQL files
2. **Regenerate init files**: Run `./scripts/generate-db-init.sh`
3. **Reset databases**: Run `./scripts/cleanup.sh --volumes` then `./scripts/setup.sh`

### Service Startup Issues
If services fail to start:

1. **Check logs**: `docker-compose logs [service-name]`
2. **Check health**: `docker-compose ps`
3. **Restart individual service**: `docker-compose restart [service-name]`

### Port Conflicts
If you get port binding errors:

1. **Check running processes**: `lsof -i :3000` (replace with actual port)
2. **Stop conflicting services**: `docker-compose down`
3. **Change ports in docker-compose.yml** if needed

## Script Dependencies

The scripts have the following dependencies:

- **bash** - Shell for script execution
- **docker** - Container runtime
- **docker-compose** - Container orchestration
- **envsubst** - Environment variable substitution
- **curl** - HTTP client for health checks
- **sed** - Text processing for template substitution

## Security Notes

- The generated `init.sql` files contain actual passwords
- These files are in `.gitignore` to prevent committing credentials
- Always use strong passwords in production
- Consider using Docker secrets for production deployments

## File Structure

```
scripts/
├── setup.sh              # Main setup script
├── generate-db-init.sh    # Database init generator
├── cleanup.sh             # Cleanup script
└── README.md             # This file

database/
├── hydra/
│   ├── init.sql.template  # Template with {{VARIABLES}}
│   └── init.sql          # Generated file (ignored by git)
└── auth/
    ├── init.sql.template  # Template with {{VARIABLES}}
    └── init.sql          # Generated file (ignored by git)
```
