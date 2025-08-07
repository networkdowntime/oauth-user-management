"""
Unit tests for AdminService.

Tests system administration functionality including audit log retrieval,
system statistics, and JWT public key management.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime
from pathlib import Path

from src.services.admin_service import AdminService
from src.schemas.audit import AuditLogResponse
from src.schemas.common import SystemStatsResponse


class TestAdminService:
    """Test suite for AdminService operations."""

    @pytest.fixture
    def mock_audit_repo(self):
        """Create a mock AuditLogRepository."""
        return AsyncMock()

    @pytest.fixture
    def mock_user_repo(self):
        """Create a mock UserRepository."""
        return AsyncMock()

    @pytest.fixture
    def mock_role_repo(self):
        """Create a mock RoleRepository."""
        return AsyncMock()

    @pytest.fixture
    def mock_service_account_repo(self):
        """Create a mock ServiceAccountRepository."""
        return AsyncMock()

    @pytest.fixture
    def admin_service(self, mock_audit_repo, mock_user_repo, mock_role_repo, mock_service_account_repo):
        """Create an AdminService instance with mocked dependencies."""
        return AdminService(
            audit_repo=mock_audit_repo,
            user_repo=mock_user_repo,
            role_repo=mock_role_repo,
            service_account_repo=mock_service_account_repo
        )

    @pytest.fixture
    def sample_audit_log(self):
        """Create a sample audit log for testing."""
        audit_log = MagicMock()
        audit_log.id = "550e8400-e29b-41d4-a716-446655440000"
        audit_log.action = "user_created"
        audit_log.resource_type = "user"
        audit_log.resource_id = "user123"
        audit_log.details = {"email": "test@example.com"}
        audit_log.performed_by = "admin123"
        audit_log.ip_address = "192.168.1.1"
        audit_log.user_agent = "Mozilla/5.0..."
        audit_log.timestamp = datetime(2023, 1, 1, 12, 0, 0)
        return audit_log

    @pytest.fixture
    def sample_user(self):
        """Create a sample user for testing."""
        user = MagicMock()
        user.id = "user123"
        user.email = "test@example.com"
        return user

    @pytest.fixture
    def sample_service_user(self):
        """Create a sample service user for testing."""
        service = MagicMock()
        service.id = "service123"
        service.email = "service@example.com"
        return service

    @pytest.fixture
    def sample_role(self):
        """Create a sample role for testing."""
        role = MagicMock()
        role.id = "role123"
        role.name = "admin"
        role.description = "Administrator role"
        return role

    async def test_get_audit_logs_no_filters(self, admin_service, mock_audit_repo, sample_audit_log):
        """Test get_audit_logs with no filters."""
        mock_audit_repo.get_by_resource.return_value = [sample_audit_log]
        
        result = await admin_service.get_audit_logs()
        
        mock_audit_repo.get_by_resource.assert_called_once_with(
            resource_type=None,
            resource_id=None,
            limit=100
        )
        
        assert len(result) == 1
        assert isinstance(result[0], AuditLogResponse)
        assert result[0].id == "550e8400-e29b-41d4-a716-446655440000"
        assert result[0].action == "user_created"
        assert result[0].resource_type == "user"

    async def test_get_audit_logs_with_filters(self, admin_service, mock_audit_repo, sample_audit_log):
        """Test get_audit_logs with resource type and ID filters."""
        mock_audit_repo.get_by_resource.return_value = [sample_audit_log]
        
        result = await admin_service.get_audit_logs(
            resource_type="user",
            resource_id="user123",
            limit=50
        )
        
        mock_audit_repo.get_by_resource.assert_called_once_with(
            resource_type="user",
            resource_id="user123",
            limit=50
        )
        
        assert len(result) == 1
        assert result[0].resource_type == "user"
        assert result[0].resource_id == "user123"

    async def test_get_audit_logs_empty_result(self, admin_service, mock_audit_repo):
        """Test get_audit_logs with empty result."""
        mock_audit_repo.get_by_resource.return_value = []
        
        result = await admin_service.get_audit_logs()
        
        assert result == []

    async def test_get_audit_logs_multiple_logs(self, admin_service, mock_audit_repo):
        """Test get_audit_logs with multiple logs."""
        log1 = MagicMock()
        log1.id = "log1"
        log1.action = "user_created"
        log1.resource_type = "user"
        log1.resource_id = "user1"
        log1.details = {}
        log1.performed_by = "admin1"
        log1.ip_address = "192.168.1.1"
        log1.user_agent = "Browser1"
        log1.timestamp = datetime.now()
        
        log2 = MagicMock()
        log2.id = "log2"
        log2.action = "user_updated"
        log2.resource_type = "user"
        log2.resource_id = "user2"
        log2.details = {}
        log2.performed_by = "admin2"
        log2.ip_address = "192.168.1.2"
        log2.user_agent = "Browser2"
        log2.timestamp = datetime.now()
        
        mock_audit_repo.get_by_resource.return_value = [log1, log2]
        
        result = await admin_service.get_audit_logs()
        
        assert len(result) == 2
        assert result[0].id == "log1"
        assert result[1].id == "log2"

    async def test_get_system_stats_mixed_users(self, admin_service, mock_user_repo, mock_role_repo, 
                                                mock_service_account_repo, sample_user, sample_role):
        """Test get_system_stats with users and service accounts."""
        # Setup users - all User entities are regular users
        users = [sample_user]
        mock_user_repo.get_all.return_value = users
        
        # Setup service accounts
        service_account = MagicMock()
        service_account.id = "service1"
        service_account.client_id = "test-service-1"
        mock_service_account_repo.get_all.return_value = [service_account]
        
        # Setup roles
        roles = [sample_role]
        mock_role_repo.get_all.return_value = roles
        
        result = await admin_service.get_system_stats()
        
        mock_user_repo.get_all.assert_called_once_with(limit=1000)
        mock_service_account_repo.get_all.assert_called_once_with(limit=1000)
        mock_role_repo.get_all.assert_called_once_with(limit=1000)
        
        assert isinstance(result, SystemStatsResponse)
        assert result.users == 1  # One regular user
        assert result.services == 1  # One service account
        assert result.roles == 1

    async def test_get_system_stats_only_regular_users(self, admin_service, mock_user_repo, 
                                                       mock_role_repo, mock_service_account_repo):
        """Test get_system_stats with only regular users."""
        # Setup users - all User entities are regular users
        user1 = MagicMock()
        user1.id = "user1"
        
        user2 = MagicMock()
        user2.id = "user2"
        
        mock_user_repo.get_all.return_value = [user1, user2]
        mock_service_account_repo.get_all.return_value = []  # No service accounts
        mock_role_repo.get_all.return_value = []
        
        result = await admin_service.get_system_stats()
        
        assert result.users == 2  # Both should count as regular users
        assert result.services == 0
        assert result.roles == 0

    async def test_get_system_stats_empty_system(self, admin_service, mock_user_repo, mock_role_repo, mock_service_account_repo):
        """Test get_system_stats with empty system."""
        mock_user_repo.get_all.return_value = []
        mock_service_account_repo.get_all.return_value = []
        mock_role_repo.get_all.return_value = []
        
        result = await admin_service.get_system_stats()
        
        assert result.users == 0
        assert result.services == 0
        assert result.roles == 0

    @patch('src.services.admin_service.settings')
    async def test_get_jwt_public_key_file_exists(self, mock_settings, admin_service):
        """Test get_jwt_public_key when file exists."""
        mock_key_content = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA1234567890...
-----END PUBLIC KEY-----"""
        
        mock_path = MagicMock(spec=Path)
        mock_path.exists.return_value = True
        mock_path.read_text.return_value = mock_key_content
        mock_settings.jwt_public_key_path = mock_path
        
        result = await admin_service.get_jwt_public_key()
        
        mock_path.exists.assert_called_once()
        mock_path.read_text.assert_called_once()
        assert result == mock_key_content

    @patch('src.services.admin_service.settings')
    async def test_get_jwt_public_key_file_not_exists(self, mock_settings, admin_service):
        """Test get_jwt_public_key when file doesn't exist."""
        mock_path = MagicMock(spec=Path)
        mock_path.exists.return_value = False
        mock_settings.jwt_public_key_path = mock_path
        
        result = await admin_service.get_jwt_public_key()
        
        mock_path.exists.assert_called_once()
        mock_path.read_text.assert_not_called()
        assert "BEGIN PUBLIC KEY" in result
        assert "1234567890" in result  # Placeholder key content

    @patch('src.services.admin_service.settings')
    async def test_get_jwt_public_key_read_error(self, mock_settings, admin_service):
        """Test get_jwt_public_key when file read fails."""
        mock_path = MagicMock(spec=Path)
        mock_path.exists.return_value = True
        mock_path.read_text.side_effect = IOError("Permission denied")
        mock_settings.jwt_public_key_path = mock_path
        
        with pytest.raises(ValueError, match="JWT public key not available"):
            await admin_service.get_jwt_public_key()

    async def test_get_audit_logs_preserves_all_fields(self, admin_service, mock_audit_repo):
        """Test that get_audit_logs preserves all audit log fields."""
        audit_log = MagicMock()
        audit_log.id = "test-id"
        audit_log.action = "test_action"
        audit_log.resource_type = "test_resource"
        audit_log.resource_id = "test_resource_id"
        audit_log.details = {"key": "value"}
        audit_log.performed_by = "test_user"
        audit_log.ip_address = "10.0.0.1"
        audit_log.user_agent = "Test Agent"
        audit_log.timestamp = datetime(2023, 6, 15, 10, 30, 0)
        
        mock_audit_repo.get_by_resource.return_value = [audit_log]
        
        result = await admin_service.get_audit_logs()
        
        assert len(result) == 1
        response = result[0]
        assert response.id == "test-id"
        assert response.action == "test_action"
        assert response.resource_type == "test_resource"
        assert response.resource_id == "test_resource_id"
        assert response.details == {"key": "value"}
        assert response.performed_by == "test_user"
        assert response.ip_address == "10.0.0.1"
        assert response.user_agent == "Test Agent"
        assert response.timestamp == datetime(2023, 6, 15, 10, 30, 0)

    async def test_get_system_stats_handles_empty_collections(self, admin_service, mock_user_repo,
                                                           mock_role_repo, mock_service_account_repo):
        """Test get_system_stats handles empty collections."""
        # Empty collections
        mock_user_repo.get_all.return_value = []
        mock_service_account_repo.get_all.return_value = []
        mock_role_repo.get_all.return_value = []
        
        result = await admin_service.get_system_stats()
        
        # All counts should be zero for empty collections
        assert result.users == 0
        assert result.services == 0
        assert result.roles == 0