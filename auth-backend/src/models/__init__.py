"""
Database models for the OAuth2 Authentication Backend.

This module imports all database models and defines association tables
for many-to-many relationships.
"""

from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from ..core.database import Base

# Association table for many-to-many relationship between users and roles
user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True),
    Column('role_id', UUID(as_uuid=True), ForeignKey('roles.id'), primary_key=True)
)

# Import all models to ensure they are registered with SQLAlchemy
from .user import User
from .role import Role
from .audit_log import AuditLog
from .service_account import ServiceAccount
from .service_account_roles import service_account_roles
from .scope import Scope
from .service_account_scopes import service_account_scopes

__all__ = [
    "User",
    "Role",
    "AuditLog",
    "ServiceAccount",
    "Scope",
    "user_roles",
    "service_account_roles",
    "service_account_scopes"
]
