"""
Hydra synchronization service.

This service handles synchronizing OAuth2 clients and scopes between
the auth-backend database and ORY Hydra.
"""

import logging
from typing import Any, Dict, List

from sqlalchemy.ext.asyncio import AsyncSession

from ..models.service_account import ServiceAccount
from ..repositories.service_account import ServiceAccountRepository
from ..services.hydra_client import HydraAdminClient

logger = logging.getLogger(__name__)


class HydraSyncResult:
    """Result of a Hydra synchronization operation."""

    def __init__(self):
        self.clients_created: List[str] = []
        self.clients_updated: List[str] = []
        self.clients_deleted: List[str] = []
        self.scopes_synced: List[str] = []
        self.errors: List[str] = []
        self.success: bool = True

    def add_error(self, error: str):
        """Add an error to the result."""
        self.errors.append(error)
        self.success = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary for API response."""
        return {
            "success": self.success,
            "summary": {
                "clients_created": len(self.clients_created),
                "clients_updated": len(self.clients_updated),
                "clients_deleted": len(self.clients_deleted),
                "scopes_synced": len(self.scopes_synced),
                "errors": len(self.errors),
            },
            "details": {
                "clients_created": self.clients_created,
                "clients_updated": self.clients_updated,
                "clients_deleted": self.clients_deleted,
                "scopes_synced": self.scopes_synced,
                "errors": self.errors,
            },
        }


class HydraSyncService:
    """Service for synchronizing data between auth-backend and Hydra."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.hydra_client = HydraAdminClient()
        self.service_account_repo = ServiceAccountRepository(db)

    async def sync_all(self) -> HydraSyncResult:
        """
        Synchronize all service accounts and scopes with Hydra.

        This will:
        1. Fetch all clients from Hydra
        2. Fetch all service accounts from database
        3. Create/update/delete clients in Hydra to match database
        4. Update client scopes in Hydra
        """
        logger.info("Starting Hydra synchronization")
        result = HydraSyncResult()

        try:
            # Get current state from both systems
            hydra_clients = await self._get_hydra_clients()
            db_service_accounts = await self.service_account_repo.get_all(limit=1000)

            # Create maps for easier comparison
            hydra_clients_map = {client["client_id"]: client for client in hydra_clients}
            db_accounts_map = {sa.client_id: sa for sa in db_service_accounts}

            # Sync clients
            await self._sync_clients(hydra_clients_map, db_accounts_map, result)

            # Sync scopes for existing clients
            await self._sync_client_scopes(db_accounts_map, result)

            logger.info(f"Hydra synchronization completed: {result.to_dict()}")

        except Exception as e:
            error_msg = f"Failed to sync with Hydra: {str(e)}"
            logger.error(error_msg, exc_info=True)
            result.add_error(error_msg)

        return result

    async def _get_hydra_clients(self) -> List[Dict[str, Any]]:
        """Fetch all clients from Hydra."""
        try:
            clients = await self.hydra_client.list_clients(limit=1000)
            return clients
        except Exception as e:
            logger.error(f"Error fetching clients from Hydra: {e}")
            raise

    async def _sync_clients(
        self,
        hydra_clients_map: Dict[str, Dict[str, Any]],
        db_accounts_map: Dict[str, ServiceAccount],
        result: HydraSyncResult,
    ):
        """Sync clients between Hydra and database."""

        # Create clients that exist in DB but not in Hydra
        for client_id, service_account in db_accounts_map.items():
            if client_id not in hydra_clients_map:
                try:
                    await self._create_hydra_client(service_account)
                    result.clients_created.append(client_id)
                    logger.info(f"Created client in Hydra: {client_id}")
                except Exception as e:
                    error_msg = f"Failed to create client {client_id}: {str(e)}"
                    result.add_error(error_msg)
                    logger.error(error_msg)

        # Update clients that exist in both
        for client_id, service_account in db_accounts_map.items():
            if client_id in hydra_clients_map:
                try:
                    hydra_client = hydra_clients_map[client_id]
                    if await self._needs_client_update(service_account, hydra_client):
                        await self._update_hydra_client(service_account)
                        result.clients_updated.append(client_id)
                        logger.info(f"Updated client in Hydra: {client_id}")
                except Exception as e:
                    error_msg = f"Failed to update client {client_id}: {str(e)}"
                    result.add_error(error_msg)
                    logger.error(error_msg)

        # Delete clients that exist in Hydra but not in DB
        for client_id in hydra_clients_map:
            if client_id not in db_accounts_map:
                try:
                    await self._delete_hydra_client(client_id)
                    result.clients_deleted.append(client_id)
                    logger.info(f"Deleted client from Hydra: {client_id}")
                except Exception as e:
                    error_msg = f"Failed to delete client {client_id}: {str(e)}"
                    result.add_error(error_msg)
                    logger.error(error_msg)

    async def _create_hydra_client(self, service_account: ServiceAccount):
        """Create a client in Hydra based on service account data."""
        client_data = self._service_account_to_hydra_client(service_account)

        await self.hydra_client.create_client(client_data)

    async def _update_hydra_client(self, service_account: ServiceAccount):
        """Update a client in Hydra based on service account data."""
        client_data = self._service_account_to_hydra_client(service_account)

        await self.hydra_client.update_client(str(service_account.client_id), client_data)

    async def _delete_hydra_client(self, client_id: str):
        """Delete a client from Hydra."""
        await self.hydra_client.delete_client(client_id)

    async def _needs_client_update(self, service_account: ServiceAccount, hydra_client: Dict[str, Any]) -> bool:
        """Check if a client needs to be updated in Hydra."""
        # Compare key fields that should match
        db_data = self._service_account_to_hydra_client(service_account)

        # Fields to compare
        fields_to_compare = [
            "client_name",
            "grant_types",
            "response_types",
            "redirect_uris",
            "scope",
            "audience",
            "token_endpoint_auth_method",
            "skip_consent",
            "allowed_cors_origins",
            "post_logout_redirect_uris",
        ]

        for field in fields_to_compare:
            db_value = db_data.get(field)
            hydra_value = hydra_client.get(field)

            # Normalize lists for comparison
            if isinstance(db_value, list) and isinstance(hydra_value, list):
                if set(db_value) != set(hydra_value):
                    logger.debug(
                        f"Client {service_account.client_id} field {field} differs: DB={db_value}, Hydra={hydra_value}"
                    )
                    return True
            elif db_value != hydra_value:
                logger.debug(
                    f"Client {service_account.client_id} field {field} differs: DB={db_value}, Hydra={hydra_value}"
                )
                return True

        return False

    async def _sync_client_scopes(self, db_accounts_map: Dict[str, ServiceAccount], result: HydraSyncResult):
        """Sync scopes for all clients."""
        for client_id, service_account in db_accounts_map.items():
            try:
                # The scope is already included in the client data during create/update
                # But we track it for reporting
                scope_names = [scope.name for scope in service_account.scopes]
                if scope_names:
                    result.scopes_synced.extend(scope_names)
                    logger.debug(f"Synced scopes for client {client_id}: {scope_names}")
            except Exception as e:
                error_msg = f"Failed to sync scopes for client {client_id}: {str(e)}"
                result.add_error(error_msg)
                logger.error(error_msg)

    def _service_account_to_hydra_client(self, service_account: ServiceAccount) -> Dict[str, Any]:
        """Convert a service account to Hydra client data."""
        # Use the existing to_hydra_client method from the model
        return service_account.to_hydra_client()


# Global factory function since service needs database session
def create_hydra_sync_service(db: AsyncSession) -> HydraSyncService:
    """Create a HydraSyncService instance with a database session."""
    return HydraSyncService(db)
