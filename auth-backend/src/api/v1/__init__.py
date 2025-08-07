"""API v1 endpoints."""

from .admin import router as admin_router
from .auth import router as auth_router
from .roles import router as roles_router
from .scopes import router as scopes_router
from .service_accounts import router as service_accounts_router
from .sync import router as sync_router
from .users import router as users_router

__all__ = [
    "auth_router",
    "users_router",
    "roles_router",
    "admin_router",
    "service_accounts_router",
    "scopes_router",
    "sync_router",
]
