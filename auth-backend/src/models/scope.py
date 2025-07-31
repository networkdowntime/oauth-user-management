"""
Scope model for OAuth2 scope management.

This module defines the Scope model which represents OAuth2 scopes
that can be assigned to service accounts.
"""

from typing import List, Optional
import enum

from sqlalchemy import Column, String, Text, Boolean
from sqlalchemy.orm import relationship

from ..core.database import Base


class ScopeAppliesTo(enum.Enum):
    """Scope applies to enumeration."""
    SERVICE_TO_SERVICE = "Service-to-service"
    BROWSER = "Browser"


class Scope(Base):
    """
    Scope model for defining OAuth2 scopes.
    
    Attributes:
        name: Unique scope name (e.g., 'data:read', 'user:profile')
        description: Human-readable description of the scope
        applies_to: Which type of clients this scope applies to (Service-to-service, Browser, or both)
        is_active: Whether this scope is active and can be assigned
        service_accounts: List of service accounts with this scope
    """
    
    __tablename__ = "scopes"
    
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=False)
    applies_to = Column(String(20), nullable=False)  # Comma-separated values: "Service-to-service", "Browser", or "Service-to-service,Browser"
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    service_accounts = relationship(
        "ServiceAccount",
        secondary="service_account_scopes",
        back_populates="scopes",
        lazy="selectin"
    )
    
    def __repr__(self) -> str:
        return f"<Scope(name='{self.name}')>"
    
    @property
    def service_account_count(self) -> int:
        """Get the number of service accounts with this scope."""
        return len(self.service_accounts)
    
    @property
    def applies_to_list(self) -> List[ScopeAppliesTo]:
        """Get applies_to as a list of enums."""
        applies_to_value = str(self.applies_to or "")
        if not applies_to_value:
            return []
        applies_to_values = [val.strip() for val in applies_to_value.split(',') if val.strip()]
        return [ScopeAppliesTo(val) for val in applies_to_values if val in [e.value for e in ScopeAppliesTo]]
    
    @applies_to_list.setter
    def applies_to_list(self, values: List[ScopeAppliesTo]):
        """Set applies_to from a list of enums."""
        if not values:
            self.applies_to = ""
        else:
            self.applies_to = ",".join([val.value for val in values])
    
    def applies_to_service(self) -> bool:
        """Check if this scope applies to service-to-service clients."""
        return ScopeAppliesTo.SERVICE_TO_SERVICE in self.applies_to_list
    
    def applies_to_browser(self) -> bool:
        """Check if this scope applies to browser clients."""
        return ScopeAppliesTo.BROWSER in self.applies_to_list
    
    def is_applicable_to_account_type(self, account_type: str) -> bool:
        """Check if this scope is applicable to a given service account type."""
        from .service_account import ServiceAccountType
        
        if account_type == ServiceAccountType.SERVICE_TO_SERVICE.value:
            return self.applies_to_service()
        elif account_type == ServiceAccountType.BROWSER.value:
            return self.applies_to_browser()
        
        return False
    
    def get_service_account_names(self) -> List[str]:
        """Get list of service account names that have this scope."""
        return [sa.client_name for sa in self.service_accounts]
    
    def to_hydra_scope(self) -> str:
        """Convert to Hydra scope format (just the name)."""
        return str(self.name)
    
    @classmethod
    def from_hydra_scope(cls, hydra_scope_name: str, description: str = "", applies_to: Optional[List[ScopeAppliesTo]] = None):
        """Create a Scope instance from Hydra scope information."""
        if applies_to is None:
            applies_to = [ScopeAppliesTo.SERVICE_TO_SERVICE, ScopeAppliesTo.BROWSER]  # Default to both
            
        scope = cls(
            name=hydra_scope_name,
            description=description or f"OAuth2 scope: {hydra_scope_name}",
            is_active=True
        )
        scope.applies_to_list = applies_to
        return scope
