"""
Shared test utilities for repository testing.

Contains helper functions and fixtures for testing repository classes
with proper mock database sessions and common test patterns.
"""
from typing import List, Dict, Any
from unittest.mock import MagicMock, AsyncMock
from uuid import UUID, uuid4
from datetime import datetime, timezone

from src.models.service_account import ServiceAccount
from src.models.role import Role


def create_mock_result_with_data(data: Any) -> MagicMock:
    """Create a mock result object for SQLAlchemy query results."""
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = data
    return mock_result


def create_mock_scalars_result(data: List[Any]) -> MagicMock:
    """Create a mock result object for SQLAlchemy scalars results."""
    mock_result = MagicMock()
    mock_scalars = MagicMock()
    mock_scalars.all.return_value = data
    mock_result.scalars.return_value = mock_scalars
    return mock_result


def create_sample_service_account(
    client_id: str = "test-client-123",
    name: str = "Test Service Account",
    description: str = "A test service account",
    is_active: bool = True
) -> ServiceAccount:
    """Create a sample ServiceAccount for testing."""
    return ServiceAccount(
        id=uuid4(),
        client_id=client_id,
        name=name,
        description=description,
        is_active=is_active,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )


def create_sample_role(
    name: str = "test_user",
    description: str = "Test user role"
) -> Role:
    """Create a sample Role for testing."""
    return Role(
        id=uuid4(),
        name=name,
        description=description,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )


def assert_service_account_equal(
    actual: ServiceAccount,
    expected: ServiceAccount,
    check_id: bool = True
) -> None:
    """Assert that two ServiceAccount objects are equal."""
    if check_id:
        assert actual.id == expected.id
    assert actual.client_id == expected.client_id
    assert actual.name == expected.name
    assert actual.description == expected.description
    assert actual.is_active == expected.is_active


def assert_role_equal(
    actual: Role,
    expected: Role,
    check_id: bool = True
) -> None:
    """Assert that two Role objects are equal."""
    if check_id:
        assert actual.id == expected.id
    assert actual.name == expected.name
    assert actual.description == expected.description


def setup_mock_session_for_create(
    mock_session: MagicMock,
    created_object: Any
) -> None:
    """Set up mock session for create operations."""
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None
    
    # Mock the refresh to set the ID if not set
    def mock_refresh(obj):
        if not hasattr(obj, 'id') or obj.id is None:
            obj.id = uuid4()
        if not hasattr(obj, 'created_at') or obj.created_at is None:
            obj.created_at = datetime.now(timezone.utc)
        if not hasattr(obj, 'updated_at') or obj.updated_at is None:
            obj.updated_at = datetime.now(timezone.utc)
    
    mock_session.refresh.side_effect = mock_refresh


def setup_mock_session_for_update(
    mock_session: MagicMock,
    updated_object: Any
) -> None:
    """Set up mock session for update operations."""
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None
    
    def mock_refresh(obj):
        obj.updated_at = datetime.now(timezone.utc)
    
    mock_session.refresh.side_effect = mock_refresh


def setup_mock_session_for_delete(mock_session: MagicMock) -> None:
    """Set up mock session for delete operations."""
    mock_session.delete.return_value = None
    mock_session.commit.return_value = None


def create_mock_async_session() -> AsyncMock:
    """Create a mock AsyncSession for testing."""
    mock_session = AsyncMock()
    
    # Set up common async operations
    mock_session.execute = AsyncMock()
    mock_session.commit = AsyncMock()
    mock_session.rollback = AsyncMock()
    mock_session.close = AsyncMock()
    mock_session.add = MagicMock()
    mock_session.delete = MagicMock()
    mock_session.refresh = AsyncMock()
    
    return mock_session
