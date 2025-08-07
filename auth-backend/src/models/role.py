"""
Role model for the authentication system.

This module defines the Role model which represents user roles
and permissions in the system.
"""

from typing import List

from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from ..core.database import Base


class Role(Base):
    """
    Role model for defining user permissions.

    Attributes:
        name: Unique role name (e.g., 'user_admin', 'read_only')
        description: Human-readable description of the role
        users: List of users with this role
        audit_logs: List of audit log entries for this role
    """

    __tablename__ = "roles"

    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)

    # Relationships
    users = relationship("User", secondary="user_roles", back_populates="roles", lazy="selectin")

    service_accounts = relationship(
        "ServiceAccount", secondary="service_account_roles", back_populates="roles", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<Role(name='{self.name}')>"

    @property
    def user_count(self) -> int:
        """Get the number of users with this role."""
        return len(self.users)

    @property
    def service_account_count(self) -> int:
        """Get the number of service accounts with this role."""
        return len(self.service_accounts)

    @property
    def total_assignments(self) -> int:
        """Get total assignments (users + service accounts)."""
        return self.user_count + self.service_account_count

    def get_user_emails(self) -> List[str]:
        """Get list of email addresses for users with this role."""
        return [user.email for user in self.users]
