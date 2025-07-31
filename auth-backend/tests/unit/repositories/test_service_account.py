"""
Unit tests for ServiceAccountRepository.

Tests all CRUD operations and business logic for service account management
using mocked database sessions to avoid actual database dependencies.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID, uuid4
from datetime import datetime, timezone

from src.repositories.service_account import ServiceAccountRepository
from src.models.service_account import ServiceAccount
from src.models.role import Role


class TestServiceAccountRepository:
    """Test suite for ServiceAccountRepository."""

    def test_init(self, mock_async_session):
        """Test repository initialization."""
        repo = ServiceAccountRepository(mock_async_session)
        assert repo.db == mock_async_session
        assert repo.model == ServiceAccount

    @pytest.mark.asyncio
    async def test_get_by_client_id_found(self, mock_async_session, sample_service_account):
        """Test getting service account by client_id when it exists."""
        # Arrange
        repo = ServiceAccountRepository(mock_async_session)
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = sample_service_account
        mock_async_session.execute.return_value = mock_result

        # Act
        result = await repo.get_by_client_id("test-client-001")

        # Assert
        assert result == sample_service_account
        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_client_id_not_found(self, mock_async_session):
        """Test getting service account by client_id when it doesn't exist."""
        # Arrange
        repo = ServiceAccountRepository(mock_async_session)
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_async_session.execute.return_value = mock_result

        # Act
        result = await repo.get_by_client_id("non-existent-client")

        # Assert
        assert result is None
        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_all_with_roles(self, mock_async_session, multiple_service_accounts):
        """Test getting all service accounts with roles."""
        # Arrange
        repo = ServiceAccountRepository(mock_async_session)
        mock_result = MagicMock()
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = multiple_service_accounts
        mock_result.scalars.return_value = mock_scalars
        mock_async_session.execute.return_value = mock_result

        # Act
        result = await repo.get_all_with_roles(skip=0, limit=100)

        # Assert
        assert result == multiple_service_accounts
        assert len(result) == 3
        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_id_with_roles_found(self, mock_async_session, sample_service_account_with_roles):
        """Test getting service account by ID with roles loaded."""
        # Arrange
        repo = ServiceAccountRepository(mock_async_session)
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = sample_service_account_with_roles
        mock_async_session.execute.return_value = mock_result

        service_account_id = str(sample_service_account_with_roles.id)

        # Act
        result = await repo.get_by_id_with_roles(service_account_id)

        # Assert
        assert result == sample_service_account_with_roles
        assert len(result.roles) == 1
        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_id_with_roles_not_found(self, mock_async_session):
        """Test getting service account by ID when it doesn't exist."""
        # Arrange
        repo = ServiceAccountRepository(mock_async_session)
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_async_session.execute.return_value = mock_result

        # Act
        result = await repo.get_by_id_with_roles(str(uuid4()))

        # Assert
        assert result is None
        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_search_by_client_id(self, mock_async_session, multiple_service_accounts):
        """Test searching service accounts by client_id."""
        # Arrange
        repo = ServiceAccountRepository(mock_async_session)
        filtered_accounts = [multiple_service_accounts[0]]  # Only first account matches
        
        mock_result = MagicMock()
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = filtered_accounts
        mock_result.scalars.return_value = mock_scalars
        mock_async_session.execute.return_value = mock_result

        # Act
        result = await repo.search("test-client-000")

        # Assert
        assert result == filtered_accounts
        assert len(result) == 1
        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_search_by_name(self, mock_async_session, multiple_service_accounts):
        """Test searching service accounts by name."""
        # Arrange
        repo = ServiceAccountRepository(mock_async_session)
        filtered_accounts = [multiple_service_accounts[1]]  # Only second account matches
        
        mock_result = MagicMock()
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = filtered_accounts
        mock_result.scalars.return_value = mock_scalars
        mock_async_session.execute.return_value = mock_result

        # Act
        result = await repo.search("Client 2")

        # Assert
        assert result == filtered_accounts
        assert len(result) == 1
        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_search_no_results(self, mock_async_session):
        """Test searching service accounts with no matching results."""
        # Arrange
        repo = ServiceAccountRepository(mock_async_session)
        
        mock_result = MagicMock()
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = []
        mock_result.scalars.return_value = mock_scalars
        mock_async_session.execute.return_value = mock_result

        # Act
        result = await repo.search("non-existent")

        # Assert
        assert result == []
        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_active_accounts(self, mock_async_session, multiple_service_accounts):
        """Test getting only active service accounts."""
        # Arrange
        repo = ServiceAccountRepository(mock_async_session)
        # Filter to only active accounts (indices 0 and 2 based on our fixture)
        active_accounts = [acc for acc in multiple_service_accounts if acc.is_active]
        
        mock_result = MagicMock()
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = active_accounts
        mock_result.scalars.return_value = mock_scalars
        mock_async_session.execute.return_value = mock_result

        # Act
        result = await repo.get_active_accounts()

        # Assert
        assert result == active_accounts
        assert len(result) == 2  # Only active accounts
        assert all(acc.is_active for acc in result)
        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_assign_role_success(self, mock_async_session, sample_service_account, sample_admin_role):
        """Test successfully assigning a role to a service account."""
        # Arrange
        repo = ServiceAccountRepository(mock_async_session)

        # Mock get_by_id_with_roles to return the service account
        with patch.object(repo, 'get_by_id_with_roles', return_value=sample_service_account):
            # Mock the role query to return the role
            mock_role_result = MagicMock()
            mock_role_result.scalar_one_or_none.return_value = sample_admin_role
            mock_async_session.execute.return_value = mock_role_result
            
            # Act
            result = await repo.assign_role(str(sample_service_account.id), str(sample_admin_role.id))

            # Assert
            assert result is True
            mock_async_session.commit.assert_called_once()
            assert sample_admin_role in sample_service_account.roles

    @pytest.mark.asyncio
    async def test_assign_role_already_assigned(self, mock_async_session, sample_service_account_with_roles):
        """Test assigning a role that's already assigned."""
        # Arrange
        repo = ServiceAccountRepository(mock_async_session)
        existing_role = sample_service_account_with_roles.roles[0]
        
        # Mock get_by_id_with_roles to return the service account with existing role
        with patch.object(repo, 'get_by_id_with_roles', return_value=sample_service_account_with_roles):
            # Mock the role query to return the existing role
            mock_role_result = MagicMock()
            mock_role_result.scalar_one_or_none.return_value = existing_role
            mock_async_session.execute.return_value = mock_role_result
            
            # Act
            result = await repo.assign_role(str(sample_service_account_with_roles.id), str(existing_role.id))

            # Assert
            assert result is True  # Should return True for already assigned
            assert len(sample_service_account_with_roles.roles) == 1  # Should not duplicate
            mock_async_session.commit.assert_not_called()  # Should not commit

    @pytest.mark.asyncio
    async def test_assign_role_service_account_not_found(self, mock_async_session):
        """Test assigning a role when service account doesn't exist."""
        # Arrange
        repo = ServiceAccountRepository(mock_async_session)
        
        # Mock get_by_id_with_roles to return None
        with patch.object(repo, 'get_by_id_with_roles', return_value=None):
            # Act
            result = await repo.assign_role(str(uuid4()), str(uuid4()))

            # Assert
            assert result is False
            mock_async_session.commit.assert_not_called()

    @pytest.mark.asyncio
    async def test_assign_role_role_not_found(self, mock_async_session, sample_service_account):
        """Test assigning a role that doesn't exist."""
        # Arrange
        repo = ServiceAccountRepository(mock_async_session)
        
        # Mock get_by_id_with_roles to return the service account
        with patch.object(repo, 'get_by_id_with_roles', return_value=sample_service_account):
            # Mock the role query to return None (role not found)
            mock_role_result = MagicMock()
            mock_role_result.scalar_one_or_none.return_value = None
            mock_async_session.execute.return_value = mock_role_result

            # Act
            result = await repo.assign_role(str(sample_service_account.id), str(uuid4()))

            # Assert
            assert result is False
            mock_async_session.commit.assert_not_called()

    @pytest.mark.asyncio
    async def test_remove_role_success(self, mock_async_session, sample_service_account_with_roles):
        """Test successfully removing a role from a service account."""
        # Arrange
        repo = ServiceAccountRepository(mock_async_session)
        role_to_remove = sample_service_account_with_roles.roles[0]
        
        # Mock get_by_id_with_roles to return the service account with role
        with patch.object(repo, 'get_by_id_with_roles', return_value=sample_service_account_with_roles):
            # Act
            result = await repo.remove_role(str(sample_service_account_with_roles.id), str(role_to_remove.id))

            # Assert
            assert result is True
            assert len(sample_service_account_with_roles.roles) == 0
            mock_async_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_remove_role_not_assigned(self, mock_async_session, sample_service_account):
        """Test removing a role that's not assigned."""
        # Arrange
        repo = ServiceAccountRepository(mock_async_session)
        
        # Mock get_by_id_with_roles to return the service account without roles
        with patch.object(repo, 'get_by_id_with_roles', return_value=sample_service_account):
            # Act
            result = await repo.remove_role(str(sample_service_account.id), str(uuid4()))

            # Assert
            assert result is False
            mock_async_session.commit.assert_not_called()

    @pytest.mark.asyncio
    async def test_remove_role_service_account_not_found(self, mock_async_session):
        """Test removing a role when service account doesn't exist."""
        # Arrange
        repo = ServiceAccountRepository(mock_async_session)
        
        # Mock get_by_id_with_roles to return None
        with patch.object(repo, 'get_by_id_with_roles', return_value=None):
            # Act
            result = await repo.remove_role(str(uuid4()), str(uuid4()))

            # Assert
            assert result is False
            mock_async_session.commit.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_last_used_success(self, mock_async_session, sample_service_account):
        """Test successfully updating last_used_at timestamp."""
        # Arrange
        repo = ServiceAccountRepository(mock_async_session)
        original_last_used = sample_service_account.last_used_at
        
        # Mock get_by_id to return the service account
        with patch.object(repo, 'get_by_id', return_value=sample_service_account):
            # Act
            result = await repo.update_last_used(str(sample_service_account.id))

            # Assert
            assert result is True
            assert sample_service_account.last_used_at != original_last_used
            assert sample_service_account.last_used_at is not None
            mock_async_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_last_used_not_found(self, mock_async_session):
        """Test updating last_used_at when service account doesn't exist."""
        # Arrange
        repo = ServiceAccountRepository(mock_async_session)
        
        # Mock get_by_id to return None
        with patch.object(repo, 'get_by_id', return_value=None):
            # Act
            result = await repo.update_last_used(str(uuid4()))

            # Assert
            assert result is False
            mock_async_session.commit.assert_not_called()

    @pytest.mark.asyncio
    async def test_deactivate_success(self, mock_async_session, sample_service_account):
        """Test successfully deactivating a service account."""
        # Arrange
        repo = ServiceAccountRepository(mock_async_session)
        sample_service_account.is_active = True  # Ensure it starts as active
        
        # Mock get_by_id to return the service account
        with patch.object(repo, 'get_by_id', return_value=sample_service_account):
            # Act
            result = await repo.deactivate(str(sample_service_account.id))

            # Assert
            assert result is True
            assert sample_service_account.is_active is False
            mock_async_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_deactivate_not_found(self, mock_async_session):
        """Test deactivating when service account doesn't exist."""
        # Arrange
        repo = ServiceAccountRepository(mock_async_session)
        
        # Mock get_by_id to return None
        with patch.object(repo, 'get_by_id', return_value=None):
            # Act
            result = await repo.deactivate(str(uuid4()))

            # Assert
            assert result is False
            mock_async_session.commit.assert_not_called()

    @pytest.mark.asyncio
    async def test_activate_success(self, mock_async_session, sample_service_account):
        """Test successfully activating a service account."""
        # Arrange
        repo = ServiceAccountRepository(mock_async_session)
        sample_service_account.is_active = False  # Ensure it starts as inactive
        
        # Mock get_by_id to return the service account
        with patch.object(repo, 'get_by_id', return_value=sample_service_account):
            # Act
            result = await repo.activate(str(sample_service_account.id))

            # Assert
            assert result is True
            assert sample_service_account.is_active is True
            mock_async_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_activate_not_found(self, mock_async_session):
        """Test activating when service account doesn't exist."""
        # Arrange
        repo = ServiceAccountRepository(mock_async_session)
        
        # Mock get_by_id to return None
        with patch.object(repo, 'get_by_id', return_value=None):
            # Act
            result = await repo.activate(str(uuid4()))

            # Assert
            assert result is False
            mock_async_session.commit.assert_not_called()

    @pytest.mark.asyncio
    async def test_client_id_exists_true(self, mock_async_session, sample_service_account):
        """Test checking if client_id exists when it does."""
        # Arrange
        repo = ServiceAccountRepository(mock_async_session)
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = sample_service_account
        mock_async_session.execute.return_value = mock_result

        # Act
        result = await repo.client_id_exists("test-client-001")

        # Assert
        assert result is True
        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_client_id_exists_false(self, mock_async_session):
        """Test checking if client_id exists when it doesn't."""
        # Arrange
        repo = ServiceAccountRepository(mock_async_session)
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_async_session.execute.return_value = mock_result

        # Act
        result = await repo.client_id_exists("non-existent-client")

        # Assert
        assert result is False
        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_client_id_exists_exclude_self(self, mock_async_session, sample_service_account):
        """Test checking if client_id exists excluding a specific ID."""
        # Arrange
        repo = ServiceAccountRepository(mock_async_session)
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None  # Should not find when excluding self
        mock_async_session.execute.return_value = mock_result

        # Act
        result = await repo.client_id_exists("test-client-001", exclude_id=str(sample_service_account.id))

        # Assert
        assert result is False
        mock_async_session.execute.assert_called_once()
