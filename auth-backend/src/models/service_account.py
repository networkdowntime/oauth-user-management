"""Service Account model for OAuth2 client management."""

from typing import Optional, Dict, Any
from sqlalchemy import Column, String, DateTime, JSON, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum

from ..core.database import Base


class ServiceAccountType(enum.Enum):
    """Service Account type enumeration."""
    SERVICE_TO_SERVICE = "Service-to-service"
    BROWSER = "Browser"


class ServiceAccount(Base):
    """
    Service Account model representing OAuth2 clients for machine-to-machine authentication.
    
    This model stores OAuth2 client information that syncs with Hydra admin API.
    Service accounts can be assigned roles just like users.
    """
    __tablename__ = "service_accounts"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # OAuth2 Required Fields
    client_id = Column(String(255), unique=True, nullable=False, index=True)
    client_secret = Column(String(512), nullable=True)  # Nullable for public clients
    grant_types = Column(JSON, nullable=False, default=lambda: ["client_credentials"])
    response_types = Column(JSON, nullable=False, default=lambda: [])
    token_endpoint_auth_method = Column(
        String(50), 
        nullable=False, 
        default="client_secret_basic"
    )
    
    # OAuth2 Optional Fields (Recommended)
    audience = Column(JSON, nullable=True)  # Array of audience URIs
    owner = Column(String(255), nullable=True)  # Owner identifier
    client_metadata = Column(JSON, nullable=True)  # Free-form metadata (renamed from metadata)
    token_endpoint_auth_signing_alg = Column(String(50), nullable=True)
    client_name = Column(String(255), nullable=False)  # Human-readable name
    redirect_uris = Column(JSON, nullable=True, default=lambda: [])
    post_logout_redirect_uris = Column(JSON, nullable=True, default=lambda: [])
    allowed_cors_origins = Column(JSON, nullable=True, default=lambda: [])
    skip_consent = Column(Boolean, default=True)  # Usually true for service accounts
    
    # Additional OAuth2 fields
    jwks = Column(JSON, nullable=True)
    jwks_uri = Column(String(500), nullable=True)
    id_token_signed_response_alg = Column(String(50), nullable=True, default="RS256")
    
    # Service Account Management Fields
    account_type = Column(
        String(50), 
        nullable=False, 
        default=ServiceAccountType.SERVICE_TO_SERVICE.value
    )
    is_active = Column(Boolean, default=True, nullable=False)
    description = Column(Text, nullable=True)
    last_used_at = Column(DateTime, nullable=True)
    created_by = Column(String(255), nullable=False)  # Who created this service account
    
    # Relationships
    roles = relationship(
        "Role",
        secondary="service_account_roles",
        back_populates="service_accounts",
        lazy='selectin'
    )
    
    scopes = relationship(
        "Scope",
        secondary="service_account_scopes",
        back_populates="service_accounts",
        lazy='selectin'
    )
    
    def __repr__(self):
        return f"<ServiceAccount(client_id='{self.client_id}', name='{self.client_name}')>"
    
    def to_hydra_client(self) -> Dict[str, Any]:
        """Convert to Hydra client format for API calls."""
        scope_string = " ".join(scope.name for scope in self.scopes) if self.scopes else ""
        return {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_types": self.grant_types,
            "response_types": self.response_types,
            "scope": scope_string,
            "token_endpoint_auth_method": self.token_endpoint_auth_method,
            "audience": self.audience or [],
            "owner": self.owner,
            "metadata": self.client_metadata or {},
            "client_name": self.client_name,
            "redirect_uris": self.redirect_uris or [],
            "post_logout_redirect_uris": self.post_logout_redirect_uris or [],
            "allowed_cors_origins": self.allowed_cors_origins or [],
            "skip_consent": self.skip_consent,
            "jwks": self.jwks,
            "jwks_uri": self.jwks_uri,
            "id_token_signed_response_alg": self.id_token_signed_response_alg,
            "account_type": self.account_type,
        }
    
    @classmethod
    def from_hydra_client(cls, hydra_client: Dict[str, Any], created_by: str, account_type: Optional[str] = None) -> "ServiceAccount":
        """Create ServiceAccount from Hydra client data."""
        # Note: Scope handling is now done through relationships, not a simple string field
        return cls(
            client_id=hydra_client.get("client_id"),
            client_secret=hydra_client.get("client_secret"),
            grant_types=hydra_client.get("grant_types", ["client_credentials"]),
            response_types=hydra_client.get("response_types", []),
            # scope field is handled separately via scope relationships
            token_endpoint_auth_method=hydra_client.get("token_endpoint_auth_method", "client_secret_basic"),
            audience=hydra_client.get("audience"),
            owner=hydra_client.get("owner"),
            client_metadata=hydra_client.get("metadata"),
            token_endpoint_auth_signing_alg=hydra_client.get("token_endpoint_auth_signing_alg"),
            client_name=hydra_client.get("client_name", ""),
            redirect_uris=hydra_client.get("redirect_uris", []),
            post_logout_redirect_uris=hydra_client.get("post_logout_redirect_uris", []),
            allowed_cors_origins=hydra_client.get("allowed_cors_origins", []),
            skip_consent=hydra_client.get("skip_consent", True),
            jwks=hydra_client.get("jwks"),
            jwks_uri=hydra_client.get("jwks_uri"),
            id_token_signed_response_alg=hydra_client.get("id_token_signed_response_alg", "RS256"),
            account_type=account_type or ServiceAccountType.SERVICE_TO_SERVICE.value,
            created_by=created_by
        )
