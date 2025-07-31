"""Hydra Admin API client for OAuth2 client management."""

import httpx
from typing import Dict, List, Any, Optional
from ..core.config import settings
from ..core.logging_config import get_logger

logger = get_logger(__name__)


class HydraAdminClient:
    """Client for interacting with Hydra Admin API."""
    
    def __init__(self):
        self.base_url = settings.hydra_admin_url
        self.timeout = 30.0
    
    async def create_client(self, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new OAuth2 client in Hydra."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/admin/clients",
                    json=client_data,
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
                result = response.json()
                logger.info(f"Created Hydra client: {client_data.get('client_id')}")
                return result
            except httpx.HTTPStatusError as e:
                logger.error(f"Failed to create Hydra client: {e.response.status_code} - {e.response.text}")
                raise
            except Exception as e:
                logger.error(f"Error creating Hydra client: {str(e)}")
                raise
    
    async def get_client(self, client_id: str) -> Optional[Dict[str, Any]]:
        """Get an OAuth2 client from Hydra."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(
                    f"{self.base_url}/admin/clients/{client_id}"
                )
                if response.status_code == 404:
                    return None
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return None
                logger.error(f"Failed to get Hydra client {client_id}: {e.response.status_code} - {e.response.text}")
                raise
            except Exception as e:
                logger.error(f"Error getting Hydra client {client_id}: {str(e)}")
                raise
    
    async def update_client(self, client_id: str, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an OAuth2 client in Hydra."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.put(
                    f"{self.base_url}/admin/clients/{client_id}",
                    json=client_data,
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
                result = response.json()
                logger.info(f"Updated Hydra client: {client_id}")
                return result
            except httpx.HTTPStatusError as e:
                logger.error(f"Failed to update Hydra client {client_id}: {e.response.status_code} - {e.response.text}")
                raise
            except Exception as e:
                logger.error(f"Error updating Hydra client {client_id}: {str(e)}")
                raise
    
    async def delete_client(self, client_id: str) -> bool:
        """Delete an OAuth2 client from Hydra."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.delete(
                    f"{self.base_url}/admin/clients/{client_id}"
                )
                if response.status_code == 404:
                    logger.warning(f"Hydra client {client_id} not found for deletion")
                    return True  # Consider it successfully deleted
                response.raise_for_status()
                logger.info(f"Deleted Hydra client: {client_id}")
                return True
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return True  # Already deleted
                logger.error(f"Failed to delete Hydra client {client_id}: {e.response.status_code} - {e.response.text}")
                raise
            except Exception as e:
                logger.error(f"Error deleting Hydra client {client_id}: {str(e)}")
                raise
    
    async def list_clients(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """List all OAuth2 clients from Hydra."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(
                    f"{self.base_url}/admin/clients",
                    params={"limit": limit, "offset": offset}
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.error(f"Failed to list Hydra clients: {e.response.status_code} - {e.response.text}")
                raise
            except Exception as e:
                logger.error(f"Error listing Hydra clients: {str(e)}")
                raise
    
    async def health_check(self) -> bool:
        """Check if Hydra Admin API is healthy."""
        async with httpx.AsyncClient(timeout=5.0) as client:
            try:
                response = await client.get(f"{self.base_url}/health/ready")
                return response.status_code == 200
            except Exception as e:
                logger.error(f"Hydra health check failed: {str(e)}")
                return False
