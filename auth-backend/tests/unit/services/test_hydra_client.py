"""
Unit tests for HydraAdminClient.

Tests OAuth2 client management functionality with Hydra Admin API
including CRUD operations, error handling, and health checks.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import httpx

from src.services.hydra_client import HydraAdminClient


class TestHydraAdminClient:
    """Test suite for HydraAdminClient operations."""

    @pytest.fixture
    def mock_settings(self):
        """Create mock settings."""
        with patch('src.services.hydra_client.settings') as mock:
            mock.hydra_admin_url = "http://hydra:4445"
            yield mock

    @pytest.fixture
    def hydra_client(self, mock_settings):
        """Create a HydraAdminClient instance."""
        return HydraAdminClient()

    @pytest.fixture
    def sample_client_data(self):
        """Create sample OAuth2 client data."""
        return {
            "client_id": "test-client-id",
            "client_name": "Test Client",
            "grant_types": ["client_credentials"],
            "response_types": ["token"],
            "scope": "read write"
        }

    @pytest.fixture
    def sample_client_response(self):
        """Create sample OAuth2 client response."""
        return {
            "client_id": "test-client-id",
            "client_name": "Test Client",
            "grant_types": ["client_credentials"],
            "response_types": ["token"],
            "scope": "read write",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z"
        }

    @patch('httpx.AsyncClient')
    async def test_create_client_success(self, mock_async_client, hydra_client, 
                                        sample_client_data, sample_client_response):
        """Test successful client creation."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = sample_client_response
        
        mock_client_instance = AsyncMock()
        mock_client_instance.post.return_value = mock_response
        mock_async_client.return_value.__aenter__.return_value = mock_client_instance
        
        result = await hydra_client.create_client(sample_client_data)
        
        mock_client_instance.post.assert_called_once_with(
            "http://hydra:4445/admin/clients",
            json=sample_client_data,
            headers={"Content-Type": "application/json"}
        )
        assert result == sample_client_response

    @patch('httpx.AsyncClient')
    async def test_create_client_http_error(self, mock_async_client, hydra_client, sample_client_data):
        """Test client creation with HTTP error."""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        
        mock_client_instance = AsyncMock()
        mock_client_instance.post.return_value = mock_response
        mock_client_instance.post.return_value.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Bad Request", request=MagicMock(), response=mock_response
        )
        mock_async_client.return_value.__aenter__.return_value = mock_client_instance
        
        with pytest.raises(httpx.HTTPStatusError):
            await hydra_client.create_client(sample_client_data)

    @patch('httpx.AsyncClient')
    async def test_create_client_generic_error(self, mock_async_client, hydra_client, sample_client_data):
        """Test client creation with generic error."""
        mock_client_instance = AsyncMock()
        mock_client_instance.post.side_effect = Exception("Connection error")
        mock_async_client.return_value.__aenter__.return_value = mock_client_instance
        
        with pytest.raises(Exception, match="Connection error"):
            await hydra_client.create_client(sample_client_data)

    @patch('httpx.AsyncClient')
    async def test_get_client_success(self, mock_async_client, hydra_client, sample_client_response):
        """Test successful client retrieval."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = sample_client_response
        
        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_response
        mock_async_client.return_value.__aenter__.return_value = mock_client_instance
        
        result = await hydra_client.get_client("test-client-id")
        
        mock_client_instance.get.assert_called_once_with(
            "http://hydra:4445/admin/clients/test-client-id"
        )
        assert result == sample_client_response

    @patch('httpx.AsyncClient')
    async def test_get_client_not_found(self, mock_async_client, hydra_client):
        """Test client retrieval when client not found."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        
        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_response
        mock_async_client.return_value.__aenter__.return_value = mock_client_instance
        
        result = await hydra_client.get_client("nonexistent-client")
        
        assert result is None

    @patch('httpx.AsyncClient')
    async def test_get_client_http_error_not_404(self, mock_async_client, hydra_client):
        """Test client retrieval with non-404 HTTP error."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        
        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_response
        mock_client_instance.get.return_value.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Internal Server Error", request=MagicMock(), response=mock_response
        )
        mock_async_client.return_value.__aenter__.return_value = mock_client_instance
        
        with pytest.raises(httpx.HTTPStatusError):
            await hydra_client.get_client("test-client-id")

    @patch('httpx.AsyncClient')
    async def test_update_client_success(self, mock_async_client, hydra_client, 
                                        sample_client_data, sample_client_response):
        """Test successful client update."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = sample_client_response
        
        mock_client_instance = AsyncMock()
        mock_client_instance.put.return_value = mock_response
        mock_async_client.return_value.__aenter__.return_value = mock_client_instance
        
        result = await hydra_client.update_client("test-client-id", sample_client_data)
        
        mock_client_instance.put.assert_called_once_with(
            "http://hydra:4445/admin/clients/test-client-id",
            json=sample_client_data,
            headers={"Content-Type": "application/json"}
        )
        assert result == sample_client_response

    @patch('httpx.AsyncClient')
    async def test_update_client_http_error(self, mock_async_client, hydra_client, sample_client_data):
        """Test client update with HTTP error."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        
        mock_client_instance = AsyncMock()
        mock_client_instance.put.return_value = mock_response
        mock_client_instance.put.return_value.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Not Found", request=MagicMock(), response=mock_response
        )
        mock_async_client.return_value.__aenter__.return_value = mock_client_instance
        
        with pytest.raises(httpx.HTTPStatusError):
            await hydra_client.update_client("nonexistent-client", sample_client_data)

    @patch('httpx.AsyncClient')
    async def test_delete_client_success(self, mock_async_client, hydra_client):
        """Test successful client deletion."""
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_response.raise_for_status.return_value = None
        
        mock_client_instance = AsyncMock()
        mock_client_instance.delete.return_value = mock_response
        mock_async_client.return_value.__aenter__.return_value = mock_client_instance
        
        result = await hydra_client.delete_client("test-client-id")
        
        mock_client_instance.delete.assert_called_once_with(
            "http://hydra:4445/admin/clients/test-client-id"
        )
        assert result is True

    @patch('httpx.AsyncClient')
    async def test_delete_client_not_found(self, mock_async_client, hydra_client):
        """Test client deletion when client not found."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        
        mock_client_instance = AsyncMock()
        mock_client_instance.delete.return_value = mock_response
        mock_async_client.return_value.__aenter__.return_value = mock_client_instance
        
        result = await hydra_client.delete_client("nonexistent-client")
        
        assert result is True  # Consider 404 as successful deletion

    @patch('httpx.AsyncClient')
    async def test_delete_client_http_error_not_404(self, mock_async_client, hydra_client):
        """Test client deletion with non-404 HTTP error."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        
        mock_client_instance = AsyncMock()
        mock_client_instance.delete.return_value = mock_response
        mock_client_instance.delete.return_value.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Internal Server Error", request=MagicMock(), response=mock_response
        )
        mock_async_client.return_value.__aenter__.return_value = mock_client_instance
        
        with pytest.raises(httpx.HTTPStatusError):
            await hydra_client.delete_client("test-client-id")

    @patch('httpx.AsyncClient')
    async def test_list_clients_success(self, mock_async_client, hydra_client, sample_client_response):
        """Test successful client listing."""
        clients_list = [sample_client_response]
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = clients_list
        
        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_response
        mock_async_client.return_value.__aenter__.return_value = mock_client_instance
        
        result = await hydra_client.list_clients()
        
        mock_client_instance.get.assert_called_once_with(
            "http://hydra:4445/admin/clients",
            params={"limit": 100, "offset": 0}
        )
        assert result == clients_list

    @patch('httpx.AsyncClient')
    async def test_list_clients_with_params(self, mock_async_client, hydra_client):
        """Test client listing with custom parameters."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = []
        
        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_response
        mock_async_client.return_value.__aenter__.return_value = mock_client_instance
        
        result = await hydra_client.list_clients(limit=50, offset=10)
        
        mock_client_instance.get.assert_called_once_with(
            "http://hydra:4445/admin/clients",
            params={"limit": 50, "offset": 10}
        )
        assert result == []

    @patch('httpx.AsyncClient')
    async def test_list_clients_http_error(self, mock_async_client, hydra_client):
        """Test client listing with HTTP error."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        
        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_response
        mock_client_instance.get.return_value.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Internal Server Error", request=MagicMock(), response=mock_response
        )
        mock_async_client.return_value.__aenter__.return_value = mock_client_instance
        
        with pytest.raises(httpx.HTTPStatusError):
            await hydra_client.list_clients()

    @patch('httpx.AsyncClient')
    async def test_health_check_success(self, mock_async_client, hydra_client):
        """Test successful health check."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        
        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_response
        mock_async_client.return_value.__aenter__.return_value = mock_client_instance
        
        result = await hydra_client.health_check()
        
        mock_client_instance.get.assert_called_once_with("http://hydra:4445/health/ready")
        assert result is True

    @patch('httpx.AsyncClient')
    async def test_health_check_failure(self, mock_async_client, hydra_client):
        """Test health check failure."""
        mock_response = MagicMock()
        mock_response.status_code = 503
        
        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_response
        mock_async_client.return_value.__aenter__.return_value = mock_client_instance
        
        result = await hydra_client.health_check()
        
        assert result is False

    @patch('httpx.AsyncClient')
    async def test_health_check_exception(self, mock_async_client, hydra_client):
        """Test health check with exception."""
        mock_client_instance = AsyncMock()
        mock_client_instance.get.side_effect = Exception("Connection failed")
        mock_async_client.return_value.__aenter__.return_value = mock_client_instance
        
        result = await hydra_client.health_check()
        
        assert result is False

    def test_init_sets_correct_attributes(self, hydra_client, mock_settings):
        """Test that initialization sets correct attributes."""
        assert hydra_client.base_url == "http://hydra:4445"
        assert hydra_client.timeout == 30.0

    @patch('httpx.AsyncClient')
    async def test_timeout_configuration(self, mock_async_client, hydra_client):
        """Test that timeout is properly configured for HTTP client."""
        mock_client_instance = AsyncMock()
        mock_async_client.return_value.__aenter__.return_value = mock_client_instance
        
        await hydra_client.create_client({"client_id": "test"})
        
        # Verify AsyncClient was called with correct timeout
        mock_async_client.assert_called_with(timeout=30.0)

    @patch('httpx.AsyncClient')
    async def test_health_check_timeout_configuration(self, mock_async_client, hydra_client):
        """Test that health check uses shorter timeout."""
        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value.status_code = 200
        mock_async_client.return_value.__aenter__.return_value = mock_client_instance
        
        await hydra_client.health_check()
        
        # Verify AsyncClient was called with shorter timeout for health check
        mock_async_client.assert_called_with(timeout=5.0)

    @patch('httpx.AsyncClient')
    async def test_get_client_generic_error(self, mock_async_client, hydra_client):
        """Test client retrieval with generic error."""
        mock_client_instance = AsyncMock()
        mock_client_instance.get.side_effect = Exception("Network error")
        mock_async_client.return_value.__aenter__.return_value = mock_client_instance
        
        with pytest.raises(Exception, match="Network error"):
            await hydra_client.get_client("test-client-id")

    @patch('httpx.AsyncClient')
    async def test_update_client_generic_error(self, mock_async_client, hydra_client, sample_client_data):
        """Test client update with generic error."""
        mock_client_instance = AsyncMock()
        mock_client_instance.put.side_effect = Exception("Connection timeout")
        mock_async_client.return_value.__aenter__.return_value = mock_client_instance
        
        with pytest.raises(Exception, match="Connection timeout"):
            await hydra_client.update_client("test-client-id", sample_client_data)

    @patch('httpx.AsyncClient')
    async def test_delete_client_generic_error(self, mock_async_client, hydra_client):
        """Test client deletion with generic error."""
        mock_client_instance = AsyncMock()
        mock_client_instance.delete.side_effect = Exception("Server error")
        mock_async_client.return_value.__aenter__.return_value = mock_client_instance
        
        with pytest.raises(Exception, match="Server error"):
            await hydra_client.delete_client("test-client-id")

    @patch('httpx.AsyncClient')
    async def test_list_clients_generic_error(self, mock_async_client, hydra_client):
        """Test client listing with generic error."""
        mock_client_instance = AsyncMock()
        mock_client_instance.get.side_effect = Exception("DNS resolution failed")
        mock_async_client.return_value.__aenter__.return_value = mock_client_instance
        
        with pytest.raises(Exception, match="DNS resolution failed"):
            await hydra_client.list_clients()
