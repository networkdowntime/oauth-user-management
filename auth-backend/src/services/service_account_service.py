"""
Service Account Service

Provides business logic for OAuth2 service account management including:
- CRUD operations with database synchronization
- Hydra OAuth2 client synchronization
- Role assignment management
- Search and filtering capabilities
"""
import logging
from typing import List, Optional, Dict, Any
from uuid import UUID

from src.models.service_account import ServiceAccount
from src.models.scope import Scope
from src.repositories.service_account import ServiceAccountRepository
from src.repositories.role import RoleRepository
from src.services.hydra_client import HydraAdminClient
from src.core.exceptions import (
    ServiceAccountNotFoundError,
    ServiceAccountAlreadyExistsError,
    RoleNotFoundError,
    HydraIntegrationError
)

logger = logging.getLogger(__name__)


class ServiceAccountService:
    """Service layer for OAuth2 service account management."""
    
    def __init__(
        self,
        service_account_repo: ServiceAccountRepository,
        role_repo: RoleRepository,
        hydra_client: HydraAdminClient
    ):
        self.service_account_repo = service_account_repo
        self.role_repo = role_repo
        self.hydra_client = hydra_client
    
    async def create_service_account(
        self,
        service_account_data: Dict[str, Any],
        sync_with_hydra: bool = True
    ) -> ServiceAccount:
        """
        Create a new service account with optional Hydra synchronization.
        
        Args:
            service_account_data: Service account properties
            sync_with_hydra: Whether to sync with Hydra OAuth2 server
            
        Returns:
            Created service account
            
        Raises:
            ServiceAccountAlreadyExistsError: If client_id already exists
            HydraIntegrationError: If Hydra sync fails
        """
        logger.info(f"Creating service account with client_id: {service_account_data.get('client_id')}")
        
        # Check if client_id already exists
        client_id = service_account_data.get('client_id')
        if client_id:
            existing = await self.service_account_repo.get_by_client_id(client_id)
            if existing:
                raise ServiceAccountAlreadyExistsError(
                    f"Service account with client_id '{client_id}' already exists"
                )
        
        # Handle scope assignment if scope_ids is provided
        scope_ids = service_account_data.pop('scope_ids', None)
        
        # Handle role assignment if role_ids is provided
        role_ids = service_account_data.pop('role_ids', None)
        
        # Create service account in database
        service_account = await self.service_account_repo.create(service_account_data)
        
        # Assign scopes if provided
        if scope_ids:
            await self._update_service_account_scopes(service_account, scope_ids)
        
        # Assign roles if provided
        if role_ids:
            await self._update_service_account_roles(service_account, role_ids)
        
        # Refresh with roles and scopes loaded for proper serialization
        service_account = await self.service_account_repo.get_by_id(str(service_account.id))
        if not service_account:
            raise ValueError("Failed to retrieve created service account")
        
        try:
            # Sync with Hydra if requested
            if sync_with_hydra:
                hydra_client_data = service_account.to_hydra_client()
                await self.hydra_client.create_client(hydra_client_data)
                logger.info(f"Successfully synced service account {service_account.client_id} with Hydra")
                
        except Exception as e:
            # If Hydra sync fails, delete the database record to maintain consistency
            logger.error(f"Failed to sync with Hydra, rolling back: {e}")
            await self.service_account_repo.delete(str(service_account.id))
            raise HydraIntegrationError(f"Failed to create OAuth2 client in Hydra: {e}")
        
        logger.info(f"Successfully created service account: {service_account.id}")
        return service_account
    
    async def get_service_account(self, service_account_id: UUID) -> ServiceAccount:
        """
        Get service account by ID.
        
        Args:
            service_account_id: Service account UUID
            
        Returns:
            Service account with roles
            
        Raises:
            ServiceAccountNotFoundError: If service account not found
        """
        service_account = await self.service_account_repo.get_by_id(str(service_account_id))
        if not service_account:
            raise ServiceAccountNotFoundError(f"Service account {service_account_id} not found")
        
        return service_account
    
    async def get_service_account_by_client_id(self, client_id: str) -> ServiceAccount:
        """
        Get service account by OAuth2 client_id.
        
        Args:
            client_id: OAuth2 client identifier
            
        Returns:
            Service account with roles
            
        Raises:
            ServiceAccountNotFoundError: If service account not found
        """
        service_account = await self.service_account_repo.get_by_client_id(client_id)
        if not service_account:
            raise ServiceAccountNotFoundError(f"Service account with client_id '{client_id}' not found")
        
        return service_account
    
    async def update_service_account(
        self,
        service_account_id: UUID,
        update_data: Dict[str, Any],
        sync_with_hydra: bool = True
    ) -> ServiceAccount:
        """
        Update service account with optional Hydra synchronization.
        
        Args:
            service_account_id: Service account UUID
            update_data: Updated properties
            sync_with_hydra: Whether to sync with Hydra OAuth2 server
            
        Returns:
            Updated service account
            
        Raises:
            ServiceAccountNotFoundError: If service account not found
            HydraIntegrationError: If Hydra sync fails
        """
        logger.info(f"Updating service account: {service_account_id}")
        
        # Get existing service account
        service_account = await self.get_service_account(service_account_id)
        
        # Handle scope assignment if scope_ids is provided
        if 'scope_ids' in update_data:
            scope_ids = update_data.pop('scope_ids')  # Remove from update_data
            if scope_ids is not None:
                await self._update_service_account_scopes(service_account, scope_ids)
        
        # Handle role assignment if role_ids is provided
        if 'role_ids' in update_data:
            role_ids = update_data.pop('role_ids')  # Remove from update_data
            if role_ids is not None:
                await self._update_service_account_roles(service_account, role_ids)
        
        # Update in database
        updated_service_account = await self.service_account_repo.update(
            service_account, update_data
        )
        
        try:
            # Sync with Hydra if requested
            if sync_with_hydra:
                hydra_client_data = updated_service_account.to_hydra_client()
                await self.hydra_client.update_client(
                    str(updated_service_account.client_id), hydra_client_data
                )
                logger.info(f"Successfully synced updated service account {updated_service_account.client_id} with Hydra")
                
        except Exception as e:
            logger.error(f"Failed to sync update with Hydra: {e}")
            # Note: We don't rollback database changes for update sync failures
            # as the database state should be the source of truth
            raise HydraIntegrationError(f"Failed to update OAuth2 client in Hydra: {e}")
        
        logger.info(f"Successfully updated service account: {service_account_id}")
        return updated_service_account
    
    async def delete_service_account(
        self,
        service_account_id: UUID,
        sync_with_hydra: bool = True
    ) -> None:
        """
        Delete service account with optional Hydra synchronization.
        
        Args:
            service_account_id: Service account UUID
            sync_with_hydra: Whether to sync with Hydra OAuth2 server
            
        Raises:
            ServiceAccountNotFoundError: If service account not found
            HydraIntegrationError: If Hydra sync fails
        """
        logger.info(f"Deleting service account: {service_account_id}")
        
        # Get existing service account
        service_account = await self.get_service_account(service_account_id)
        
        try:
            # Delete from Hydra first if requested
            if sync_with_hydra:
                await self.hydra_client.delete_client(str(service_account.client_id))
                logger.info(f"Successfully deleted OAuth2 client {service_account.client_id} from Hydra")
                
        except Exception as e:
            logger.error(f"Failed to delete from Hydra: {e}")
            # Continue with database deletion even if Hydra sync fails
            # as database should be the source of truth
        
        # Delete from database using cascade deletion to remove all role and scope relationships
        await self.service_account_repo.delete_service_account_with_roles_and_scopes(str(service_account_id))
        logger.info(f"Successfully deleted service account with all associations: {service_account_id}")
    
    async def list_service_accounts(
        self,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> List[ServiceAccount]:
        """
        List service accounts with optional filtering.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            search: Search term for client_id, name, or description
            is_active: Filter by active status
            
        Returns:
            List of service accounts
        """
        return await self.service_account_repo.search(
            query="",  # Empty query to get all, filtered by other params
            skip=skip,
            limit=limit
        )
    
    async def assign_role_to_service_account(
        self,
        service_account_id: UUID,
        role_id: UUID
    ) -> ServiceAccount:
        """
        Assign a role to a service account.
        
        Args:
            service_account_id: Service account UUID
            role_id: Role UUID
            
        Returns:
            Updated service account with roles
            
        Raises:
            ServiceAccountNotFoundError: If service account not found
            RoleNotFoundError: If role not found
        """
        logger.info(f"Assigning role {role_id} to service account {service_account_id}")
        
        # Verify service account exists
        await self.get_service_account(service_account_id)
        
        # Verify role exists
        role = await self.role_repo.get_by_id(str(role_id))
        if not role:
            raise RoleNotFoundError(f"Role {role_id} not found")
        
        # Assign role
        success = await self.service_account_repo.assign_role(
            str(service_account_id), str(role_id)
        )
        
        if not success:
            raise RoleNotFoundError(f"Failed to assign role {role_id} to service account {service_account_id}")
        
        # Return updated service account
        service_account = await self.get_service_account(service_account_id)
        logger.info(f"Successfully assigned role {role_id} to service account {service_account_id}")
        return service_account
    
    async def remove_role_from_service_account(
        self,
        service_account_id: UUID,
        role_id: UUID
    ) -> ServiceAccount:
        """
        Remove a role from a service account.
        
        Args:
            service_account_id: Service account UUID
            role_id: Role UUID
            
        Returns:
            Updated service account with roles
            
        Raises:
            ServiceAccountNotFoundError: If service account not found
            RoleNotFoundError: If role not found or not assigned
        """
        logger.info(f"Removing role {role_id} from service account {service_account_id}")
        
        # Verify service account exists
        await self.get_service_account(service_account_id)
        
        # Remove role
        success = await self.service_account_repo.remove_role(
            str(service_account_id), str(role_id)
        )
        
        if not success:
            raise RoleNotFoundError(f"Role {role_id} not found or not assigned to service account {service_account_id}")
        
        # Return updated service account
        service_account = await self.get_service_account(service_account_id)
        logger.info(f"Successfully removed role {role_id} from service account {service_account_id}")
        return service_account
    
    async def activate_service_account(self, service_account_id: UUID) -> ServiceAccount:
        """
        Activate a service account.
        
        Args:
            service_account_id: Service account UUID
            
        Returns:
            Updated service account
        """
        logger.info(f"Activating service account: {service_account_id}")
        success = await self.service_account_repo.activate(str(service_account_id))
        if not success:
            raise ServiceAccountNotFoundError(f"Service account {service_account_id} not found")
        
        return await self.get_service_account(service_account_id)
    
    async def deactivate_service_account(self, service_account_id: UUID) -> ServiceAccount:
        """
        Deactivate a service account.
        
        Args:
            service_account_id: Service account UUID
            
        Returns:
            Updated service account
        """
        logger.info(f"Deactivating service account: {service_account_id}")
        success = await self.service_account_repo.deactivate(str(service_account_id))
        if not success:
            raise ServiceAccountNotFoundError(f"Service account {service_account_id} not found")
        
        return await self.get_service_account(service_account_id)
    
    async def sync_with_hydra(self, service_account_id: UUID) -> ServiceAccount:
        """
        Manually sync a service account with Hydra.
        
        Args:
            service_account_id: Service account UUID
            
        Returns:
            Service account
            
        Raises:
            ServiceAccountNotFoundError: If service account not found
            HydraIntegrationError: If sync fails
        """
        logger.info(f"Manually syncing service account {service_account_id} with Hydra")
        
        # Get service account
        service_account = await self.get_service_account(service_account_id)
        
        try:
            # Get current state from Hydra
            hydra_client = await self.hydra_client.get_client(str(service_account.client_id))
            
            if hydra_client:
                # Update existing client in Hydra
                hydra_client_data = service_account.to_hydra_client()
                await self.hydra_client.update_client(str(service_account.client_id), hydra_client_data)
            else:
                # Create new client in Hydra
                hydra_client_data = service_account.to_hydra_client()
                await self.hydra_client.create_client(hydra_client_data)
            
            logger.info(f"Successfully synced service account {service_account_id} with Hydra")
            return service_account
            
        except Exception as e:
            logger.error(f"Failed to sync service account {service_account_id} with Hydra: {e}")
            raise HydraIntegrationError(f"Failed to sync with Hydra: {e}")
    
    async def _update_service_account_scopes(self, service_account: ServiceAccount, scope_ids: List[str]) -> None:
        """
        Update the scopes assigned to a service account.
        
        Args:
            service_account: The service account to update
            scope_ids: List of scope IDs to assign
        """
        from sqlalchemy import select
        
        # Clear existing scopes
        service_account.scopes.clear()
        
        # Add new scopes if any provided
        if scope_ids:
            # Query scopes by IDs
            result = await self.service_account_repo.db.execute(
                select(Scope).where(Scope.id.in_(scope_ids))
            )
            scopes = result.scalars().all()
            
            # Add each scope to the service account using direct relationship
            for scope in scopes:
                if scope not in service_account.scopes:
                    service_account.scopes.append(scope)
        
        # Commit the changes
        await self.service_account_repo.db.commit()

    async def _update_service_account_roles(self, service_account: ServiceAccount, role_ids: List[str]) -> None:
        """
        Update the roles assigned to a service account.
        
        Args:
            service_account: The service account to update
            role_ids: List of role IDs to assign
        """
        from sqlalchemy import select
        from ..models.role import Role
        
        # Clear existing roles
        service_account.roles.clear()
        
        # Add new roles if any provided
        if role_ids:
            # Query roles by IDs
            result = await self.service_account_repo.db.execute(
                select(Role).where(Role.id.in_(role_ids))
            )
            roles = result.scalars().all()
            
            # Add each role to the service account using direct relationship
            for role in roles:
                if role not in service_account.roles:
                    service_account.roles.append(role)
        
        # Commit the changes
        await self.service_account_repo.db.commit()
