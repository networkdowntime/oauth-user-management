"""Role-related Pydantic schemas."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class RoleResponse(BaseModel):
    """Role response schema matching frontend interface."""
    
    id: str
    name: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    user_count: int = 0
    
    class Config:
        from_attributes = True


class RoleCreate(BaseModel):
    """Schema for creating a new role."""
    
    name: str
    description: Optional[str] = None


class RoleUpdate(BaseModel):
    """Schema for updating a role."""
    
    name: Optional[str] = None
    description: Optional[str] = None
