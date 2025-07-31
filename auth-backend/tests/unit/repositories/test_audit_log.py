"""
Unit tests for AuditLogRepository.

Tests all audit logging operations including JSON serialization,
resource filtering, and user activity tracking.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID, uuid4
from datetime import datetime, timezone
import json

from src.repositories.audit_log import AuditLogRepository
from src.models.audit_log import AuditLog


class TestAuditLogRepository:
    """Test suite for AuditLogRepository."""

    def test_init(self, mock_async_session):
        """Test repository initialization."""
        repo = AuditLogRepository(mock_async_session)
        assert repo.db == mock_async_session
        assert repo.model == AuditLog

    @pytest.mark.asyncio
    async def test_get_by_resource_found(self, mock_async_session, sample_audit_log):
        """Test getting audit logs by resource when they exist."""
        # Arrange
        repo = AuditLogRepository(mock_async_session)
        mock_result = MagicMock()
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = [sample_audit_log]
        mock_result.scalars.return_value = mock_scalars
        mock_async_session.execute.return_value = mock_result

        # Act
        result = await repo.get_by_resource("User", str(sample_audit_log.resource_id))

        # Assert
        assert result == [sample_audit_log]
        assert len(result) == 1
        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_resource_not_found(self, mock_async_session):
        """Test getting audit logs by resource when they don't exist."""
        # Arrange
        repo = AuditLogRepository(mock_async_session)
        mock_result = MagicMock()
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = []
        mock_result.scalars.return_value = mock_scalars
        mock_async_session.execute.return_value = mock_result

        # Act
        result = await repo.get_by_resource("User", str(uuid4()))

        # Assert
        assert result == []
        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_resource_with_action_filter(self, mock_async_session, sample_audit_log):
        """Test getting audit logs by resource with limit."""
        # Arrange
        repo = AuditLogRepository(mock_async_session)
        mock_result = MagicMock()
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = [sample_audit_log]
        mock_result.scalars.return_value = mock_scalars
        mock_async_session.execute.return_value = mock_result

        # Act
        result = await repo.get_by_resource(
            resource_type="User", 
            resource_id=str(sample_audit_log.resource_id),
            limit=50
        )

        # Assert
        assert result == [sample_audit_log]
        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_resource_with_date_range(self, mock_async_session, sample_audit_log):
        """Test getting audit logs by resource with custom limit."""
        # Arrange
        repo = AuditLogRepository(mock_async_session)
        mock_result = MagicMock()
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = [sample_audit_log]
        mock_result.scalars.return_value = mock_scalars
        mock_async_session.execute.return_value = mock_result

        # Act
        result = await repo.get_by_resource(
            resource_type="User", 
            resource_id=str(sample_audit_log.resource_id),
            limit=25
        )

        # Assert
        assert result == [sample_audit_log]
        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_user_logs_found(self, mock_async_session, sample_audit_log):
        """Test getting user logs when they exist."""
        # Arrange
        repo = AuditLogRepository(mock_async_session)
        mock_result = MagicMock()
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = [sample_audit_log]
        mock_result.scalars.return_value = mock_scalars
        mock_async_session.execute.return_value = mock_result

        # Act
        result = await repo.get_user_logs(str(uuid4()), limit=50)

        # Assert
        assert result == [sample_audit_log]
        assert len(result) == 1
        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_user_logs_not_found(self, mock_async_session):
        """Test getting user logs when they don't exist."""
        # Arrange
        repo = AuditLogRepository(mock_async_session)
        mock_result = MagicMock()
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = []
        mock_result.scalars.return_value = mock_scalars
        mock_async_session.execute.return_value = mock_result

        # Act
        result = await repo.get_user_logs(str(uuid4()), limit=50)

        # Assert
        assert result == []
        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_user_logs_with_skip(self, mock_async_session):
        """Test getting user logs with custom limit."""
        # Arrange
        repo = AuditLogRepository(mock_async_session)
        mock_result = MagicMock()
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = []
        mock_result.scalars.return_value = mock_scalars
        mock_async_session.execute.return_value = mock_result

        # Act
        result = await repo.get_user_logs(str(uuid4()), limit=25)

        # Assert
        assert result == []
        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_with_serialization_success(self, mock_async_session):
        """Test creating audit log with JSON serialization."""
        # Arrange
        repo = AuditLogRepository(mock_async_session)
        resource_id = str(uuid4())
        
        # Mock execute and commit
        mock_async_session.execute = AsyncMock()
        mock_async_session.commit = AsyncMock()
        
        # Test data with complex object that needs serialization
        test_data = {
            "user": {"email": "test@example.com"},
            "changes": ["field1", "field2"],
            "metadata": {
                "timestamp": datetime.now(timezone.utc),
                "version": 1.0
            }
        }

        # Act
        result = await repo.create_with_serialization(
            action="UPDATE",
            resource_type="User",
            resource_id=resource_id,
            details=test_data,
            performed_by="admin@example.com"
        )

        # Assert
        assert result is not None
        assert result.action == "UPDATE"
        assert result.resource_type == "User"
        assert result.resource_id == resource_id
        assert result.performed_by == "admin@example.com"
        
        # Verify details are properly cleaned
        assert result.details["user"]["email"] == "test@example.com"
        assert result.details["changes"] == ["field1", "field2"]
        
        mock_async_session.execute.assert_called_once()
        mock_async_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_with_serialization_simple_data(self, mock_async_session):
        """Test creating audit log with simple string data."""
        # Arrange
        repo = AuditLogRepository(mock_async_session)
        resource_id = str(uuid4())
        
        # Mock execute and commit
        mock_async_session.execute = AsyncMock()
        mock_async_session.commit = AsyncMock()

        # Act
        result = await repo.create_with_serialization(
            action="CREATE",
            resource_type="Role",
            resource_id=resource_id,
            details="Simple string details",
            performed_by="admin@example.com"
        )

        # Assert
        assert result is not None
        assert result.action == "CREATE"
        assert result.resource_type == "Role"
        assert result.resource_id == resource_id
        assert result.performed_by == "admin@example.com"
        
        mock_async_session.execute.assert_called_once()
        mock_async_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_with_serialization_none_details(self, mock_async_session):
        """Test creating audit log with None details."""
        # Arrange
        repo = AuditLogRepository(mock_async_session)
        resource_id = str(uuid4())
        
        # Mock execute and commit
        mock_async_session.execute = AsyncMock()
        mock_async_session.commit = AsyncMock()

        # Act
        result = await repo.create_with_serialization(
            action="DELETE",
            resource_type="ServiceAccount",
            resource_id=resource_id,
            details=None,
            performed_by="admin@example.com"
        )

        # Assert
        assert result is not None
        assert result.details == {}  # Empty dict when None passed
        
        mock_async_session.execute.assert_called_once()
        mock_async_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_with_serialization_json_cleaning(self, mock_async_session):
        """Test JSON cleaning for non-serializable objects."""
        # Arrange
        repo = AuditLogRepository(mock_async_session)
        resource_id = str(uuid4())
        
        # Mock execute and commit
        mock_async_session.execute = AsyncMock()
        mock_async_session.commit = AsyncMock()
        
        # Test data with datetime and UUID objects that need cleaning
        test_data = {
            "resource_id": resource_id,  # String
            "created_at": datetime.now(timezone.utc),  # datetime object
            "regular_field": "normal string",
            "numeric_field": 42
        }

        # Act
        result = await repo.create_with_serialization(
            action="CREATE",
            resource_type="User",
            resource_id=resource_id,
            details=test_data,
            performed_by="admin@example.com"
        )

        # Assert
        assert result is not None
        
        # Verify details are properly cleaned
        assert result.details["resource_id"] == resource_id
        
        # Regular fields should remain unchanged
        assert result.details["regular_field"] == "normal string"
        assert result.details["numeric_field"] == 42
        
        mock_async_session.execute.assert_called_once()
        mock_async_session.commit.assert_called_once()
