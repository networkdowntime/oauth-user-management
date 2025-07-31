"""
Unit tests for BaseRepository.

Tests the base repository functionality that all other repositories inherit.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID, uuid4
from datetime import datetime, timezone

from src.repositories.base import BaseRepository
from src.models.service_account import ServiceAccount


class TestBaseRepository:
    """Test suite for BaseRepository."""

    def test_init(self):
        """Test repository initialization."""
        mock_session = AsyncMock()
        repo = BaseRepository(ServiceAccount, mock_session)
        assert repo.db == mock_session
        assert repo.model == ServiceAccount

    @pytest.mark.asyncio
    async def test_get_by_id_found(self):
        """Test getting an object by ID when it exists."""
        # Arrange
        mock_session = AsyncMock()
        repo = BaseRepository(ServiceAccount, mock_session)
        
        # Create a sample service account
        test_id = uuid4()
        service_account = ServiceAccount(
            id=test_id,
            client_id="test-client",
            client_name="Test Account",
            description="Test Description",
            is_active=True,
            created_by="test-user",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        
        # Mock the database result
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = service_account
        mock_session.execute.return_value = mock_result

        # Act
        result = await repo.get_by_id(str(test_id))

        # Assert
        assert result == service_account
        mock_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self):
        """Test getting an object by ID when it doesn't exist."""
        # Arrange
        mock_session = AsyncMock()
        repo = BaseRepository(ServiceAccount, mock_session)
        
        # Mock the database result (no object found)
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        # Act
        result = await repo.get_by_id(str(uuid4()))

        # Assert
        assert result is None
        mock_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_all(self):
        """Test getting all objects."""
        # Arrange
        mock_session = AsyncMock()
        repo = BaseRepository(ServiceAccount, mock_session)
        
        # Create sample service accounts
        account1 = ServiceAccount(
            id=uuid4(),
            client_id="test-client-1",
            client_name="Test Account 1",
            description="Test Description 1",
            is_active=True,
            created_by="test-user",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        account2 = ServiceAccount(
            id=uuid4(),
            client_id="test-client-2", 
            client_name="Test Account 2",
            description="Test Description 2",
            is_active=False,
            created_by="test-user",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        
        accounts = [account1, account2]
        
        # Mock the database result
        mock_result = MagicMock()
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = accounts
        mock_result.scalars.return_value = mock_scalars
        mock_session.execute.return_value = mock_result

        # Act
        result = await repo.get_all(skip=0, limit=100)

        # Assert
        assert result == accounts
        assert len(result) == 2
        mock_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_create(self):
        """Test creating a new object."""
        # Arrange
        mock_session = AsyncMock()
        repo = BaseRepository(ServiceAccount, mock_session)
        
        # Create data for a service account
        service_account_data = {
            "client_id": "new-client",
            "client_name": "New Account",
            "description": "New Description",
            "is_active": True,
            "created_by": "test-user"
        }
        
        # Mock the session operations
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.return_value = None

        # Act
        result = await repo.create(service_account_data)

        # Assert
        assert isinstance(result, ServiceAccount)
        assert result.client_id == "new-client"
        assert result.client_name == "New Account"
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()

    @pytest.mark.asyncio
    async def test_update(self):
        """Test updating an existing object."""
        # Arrange
        mock_session = AsyncMock()
        repo = BaseRepository(ServiceAccount, mock_session)
        
        # Create a service account to update
        service_account = ServiceAccount(
            id=uuid4(),
            client_id="update-client",
            client_name="Old Account Name",
            description="Old Description",
            is_active=False,
            created_by="test-user",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        
        # Update data
        update_data = {
            "client_name": "Updated Account",
            "description": "Updated Description"
        }
        
        # Mock the session operations
        mock_session.commit.return_value = None
        mock_session.refresh.return_value = None

        # Act
        result = await repo.update(service_account, update_data)

        # Assert
        assert result == service_account
        assert result.client_name == "Updated Account"
        assert result.description == "Updated Description"
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once_with(service_account)

    @pytest.mark.asyncio
    async def test_delete(self):
        """Test deleting an object by ID."""
        # Arrange
        mock_session = AsyncMock()
        repo = BaseRepository(ServiceAccount, mock_session)
        
        test_id = str(uuid4())
        
        # Mock the session operations
        mock_result = MagicMock()
        mock_result.rowcount = 1
        mock_session.execute.return_value = mock_result
        mock_session.commit.return_value = None

        # Act
        result = await repo.delete(test_id)

        # Assert
        assert result is True
        mock_session.execute.assert_called_once()
        mock_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_not_found(self):
        """Test deleting an object that doesn't exist."""
        # Arrange
        mock_session = AsyncMock()
        repo = BaseRepository(ServiceAccount, mock_session)
        
        test_id = str(uuid4())
        
        # Mock the session operations (no rows affected)
        mock_result = MagicMock()
        mock_result.rowcount = 0
        mock_session.execute.return_value = mock_result
        mock_session.commit.return_value = None

        # Act
        result = await repo.delete(test_id)

        # Assert
        assert result is False
        mock_session.execute.assert_called_once()
        mock_session.commit.assert_called_once()
