"""API package."""

from .v1 import (
    admin_router,
    auth_router,
    roles_router,
    scopes_router,
    service_accounts_router,
    users_router,
)

__all__ = [
    "auth_router",
    "users_router",
    "service_accounts_router",
    "roles_router",
    "scopes_router",
    "admin_router",
]
