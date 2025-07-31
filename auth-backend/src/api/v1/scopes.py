"""
API endpoints for scope management.

This module provides REST API endpoints for managing OAuth2 scopes.
"""

from typing import List, Optional, Dict, Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.database import get_db
from ...schemas.scope import (
    ScopeCreate,
    ScopeUpdate,
    ScopeResponse,
    ScopeListResponse,
    ScopeBulkActivate,
    ScopeBulkDeactivate,
    ScopeBulkDelete,
    ScopeAppliesTo
)
from ...models.scope import Scope
from ...services.scope_service import ScopeService
from ...services.hydra_client import HydraAdminClient
from ...core.exceptions import NotFoundError, ConflictError, ValidationError

router = APIRouter(prefix="/scopes")


def get_scope_service(db: AsyncSession = Depends(get_db)) -> ScopeService:
    """Get scope service instance."""
    hydra_client = HydraAdminClient()
    return ScopeService(db, hydra_client)


def scope_to_response(scope: Scope) -> ScopeResponse:
    """Convert a Scope model to ScopeResponse schema."""
    from ...schemas.scope import ScopeAppliesTo as SchemaScopeAppliesTo
    
    # Convert model enums to schema enums
    applies_to_schema = [SchemaScopeAppliesTo(val.value) for val in scope.applies_to_list]
    
    return ScopeResponse(
        id=str(scope.id),
        name=scope.name,
        description=scope.description,
        applies_to=applies_to_schema,
        is_active=scope.is_active,
        service_account_count=scope.service_account_count
    )


@router.get("/", response_model=ScopeListResponse)
async def list_scopes(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of items to return"),
    active_only: bool = Query(False, description="Return only active scopes"),
    applies_to: Optional[ScopeAppliesTo] = Query(None, description="Filter by applies_to"),
    search: Optional[str] = Query(None, description="Search term for name or description"),
    scope_service: ScopeService = Depends(get_scope_service)
):
    """List scopes with optional filtering."""
    try:
        scopes, total = await scope_service.list_scopes(
            skip=skip,
            limit=limit,
            active_only=active_only,
            applies_to=applies_to,
            search=search
        )
        
        # Convert to response format using helper function
        scope_responses = [scope_to_response(scope) for scope in scopes]
        
        return ScopeListResponse(scopes=scope_responses, total=total)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=ScopeResponse, status_code=201)
async def create_scope(
    scope_data: ScopeCreate,
    scope_service: ScopeService = Depends(get_scope_service)
):
    """Create a new scope."""
    try:
        scope = await scope_service.create_scope(scope_data)
        return scope_to_response(scope)
    
    except ConflictError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{scope_id}", response_model=ScopeResponse)
async def get_scope(
    scope_id: UUID,
    scope_service: ScopeService = Depends(get_scope_service)
):
    """Get a scope by ID."""
    try:
        scope = await scope_service.get_scope(scope_id)
        return scope_to_response(scope)
    
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{scope_id}", response_model=ScopeResponse)
async def update_scope(
    scope_id: UUID,
    scope_data: ScopeUpdate,
    scope_service: ScopeService = Depends(get_scope_service)
):
    """Update a scope."""
    try:
        scope = await scope_service.update_scope(scope_id, scope_data)
        return scope_to_response(scope)
    
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{scope_id}", status_code=204)
async def delete_scope(
    scope_id: UUID,
    scope_service: ScopeService = Depends(get_scope_service)
):
    """Delete a scope."""
    try:
        await scope_service.delete_scope(scope_id)
    
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ConflictError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/bulk/activate")
async def bulk_activate_scopes(
    request: ScopeBulkActivate,
    scope_service: ScopeService = Depends(get_scope_service)
):
    """Bulk activate scopes."""
    try:
        scope_ids = [UUID(id_str) for id_str in request.scope_ids]
        updated_count = await scope_service.bulk_activate_scopes(scope_ids)
        return {"message": f"Activated {updated_count} scopes"}
    
    except ValueError as e:
        raise HTTPException(status_code=422, detail="Invalid UUID format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/bulk/deactivate")
async def bulk_deactivate_scopes(
    request: ScopeBulkDeactivate,
    scope_service: ScopeService = Depends(get_scope_service)
):
    """Bulk deactivate scopes."""
    try:
        scope_ids = [UUID(id_str) for id_str in request.scope_ids]
        updated_count = await scope_service.bulk_deactivate_scopes(scope_ids)
        return {"message": f"Deactivated {updated_count} scopes"}
    
    except ValueError as e:
        raise HTTPException(status_code=422, detail="Invalid UUID format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/bulk/delete")
async def bulk_delete_scopes(
    request: ScopeBulkDelete,
    scope_service: ScopeService = Depends(get_scope_service)
):
    """Bulk delete scopes."""
    try:
        scope_ids = [UUID(id_str) for id_str in request.scope_ids]
        deleted_count = await scope_service.bulk_delete_scopes(scope_ids)
        return {"message": f"Deleted {deleted_count} scopes"}
    
    except ValueError as e:
        raise HTTPException(status_code=422, detail="Invalid UUID format")
    except ConflictError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/for-account-type/{account_type}")
async def get_scopes_for_account_type(
    account_type: str,
    scope_service: ScopeService = Depends(get_scope_service)
):
    """Get scopes applicable to a specific service account type."""
    try:
        from ...models.service_account import ServiceAccountType
        
        # Validate account type
        if account_type not in [e.value for e in ServiceAccountType]:
            raise HTTPException(status_code=422, detail=f"Invalid account type: {account_type}")
        
        account_type_enum = ServiceAccountType(account_type)
        scopes = await scope_service.get_scopes_for_account_type(account_type_enum)
        
        scope_responses = [scope_to_response(scope) for scope in scopes]
        return {"scopes": scope_responses}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{scope_id}/services", response_model=List[Dict[str, Any]])
async def get_services_by_scope(
    scope_id: UUID,
    scope_service: ScopeService = Depends(get_scope_service)
):
    """Get all services with a specific scope."""
    try:
        # Check if scope exists - this will raise NotFoundError if not found
        await scope_service.get_scope(scope_id)
        
        services = await scope_service.get_service_accounts_by_scope(scope_id)
        return services
    
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{scope_id}/available-services", response_model=List[Dict[str, Any]])
async def get_available_services_for_scope(
    scope_id: UUID,
    scope_service: ScopeService = Depends(get_scope_service)
):
    """Get all services who don't have a specific scope."""
    try:
        # Check if scope exists - this will raise NotFoundError if not found
        await scope_service.get_scope(scope_id)
        
        services = await scope_service.get_service_accounts_without_scope(scope_id)
        return services
    
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{scope_id}/services/{service_id}")
async def add_service_to_scope(
    scope_id: UUID,
    service_id: UUID,
    scope_service: ScopeService = Depends(get_scope_service)
):
    """Add a service to a scope."""
    try:
        # TODO: Get performed_by from JWT token
        performed_by = "admin@example.com"  # Placeholder
        
        success = await scope_service.assign_service_to_scope(service_id, scope_id, performed_by)
        if not success:
            raise HTTPException(
                status_code=400,
                detail="Failed to assign service to scope"
            )
        
        return {"message": "Service added to scope successfully"}
    
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{scope_id}/services/{service_id}")
async def remove_service_from_scope(
    scope_id: UUID,
    service_id: UUID,
    scope_service: ScopeService = Depends(get_scope_service)
):
    """Remove a service from a scope."""
    try:
        # TODO: Get performed_by from JWT token
        performed_by = "admin@example.com"  # Placeholder
        
        success = await scope_service.remove_service_from_scope(service_id, scope_id, performed_by)
        if not success:
            raise HTTPException(
                status_code=400,
                detail="Failed to remove service from scope"
            )
        
        return {"message": "Service removed from scope successfully"}
    
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
