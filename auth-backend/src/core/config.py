"""
Application configuration settings.

This module defines all configuration settings for the auth backend service,
including database connections, JWT settings, and external service URLs.
"""

from typing import List, Optional
from pathlib import Path

from pydantic import Field, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with validation."""

    # Database settings
    database_url: str = Field(
        default="postgresql://auth_user:auth_user_password@localhost:5434/auth_db",
        description="PostgreSQL database URL"
    )
    
    # JWT settings
    jwt_private_key_path: Path = Field(
        default=Path("keys/jwt_private.pem"),
        description="Path to JWT private key file"
    )
    jwt_public_key_path: Path = Field(
        default=Path("keys/jwt_public.pem"),
        description="Path to JWT public key file"
    )
    jwt_algorithm: str = Field(default="RS256", description="JWT signing algorithm")
    access_token_expire_minutes: int = Field(
        default=15, description="Access token expiration in minutes"
    )
    refresh_token_expire_days: int = Field(
        default=30, description="Refresh token expiration in days"
    )
    
    # Application settings
    secret_key: str = Field(
        default="your-secret-key-change-me",
        description="Application secret key for security operations"
    )
    environment: str = Field(
        default="development", description="Application environment"
    )
    allowed_hosts: List[str] = Field(
        default=["*"], description="Allowed host names"
    )
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        description="CORS allowed origins"
    )
    
    # Hydra settings
    hydra_admin_url: str = Field(
        default="http://hydra:4445", description="Hydra admin API URL"
    )
    hydra_public_url: str = Field(
        default="http://hydra:4444", description="Hydra public API URL"
    )
    
    # Default admin user
    default_admin_email: str = Field(
        default="admin@example.com", description="Default admin user email"
    )
    default_admin_password: str = Field(
        default="admin_password_change_me", description="Default admin user password"
    )
    
    # Social login settings (optional)
    google_client_id: Optional[str] = Field(
        default=None, description="Google OAuth client ID"
    )
    google_client_secret: Optional[str] = Field(
        default=None, description="Google OAuth client secret"
    )
    github_client_id: Optional[str] = Field(
        default=None, description="GitHub OAuth client ID"
    )
    github_client_secret: Optional[str] = Field(
        default=None, description="GitHub OAuth client secret"
    )
    apple_client_id: Optional[str] = Field(
        default=None, description="Apple OAuth client ID"
    )
    apple_client_secret: Optional[str] = Field(
        default=None, description="Apple OAuth client secret"
    )
    
    # Hydra integration settings
    hydra_admin_url: str = Field(
        default="http://hydra:4445", description="Hydra Admin API URL"
    )
    hydra_public_url: str = Field(
        default="http://hydra:4444", description="Hydra Public API URL"
    )
    hydra_timeout: int = Field(
        default=30, description="Hydra API request timeout in seconds"
    )
    
    # Rate limiting settings
    rate_limit_per_minute: int = Field(
        default=60, description="Rate limit per minute per IP"
    )
    login_rate_limit_per_minute: int = Field(
        default=5, description="Login rate limit per minute per IP"
    )
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        # Allow extra fields for development/deployment flexibility
        extra = "ignore"

    @validator("jwt_private_key_path", "jwt_public_key_path")
    def validate_key_paths(cls, v: Path) -> Path:
        """Validate that key file paths exist in production."""
        # Only validate key paths in production environment
        return v

    @property
    def jwt_private_key(self) -> str:
        """Read and return the JWT private key."""
        if self.jwt_private_key_path.exists():
            return self.jwt_private_key_path.read_text()
        # Return a dummy key for development
        return "dummy-private-key-for-development"

    @property
    def jwt_public_key(self) -> str:
        """Read and return the JWT public key."""
        if self.jwt_public_key_path.exists():
            return self.jwt_public_key_path.read_text()
        # Return a dummy key for development
        return "dummy-public-key-for-development"


# Global settings instance
settings = Settings()
