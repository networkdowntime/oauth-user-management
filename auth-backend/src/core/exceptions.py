"""Exception handlers for the FastAPI application."""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_500_INTERNAL_SERVER_ERROR

from .logging_config import get_logger

logger = get_logger(__name__)


class AuthenticationError(Exception):
    """Custom authentication error."""
    pass


class AuthorizationError(Exception):
    """Custom authorization error."""
    pass


class ValidationError(Exception):
    """Custom validation error."""
    pass


class UserNotFoundError(Exception):
    """User not found error."""
    pass


class RoleNotFoundError(Exception):
    """Role not found error."""
    pass


class ServiceAccountNotFoundError(Exception):
    """Service account not found error."""
    pass


class ServiceAccountAlreadyExistsError(Exception):
    """Service account already exists error."""
    pass


class HydraIntegrationError(Exception):
    """Hydra integration error."""
    pass


class NotFoundError(Exception):
    """Generic not found error."""
    pass


class ConflictError(Exception):
    """Generic conflict error."""
    pass


def setup_exception_handlers(app: FastAPI) -> None:
    """Setup custom exception handlers for the application."""
    
    @app.exception_handler(AuthenticationError)
    async def authentication_exception_handler(request: Request, exc: AuthenticationError):
        """Handle authentication errors."""
        logger.warning(f"Authentication error: {str(exc)}")
        return JSONResponse(
            status_code=401,
            content={"error": "authentication_error", "message": str(exc)}
        )
    
    @app.exception_handler(AuthorizationError)
    async def authorization_exception_handler(request: Request, exc: AuthorizationError):
        """Handle authorization errors."""
        logger.warning(f"Authorization error: {str(exc)}")
        return JSONResponse(
            status_code=403,
            content={"error": "authorization_error", "message": str(exc)}
        )
    
    @app.exception_handler(ValidationError)
    async def validation_exception_handler(request: Request, exc: ValidationError):
        """Handle validation errors."""
        logger.warning(f"Validation error: {str(exc)}")
        return JSONResponse(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            content={"error": "validation_error", "message": str(exc)}
        )
    
    @app.exception_handler(ValueError)
    async def value_error_exception_handler(request: Request, exc: ValueError):
        """Handle value errors."""
        logger.warning(f"Value error: {str(exc)}")
        return JSONResponse(
            status_code=400,
            content={"error": "bad_request", "message": str(exc)}
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle general exceptions."""
        logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "internal_server_error", "message": "An unexpected error occurred"}
        )
