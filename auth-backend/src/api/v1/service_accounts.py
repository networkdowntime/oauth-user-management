"""
Service Account API endpoints for OAuth2 client management.

Provides REST API endpoints for:
- CRUD operations on service accounts
- Role assignment management
- Hydra synchroniza        logger.info(f"Service account retrieved successfully: {service_account.id}")
        response_data = serialize_service_account_response(service_account)
        return response_datan
- Search and filtering
"""

import logging
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.database import get_db
from ...core.exceptions import (
    HydraIntegrationError,
    RoleNotFoundError,
    ServiceAccountAlreadyExistsError,
    ServiceAccountNotFoundError,
)
from ...models.service_account import ServiceAccount
from ...repositories.role import RoleRepository
from ...repositories.service_account import ServiceAccountRepository
from ...schemas.service_account import (
    ServiceAccountCreate,
    ServiceAccountListResponse,
    ServiceAccountResponse,
    ServiceAccountUpdate,
)
from ...services.hydra_client import HydraAdminClient
from ...services.service_account_service import ServiceAccountService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/service-accounts", tags=["Service Accounts"])


def serialize_service_account_response(service_account: ServiceAccount) -> ServiceAccountResponse:
    """
    Serialize a service account with its roles and scopes for API response.
    """
    from ...schemas.scope import ScopeResponse
    from ...schemas.service_account import RoleResponse

    # Serialize roles
    roles_data = []
    if hasattr(service_account, "roles") and service_account.roles:
        for role in service_account.roles:
            roles_data.append(
                RoleResponse(
                    id=role.id,
                    name=role.name,
                    description=role.description,
                    permissions=[],  # Placeholder as per schema
                    created_at=role.created_at,
                    updated_at=role.updated_at,
                )
            )

    # Serialize scopes
    scopes_data = []
    if hasattr(service_account, "scopes") and service_account.scopes:
        for scope in service_account.scopes:
            # Use the applies_to_list property which properly converts
            # the comma-separated string to a list of enum values
            applies_to_list = scope.applies_to_list

            scopes_data.append(
                ScopeResponse(
                    id=str(scope.id),  # Convert UUID to string
                    name=scope.name,
                    description=scope.description,
                    applies_to=applies_to_list,
                    is_active=scope.is_active,
                    service_account_count=0,  # Set to 0 to avoid async context issues
                )
            )

    # Create the service account response manually
    return ServiceAccountResponse(
        id=service_account.id,
        client_id=service_account.client_id,
        client_secret=service_account.client_secret,
        client_name=service_account.client_name,
        description=service_account.description,
        account_type=service_account.account_type,
        grant_types=service_account.grant_types or [],
        response_types=service_account.response_types or [],
        token_endpoint_auth_method=service_account.token_endpoint_auth_method,
        audience=service_account.audience,
        owner=service_account.owner,
        client_metadata=service_account.client_metadata,
        redirect_uris=service_account.redirect_uris or [],
        post_logout_redirect_uris=service_account.post_logout_redirect_uris or [],
        allowed_cors_origins=service_account.allowed_cors_origins or [],
        skip_consent=service_account.skip_consent,
        is_active=service_account.is_active,
        last_used_at=service_account.last_used_at,
        created_by=service_account.created_by,
        created_at=service_account.created_at,
        updated_at=service_account.updated_at,
        roles=roles_data,
        scopes=scopes_data,
    )


async def get_service_account_service(db: AsyncSession = Depends(get_db)) -> ServiceAccountService:
    """Dependency to get service account service."""
    service_account_repo = ServiceAccountRepository(db)
    role_repo = RoleRepository(db)
    hydra_client = HydraAdminClient()
    return ServiceAccountService(service_account_repo, role_repo, hydra_client)


@router.post("/", response_model=ServiceAccountResponse, status_code=status.HTTP_201_CREATED)
async def create_service_account(
    request: ServiceAccountCreate,
    service_account_service: ServiceAccountService = Depends(get_service_account_service),
) -> ServiceAccountResponse:
    """Create a new service account with automatic Hydra client registration."""
    try:
        logger.info(f"Creating service account: {request.client_name}")

        # Convert Pydantic model to dict for service layer
        service_account_data = request.model_dump()

        service_account = await service_account_service.create_service_account(
            service_account_data=service_account_data, sync_with_hydra=True
        )

        logger.info(f"Service account created successfully: {service_account.id}")

        # Use the same serialization function as other endpoints for consistency
        response_data = serialize_service_account_response(service_account)
        return response_data

    except ServiceAccountAlreadyExistsError as e:
        logger.warning(f"Service account already exists: {e}")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except HydraIntegrationError as e:
        logger.error(f"Hydra integration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"OAuth2 server integration error: {e}",
        )
    except Exception as e:
        logger.error(f"Unexpected error creating service account: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("/{service_account_id}", response_model=ServiceAccountResponse)
async def get_service_account(
    service_account_id: UUID,
    service_account_service: ServiceAccountService = Depends(get_service_account_service),
) -> ServiceAccountResponse:
    """Get a service account by ID."""
    try:
        service_account = await service_account_service.get_service_account(service_account_id)
        response_data = serialize_service_account_response(service_account)
        return response_data

    except ServiceAccountNotFoundError as e:
        logger.warning(f"Service account not found: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error retrieving service account {service_account_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("/", response_model=ServiceAccountListResponse)
async def list_service_accounts(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of items to return"),
    active_only: bool = Query(True, description="Only return active service accounts"),
    search: Optional[str] = Query(None, description="Search term for name or description"),
    service_account_service: ServiceAccountService = Depends(get_service_account_service),
) -> ServiceAccountListResponse:
    """List service accounts with optional filtering."""
    try:
        is_active = True if active_only else None

        service_accounts = await service_account_service.list_service_accounts(
            skip=skip, limit=limit, search=search, is_active=is_active
        )

        # Serialize each service account safely
        items = [serialize_service_account_response(sa) for sa in service_accounts]

        return ServiceAccountListResponse(items=items, total=len(service_accounts), skip=skip, limit=limit)

    except Exception as e:
        logger.error(f"Error listing service accounts: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.put("/{service_account_id}", response_model=ServiceAccountResponse)
async def update_service_account(
    service_account_id: UUID,
    request: ServiceAccountUpdate,
    sync_to_hydra: bool = Query(True, description="Synchronize changes to Hydra"),
    service_account_service: ServiceAccountService = Depends(get_service_account_service),
) -> ServiceAccountResponse:
    """Update a service account."""
    try:
        logger.info(f"Updating service account: {service_account_id}")

        # Convert Pydantic model to dict, excluding None values
        update_data = request.model_dump(exclude_unset=True)

        service_account = await service_account_service.update_service_account(
            service_account_id=service_account_id,
            update_data=update_data,
            sync_with_hydra=sync_to_hydra,
        )

        logger.info(f"Service account updated successfully: {service_account_id}")
        response_data = serialize_service_account_response(service_account)
        return response_data

    except ServiceAccountNotFoundError as e:
        logger.warning(f"Service account not found: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except HydraIntegrationError as e:
        logger.error(f"Hydra integration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"OAuth2 server integration error: {e}",
        )
    except Exception as e:
        logger.error(f"Error updating service account {service_account_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.delete("/{service_account_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service_account(
    service_account_id: UUID,
    sync_to_hydra: bool = Query(True, description="Remove client from Hydra"),
    service_account_service: ServiceAccountService = Depends(get_service_account_service),
):
    """Delete a service account."""
    try:
        logger.info(f"Deleting service account: {service_account_id}")

        await service_account_service.delete_service_account(
            service_account_id=service_account_id, sync_with_hydra=sync_to_hydra
        )

        logger.info(f"Service account deleted successfully: {service_account_id}")

    except ServiceAccountNotFoundError as e:
        logger.warning(f"Service account not found: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except HydraIntegrationError as e:
        logger.error(f"Hydra integration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"OAuth2 server integration error: {e}",
        )
    except Exception as e:
        logger.error(f"Error deleting service account {service_account_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


# Role Management Endpoints


@router.post("/{service_account_id}/roles/{role_id}", response_model=ServiceAccountResponse)
async def assign_role_to_service_account(
    service_account_id: UUID,
    role_id: UUID,
    service_account_service: ServiceAccountService = Depends(get_service_account_service),
) -> ServiceAccountResponse:
    """Assign a role to a service account."""
    try:
        logger.info(f"Assigning role {role_id} to service account {service_account_id}")

        service_account = await service_account_service.assign_role_to_service_account(
            service_account_id=service_account_id, role_id=role_id
        )

        logger.info(f"Role assigned successfully")
        response_data = serialize_service_account_response(service_account)
        return response_data

    except ServiceAccountNotFoundError as e:
        logger.warning(f"Service account not found: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RoleNotFoundError as e:
        logger.warning(f"Role not found: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error assigning role: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.delete("/{service_account_id}/roles/{role_id}", response_model=ServiceAccountResponse)
async def remove_role_from_service_account(
    service_account_id: UUID,
    role_id: UUID,
    service_account_service: ServiceAccountService = Depends(get_service_account_service),
) -> ServiceAccountResponse:
    """Remove a role from a service account."""
    try:
        logger.info(f"Removing role {role_id} from service account {service_account_id}")

        service_account = await service_account_service.remove_role_from_service_account(
            service_account_id=service_account_id, role_id=role_id
        )

        logger.info(f"Role removed successfully")
        response_data = serialize_service_account_response(service_account)
        return response_data

    except ServiceAccountNotFoundError as e:
        logger.warning(f"Service account not found: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RoleNotFoundError as e:
        logger.warning(f"Role not found: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error removing role: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


# Service Account Management Endpoints


@router.post("/{service_account_id}/activate", response_model=ServiceAccountResponse)
async def activate_service_account(
    service_account_id: UUID,
    service_account_service: ServiceAccountService = Depends(get_service_account_service),
) -> ServiceAccountResponse:
    """Activate a service account."""
    try:
        service_account = await service_account_service.update_service_account(
            service_account_id=service_account_id,
            update_data={"is_active": True},
            sync_with_hydra=True,
        )
        response_data = serialize_service_account_response(service_account)
        return response_data

    except ServiceAccountNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error activating service account: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.post("/{service_account_id}/deactivate", response_model=ServiceAccountResponse)
async def deactivate_service_account(
    service_account_id: UUID,
    service_account_service: ServiceAccountService = Depends(get_service_account_service),
) -> ServiceAccountResponse:
    """Deactivate a service account."""
    try:
        service_account = await service_account_service.update_service_account(
            service_account_id=service_account_id,
            update_data={"is_active": False},
            sync_with_hydra=True,
        )
        response_data = serialize_service_account_response(service_account)
        return response_data

    except ServiceAccountNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error deactivating service account: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.post("/{service_account_id}/sync", response_model=ServiceAccountResponse)
async def sync_service_account_to_hydra(
    service_account_id: UUID,
    service_account_service: ServiceAccountService = Depends(get_service_account_service),
) -> ServiceAccountResponse:
    """Manually synchronize a service account to Hydra."""
    try:
        # Get the service account and sync it by updating with no changes
        service_account = await service_account_service.get_service_account(service_account_id)

        # Force sync by doing a no-op update
        service_account = await service_account_service.update_service_account(
            service_account_id=service_account_id,
            update_data={},  # No changes, just sync
            sync_with_hydra=True,
        )

        response_data = serialize_service_account_response(service_account)
        return response_data

    except ServiceAccountNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except HydraIntegrationError as e:
        logger.error(f"Hydra integration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"OAuth2 server integration error: {e}",
        )
    except Exception as e:
        logger.error(f"Error syncing service account: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
