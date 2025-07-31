"""
OAuth2 Authentication Backend Service

This service handles authentication and authorization for the OAuth2 system.
It integrates with Ory Hydra and provides user/service/role management.
"""

import structlog
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from .api.v1.auth import router as auth_router
from .api.v1.users import router as users_router  
from .api.v1.service_accounts import router as service_accounts_router
from .api.v1.roles import router as roles_router
from .api.v1.admin import router as admin_router
from .api.v1.scopes import router as scopes_router
from .core.config import settings
from .core.database import create_tables, initialize_default_data
from .core.exceptions import setup_exception_handlers
from .core.logging_config import setup_logging
from .core.rate_limiting import limiter


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan events.
    
    Handles startup and shutdown tasks including database initialization
    and default data creation.
    """
    # Startup
    logger = structlog.get_logger()
    setup_logging()
    
    # Try to initialize database, but don't fail if database is not available
    try:
        await create_tables()
        await initialize_default_data()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.warning(f"Database initialization failed: {e}")
        logger.warning("Application will start without database connectivity")
    
    yield
    
    # Shutdown
    pass


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        FastAPI: Configured application instance
    """
    app = FastAPI(
        title="OAuth2 Auth Backend",
        description="Authentication and authorization backend for OAuth2 system",
        version="1.0.0",
        docs_url="/docs" if settings.environment == "development" else None,
        redoc_url="/redoc" if settings.environment == "development" else None,
        lifespan=lifespan,
    )

    # Add security middleware
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.allowed_hosts,
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add rate limiting
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # Setup exception handlers
    setup_exception_handlers(app)

    # Include routers
    app.include_router(admin_router, prefix="/api/v1", tags=["Admin"])
    app.include_router(auth_router, prefix="/api/v1", tags=["Authentication"])
    app.include_router(roles_router, prefix="/api/v1", tags=["Roles"])
    app.include_router(service_accounts_router, prefix="/api/v1", tags=["Service Accounts"])
    app.include_router(scopes_router, prefix="/api/v1", tags=["Scopes"])
    app.include_router(users_router, prefix="/api/v1", tags=["Users"])


    # Health check endpoint
    @app.get("/health")
    async def health_check() -> dict[str, str]:
        """Health check endpoint for monitoring."""
        return {"status": "healthy"}

    return app


# Create the application instance
app = create_app()
