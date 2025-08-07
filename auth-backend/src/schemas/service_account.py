"""Pydantic schemas for Service Account API endpoints."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .scope import ScopeResponse


class ServiceAccountType(str, Enum):
    """Service Account type enumeration."""

    SERVICE_TO_SERVICE = "Service-to-service"
    BROWSER = "Browser"


class ServiceAccountBase(BaseModel):
    """Base schema for service account data."""

    client_id: str = Field(..., description="OAuth2 client identifier")
    client_name: str = Field(..., description="Human-readable name")
    description: Optional[str] = Field(None, description="Service account description")
    account_type: ServiceAccountType = Field(
        default=ServiceAccountType.SERVICE_TO_SERVICE, description="Type of service account"
    )
    grant_types: List[str] = Field(default=["client_credentials"], description="OAuth2 grant types")
    token_endpoint_auth_method: str = Field(
        default="client_secret_basic", description="OAuth2 token endpoint authentication method"
    )
    audience: Optional[List[str]] = Field(None, description="OAuth2 audience URIs")
    owner: Optional[str] = Field(None, description="Owner identifier")
    client_metadata: Optional[Dict[str, Any]] = Field(None, description="Free-form metadata")
    redirect_uris: Optional[List[str]] = Field(default=[], description="OAuth2 redirect URIs")
    post_logout_redirect_uris: Optional[List[str]] = Field(default=[], description="Post-logout redirect URIs")
    allowed_cors_origins: Optional[List[str]] = Field(default=[], description="Allowed CORS origins")
    skip_consent: bool = Field(default=True, description="Skip OAuth2 consent")
    is_active: bool = Field(default=True, description="Whether the service account is active")

    @field_validator("grant_types")
    @classmethod
    def validate_grant_types(cls, v: List[str]) -> List[str]:
        """Validate grant types."""
        valid_grant_types = [
            "client_credentials",
            "authorization_code",
            "refresh_token",
            "implicit",
            "password",
        ]
        for grant_type in v:
            if grant_type not in valid_grant_types:
                raise ValueError(f"Invalid grant type: {grant_type}")
        return v

    @field_validator("token_endpoint_auth_method")
    @classmethod
    def validate_auth_method(cls, v: str) -> str:
        """Validate token endpoint auth method."""
        valid_methods = ["client_secret_basic", "client_secret_post", "private_key_jwt", "none"]
        if v not in valid_methods:
            raise ValueError(f"Invalid auth method: {v}")
        return v


class ServiceAccountCreate(ServiceAccountBase):
    """Schema for creating a service account."""

    client_secret: Optional[str] = Field(None, description="OAuth2 client secret")
    created_by: str = Field(..., description="Who is creating this service account")
    scope_ids: List[str] = Field(default=[], description="List of scope IDs to assign to this service account")
    role_ids: List[str] = Field(default=[], description="List of role IDs to assign to this service account")

    @field_validator("client_id")
    @classmethod
    def validate_client_id(cls, v: str) -> str:
        """Validate client_id format."""
        if not v or len(v.strip()) == 0:
            raise ValueError("client_id cannot be empty")
        if len(v) > 255:
            raise ValueError("client_id cannot exceed 255 characters")
        return v.strip()

    @field_validator("client_name")
    @classmethod
    def validate_client_name(cls, v: str) -> str:
        """Validate client_name."""
        if not v or len(v.strip()) == 0:
            raise ValueError("client_name cannot be empty")
        if len(v) > 255:
            raise ValueError("client_name cannot exceed 255 characters")
        return v.strip()


class ServiceAccountUpdate(BaseModel):
    """Schema for updating a service account."""

    client_name: Optional[str] = Field(None, description="Human-readable name")
    description: Optional[str] = Field(None, description="Service account description")
    grant_types: Optional[List[str]] = Field(None, description="OAuth2 grant types")
    scope_ids: Optional[List[str]] = Field(None, description="List of scope IDs to assign to this service account")
    role_ids: Optional[List[str]] = Field(None, description="List of role IDs to assign to this service account")
    token_endpoint_auth_method: Optional[str] = Field(None, description="OAuth2 token endpoint authentication method")
    audience: Optional[List[str]] = Field(None, description="OAuth2 audience URIs")
    owner: Optional[str] = Field(None, description="Owner identifier")
    client_metadata: Optional[Dict[str, Any]] = Field(None, description="Free-form metadata")
    redirect_uris: Optional[List[str]] = Field(None, description="OAuth2 redirect URIs")
    post_logout_redirect_uris: Optional[List[str]] = Field(None, description="Post-logout redirect URIs")
    allowed_cors_origins: Optional[List[str]] = Field(None, description="Allowed CORS origins")
    skip_consent: Optional[bool] = Field(None, description="Skip OAuth2 consent")
    is_active: Optional[bool] = Field(None, description="Whether the service account is active")

    @field_validator("grant_types")
    @classmethod
    def validate_grant_types(cls, v: Optional[List[str]]) -> Optional[List[str]]:
        """Validate grant types."""
        if v is None:
            return v
        valid_grant_types = [
            "client_credentials",
            "authorization_code",
            "refresh_token",
            "implicit",
            "password",
        ]
        for grant_type in v:
            if grant_type not in valid_grant_types:
                raise ValueError(f"Invalid grant type: {grant_type}")
        return v

    @field_validator("token_endpoint_auth_method")
    @classmethod
    def validate_auth_method(cls, v: Optional[str]) -> Optional[str]:
        """Validate token endpoint auth method."""
        if v is None:
            return v
        valid_methods = ["client_secret_basic", "client_secret_post", "private_key_jwt", "none"]
        if v not in valid_methods:
            raise ValueError(f"Invalid auth method: {v}")
        return v


class RoleResponse(BaseModel):
    """Schema for role data in responses."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    description: Optional[str]
    permissions: List[str] = Field(default=[], description="Role permissions (placeholder)")
    created_at: datetime
    updated_at: datetime


class ServiceAccountResponse(ServiceAccountBase):
    """Schema for service account responses."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    client_secret: Optional[str] = Field(None, description="OAuth2 client secret")
    response_types: List[str] = Field(default=[], description="OAuth2 response types")
    last_used_at: Optional[datetime] = Field(None, description="Last time this service account was used")
    created_by: str = Field(..., description="Who created this service account")
    created_at: datetime
    updated_at: datetime
    roles: List[RoleResponse] = Field(default=[], description="Assigned roles")
    scopes: List[ScopeResponse] = Field(default=[], description="Assigned scopes")


class ServiceAccountListResponse(BaseModel):
    """Schema for paginated service account list."""

    items: List[ServiceAccountResponse]
    total: int
    skip: int
    limit: int


class RoleAssignmentRequest(BaseModel):
    """Schema for role assignment requests."""

    role_id: UUID = Field(..., description="Role UUID to assign")


class ServiceAccountScopesResponse(BaseModel):
    """Schema for available service account scopes."""

    scopes: List[str] = Field(..., description="Available OAuth2 scopes")
    descriptions: Dict[str, str] = Field(default={}, description="Scope descriptions")


class ScopeAssignmentRequest(BaseModel):
    """Schema for scope assignment requests."""

    scope_id: UUID = Field(..., description="Scope UUID to assign")


class ServiceAccountScopeUpdate(BaseModel):
    """Schema for updating service account scope assignments."""

    scope_ids: List[UUID] = Field(..., description="List of scope UUIDs to assign to the service account")
