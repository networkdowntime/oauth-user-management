"""
Service layer for scope management with async support.

This module handles business logic for managing OAuth2 scopes,
including synchronization with Hydra admin API.
"""

from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID

from sqlalchemy import and_, delete, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.exceptions import ConflictError, NotFoundError
from ..models.scope import Scope, ScopeAppliesTo
from ..models.service_account import ServiceAccount, ServiceAccountType
from ..schemas.scope import ScopeAppliesTo as SchemaScopeAppliesTo
from ..schemas.scope import (
    ScopeCreate,
    ScopeUpdate,
)
from .hydra_client import HydraAdminClient


class ScopeService:
    """Service for managing OAuth2 scopes."""

    def __init__(self, db: AsyncSession, hydra_client: HydraAdminClient):
        self.db = db
        self.hydra_client = hydra_client

    async def create_scope(self, scope_data: ScopeCreate) -> Scope:
        """Create a new scope."""
        # Check if scope name already exists
        result = await self.db.execute(select(Scope).where(Scope.name == scope_data.name))
        existing_scope = result.scalar_one_or_none()
        if existing_scope:
            raise ConflictError(f"Scope with name '{scope_data.name}' already exists")

        # Create scope instance
        scope = Scope(name=scope_data.name, description=scope_data.description, is_active=scope_data.is_active)
        # Convert schema enum to model enum
        model_applies_to = [ScopeAppliesTo(val.value) for val in scope_data.applies_to]
        scope.applies_to_list = model_applies_to

        self.db.add(scope)
        await self.db.commit()
        await self.db.refresh(scope)

        return scope

    async def get_scope(self, scope_id: UUID) -> Scope:
        """Get a scope by ID."""
        result = await self.db.execute(select(Scope).where(Scope.id == scope_id))
        scope = result.scalar_one_or_none()
        if not scope:
            raise NotFoundError(f"Scope with ID {scope_id} not found")
        return scope

    async def get_scope_by_name(self, name: str) -> Optional[Scope]:
        """Get a scope by name."""
        result = await self.db.execute(select(Scope).where(Scope.name == name))
        return result.scalar_one_or_none()

    async def list_scopes(
        self,
        skip: int = 0,
        limit: int = 100,
        active_only: bool = False,
        applies_to: Optional[SchemaScopeAppliesTo] = None,
        search: Optional[str] = None,
    ) -> Tuple[List[Scope], int]:
        """List scopes with optional filtering."""
        # Build the base query
        query = select(Scope)
        count_query = select(func.count(Scope.id))

        # Apply filters
        conditions = []
        if active_only:
            conditions.append(Scope.is_active == True)

        if applies_to:
            # Since applies_to is stored as comma-separated string, use LIKE
            conditions.append(Scope.applies_to.like(f"%{applies_to.value}%"))

        if search:
            search_filter = or_(Scope.name.ilike(f"%{search}%"), Scope.description.ilike(f"%{search}%"))
            conditions.append(search_filter)

        if conditions:
            query = query.where(and_(*conditions))
            count_query = count_query.where(and_(*conditions))

        # Get total count
        total_result = await self.db.execute(count_query)
        total = total_result.scalar() or 0

        # Apply pagination and execute
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        scopes = result.scalars().all()

        return list(scopes), total

    async def update_scope(self, scope_id: UUID, scope_data: ScopeUpdate) -> Scope:
        """Update a scope."""
        # Get the existing scope
        scope = await self.get_scope(scope_id)

        # Update fields if provided
        if scope_data.description is not None:
            scope.description = scope_data.description
        if scope_data.is_active is not None:
            scope.is_active = scope_data.is_active
        if scope_data.applies_to is not None:
            model_applies_to = [ScopeAppliesTo(val.value) for val in scope_data.applies_to]
            scope.applies_to_list = model_applies_to

        await self.db.commit()
        await self.db.refresh(scope)

        return scope

    async def delete_scope(self, scope_id: UUID) -> None:
        """Delete a scope."""
        scope = await self.get_scope(scope_id)

        # Check if scope is in use by service accounts
        # For simplicity, let's check if any service accounts are using this scope
        # In a real implementation, you might want to check the many-to-many relationship

        await self.db.delete(scope)
        await self.db.commit()

    async def bulk_activate_scopes(self, scope_ids: List[UUID]) -> int:
        """Bulk activate scopes."""
        result = await self.db.execute(update(Scope).where(Scope.id.in_(scope_ids)).values(is_active=True))
        await self.db.commit()
        return result.rowcount

    async def bulk_deactivate_scopes(self, scope_ids: List[UUID]) -> int:
        """Bulk deactivate scopes."""
        result = await self.db.execute(update(Scope).where(Scope.id.in_(scope_ids)).values(is_active=False))
        await self.db.commit()
        return result.rowcount

    async def bulk_delete_scopes(self, scope_ids: List[UUID]) -> int:
        """Bulk delete scopes."""
        # Check if any scopes are in use
        # For simplicity, we'll proceed with deletion
        # In production, you'd want to check relationships first

        result = await self.db.execute(delete(Scope).where(Scope.id.in_(scope_ids)))
        await self.db.commit()
        return result.rowcount

    async def get_scopes_for_account_type(self, account_type: ServiceAccountType) -> List[Scope]:
        """Get scopes that apply to a specific service account type."""
        # Map service account types to scope applies_to values
        type_mapping = {
            ServiceAccountType.SERVICE_TO_SERVICE: ScopeAppliesTo.SERVICE_TO_SERVICE,
            ServiceAccountType.BROWSER: ScopeAppliesTo.BROWSER,
        }

        applies_to = type_mapping.get(account_type)
        if not applies_to:
            return []

        result = await self.db.execute(
            select(Scope).where(and_(Scope.is_active == True, Scope.applies_to.like(f"%{applies_to.value}%")))
        )
        return list(result.scalars().all())

    async def get_service_accounts_by_scope(self, scope_id: UUID) -> List[Dict[str, Any]]:
        """Get all service accounts with a specific scope."""
        result = await self.db.execute(select(ServiceAccount).join(ServiceAccount.scopes).where(Scope.id == scope_id))
        service_accounts = result.scalars().all()

        # Convert to simple dict format (not using Pydantic response for internal API)
        return [
            {
                "id": str(sa.id),
                "client_id": sa.client_id,
                "client_name": sa.client_name,
                "account_type": sa.account_type,
                "is_active": sa.is_active,
                "description": sa.description,
                "created_by": sa.created_by,
            }
            for sa in service_accounts
        ]

    async def get_service_accounts_without_scope(self, scope_id: UUID) -> List[Dict[str, Any]]:
        """Get all service accounts who don't have a specific scope."""
        # Get all service accounts that don't have this scope
        subquery = select(ServiceAccount.id).join(ServiceAccount.scopes).where(Scope.id == scope_id)

        result = await self.db.execute(select(ServiceAccount).where(ServiceAccount.id.not_in(subquery)))
        service_accounts = result.scalars().all()

        return [
            {
                "id": str(sa.id),
                "client_id": sa.client_id,
                "client_name": sa.client_name,
                "account_type": sa.account_type,
                "is_active": sa.is_active,
                "description": sa.description,
                "created_by": sa.created_by,
            }
            for sa in service_accounts
        ]

    async def assign_service_to_scope(self, service_id: UUID, scope_id: UUID, performed_by: str) -> bool:
        """Assign a service account to a scope."""
        # Get the service account
        service_result = await self.db.execute(select(ServiceAccount).where(ServiceAccount.id == service_id))
        service_account = service_result.scalar_one_or_none()
        if not service_account:
            raise NotFoundError(f"Service account with ID {service_id} not found")

        # Get the scope
        scope_result = await self.db.execute(select(Scope).where(Scope.id == scope_id))
        scope = scope_result.scalar_one_or_none()
        if not scope:
            raise NotFoundError(f"Scope with ID {scope_id} not found")

        # Check if already assigned
        if scope in service_account.scopes:
            return True  # Already assigned

        # Assign the scope
        service_account.scopes.append(scope)
        await self.db.commit()

        # TODO: Add audit log entry
        # await self.audit_repo.log_action(...)

        return True

    async def remove_service_from_scope(self, service_id: UUID, scope_id: UUID, performed_by: str) -> bool:
        """Remove a service account from a scope."""
        # Get the service account
        service_result = await self.db.execute(select(ServiceAccount).where(ServiceAccount.id == service_id))
        service_account = service_result.scalar_one_or_none()
        if not service_account:
            raise NotFoundError(f"Service account with ID {service_id} not found")

        # Get the scope
        scope_result = await self.db.execute(select(Scope).where(Scope.id == scope_id))
        scope = scope_result.scalar_one_or_none()
        if not scope:
            raise NotFoundError(f"Scope with ID {scope_id} not found")

        # Check if assigned
        if scope not in service_account.scopes:
            return True  # Not assigned anyway

        # Remove the scope
        service_account.scopes.remove(scope)
        await self.db.commit()

        # TODO: Add audit log entry
        # await self.audit_repo.log_action(...)

        return True
