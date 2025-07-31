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

    # OAuth2 Flow Methods
    
    async def get_login_request(self, login_challenge: str) -> Dict[str, Any]:
        """Get login request information from Hydra."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(
                    f"{self.base_url}/admin/oauth2/auth/requests/login",
                    params={"login_challenge": login_challenge}
                )
                response.raise_for_status()
                result = response.json()
                logger.info(f"Retrieved login request for challenge: {login_challenge}")
                return result
            except httpx.HTTPStatusError as e:
                logger.error(f"Failed to get login request {login_challenge}: {e.response.status_code} - {e.response.text}")
                raise
            except Exception as e:
                logger.error(f"Error getting login request {login_challenge}: {str(e)}")
                raise

    async def accept_login_request(self, login_challenge: str, subject: str, remember: bool = False, 
                                 remember_for: int = 3600, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Accept a login request in Hydra."""
        accept_data: Dict[str, Any] = {
            "subject": subject,
            "remember": remember,
            "remember_for": remember_for
        }
        if context:
            accept_data["context"] = context
            
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.put(
                    f"{self.base_url}/admin/oauth2/auth/requests/login/accept",
                    params={"login_challenge": login_challenge},
                    json=accept_data,
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
                result = response.json()
                logger.info(f"Accepted login request for challenge: {login_challenge}, subject: {subject}")
                return result
            except httpx.HTTPStatusError as e:
                logger.error(f"Failed to accept login request {login_challenge}: {e.response.status_code} - {e.response.text}")
                raise
            except Exception as e:
                logger.error(f"Error accepting login request {login_challenge}: {str(e)}")
                raise

    async def reject_login_request(self, login_challenge: str, error: str = "access_denied", 
                                 error_description: str = "The user denied the request") -> Dict[str, Any]:
        """Reject a login request in Hydra."""
        reject_data = {
            "error": error,
            "error_description": error_description
        }
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.put(
                    f"{self.base_url}/admin/oauth2/auth/requests/login/reject",
                    params={"login_challenge": login_challenge},
                    json=reject_data,
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
                result = response.json()
                logger.info(f"Rejected login request for challenge: {login_challenge}")
                return result
            except httpx.HTTPStatusError as e:
                logger.error(f"Failed to reject login request {login_challenge}: {e.response.status_code} - {e.response.text}")
                raise
            except Exception as e:
                logger.error(f"Error rejecting login request {login_challenge}: {str(e)}")
                raise

    async def get_consent_request(self, consent_challenge: str) -> Dict[str, Any]:
        """Get consent request information from Hydra."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(
                    f"{self.base_url}/admin/oauth2/auth/requests/consent",
                    params={"consent_challenge": consent_challenge}
                )
                response.raise_for_status()
                result = response.json()
                logger.info(f"Retrieved consent request for challenge: {consent_challenge}")
                return result
            except httpx.HTTPStatusError as e:
                logger.error(f"Failed to get consent request {consent_challenge}: {e.response.status_code} - {e.response.text}")
                raise
            except Exception as e:
                logger.error(f"Error getting consent request {consent_challenge}: {str(e)}")
                raise

    async def accept_consent_request(self, consent_challenge: str, grant_scope: List[str], 
                                   grant_access_token_audience: Optional[List[str]] = None,
                                   remember: bool = False, remember_for: int = 3600,
                                   session: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Accept a consent request in Hydra."""
        accept_data: Dict[str, Any] = {
            "grant_scope": grant_scope,
            "remember": remember,
            "remember_for": remember_for
        }
        if grant_access_token_audience:
            accept_data["grant_access_token_audience"] = grant_access_token_audience
        if session:
            accept_data["session"] = session
            
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.put(
                    f"{self.base_url}/admin/oauth2/auth/requests/consent/accept",
                    params={"consent_challenge": consent_challenge},
                    json=accept_data,
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
                result = response.json()
                logger.info(f"Accepted consent request for challenge: {consent_challenge}")
                return result
            except httpx.HTTPStatusError as e:
                logger.error(f"Failed to accept consent request {consent_challenge}: {e.response.status_code} - {e.response.text}")
                raise
            except Exception as e:
                logger.error(f"Error accepting consent request {consent_challenge}: {str(e)}")
                raise

    async def reject_consent_request(self, consent_challenge: str, error: str = "access_denied",
                                   error_description: str = "The user denied the request") -> Dict[str, Any]:
        """Reject a consent request in Hydra."""
        reject_data = {
            "error": error,
            "error_description": error_description
        }
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.put(
                    f"{self.base_url}/admin/oauth2/auth/requests/consent/reject",
                    params={"consent_challenge": consent_challenge},
                    json=reject_data,
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
                result = response.json()
                logger.info(f"Rejected consent request for challenge: {consent_challenge}")
                return result
            except httpx.HTTPStatusError as e:
                logger.error(f"Failed to reject consent request {consent_challenge}: {e.response.status_code} - {e.response.text}")
                raise
            except Exception as e:
                logger.error(f"Error rejecting consent request {consent_challenge}: {str(e)}")
                raise

    async def get_logout_request(self, logout_challenge: str) -> Dict[str, Any]:
        """Get logout request information from Hydra."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(
                    f"{self.base_url}/admin/oauth2/auth/requests/logout",
                    params={"logout_challenge": logout_challenge}
                )
                response.raise_for_status()
                result = response.json()
                logger.info(f"Retrieved logout request for challenge: {logout_challenge}")
                return result
            except httpx.HTTPStatusError as e:
                logger.error(f"Failed to get logout request {logout_challenge}: {e.response.status_code} - {e.response.text}")
                raise
            except Exception as e:
                logger.error(f"Error getting logout request {logout_challenge}: {str(e)}")
                raise

    async def accept_logout_request(self, logout_challenge: str) -> Dict[str, Any]:
        """Accept a logout request in Hydra."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.put(
                    f"{self.base_url}/admin/oauth2/auth/requests/logout/accept",
                    params={"logout_challenge": logout_challenge},
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
                result = response.json()
                logger.info(f"Accepted logout request for challenge: {logout_challenge}")
                return result
            except httpx.HTTPStatusError as e:
                logger.error(f"Failed to accept logout request {logout_challenge}: {e.response.status_code} - {e.response.text}")
                raise
            except Exception as e:
                logger.error(f"Error accepting logout request {logout_challenge}: {str(e)}")
                raise

    async def reject_logout_request(self, logout_challenge: str) -> Dict[str, Any]:
        """Reject a logout request in Hydra."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.put(
                    f"{self.base_url}/admin/oauth2/auth/requests/logout/reject",
                    params={"logout_challenge": logout_challenge},
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
                result = response.json()
                logger.info(f"Rejected logout request for challenge: {logout_challenge}")
                return result
            except httpx.HTTPStatusError as e:
                logger.error(f"Failed to reject logout request {logout_challenge}: {e.response.status_code} - {e.response.text}")
                raise
            except Exception as e:
                logger.error(f"Error rejecting logout request {logout_challenge}: {str(e)}")
                raise
