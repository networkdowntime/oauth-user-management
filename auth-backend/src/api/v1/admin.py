"""API endpoints for admin operations."""

from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.database import get_db
from ...repositories.audit_log import AuditLogRepository
from ...schemas.audit import AuditLogResponse
from ...schemas.common import SystemStatsResponse
from ...services.admin_service import AdminService

router = APIRouter()


def get_admin_service(db: AsyncSession = Depends(get_db)) -> AdminService:
    """Dependency to get admin service instance."""
    from ...repositories.role import RoleRepository
    from ...repositories.service_account import ServiceAccountRepository
    from ...repositories.user import UserRepository

    audit_repo = AuditLogRepository(db)
    user_repo = UserRepository(db)
    role_repo = RoleRepository(db)
    service_account_repo = ServiceAccountRepository(db)
    return AdminService(audit_repo, user_repo, role_repo, service_account_repo)


@router.get("/audit-logs", response_model=List[AuditLogResponse])
async def get_audit_logs(
    resource_type: Optional[str] = None,
    resource_id: Optional[str] = None,
    limit: int = 100,
    admin_service: AdminService = Depends(get_admin_service),
):
    """Get audit logs with optional filtering."""
    return await admin_service.get_audit_logs(resource_type=resource_type, resource_id=resource_id, limit=limit)


@router.get("/system-stats", response_model=SystemStatsResponse)
async def get_system_stats(admin_service: AdminService = Depends(get_admin_service)):
    """Get system statistics."""
    return await admin_service.get_system_stats()


@router.get("/jwt-public-key", response_model=str)
async def get_jwt_public_key(admin_service: AdminService = Depends(get_admin_service)):
    """Get JWT public key."""
    return await admin_service.get_jwt_public_key()
