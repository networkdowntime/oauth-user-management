"""
Unit tests for RoleService.

Tests role management functionality including CRUD operations,
user associations, and audit logging.
"""
import pytest
from unittest.mock import AsyncMock, patch
from datetime import datetime
from uuid import uuid4

from src.services.role_service import RoleService
from src.models.role import Role
from src.models.user import User
from src.schemas.role import RoleCreate, RoleUpdate


class TestRoleService:
    """Test suite for RoleService operations."""

    @pytest.fixture
    def mock_role_repo(self):
        """Create mock RoleRepository."""
        return AsyncMock()

    @pytest.fixture
    def mock_user_repo(self):
        """Create mock UserRepository."""
        return AsyncMock()

    @pytest.fixture
    def mock_audit_repo(self):
        """Create mock AuditLogRepository."""
        return AsyncMock()

    @pytest.fixture
    def mock_service_account_repo(self):
        """Create mock ServiceAccountRepository."""
        return AsyncMock()

    @pytest.fixture
    def role_service(self, mock_role_repo, mock_user_repo, mock_service_account_repo, mock_audit_repo):
        """Create RoleService instance with mocked dependencies."""
        return RoleService(mock_role_repo, mock_user_repo, mock_service_account_repo, mock_audit_repo)

    @pytest.fixture
    def sample_role(self):
        """Create sample Role model."""
        role_id = uuid4()
        user_id = uuid4()
        user = User(
            id=user_id,
            email="test@example.com",
            display_name="Test User",
            password_hash="hashed_password",
            is_active=True,
            failed_login_attempts=0,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            roles=[]
        )
        return Role(
            id=role_id,
            name="admin",
            description="Administrator role",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            users=[user]
        )

    @pytest.fixture
    def sample_role_create(self):
        """Create sample RoleCreate schema."""
        return RoleCreate(
            name="new_role",
            description="New role for testing"
        )

    @pytest.fixture
    def sample_role_update(self):
        """Create sample RoleUpdate schema."""
        return RoleUpdate(
            name="updated_role",
            description="Updated description"
        )

    async def test_get_all_roles_success(self, role_service, mock_role_repo, sample_role):
        """Test successful retrieval of all roles."""
        mock_role_repo.get_all_with_users.return_value = [sample_role]
        
        result = await role_service.get_all_roles(skip=0, limit=100)
        
        mock_role_repo.get_all_with_users.assert_called_once_with(0, 100)
        assert len(result) == 1
        assert result[0].name == "admin"
        assert result[0].description == "Administrator role"

    async def test_get_all_roles_empty(self, role_service, mock_role_repo):
        """Test retrieval when no roles exist."""
        mock_role_repo.get_all_with_users.return_value = []
        
        result = await role_service.get_all_roles()
        
        assert result == []

    async def test_get_role_by_id_success(self, role_service, mock_role_repo, sample_role):
        """Test successful role retrieval by ID."""
        role_id = str(sample_role.id)
        mock_role_repo.get_by_id_with_users.return_value = sample_role
        
        result = await role_service.get_role_by_id(role_id)
        
        mock_role_repo.get_by_id_with_users.assert_called_once_with(role_id)
        assert result is not None
        assert result.name == "admin"

    async def test_get_role_by_id_not_found(self, role_service, mock_role_repo):
        """Test role retrieval when role not found."""
        mock_role_repo.get_by_id_with_users.return_value = None
        
        result = await role_service.get_role_by_id("nonexistent-id")
        
        assert result is None

    async def test_create_role_success(self, role_service, mock_role_repo, 
                                     sample_role_create, sample_role):
        """Test successful role creation."""
        mock_role_repo.get_by_name.return_value = None
        mock_role_repo.create.return_value = sample_role
        
        with patch.object(role_service, '_log_action') as mock_log:
            result = await role_service.create_role(sample_role_create, "admin")
        
        mock_role_repo.get_by_name.assert_called_once_with(sample_role_create.name)
        mock_role_repo.create.assert_called_once()
        mock_log.assert_called_once()
        assert result.name == sample_role.name

    async def test_create_role_already_exists(self, role_service, mock_role_repo, 
                                            sample_role_create, sample_role):
        """Test role creation when name already exists."""
        mock_role_repo.get_by_name.return_value = sample_role
        
        with pytest.raises(ValueError, match="Role with name .* already exists"):
            await role_service.create_role(sample_role_create, "admin")

    async def test_update_role_success(self, role_service, mock_role_repo, 
                                     sample_role, sample_role_update):
        """Test successful role update."""
        role_id = str(sample_role.id)
        mock_role_repo.get_by_id_with_users.return_value = sample_role
        mock_role_repo.get_by_name.return_value = None  # Name doesn't exist
        mock_role_repo.update.return_value = sample_role
        
        with patch.object(role_service, '_log_action') as mock_log:
            result = await role_service.update_role(role_id, sample_role_update, "admin")
        
        mock_role_repo.update.assert_called_once()
        mock_log.assert_called_once()
        assert result.name == sample_role.name

    async def test_update_role_not_found(self, role_service, mock_role_repo, sample_role_update):
        """Test role update when role not found."""
        mock_role_repo.get_by_id_with_users.return_value = None
        
        result = await role_service.update_role("nonexistent-id", sample_role_update, "admin")
        
        assert result is None

    async def test_update_role_name_exists(self, role_service, mock_role_repo, 
                                         sample_role, sample_role_update):
        """Test role update when new name already exists."""
        role_id = str(sample_role.id)
        existing_role = Role(id=uuid4(), name="existing", description="Existing role",
                           created_at=datetime.utcnow(), updated_at=datetime.utcnow())
        
        mock_role_repo.get_by_id_with_users.return_value = sample_role
        mock_role_repo.get_by_name.return_value = existing_role
        
        with pytest.raises(ValueError, match="Role with name .* already exists"):
            await role_service.update_role(role_id, sample_role_update, "admin")

    async def test_delete_role_success(self, role_service, mock_role_repo, sample_role):
        """Test successful role deletion."""
        role_id = str(sample_role.id)
        mock_role_repo.get_by_id.return_value = sample_role
        mock_role_repo.delete.return_value = True
        
        with patch.object(role_service, '_log_action') as mock_log:
            result = await role_service.delete_role(role_id, "admin")
        
        mock_role_repo.delete.assert_called_once_with(role_id)
        mock_log.assert_called_once()
        assert result is True

    async def test_delete_role_not_found(self, role_service, mock_role_repo):
        """Test role deletion when role not found."""
        mock_role_repo.get_by_id.return_value = None
        
        result = await role_service.delete_role("nonexistent-id", "admin")
        
        assert result is False

    async def test_delete_role_failure(self, role_service, mock_role_repo, sample_role):
        """Test role deletion failure."""
        role_id = str(sample_role.id)
        mock_role_repo.get_by_id.return_value = sample_role
        mock_role_repo.delete.return_value = False
        
        result = await role_service.delete_role(role_id, "admin")
        
        assert result is False

    async def test_assign_user_to_role_success(self, role_service, mock_user_repo, mock_role_repo):
        """Test successful user assignment to role."""
        user_id = "user-123"
        role_id = "role-456"
        mock_user_repo.assign_role.return_value = True
        
        with patch.object(role_service, '_log_action') as mock_log:
            result = await role_service.assign_user_to_role(user_id, role_id, "admin")
        
        mock_user_repo.assign_role.assert_called_once_with(user_id, role_id)
        mock_log.assert_called_once()
        assert result is True

    async def test_assign_user_to_role_failure(self, role_service, mock_user_repo):
        """Test user assignment to role failure."""
        mock_user_repo.assign_role.return_value = False
        
        result = await role_service.assign_user_to_role("user-id", "role-id", "admin")
        
        assert result is False

    async def test_remove_user_from_role_success(self, role_service, mock_user_repo, mock_role_repo):
        """Test successful user removal from role."""
        user_id = "user-123"
        role_id = "role-456"
        mock_user_repo.remove_role.return_value = True
        
        with patch.object(role_service, '_log_action') as mock_log:
            result = await role_service.remove_user_from_role(user_id, role_id, "admin")
        
        mock_user_repo.remove_role.assert_called_once_with(user_id, role_id)
        mock_log.assert_called_once()
        assert result is True

    async def test_remove_user_from_role_failure(self, role_service, mock_user_repo):
        """Test user removal from role failure."""
        mock_user_repo.remove_role.return_value = False
        
        result = await role_service.remove_user_from_role("user-id", "role-id", "admin")
        
        assert result is False

    def test_role_to_response_conversion(self, role_service, sample_role):
        """Test role model to response schema conversion."""
        result = role_service._role_to_response(sample_role)
        
        assert result.name == sample_role.name
        assert result.description == sample_role.description
        assert result.user_count == sample_role.user_count

    async def test_log_action(self, role_service, mock_audit_repo):
        """Test audit log action logging."""
        await role_service._log_action(
            action="test_action",
            resource_type="role",
            resource_id="role-123",
            details={"key": "value"},
            performed_by="admin"
        )
        
        mock_audit_repo.create_with_serialization.assert_called_once_with(
            action="test_action",
            resource_type="role",
            resource_id="role-123",
            details={"key": "value"},
            performed_by="admin",
            ip_address=None,
            user_agent=None
        )
