"""
Pytest configuration and fixtures for auth-backend tests.

This module provides common test fixtures including mocked database sessions,
test data factories, and shared testing utilities.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, Mock
from uuid import uuid4
from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy.orm import Session

from src.models.service_account import ServiceAccount
from src.models.role import Role
from src.models.user import User
from src.models.audit_log import AuditLog


@pytest.fixture
def mock_async_session():
    """Create a mock AsyncSession for testing."""
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.commit = AsyncMock()
    mock_session.rollback = AsyncMock()
    mock_session.close = AsyncMock()
    mock_session.execute = AsyncMock()
    mock_session.scalar = AsyncMock()
    mock_session.scalars = AsyncMock()
    return mock_session


@pytest.fixture
def mock_result():
    """Create a mock SQLAlchemy Result for testing."""
    mock_result = MagicMock(spec=Result)
    mock_result.scalar_one_or_none = MagicMock()
    mock_result.scalars = MagicMock()
    mock_result.all = MagicMock()
    return mock_result


@pytest.fixture
def sample_service_account():
    """Create a sample ServiceAccount for testing."""
    return ServiceAccount(
        id=uuid4(),
        client_id="test-client-001",
        client_secret="test-secret-123",
        client_name="Test OAuth Client",
        description="A test OAuth client for unit testing",
        grant_types=["client_credentials"],
        response_types=[],
        scope="read write",
        token_endpoint_auth_method="client_secret_basic",
        audience=["https://api.example.com"],
        owner="test-owner",
        client_metadata={"app_type": "test"},
        redirect_uris=[],
        skip_consent=True,
        is_active=True,
        last_used_at=None,
        created_by="test-admin",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        roles=[]
    )


@pytest.fixture
def sample_service_account_with_roles(sample_role):
    """Create a sample ServiceAccount with roles for testing."""
    service_account = ServiceAccount(
        id=uuid4(),
        client_id="test-client-002",
        client_secret="test-secret-456",
        client_name="Test OAuth Client with Roles",
        description="A test OAuth client with roles for unit testing",
        grant_types=["client_credentials"],
        response_types=[],
        scope="read write admin",
        token_endpoint_auth_method="client_secret_basic",
        audience=["https://api.example.com"],
        owner="test-owner",
        client_metadata={"app_type": "test"},
        redirect_uris=[],
        skip_consent=True,
        is_active=True,
        last_used_at=None,
        created_by="test-admin",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        roles=[sample_role]
    )
    return service_account


@pytest.fixture
def sample_role():
    """Create a sample Role for testing."""
    return Role(
        id=uuid4(),
        name="test_user",
        description="Test user role",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )


@pytest.fixture
def sample_admin_role():
    """Create a sample admin Role for testing."""
    return Role(
        id=uuid4(),
        name="admin",
        description="Administrator role",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )


@pytest.fixture
def multiple_service_accounts(sample_role):
    """Create multiple ServiceAccounts for testing list operations."""
    accounts = []
    for i in range(3):
        account = ServiceAccount(
            id=uuid4(),
            client_id=f"test-client-{i:03d}",
            client_secret=f"test-secret-{i:03d}",
            client_name=f"Test OAuth Client {i+1}",
            description=f"Test client {i+1} for unit testing",
            grant_types=["client_credentials"],
            response_types=[],
            scope="read write",
            token_endpoint_auth_method="client_secret_basic",
            audience=["https://api.example.com"],
            owner="test-owner",
            client_metadata={"app_type": "test"},
            redirect_uris=[],
            skip_consent=True,
            is_active=(i % 2 == 0),  # Alternate active/inactive
            last_used_at=None,
            created_by="test-admin",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            roles=[] if i == 0 else [sample_role]
        )
        accounts.append(account)
    return accounts


class MockScalars:
    """Mock class for SQLAlchemy scalars result."""
    
    def __init__(self, items: List):
        self.items = items
    
    def all(self):
        """Return all items."""
        return self.items


def create_mock_result_with_items(items: List) -> Mock:
    """Create a mock result that returns the given items."""
    mock_result = Mock()
    mock_scalars = MockScalars(items)
    mock_result.scalars.return_value = mock_scalars
    return mock_result


def create_mock_result_single(item: Optional[object]) -> Mock:
    """Create a mock result that returns a single item."""
    mock_result = Mock()
    mock_result.scalar_one_or_none.return_value = item
    return mock_result


@pytest.fixture
def service_account_create_data():
    """Sample data for creating a service account."""
    return {
        "client_id": "new-test-client",
        "client_secret": "new-test-secret",
        "client_name": "New Test Client",
        "description": "A new test client",
        "grant_types": ["client_credentials"],
        "response_types": [],
        "scope": "read write",
        "token_endpoint_auth_method": "client_secret_basic",
        "audience": ["https://api.example.com"],
        "owner": "test-owner",
        "client_metadata": {"app_type": "new"},
        "redirect_uris": [],
        "skip_consent": True,
        "is_active": True,
        "created_by": "test-admin"
    }


@pytest.fixture
def service_account_update_data():
    """Sample data for updating a service account."""
    return {
        "client_name": "Updated Test Client",
        "description": "An updated test client",
        "scope": "read write admin"
    }


@pytest.fixture
def sample_user():
    """Create a sample User for testing."""
    return User(
        id=uuid4(),
        email="test@example.com",
        display_name="Test User",
        password_hash="hashed_password_123",
        is_active=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        roles=[]
    )


@pytest.fixture
def sample_user_role():
    """Create a sample user Role for testing."""
    return Role(
        id=uuid4(),
        name="user",
        description="Regular user role",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )


@pytest.fixture
def sample_user_with_roles(sample_user, sample_admin_role):
    """Create a sample User with roles assigned."""
    sample_user.roles = [sample_admin_role]
    return sample_user


@pytest.fixture
def sample_users_with_roles(sample_admin_role, sample_user_role):
    """Create multiple sample Users with different roles."""
    user1 = User(
        id=uuid4(),
        email="admin@example.com",
        display_name="Admin User",
        password_hash="hashed_password_admin",
        is_active=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        roles=[sample_admin_role]
    )
    
    user2 = User(
        id=uuid4(),
        email="user@example.com",
        display_name="Regular User",
        password_hash="hashed_password_user",
        is_active=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        roles=[sample_user_role]
    )
    
    return [user1, user2]


@pytest.fixture
def sample_audit_log():
    """Create a sample AuditLog for testing."""
    return AuditLog(
        id=uuid4(),
        action="CREATE",
        resource_type="User",
        resource_id=str(uuid4()),
        details={"field": "value", "change": "created"},
        performed_by="admin@example.com",
        ip_address="192.168.1.1",
        user_agent="Mozilla/5.0",
        timestamp=datetime.now(timezone.utc)
    )
