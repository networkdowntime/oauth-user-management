"""
Unit tests for RoleRepository.

Tests all CRUD operations and business logic for role management
using mocked database sessions to avoid actual database dependencies.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID, uuid4
from datetime import datetime, timezone

from src.repositories.role import RoleRepository
from src.models.role import Role


class TestRoleRepository:
    """Test suite for RoleRepository."""

    def test_init(self, mock_async_session):
        """Test repository initialization."""
        repo = RoleRepository(mock_async_session)
        assert repo.db == mock_async_session
        assert repo.model == Role

    @pytest.mark.asyncio
    async def test_get_by_name_found(self, mock_async_session, sample_role):
        """Test getting role by name when it exists."""
        # Arrange
        repo = RoleRepository(mock_async_session)
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = sample_role
        mock_async_session.execute.return_value = mock_result

        # Act
        result = await repo.get_by_name("test_user")

        # Assert
        assert result == sample_role
        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_name_not_found(self, mock_async_session):
        """Test getting role by name when it doesn't exist."""
        # Arrange
        repo = RoleRepository(mock_async_session)
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_async_session.execute.return_value = mock_result

        # Act
        result = await repo.get_by_name("non_existent_role")

        # Assert
        assert result is None
        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_id_with_users_found(self, mock_async_session, sample_role):
        """Test getting role by ID with users loaded."""
        # Arrange
        repo = RoleRepository(mock_async_session)
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = sample_role
        mock_async_session.execute.return_value = mock_result

        role_id = str(sample_role.id)

        # Act
        result = await repo.get_by_id_with_users(role_id)

        # Assert
        assert result == sample_role
        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_id_with_users_not_found(self, mock_async_session):
        """Test getting role by ID when it doesn't exist."""
        # Arrange
        repo = RoleRepository(mock_async_session)
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_async_session.execute.return_value = mock_result

        # Act
        result = await repo.get_by_id_with_users(str(uuid4()))

        # Assert
        assert result is None
        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_all_with_users(self, mock_async_session):
        """Test getting all roles with users."""
        # Arrange
        repo = RoleRepository(mock_async_session)
        
        # Create sample roles
        role1 = Role(
            id=uuid4(),
            name="admin",
            description="Administrator role",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        role2 = Role(
            id=uuid4(),
            name="user",
            description="Regular user role",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        
        roles = [role1, role2]
        
        mock_result = MagicMock()
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = roles
        mock_result.scalars.return_value = mock_scalars
        mock_async_session.execute.return_value = mock_result

        # Act
        result = await repo.get_all_with_users(skip=0, limit=100)

        # Assert
        assert result == roles
        assert len(result) == 2
        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_all_with_users_empty(self, mock_async_session):
        """Test getting all roles when none exist."""
        # Arrange
        repo = RoleRepository(mock_async_session)
        
        mock_result = MagicMock()
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = []
        mock_result.scalars.return_value = mock_scalars
        mock_async_session.execute.return_value = mock_result

        # Act
        result = await repo.get_all_with_users()

        # Assert
        assert result == []
        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_all_with_users_with_pagination(self, mock_async_session):
        """Test getting all roles with pagination parameters."""
        # Arrange
        repo = RoleRepository(mock_async_session)
        
        # Create a single role for pagination test
        role = Role(
            id=uuid4(),
            name="paginated_role",
            description="Role for pagination test",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        
        mock_result = MagicMock()
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = [role]
        mock_result.scalars.return_value = mock_scalars
        mock_async_session.execute.return_value = mock_result

        # Act
        result = await repo.get_all_with_users(skip=10, limit=5)

        # Assert
        assert result == [role]
        mock_async_session.execute.assert_called_once()
        
        # Verify that the query was called with the correct parameters
        # (We can't easily verify the exact SQL, but we can verify the method was called)
