"""
Tests for the Role model.

This module tests the Role model functionality including properties,
methods, and relationships.
"""
from src.models.role import Role
from src.models.user import User
from src.models.service_account import ServiceAccount


class TestRole:
    """Test cases for the Role model."""

    def test_role_creation(self):
        """Test creating a new role."""
        role = Role(
            name="test_role",
            description="Test role for testing"
        )
        
        assert role.name == "test_role"
        assert role.description == "Test role for testing"

    def test_role_repr(self):
        """Test role string representation."""
        role = Role(name="admin")
        assert repr(role) == "<Role(name='admin')>"

    def test_user_count_property_empty(self):
        """Test user_count property when no users assigned."""
        role = Role(name="test_role")
        role.users = []
        assert role.user_count == 0

    def test_user_count_property_with_users(self):
        """Test user_count property when users are assigned."""
        user1 = User(email="user1@example.com")
        user2 = User(email="user2@example.com")
        
        role = Role(name="test_role")
        role.users = [user1, user2]
        
        assert role.user_count == 2

    def test_service_account_count_property_empty(self):
        """Test service_account_count property when no service accounts assigned."""
        role = Role(name="test_role")
        role.service_accounts = []
        assert role.service_account_count == 0

    def test_service_account_count_property_with_accounts(self):
        """Test service_account_count property when service accounts are assigned."""
        sa1 = ServiceAccount(client_id="client1", client_name="Client 1")
        sa2 = ServiceAccount(client_id="client2", client_name="Client 2")
        
        role = Role(name="test_role")
        role.service_accounts = [sa1, sa2]
        
        assert role.service_account_count == 2

    def test_total_assignments_property(self):
        """Test total_assignments property with mixed assignments."""
        user = User(email="user@example.com")
        sa = ServiceAccount(client_id="client1", client_name="Client 1")
        
        role = Role(name="test_role")
        role.users = [user]
        role.service_accounts = [sa]
        
        assert role.total_assignments == 2

    def test_get_user_emails_empty(self):
        """Test get_user_emails method when no users assigned."""
        role = Role(name="test_role")
        role.users = []
        assert role.get_user_emails() == []

    def test_get_user_emails_with_users(self):
        """Test get_user_emails method when users are assigned."""
        user1 = User(email="user1@example.com")
        user2 = User(email="user2@example.com")
        
        role = Role(name="test_role")
        role.users = [user1, user2]
        
        emails = role.get_user_emails()
        assert set(emails) == {"user1@example.com", "user2@example.com"}
