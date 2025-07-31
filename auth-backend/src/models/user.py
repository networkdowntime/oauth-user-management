"""
User model for the authentication system.

This module defines the User model which represents human users
in the system. Service accounts are handled separately via the ServiceAccount model.
"""

from datetime import datetime
from typing import List

from sqlalchemy import Column, String, Boolean, DateTime, Integer
from sqlalchemy.orm import relationship

from ..core.database import Base


class User(Base):
    """
    User model for human users in the authentication system.
    
    Attributes:
        email: User's email address (unique identifier)
        password_hash: Hashed password (only for password authentication)
        is_active: Whether the user account is active
        display_name: Display name for the user
        last_login_at: Timestamp of last successful login
        failed_login_attempts: Number of consecutive failed login attempts
        locked_until: Account lock expiration timestamp
        social_provider: Social login provider (google, github, apple)
        social_provider_id: Unique ID from social provider
        roles: List of roles assigned to this user
        audit_logs: List of audit log entries for this user
    """
    
    __tablename__ = "users"
    
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=True)  # Nullable for social-only users
    is_active = Column(Boolean, default=True, nullable=False)
    display_name = Column(String(255), nullable=True)
    
    # Authentication tracking
    last_login_at = Column(DateTime, nullable=True)
    failed_login_attempts = Column(Integer, default=0, nullable=False)
    locked_until = Column(DateTime, nullable=True)
    
    # Social login support
    social_provider = Column(String(50), nullable=True)  # google, github, apple
    social_provider_id = Column(String(255), nullable=True)
    
    # Relationships
    roles = relationship(
        "Role",
        secondary="user_roles",
        back_populates="users",
        lazy="selectin"
    )
    
    def __repr__(self) -> str:
        return f"<User(email='{self.email}')>"
    
    @property
    def is_locked(self) -> bool:
        """Check if the user account is currently locked."""
        if self.locked_until is None:
            return False
        return datetime.utcnow() < self.locked_until
    
    @property
    def role_names(self) -> List[str]:
        """Get list of role names for this user."""
        return [role.name for role in self.roles]
    
    def has_role(self, role_name: str) -> bool:
        """Check if user has a specific role."""
        return role_name in self.role_names
    
    def is_admin(self) -> bool:
        """Check if user has admin privileges."""
        return self.has_role("user_admin")
    
    def can_login(self) -> bool:
        """Check if user can login (active and not locked)."""
        return self.is_active and not self.is_locked
