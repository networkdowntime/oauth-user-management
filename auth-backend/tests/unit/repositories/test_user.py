"""
Unit tests for UserRepository.

Tests all CRUD operations and business logic for user management
using mocked database sessions to avoid actua    @pytest.mark.asyncio
    async def test_get_users_by_role(self, mock_async_session, sample_users_with_roles, sample_admin_role):ies.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID, uuid4
from datetime import datetime, timezone

from src.repositories.user import UserRepository
from src.models.user import User
from src.models.role import Role


class TestUserRepository:
    """Test suite for UserRepository."""

    def test_init(self, mock_async_session):
        """Test repository initialization."""
        repo = UserRepository(mock_async_session)
        assert repo.db == mock_async_session
        assert repo.model == User

    @pytest.mark.asyncio
    async def test_get_by_email_found(self, mock_async_session, sample_user):
        """Test getting user by email when it exists."""
        # Arrange
        repo = UserRepository(mock_async_session)
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = sample_user
        mock_async_session.execute.return_value = mock_result

        # Act
        result = await repo.get_by_email("test@example.com")

        # Assert
        assert result == sample_user
        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_email_not_found(self, mock_async_session):
        """Test getting user by email when it doesn't exist."""
        # Arrange
        repo = UserRepository(mock_async_session)
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_async_session.execute.return_value = mock_result

        # Act
        result = await repo.get_by_email("nonexistent@example.com")

        # Assert
        assert result is None
        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_id_with_roles_found(self, mock_async_session, sample_user_with_roles):
        """Test getting user by ID with roles when it exists."""
        # Arrange
        repo = UserRepository(mock_async_session)
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = sample_user_with_roles
        mock_async_session.execute.return_value = mock_result

        # Act
        result = await repo.get_by_id_with_roles(str(sample_user_with_roles.id))

        # Assert
        assert result == sample_user_with_roles
        assert len(result.roles) > 0
        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_id_with_roles_not_found(self, mock_async_session):
        """Test getting user by ID with roles when it doesn't exist."""
        # Arrange
        repo = UserRepository(mock_async_session)
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_async_session.execute.return_value = mock_result

        # Act
        result = await repo.get_by_id_with_roles(str(uuid4()))

        # Assert
        assert result is None
        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_all_with_roles(self, mock_async_session, sample_users_with_roles):
        """Test getting all users with roles."""
        # Arrange
        repo = UserRepository(mock_async_session)
        mock_result = MagicMock()
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = sample_users_with_roles
        mock_result.scalars.return_value = mock_scalars
        mock_async_session.execute.return_value = mock_result

        # Act
        result = await repo.get_all_with_roles(skip=0, limit=100)

        # Assert
        assert result == sample_users_with_roles
        assert len(result) == 2
        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_all_with_roles_pagination(self, mock_async_session):
        """Test getting all users with pagination."""
        # Arrange
        repo = UserRepository(mock_async_session)
        mock_result = MagicMock()
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = []
        mock_result.scalars.return_value = mock_scalars
        mock_async_session.execute.return_value = mock_result

        # Act
        result = await repo.get_all_with_roles(skip=10, limit=5)

        # Assert
        assert result == []
        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    @pytest.mark.asyncio
    async def test_get_users_by_role(self, mock_async_session, sample_users_with_roles, sample_admin_role):
        """Test getting users by role."""
        # Arrange
        repo = UserRepository(mock_async_session)
        users_with_role = [user for user in sample_users_with_roles if sample_admin_role in user.roles]
        mock_result = MagicMock()
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = users_with_role
        mock_result.scalars.return_value = mock_scalars
        mock_async_session.execute.return_value = mock_result

        # Act
        result = await repo.get_users_by_role(str(sample_admin_role.id))

        # Assert
        assert result == users_with_role
        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_users_without_role(self, mock_async_session, sample_users_with_roles, sample_admin_role):
        """Test getting users without a specific role."""
        # Arrange
        repo = UserRepository(mock_async_session)
        
        # Create users where only one has the role
        user_with_role = sample_users_with_roles[0]
        user_with_role.roles = [sample_admin_role]
        user_without_role = sample_users_with_roles[1]
        user_without_role.roles = []
        
        # Mock should return only users without the role
        users_without_role = [user_without_role]  # Only the user without the admin role
        
        mock_result = MagicMock()
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = users_without_role
        mock_result.scalars.return_value = mock_scalars
        mock_async_session.execute.return_value = mock_result

        # Act
        result = await repo.get_users_without_role(str(sample_admin_role.id))

        # Assert
        assert len(result) == 1
        assert result[0] == user_without_role
        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_assign_role_success(self, mock_async_session, sample_user, sample_admin_role):
        """Test successfully assigning a role to a user."""
        # Arrange
        repo = UserRepository(mock_async_session)

        # Mock get_by_id_with_roles to return the user
        with patch.object(repo, 'get_by_id_with_roles', return_value=sample_user):
            # Mock the role query to return the role
            mock_role_result = MagicMock()
            mock_role_result.scalar_one_or_none.return_value = sample_admin_role
            mock_async_session.execute.return_value = mock_role_result
            
            # Act
            result = await repo.assign_role(str(sample_user.id), str(sample_admin_role.id))

            # Assert
            assert result is True
            mock_async_session.commit.assert_called_once()
            assert sample_admin_role in sample_user.roles

    @pytest.mark.asyncio
    async def test_assign_role_already_assigned(self, mock_async_session, sample_user_with_roles):
        """Test assigning a role that's already assigned."""
        # Arrange
        repo = UserRepository(mock_async_session)
        existing_role = sample_user_with_roles.roles[0]
        
        # Mock get_by_id_with_roles to return the user with existing role
        with patch.object(repo, 'get_by_id_with_roles', return_value=sample_user_with_roles):
            # Mock the role query to return the existing role
            mock_role_result = MagicMock()
            mock_role_result.scalar_one_or_none.return_value = existing_role
            mock_async_session.execute.return_value = mock_role_result
            
            # Act
            result = await repo.assign_role(str(sample_user_with_roles.id), str(existing_role.id))

            # Assert
            assert result is True  # Should return True for already assigned
            assert len(sample_user_with_roles.roles) == 1  # Should not duplicate
            mock_async_session.commit.assert_not_called()  # Should not commit

    @pytest.mark.asyncio
    async def test_assign_role_user_not_found(self, mock_async_session):
        """Test assigning a role when user doesn't exist."""
        # Arrange
        repo = UserRepository(mock_async_session)
        
        # Mock get_by_id_with_roles to return None
        with patch.object(repo, 'get_by_id_with_roles', return_value=None):
            # Act
            result = await repo.assign_role(str(uuid4()), str(uuid4()))

            # Assert
            assert result is False
            mock_async_session.commit.assert_not_called()

    @pytest.mark.asyncio
    async def test_assign_role_role_not_found(self, mock_async_session, sample_user):
        """Test assigning a role that doesn't exist."""
        # Arrange
        repo = UserRepository(mock_async_session)
        
        # Mock get_by_id_with_roles to return the user
        with patch.object(repo, 'get_by_id_with_roles', return_value=sample_user):
            # Mock the role query to return None (role not found)
            mock_role_result = MagicMock()
            mock_role_result.scalar_one_or_none.return_value = None
            mock_async_session.execute.return_value = mock_role_result

            # Act
            result = await repo.assign_role(str(sample_user.id), str(uuid4()))

            # Assert
            assert result is False
            mock_async_session.commit.assert_not_called()

    @pytest.mark.asyncio
    async def test_remove_role_success(self, mock_async_session, sample_user_with_roles):
        """Test successfully removing a role from a user."""
        # Arrange
        repo = UserRepository(mock_async_session)
        role_to_remove = sample_user_with_roles.roles[0]
        
        # Mock get_by_id_with_roles to return the user with role
        with patch.object(repo, 'get_by_id_with_roles', return_value=sample_user_with_roles):
            # Act
            result = await repo.remove_role(str(sample_user_with_roles.id), str(role_to_remove.id))

            # Assert
            assert result is True
            mock_async_session.commit.assert_called_once()
            assert role_to_remove not in sample_user_with_roles.roles

    @pytest.mark.asyncio
    async def test_remove_role_not_assigned(self, mock_async_session, sample_user):
        """Test removing a role that's not assigned."""
        # Arrange
        repo = UserRepository(mock_async_session)
        
        # Mock get_by_id_with_roles to return the user without roles
        with patch.object(repo, 'get_by_id_with_roles', return_value=sample_user):
            # Act
            result = await repo.remove_role(str(sample_user.id), str(uuid4()))

            # Assert
            assert result is False  # Role not found
            mock_async_session.commit.assert_not_called()

    @pytest.mark.asyncio
    async def test_remove_role_user_not_found(self, mock_async_session):
        """Test removing a role when user doesn't exist."""
        # Arrange
        repo = UserRepository(mock_async_session)
        
        # Mock get_by_id_with_roles to return None
        with patch.object(repo, 'get_by_id_with_roles', return_value=None):
            # Act
            result = await repo.remove_role(str(uuid4()), str(uuid4()))

            # Assert
            assert result is False
            mock_async_session.commit.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_password_success(self, mock_async_session, sample_user):
        """Test successfully updating user password."""
        # Arrange
        repo = UserRepository(mock_async_session)
        new_password_hash = "new_hashed_password_123"
        
        # Mock get_by_id to return the user
        with patch.object(repo, 'get_by_id', return_value=sample_user):
            # Act
            result = await repo.update_password(str(sample_user.id), new_password_hash)

            # Assert
            assert result is True
            assert sample_user.password_hash == new_password_hash
            mock_async_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_password_user_not_found(self, mock_async_session):
        """Test updating password when user doesn't exist."""
        # Arrange
        repo = UserRepository(mock_async_session)
        
        # Mock get_by_id to return None
        with patch.object(repo, 'get_by_id', return_value=None):
            # Act
            result = await repo.update_password(str(uuid4()), "new_password_hash")

            # Assert
            assert result is False
            mock_async_session.commit.assert_not_called()
