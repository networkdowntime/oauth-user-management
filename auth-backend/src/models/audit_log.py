"""
Audit log model for tracking system events.

This module defines the AuditLog model which tracks all important
system events for security and compliance purposes.
"""

from datetime import datetime
from typing import Optional, Dict, Any
import json

from sqlalchemy import Column, String, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from ..core.database import Base


class AuditLog(Base):
    """
    Audit log model for tracking system events.
    
    Attributes:
        action: The action that was performed (e.g., 'user_created', 'login_success')
        resource_type: Type of resource affected (e.g., 'user', 'role', 'service')
        resource_id: ID of the affected resource
        details: Additional details about the action (stored as JSON)
        performed_by: Email or ID of who performed the action
        ip_address: IP address from which the action was performed
        user_agent: User agent string of the client
        timestamp: When the action occurred
    """
    
    __tablename__ = "audit_logs"
    
    action = Column(String(100), nullable=False, index=True)
    resource_type = Column(String(50), nullable=False, index=True)
    resource_id = Column(String(255), nullable=True, index=True)
    details = Column(JSON, nullable=True)
    performed_by = Column(String(255), nullable=False, index=True)
    ip_address = Column(String(45), nullable=True)  # IPv6 max length
    user_agent = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.now, nullable=False, index=True)
    
    def __repr__(self) -> str:
        return f"<AuditLog(action='{self.action}', resource_type='{self.resource_type}')>"
    
    @property
    def details_str(self) -> str:
        """Get details as a formatted string."""
        if self.details:
            return json.dumps(self.details, indent=2)
        return ""
    
    @classmethod
    def create_log(
        cls,
        action: str,
        resource_type: str,
        performed_by: str,
        resource_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> "AuditLog":
        """
        Create a new audit log entry.
        
        Args:
            action: The action that was performed
            resource_type: Type of resource affected
            performed_by: Who performed the action
            resource_id: ID of the affected resource
            details: Additional details about the action
            ip_address: IP address from which the action was performed
            user_agent: User agent string of the client
            
        Returns:
            AuditLog: New audit log instance
        """
        return cls(
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            performed_by=performed_by,
            ip_address=ip_address,
            user_agent=user_agent,
        )
