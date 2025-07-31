"""Service Account repository for database operations."""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload

from ..models.service_account import ServiceAccount
from ..models.role import Role
from .base import BaseRepository


class ServiceAccountRepository(BaseRepository[ServiceAccount]):
    """Repository for service account-related database operations."""
    
    def __init__(self, db: AsyncSession):
        super().__init__(ServiceAccount, db)
    
    async def get_by_client_id(self, client_id: str) -> Optional[ServiceAccount]:
        """Get service account by client_id."""
        result = await self.db.execute(
            select(ServiceAccount)
            .options(
                selectinload(ServiceAccount.roles),
                selectinload(ServiceAccount.scopes)
            )
            .where(ServiceAccount.client_id == client_id)
        )
        return result.scalar_one_or_none()
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ServiceAccount]:
        """Get all service accounts with pagination."""
        result = await self.db.execute(
            select(ServiceAccount)
            .options(
                selectinload(ServiceAccount.roles),
                selectinload(ServiceAccount.scopes)
            )
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_by_id(self, id: str) -> Optional[ServiceAccount]:
        """Get service account by ID."""
        result = await self.db.execute(
            select(ServiceAccount)
            .options(
                selectinload(ServiceAccount.roles),
                selectinload(ServiceAccount.scopes)
            )
            .where(ServiceAccount.id == id)
        )
        return result.scalar_one_or_none()
    
    async def search(self, query: str, skip: int = 0, limit: int = 100) -> List[ServiceAccount]:
        """Search service accounts by client_id or client_name."""
        search_filter = or_(
            ServiceAccount.client_id.ilike(f"%{query}%"),
            ServiceAccount.client_name.ilike(f"%{query}%"),
            ServiceAccount.description.ilike(f"%{query}%")
        )
        
        result = await self.db.execute(
            select(ServiceAccount)
            .options(selectinload(ServiceAccount.roles))
            .where(search_filter)
            .offset(skip)
            .limit(limit)
            .order_by(ServiceAccount.created_at.desc())
        )
        return list(result.scalars().all())
    
    async def get_active_accounts(self, skip: int = 0, limit: int = 100) -> List[ServiceAccount]:
        """Get all active service accounts."""
        result = await self.db.execute(
            select(ServiceAccount)
            .options(selectinload(ServiceAccount.roles))
            .where(ServiceAccount.is_active == True)
            .offset(skip)
            .limit(limit)
            .order_by(ServiceAccount.created_at.desc())
        )
        return list(result.scalars().all())
    
    async def assign_role(self, service_account_id: str, role_id: str) -> bool:
        """Assign a role to a service account."""
        service_account = await self.get_by_id(service_account_id)
        if not service_account:
            return False
        
        # Get the role directly using SQLAlchemy select
        role_result = await self.db.execute(
            select(Role).where(Role.id == role_id)
        )
        role = role_result.scalar_one_or_none()
        if not role:
            return False
        
        # Check if service account already has this role
        if any(str(r.id) == role_id for r in service_account.roles):
            return True  # Already assigned
        
        service_account.roles.append(role)
        await self.db.commit()
        return True
    
    async def remove_role(self, service_account_id: str, role_id: str) -> bool:
        """Remove a role from a service account."""
        service_account = await self.get_by_id(service_account_id)
        if not service_account:
            return False
        
        # Find and remove the role
        for i, role in enumerate(service_account.roles):
            if str(role.id) == role_id:
                service_account.roles.pop(i)
                await self.db.commit()
                return True
        
        return False  # Role not found
    
    async def update_last_used(self, service_account_id: str) -> bool:
        """Update the last_used_at timestamp for a service account."""
        from datetime import datetime, timezone
        
        service_account = await self.get_by_client_id(service_account_id)
        if not service_account:
            return False
        
        setattr(service_account, 'last_used_at', datetime.now(timezone.utc))
        await self.db.commit()
        return True
    
    async def deactivate(self, service_account_id: str) -> bool:
        """Deactivate a service account."""
        service_account = await self.get_by_client_id(service_account_id)
        if not service_account:
            return False
        
        setattr(service_account, 'is_active', False)
        await self.db.commit()
        return True
    
    async def activate(self, service_account_id: str) -> bool:
        """Activate a service account."""
        service_account = await self.get_by_client_id(service_account_id)
        if not service_account:
            return False
        
        setattr(service_account, 'is_active', True)
        await self.db.commit()
        return True
    
    async def client_id_exists(self, client_id: str, exclude_id: Optional[str] = None) -> bool:
        """Check if a client_id already exists."""
        query = select(ServiceAccount).where(ServiceAccount.client_id == client_id)
        
        if exclude_id:
            query = query.where(ServiceAccount.id != exclude_id)
        
        result = await self.db.execute(query)
        return result.scalar_one_or_none() is not None
    
    async def get_service_accounts_by_role(self, role_id: str) -> List[ServiceAccount]:
        """Get all service accounts with a specific role."""
        result = await self.db.execute(
            select(ServiceAccount)
            .options(selectinload(ServiceAccount.roles))
            .join(ServiceAccount.roles)
            .where(Role.id == role_id)
            .order_by(ServiceAccount.created_at.desc())
        )
        return list(result.scalars().all())
    
    async def get_service_accounts_without_role(self, role_id: str) -> List[ServiceAccount]:
        """Get all service accounts who don't have a specific role."""
        # Get all service accounts
        all_accounts_result = await self.db.execute(
            select(ServiceAccount)
            .options(selectinload(ServiceAccount.roles))
            .order_by(ServiceAccount.created_at.desc())
        )
        all_accounts = list(all_accounts_result.scalars().all())
        
        # Filter out service accounts who have the role
        accounts_without_role = [
            account for account in all_accounts 
            if not any(role.id == role_id for role in account.roles)
        ]
        
        return accounts_without_role
    
    async def delete_service_account_with_roles_and_scopes(self, service_account_id: str) -> bool:
        """Delete a service account and cascade delete all associated role and scope relationships."""
        # First get the service account with roles and scopes to verify it exists
        service_account = await self.get_by_id(service_account_id)
        if not service_account:
            return False
        
        # Clear all role relationships first
        service_account.roles.clear()
        
        # Clear all scope relationships
        service_account.scopes.clear()
        
        # Now delete the service account
        await self.db.delete(service_account)
        await self.db.commit()
        return True
