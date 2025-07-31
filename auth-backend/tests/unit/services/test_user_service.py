"""
Unit tests for UserService.

Tests user management functionality including CRUD operations,
role assignments, password management, and audit logging.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime
from uuid import uuid4

from src.services.user_service import UserService
from src.models.user import User
from src.models.role import Role
from src.schemas.user import UserCreate, UserUpdate, UserPasswordReset


class TestUserService:
    """Test suite for UserService operations."""

    @pytest.fixture
    def mock_user_repo(self):
        """Create mock UserRepository."""
        return AsyncMock()

    @pytest.fixture
    def mock_role_repo(self):
        """Create mock RoleRepository."""
        return AsyncMock()

    @pytest.fixture
    def mock_audit_repo(self):
        """Create mock AuditLogRepository."""
        return AsyncMock()

    @pytest.fixture
    def user_service(self, mock_user_repo, mock_role_repo, mock_audit_repo):
        """Create UserService instance with mocked dependencies."""
        return UserService(mock_user_repo, mock_role_repo, mock_audit_repo)

    @pytest.fixture
    def sample_user(self):
        """Create sample User model."""
        user_id = uuid4()
        role_id = uuid4()
        role = Role(
            id=role_id,
            name="admin",
            description="Administrator role",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        return User(
            id=user_id,
            email="test@example.com",
            display_name="Test User",
            password_hash="hashed_password",
            is_active=True,
            failed_login_attempts=0,
            last_login_at=None,
            locked_until=None,
            social_provider=None,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            roles=[role]
        )

    @pytest.fixture
    def sample_user_create(self):
        """Create sample UserCreate schema."""
        return UserCreate(
            email="new@example.com",
            password="secure_password",
            display_name="New User",
            is_active=True
        )

    @pytest.fixture
    def sample_user_update(self):
        """Create sample UserUpdate schema."""
        return UserUpdate(
            email="updated@example.com",
            display_name="Updated User",
            is_active=False,
            role_ids=["role-1", "role-2"]
        )

    async def test_get_users_success(self, user_service, mock_user_repo, sample_user):
        """Test successful retrieval of all users."""
        mock_user_repo.get_all_with_roles.return_value = [sample_user]
        
        result = await user_service.get_users(skip=0, limit=100)
        
        mock_user_repo.get_all_with_roles.assert_called_once_with(0, 100)
        assert len(result) == 1
        assert result[0].email == "test@example.com"
        assert result[0].display_name == "Test User"

    async def test_get_all_users_empty(self, user_service, mock_user_repo):
        """Test retrieval when no users exist."""
        mock_user_repo.get_all_with_roles.return_value = []
        
        result = await user_service.get_users()
        
        assert result == []

    async def test_get_user_by_id_success(self, user_service, mock_user_repo, sample_user):
        """Test successful user retrieval by ID."""
        user_id = str(sample_user.id)
        mock_user_repo.get_by_id_with_roles.return_value = sample_user
        
        result = await user_service.get_user_by_id(user_id)
        
        mock_user_repo.get_by_id_with_roles.assert_called_once_with(user_id)
        assert result is not None
        assert result.email == "test@example.com"

    async def test_get_user_by_id_not_found(self, user_service, mock_user_repo):
        """Test user retrieval when user not found."""
        mock_user_repo.get_by_id_with_roles.return_value = None
        
        result = await user_service.get_user_by_id("nonexistent-id")
        
        assert result is None

    @patch('src.services.user_service.ph')
    async def test_create_user_success(self, mock_ph, user_service, mock_user_repo, 
                                      sample_user_create, sample_user):
        """Test successful user creation."""
        mock_user_repo.get_by_email.return_value = None
        mock_user_repo.create.return_value = sample_user
        mock_user_repo.get_by_id_with_roles.return_value = sample_user
        mock_ph.hash.return_value = "hashed_password"
        
        result = await user_service.create_user(sample_user_create, "admin")
        
        mock_user_repo.get_by_email.assert_called_once_with(sample_user_create.email)
        mock_ph.hash.assert_called_once_with(sample_user_create.password)
        mock_user_repo.create.assert_called_once()
        assert result.email == sample_user.email

    async def test_create_user_already_exists(self, user_service, mock_user_repo, 
                                            sample_user_create, sample_user):
        """Test user creation when email already exists."""
        mock_user_repo.get_by_email.return_value = sample_user
        
        with pytest.raises(ValueError, match="User with email .* already exists"):
            await user_service.create_user(sample_user_create, "admin")

    async def test_update_user_success(self, user_service, mock_user_repo, mock_audit_repo,
                                     sample_user, sample_user_update):
        """Test successful user update."""
        user_id = str(sample_user.id)
        # First call for checking if user exists, second call for role update, third for final fetch
        mock_user_repo.get_by_id_with_roles.side_effect = [sample_user, sample_user, sample_user]
        mock_user_repo.update.return_value = sample_user
        
        result = await user_service.update_user(user_id, sample_user_update, "admin")
        
        mock_user_repo.update.assert_called_once()
        # Should have multiple audit calls for role changes plus main update
        assert mock_audit_repo.create_with_serialization.call_count >= 1
        assert result.email == sample_user.email

    async def test_update_user_not_found(self, user_service, mock_user_repo, sample_user_update):
        """Test user update when user not found."""
        mock_user_repo.get_by_id_with_roles.return_value = None
        
        result = await user_service.update_user("nonexistent-id", sample_user_update, "admin")
        
        assert result is None

    @patch('src.services.user_service.ph')
    async def test_update_user_with_password(self, mock_ph, user_service, mock_user_repo, 
                                           mock_audit_repo, sample_user):
        """Test user update with password change."""
        user_id = str(sample_user.id)
        update_data = UserUpdate(password="new_password")
        mock_user_repo.get_by_id_with_roles.side_effect = [sample_user, sample_user]
        mock_user_repo.update.return_value = sample_user
        mock_ph.hash.return_value = "new_hashed_password"
        
        result = await user_service.update_user(user_id, update_data, "admin")
        
        mock_ph.hash.assert_called_once_with("new_password")
        assert result is not None

    async def test_delete_user_success(self, user_service, mock_user_repo, sample_user):
        """Test successful user deletion."""
        user_id = str(sample_user.id)
        mock_user_repo.get_by_id.return_value = sample_user
        mock_user_repo.delete.return_value = True
        
        with patch.object(user_service, '_log_action') as mock_log:
            result = await user_service.delete_user(user_id, "admin")
        
        mock_user_repo.delete.assert_called_once_with(user_id)
        mock_log.assert_called_once()
        assert result is True

    async def test_delete_user_not_found(self, user_service, mock_user_repo):
        """Test user deletion when user not found."""
        mock_user_repo.get_by_id.return_value = None
        
        result = await user_service.delete_user("nonexistent-id", "admin")
        
        assert result is False

    async def test_delete_user_failure(self, user_service, mock_user_repo, sample_user):
        """Test user deletion failure."""
        user_id = str(sample_user.id)
        mock_user_repo.get_by_id.return_value = sample_user
        mock_user_repo.delete.return_value = False
        
        result = await user_service.delete_user(user_id, "admin")
        
        assert result is False

    @patch('src.services.user_service.ph')
    async def test_reset_user_password_success(self, mock_ph, user_service, mock_user_repo, sample_user):
        """Test successful password reset."""
        user_id = str(sample_user.id)
        password_data = UserPasswordReset(new_password="new_secure_password")
        mock_user_repo.get_by_id.return_value = sample_user
        mock_user_repo.update_password.return_value = True
        mock_ph.hash.return_value = "new_hashed_password"
        
        result = await user_service.reset_user_password(user_id, password_data, "admin")
        
        mock_ph.hash.assert_called_once_with("new_secure_password")
        mock_user_repo.update_password.assert_called_once_with(user_id, "new_hashed_password")
        assert result is True

    async def test_reset_user_password_user_not_found(self, user_service, mock_user_repo):
        """Test password reset when user not found."""
        password_data = UserPasswordReset(new_password="new_password")
        mock_user_repo.get_by_id.return_value = None
        
        result = await user_service.reset_user_password("nonexistent-id", password_data, "admin")
        
        assert result is False

    async def test_reset_user_password_failure(self, user_service, mock_user_repo, sample_user):
        """Test password reset failure."""
        user_id = str(sample_user.id)
        password_data = UserPasswordReset(new_password="new_password")
        mock_user_repo.get_by_id.return_value = sample_user
        mock_user_repo.update_password.return_value = False
        
        with patch('src.services.user_service.ph'):
            result = await user_service.reset_user_password(user_id, password_data, "admin")
        
        assert result is False

    async def test_assign_role_to_user_success(self, user_service, mock_user_repo, 
                                             mock_role_repo, sample_user):
        """Test successful role assignment."""
        user_id = str(sample_user.id)
        role_id = "role-123"
        role = Role(id=uuid4(), name="admin", description="Admin role", 
                   created_at=datetime.utcnow(), updated_at=datetime.utcnow())
        
        mock_user_repo.assign_role.return_value = True
        mock_user_repo.get_by_id.return_value = sample_user
        mock_role_repo.get_by_id.return_value = role
        
        result = await user_service.assign_role_to_user(user_id, role_id, "admin")
        
        mock_user_repo.assign_role.assert_called_once_with(user_id, role_id)
        assert result is True

    async def test_assign_role_to_user_failure(self, user_service, mock_user_repo):
        """Test role assignment failure."""
        mock_user_repo.assign_role.return_value = False
        
        result = await user_service.assign_role_to_user("user-id", "role-id", "admin")
        
        assert result is False

    async def test_remove_role_from_user_success(self, user_service, mock_user_repo, 
                                               mock_role_repo, sample_user):
        """Test successful role removal."""
        user_id = str(sample_user.id)
        role_id = "role-123"
        role = Role(id=uuid4(), name="admin", description="Admin role",
                   created_at=datetime.utcnow(), updated_at=datetime.utcnow())
        
        mock_user_repo.get_by_id.return_value = sample_user
        mock_role_repo.get_by_id.return_value = role
        mock_user_repo.remove_role.return_value = True
        
        result = await user_service.remove_role_from_user(user_id, role_id, "admin")
        
        mock_user_repo.remove_role.assert_called_once_with(user_id, role_id)
        assert result is True

    async def test_remove_role_from_user_failure(self, user_service, mock_user_repo,
                                               mock_role_repo, sample_user):
        """Test role removal failure."""
        user_id = str(sample_user.id)
        role_id = "role-123"
        
        mock_user_repo.get_by_id.return_value = sample_user
        mock_role_repo.get_by_id.return_value = None
        mock_user_repo.remove_role.return_value = False
        
        result = await user_service.remove_role_from_user(user_id, role_id, "admin")
        
        assert result is False

    def test_user_to_response_conversion(self, user_service, sample_user):
        """Test user model to response schema conversion."""
        result = user_service._user_to_response(sample_user)
        
        assert result.email == sample_user.email
        assert result.display_name == sample_user.display_name
        assert result.is_active == sample_user.is_active
        assert len(result.roles) == 1
        assert result.roles[0].name == "admin"

    def test_generate_service_password(self, user_service):
        """Test service password generation."""
        password = user_service._generate_service_password()
        
        assert len(password) == 24
        assert all(c.isalnum() or c in "!@#$%^&*" for c in password)

    async def test_update_user_roles_add_and_remove(self, user_service, mock_user_repo, sample_user):
        """Test updating user roles with additions and removals."""
        user_id = str(sample_user.id)
        new_role_ids = ["role-2", "role-3"]  # Remove existing role-1, add role-2 and role-3
        
        # Current user has role with ID from sample_user
        current_role_id = str(sample_user.roles[0].id)
        mock_user_repo.get_by_id_with_roles.return_value = sample_user
        
        await user_service._update_user_roles(user_id, new_role_ids, "admin")
        
        # Should remove current role
        mock_user_repo.remove_role.assert_called_once_with(user_id, current_role_id)
        # Should add new roles
        assert mock_user_repo.assign_role.call_count == 2
        mock_user_repo.assign_role.assert_any_call(user_id, "role-2")
        mock_user_repo.assign_role.assert_any_call(user_id, "role-3")

    async def test_update_user_roles_user_not_found(self, user_service, mock_user_repo):
        """Test updating roles when user not found."""
        mock_user_repo.get_by_id_with_roles.return_value = None
        
        # Should handle gracefully without throwing exception
        await user_service._update_user_roles("nonexistent-id", ["role-1"], "admin")
        
        # Should not call any role assignment methods
        mock_user_repo.remove_role.assert_not_called()
        mock_user_repo.assign_role.assert_not_called()

    async def test_log_action(self, user_service, mock_audit_repo):
        """Test audit log action logging."""
        await user_service._log_action(
            action="test_action",
            resource_type="user",
            resource_id="user-123",
            details={"key": "value"},
            performed_by="admin"
        )
        
        mock_audit_repo.create_with_serialization.assert_called_once_with(
            action="test_action",
            resource_type="user",
            resource_id="user-123",
            details={"key": "value"},
            performed_by="admin"
        )
