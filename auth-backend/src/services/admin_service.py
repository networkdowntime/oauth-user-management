"""Admin service for system-wide operations."""

from typing import List, Optional
from pathlib import Path

from ..repositories.audit_log import AuditLogRepository
from ..repositories.user import UserRepository
from ..repositories.role import RoleRepository
from ..schemas.audit import AuditLogResponse
from ..schemas.common import SystemStatsResponse
from ..core.config import settings
from ..core.logging_config import get_logger

logger = get_logger(__name__)


class AdminService:
    """Service for admin-related operations."""
    
    def __init__(self, audit_repo: AuditLogRepository, user_repo: UserRepository, role_repo: RoleRepository):
        self.audit_repo = audit_repo
        self.user_repo = user_repo
        self.role_repo = role_repo
    
    async def get_audit_logs(
        self,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        limit: int = 100
    ) -> List[AuditLogResponse]:
        """Get audit logs with optional filtering."""
        logs = await self.audit_repo.get_by_resource(
            resource_type=resource_type,
            resource_id=resource_id,
            limit=limit
        )
        
        return [
            AuditLogResponse(
                id=str(log.id),
                action=log.action,
                resource_type=log.resource_type,
                resource_id=log.resource_id,
                details=log.details,
                performed_by=log.performed_by,
                ip_address=log.ip_address,
                user_agent=log.user_agent,
                timestamp=log.timestamp
            )
            for log in logs
        ]
    
    async def get_system_stats(self) -> SystemStatsResponse:
        """Get system statistics."""
        # Count users (excluding service accounts if they have a different user_type)  
        users = await self.user_repo.get_all(limit=1000)  # Get all users with a reasonable limit
        user_count = len([user for user in users if getattr(user, 'user_type', 'user') == "user"])
        
        # Count service accounts (if they exist as a separate user type)
        service_count = len([user for user in users if getattr(user, 'user_type', 'user') == "service"])
        
        # Count roles
        roles = await self.role_repo.get_all(limit=1000)  # Get all roles with a reasonable limit
        role_count = len(roles)
        
        return SystemStatsResponse(
            users=user_count,
            services=service_count,
            roles=role_count
        )
    
    async def get_jwt_public_key(self) -> str:
        """Get JWT public key."""
        try:
            public_key_path = settings.jwt_public_key_path
            if public_key_path.exists():
                return public_key_path.read_text()
            else:
                # Return a placeholder key for development
                return """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA1234567890...
-----END PUBLIC KEY-----"""
        except Exception as e:
            logger.error(f"Failed to read JWT public key: {e}")
            raise ValueError("JWT public key not available")
