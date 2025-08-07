"""
Pydantic schemas for Scope management API.

This module defines the Pydantic models used for request/response validation
in scope-related API endpoints.
"""

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class ScopeAppliesTo(str, Enum):
    """Scope applies to enumeration."""

    SERVICE_TO_SERVICE = "Service-to-service"
    BROWSER = "Browser"


class ScopeBase(BaseModel):
    """Base scope schema with common fields."""

    name: str = Field(..., description="Unique scope name (e.g., 'data:read')", min_length=1, max_length=100)
    description: str = Field(..., description="Human-readable description", min_length=1)
    applies_to: List[ScopeAppliesTo] = Field(..., description="Which client types this scope applies to")
    is_active: bool = Field(default=True, description="Whether this scope is active")


class ScopeCreate(ScopeBase):
    """Schema for creating a new scope."""

    pass


class ScopeUpdate(BaseModel):
    """Schema for updating a scope."""

    description: Optional[str] = Field(None, description="Human-readable description", min_length=1)
    applies_to: Optional[List[ScopeAppliesTo]] = Field(None, description="Which client types this scope applies to")
    is_active: Optional[bool] = Field(None, description="Whether this scope is active")


class ScopeResponse(ScopeBase):
    """Schema for scope responses."""

    id: str = Field(..., description="Unique scope identifier")
    service_account_count: int = Field(..., description="Number of service accounts with this scope")

    class Config:
        from_attributes = True


class ScopeListResponse(BaseModel):
    """Schema for listing scopes."""

    scopes: List[ScopeResponse] = Field(..., description="List of scopes")
    total: int = Field(..., description="Total number of scopes")


class ServiceAccountScopeUpdate(BaseModel):
    """Schema for updating service account scope assignments."""

    scope_ids: List[str] = Field(..., description="List of scope IDs to assign to the service account")


# Bulk operations
class ScopeBulkOperation(BaseModel):
    """Schema for bulk scope operations."""

    scope_ids: List[str] = Field(..., description="List of scope IDs to operate on")


class ScopeBulkActivate(ScopeBulkOperation):
    """Schema for bulk activating scopes."""

    pass


class ScopeBulkDeactivate(ScopeBulkOperation):
    """Schema for bulk deactivating scopes."""

    pass


class ScopeBulkDelete(ScopeBulkOperation):
    """Schema for bulk deleting scopes."""

    pass
