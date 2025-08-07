"""
Database models for the OAuth2 Authentication Backend.

This module imports all database models and association tables
for many-to-many relationships.
"""

from .audit_log import AuditLog
from .role import Role
from .scope import Scope
from .service_account import ServiceAccount
from .service_account_roles import service_account_roles
from .service_account_scopes import service_account_scopes

# Import all models to ensure they are registered with SQLAlchemy
from .user import User

# Import association tables
from .user_roles import user_roles

__all__ = [
    "User",
    "Role",
    "AuditLog",
    "ServiceAccount",
    "Scope",
    "user_roles",
    "service_account_roles",
    "service_account_scopes",
]
