"""API endpoints for user management."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.database import get_db
from ...repositories.user import UserRepository
from ...repositories.role import RoleRepository
from ...repositories.audit_log import AuditLogRepository
from ...services.user_service import UserService
from ...schemas.user import UserResponse, UserCreate, UserUpdate, UserPasswordReset
from ...schemas.common import SuccessResponse
from ...schemas.audit import AuditLogResponse

router = APIRouter()


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    """Dependency to get user service instance."""
    user_repo = UserRepository(db)
    role_repo = RoleRepository(db)
    audit_repo = AuditLogRepository(db)
    return UserService(user_repo, role_repo, audit_repo)


@router.get("/users", response_model=List[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    user_service: UserService = Depends(get_user_service)
):
    """Get all users."""
    return await user_service.get_users(skip=skip, limit=limit)


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service)
):
    """Get user by ID."""
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    """Create a new user."""
    try:
        # TODO: Get performed_by from JWT token
        performed_by = "admin@example.com"  # Placeholder
        return await user_service.create_user(user_data, performed_by)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    user_service: UserService = Depends(get_user_service)
):
    """Update an existing user."""
    # TODO: Get performed_by from JWT token
    performed_by = "admin@example.com"  # Placeholder
    
    user = await user_service.update_user(user_id, user_data, performed_by)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.delete("/users/{user_id}", response_model=SuccessResponse)
async def delete_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service)
):
    """Delete a user."""
    # TODO: Get performed_by from JWT token
    performed_by = "admin@example.com"  # Placeholder
    
    success = await user_service.delete_user(user_id, performed_by)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return SuccessResponse(message="User deleted successfully")


@router.post("/users/{user_id}/reset-password", response_model=SuccessResponse)
async def reset_user_password(
    user_id: str,
    password_data: UserPasswordReset,
    user_service: UserService = Depends(get_user_service)
):
    """Reset a user's password."""
    # TODO: Get performed_by from JWT token
    performed_by = "admin@example.com"  # Placeholder
    
    success = await user_service.reset_user_password(user_id, password_data, performed_by)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return SuccessResponse(message="Password reset successfully")


@router.post("/users/{user_id}/roles/{role_id}", response_model=SuccessResponse)
async def assign_role_to_user(
    user_id: str,
    role_id: str,
    user_service: UserService = Depends(get_user_service)
):
    """Assign a role to a user."""
    # TODO: Get performed_by from JWT token
    performed_by = "admin@example.com"  # Placeholder
    
    success = await user_service.assign_role_to_user(user_id, role_id, performed_by)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to assign role to user"
        )
    
    return SuccessResponse(message="Role assigned successfully")


@router.delete("/users/{user_id}/roles/{role_id}", response_model=SuccessResponse)
async def remove_role_from_user(
    user_id: str,
    role_id: str,
    user_service: UserService = Depends(get_user_service)
):
    """Remove a role from a user."""
    # TODO: Get performed_by from JWT token
    performed_by = "admin@example.com"  # Placeholder
    
    success = await user_service.remove_role_from_user(user_id, role_id, performed_by)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to remove role from user"
        )
    
    return SuccessResponse(message="Role removed successfully")


@router.post("/users/{user_id}/lock", response_model=UserResponse)
async def lock_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service)
):
    """Lock a user account."""
    from datetime import datetime, timedelta, timezone
    
    # TODO: Get performed_by from JWT token
    performed_by = "admin@example.com"  # Placeholder
    
    # Lock for 24 hours
    lock_until = datetime.now(timezone.utc) + timedelta(hours=24)
    
    update_data = UserUpdate(locked_until=lock_until)
    user = await user_service.update_user(user_id, update_data, performed_by)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.post("/users/{user_id}/unlock", response_model=UserResponse)
async def unlock_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service)
):
    """Unlock a user account."""
    # TODO: Get performed_by from JWT token
    performed_by = "admin@example.com"  # Placeholder
    
    update_data = UserUpdate(locked_until=None)
    user = await user_service.update_user(user_id, update_data, performed_by)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.get("/users/{user_id}/audit-logs", response_model=List[AuditLogResponse])
async def get_user_audit_logs(
    user_id: str,
    limit: int = 10,
    user_service: UserService = Depends(get_user_service),
    db: AsyncSession = Depends(get_db)
):
    """Get audit logs for a specific user."""
    # Check if user exists
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get audit logs from repository
    audit_repo = AuditLogRepository(db)
    audit_logs = await audit_repo.get_user_logs(user_id, limit)
    
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
        for log in audit_logs
    ]
