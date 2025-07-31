# OAuth2 User Management System

A comprehensive OAuth2 server implementation using Ory Hydra with a Python auth backend and React management UI.

## Architecture

- **Ory Hydra**: OAuth2/OpenID Connect server
- **PostgreSQL (Hydra)**: Dedicated database for Hydra's data
- **PostgreSQL (Auth)**: Dedicated database for user/service/role management
- **Auth Backend**: Python FastAPI service for authentication logic
- **Management UI**: React application for user/service/role administration

## Features

- OAuth2 Authorization Code Flow with PKCE
- Client Credentials Grant for service-to-service authentication
- JWT tokens with RS256 signing
- Short-lived access tokens (15 min) with refresh tokens
- Role-based access control (RBAC)
- Social login support (Google, Apple, GitHub)
- Password authentication with Argon2 hashing
- Rate limiting and brute force protection
- Comprehensive audit logging
- Management UI for users, services, and roles

## Quick Start

1. Copy the environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file with your configuration:
   - Change all default passwords
   - Configure social login providers (optional)
   - Set your admin email and password

3. Generate JWT signing keys:
   ```bash
   ./scripts/generate-keys.sh
   ```

4. Start the services:
   ```bash
   docker-compose up -d
   ```

5. The services will be available at:
   - Management UI: http://localhost:3000
   - Auth Backend API: http://localhost:8000
   - Hydra Public API: http://localhost:4444
   - Hydra Admin API: http://localhost:4445

## Database Configuration

The system uses two separate PostgreSQL databases:

### Hydra Database (Port 5433)
- **Admin User**: Set via `POSTGRES_HYDRA_ADMIN_USER`
- **Application User**: `hydra_user` (created by init script)
- **Database**: `hydra_db`

### Auth Backend Database (Port 5434)
- **Admin User**: Set via `POSTGRES_AUTH_ADMIN_USER`
- **Application User**: `auth_user` (created by init script)
- **Database**: `auth_db`

## Security Features

- Passwords hashed with Argon2
- JWT tokens signed with RS256 (asymmetric keys)
- Rate limiting per IP and user
- PKCE for OAuth2 flows
- Secure HTTP-only refresh token cookies
- Comprehensive audit logging
- Input validation and sanitization

## Development

See individual service README files for development instructions:
- [Auth Backend](./auth-backend/README.md)
- [Management UI](./management-ui/README.md)

## Production Deployment

1. Change all default passwords in `.env`
2. Use production-grade secrets management
3. Configure proper SSL/TLS termination
4. Set up proper backup strategies for databases
5. Configure monitoring and logging
6. Review and adjust rate limiting settings

## API Documentation

Once running, API documentation is available at:
- Auth Backend: http://localhost:8000/docs

## License

[Add your license here]
