"""
OAuth2 Token Validation Middleware for authentication with Hydra
"""

import httpx
from functools import wraps
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Dict, Any, Callable, Awaitable
import logging

from ..core.config import settings

logger = logging.getLogger(__name__)

# HTTP Bearer token scheme
security = HTTPBearer()

class OAuth2Validator:
    """Validates OAuth2 tokens using Hydra's introspection endpoint"""
    
    def __init__(self):
        self.hydra_admin_url = settings.hydra_admin_url
        
    async def introspect_token(self, token: str) -> Dict[str, Any]:
        """Introspect token using Hydra's admin API"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.hydra_admin_url}/admin/oauth2/introspect",
                    data={"token": token},
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Failed to introspect token with Hydra: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Unable to validate token - authentication service unavailable"
            )
    
    async def validate_token(self, token: str) -> Dict[str, Any]:
        """Validate OAuth2 token and return user info"""
        try:
            # Introspect the token with Hydra
            introspection_result = await self.introspect_token(token)
            
            # Check if token is active
            if not introspection_result.get("active", False):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token is not active"
                )
            
            # Check if token is for the correct client (management-ui)
            client_id = introspection_result.get("client_id")
            if client_id != settings.hydra_client_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token is not valid for this application"
                )
            
            return introspection_result
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Token validation error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Token validation failed"
            )

# Global validator instance
oauth2_validator = OAuth2Validator()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """
    Dependency to get the current authenticated user from OAuth2 token
    """
    token = credentials.credentials
    token_info = await oauth2_validator.validate_token(token)
    
    # Extract user information from token introspection
    user_info = {
        "sub": token_info.get("sub"),  # Subject (user ID)
        "client_id": token_info.get("client_id"),
        "scope": token_info.get("scope", "").split() if token_info.get("scope") else [],
        "exp": token_info.get("exp"),  # Expiration
        "iat": token_info.get("iat"),  # Issued at
        "active": token_info.get("active", False),
        "token_type": token_info.get("token_type", "bearer"),
        # Additional claims if present
        "email": token_info.get("email"),
        "name": token_info.get("name"),
        "username": token_info.get("username"),
    }
    
    return user_info

async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))
) -> Optional[Dict[str, Any]]:
    """
    Optional dependency to get the current authenticated user.
    Returns None if no valid token is provided.
    """
    if not credentials:
        return None
    
    try:
        return await get_current_user(credentials)
    except HTTPException:
        return None

def require_scope(required_scope: str):
    """
    Decorator to require a specific OAuth2 scope
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Get user from dependency injection
            user = kwargs.get('current_user')
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            user_scopes = user.get("scope", [])
            if required_scope not in user_scopes:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Insufficient permissions. Required scope: {required_scope}"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator
