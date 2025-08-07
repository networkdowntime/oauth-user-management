"""User-related Pydantic schemas."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class RoleInUser(BaseModel):
    """Role schema when included in user responses."""

    id: str
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    """User response schema matching frontend interface."""

    id: str
    email: EmailStr
    display_name: Optional[str] = None
    is_active: bool
    last_login_at: Optional[datetime] = None
    failed_login_attempts: int
    locked_until: Optional[datetime] = None
    social_provider: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    roles: List[RoleInUser] = []

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    """Schema for creating a new user."""

    email: EmailStr
    display_name: Optional[str] = None
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")
    is_active: bool = True


class UserUpdate(BaseModel):
    """Schema for updating a user."""

    email: Optional[EmailStr] = None
    display_name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8, description="Password must be at least 8 characters")
    is_active: Optional[bool] = None
    locked_until: Optional[datetime] = None
    role_ids: Optional[List[str]] = None


class UserPasswordReset(BaseModel):
    """Schema for resetting a user's password."""

    new_password: str = Field(..., min_length=8, description="Password must be at least 8 characters")
