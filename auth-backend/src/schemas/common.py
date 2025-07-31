"""Common Pydantic schemas for API responses."""

from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Standard error response schema."""
    
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None


class SuccessResponse(BaseModel):
    """Standard success response schema."""
    
    success: bool = True
    message: str


class SystemStatsResponse(BaseModel):
    """System statistics response schema."""
    
    users: int
    services: int
    roles: int
