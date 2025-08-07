"""API endpoints for role management."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.database import get_db
from ...repositories.audit_log import AuditLogRepository
from ...repositories.role import RoleRepository
from ...repositories.service_account import ServiceAccountRepository
from ...repositories.user import UserRepository
from ...schemas.common import SuccessResponse
from ...schemas.role import RoleCreate, RoleResponse, RoleUpdate
from ...schemas.service_account import ServiceAccountResponse
from ...schemas.user import UserResponse
from ...services.role_service import RoleService

router = APIRouter()


def get_role_service(db: AsyncSession = Depends(get_db)) -> RoleService:
    """Dependency to get role service instance."""
    role_repo = RoleRepository(db)
    user_repo = UserRepository(db)
    service_account_repo = ServiceAccountRepository(db)
    audit_repo = AuditLogRepository(db)
    return RoleService(role_repo, user_repo, service_account_repo, audit_repo)


@router.get("/roles", response_model=List[RoleResponse])
async def get_roles(skip: int = 0, limit: int = 100, role_service: RoleService = Depends(get_role_service)):
    """Get all roles."""
    return await role_service.get_all_roles(skip=skip, limit=limit)


@router.get("/roles/{role_id}", response_model=RoleResponse)
async def get_role(role_id: str, role_service: RoleService = Depends(get_role_service)):
    """Get role by ID."""
    role = await role_service.get_role_by_id(role_id)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return role


@router.post("/roles", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(role_data: RoleCreate, role_service: RoleService = Depends(get_role_service)):
    """Create a new role."""
    try:
        # TODO: Get performed_by from JWT token
        performed_by = "admin@example.com"  # Placeholder
        return await role_service.create_role(role_data, performed_by)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/roles/{role_id}", response_model=RoleResponse)
async def update_role(role_id: str, role_data: RoleUpdate, role_service: RoleService = Depends(get_role_service)):
    """Update an existing role."""
    # TODO: Get performed_by from JWT token
    performed_by = "admin@example.com"  # Placeholder

    role = await role_service.update_role(role_id, role_data, performed_by)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return role


@router.delete("/roles/{role_id}", response_model=SuccessResponse)
async def delete_role(role_id: str, role_service: RoleService = Depends(get_role_service)):
    """Delete a role."""
    # TODO: Get performed_by from JWT token
    performed_by = "admin@example.com"  # Placeholder

    success = await role_service.delete_role(role_id, performed_by)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

    return SuccessResponse(message="Role deleted successfully")


@router.get("/roles/{role_id}/users", response_model=List[UserResponse])
async def get_users_by_role(role_id: str, role_service: RoleService = Depends(get_role_service)):
    """Get all users with a specific role."""
    # Check if role exists
    role = await role_service.get_role_by_id(role_id)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

    return await role_service.get_users_by_role(role_id)


@router.get("/roles/{role_id}/services", response_model=List[ServiceAccountResponse])
async def get_services_by_role(role_id: str, role_service: RoleService = Depends(get_role_service)):
    """Get all services with a specific role."""
    # Check if role exists
    role = await role_service.get_role_by_id(role_id)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

    return await role_service.get_service_accounts_by_role(role_id)


@router.get("/roles/{role_id}/available-users", response_model=List[UserResponse])
async def get_available_users_for_role(role_id: str, role_service: RoleService = Depends(get_role_service)):
    """Get all users who don't have a specific role."""
    # Check if role exists
    role = await role_service.get_role_by_id(role_id)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

    return await role_service.get_users_without_role(role_id)


@router.get("/roles/{role_id}/available-services", response_model=List[ServiceAccountResponse])
async def get_available_services_for_role(role_id: str, role_service: RoleService = Depends(get_role_service)):
    """Get all services who don't have a specific role."""
    # Check if role exists
    role = await role_service.get_role_by_id(role_id)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

    return await role_service.get_service_accounts_without_role(role_id)


@router.post("/roles/{role_id}/users/{user_id}", response_model=SuccessResponse)
async def add_user_to_role(role_id: str, user_id: str, role_service: RoleService = Depends(get_role_service)):
    """Add a user to a role."""
    # TODO: Get performed_by from JWT token
    performed_by = "admin@example.com"  # Placeholder

    success = await role_service.assign_user_to_role(user_id, role_id, performed_by)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to assign user to role")

    return SuccessResponse(message="User added to role successfully")


@router.delete("/roles/{role_id}/users/{user_id}", response_model=SuccessResponse)
async def remove_user_from_role(role_id: str, user_id: str, role_service: RoleService = Depends(get_role_service)):
    """Remove a user from a role."""
    # TODO: Get performed_by from JWT token
    performed_by = "admin@example.com"  # Placeholder

    success = await role_service.remove_user_from_role(user_id, role_id, performed_by)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to remove user from role")

    return SuccessResponse(message="User removed from role successfully")


@router.post("/roles/{role_id}/services/{service_id}", response_model=SuccessResponse)
async def add_service_to_role(role_id: str, service_id: str, role_service: RoleService = Depends(get_role_service)):
    """Add a service to a role."""
    # TODO: Get performed_by from JWT token
    performed_by = "admin@example.com"  # Placeholder

    success = await role_service.assign_service_to_role(service_id, role_id, performed_by)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to assign service to role")

    return SuccessResponse(message="Service added to role successfully")


@router.delete("/roles/{role_id}/services/{service_id}", response_model=SuccessResponse)
async def remove_service_from_role(
    role_id: str, service_id: str, role_service: RoleService = Depends(get_role_service)
):
    """Remove a service from a role."""
    # TODO: Get performed_by from JWT token
    performed_by = "admin@example.com"  # Placeholder

    success = await role_service.remove_service_from_role(service_id, role_id, performed_by)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to remove service from role")

    return SuccessResponse(message="Service removed from role successfully")
