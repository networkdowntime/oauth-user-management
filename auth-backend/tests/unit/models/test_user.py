"""
Tests for the User model.

This module tests the User model functionality including properties,
methods, and relationships.
"""
from datetime import datetime, timedelta

from src.models.user import User
from src.models.role import Role


class TestUser:
    """Test cases for the User model."""

    def test_user_creation(self):
        """Test creating a new user."""
        user = User(
            email="test@example.com",
            display_name="Test User",
            password_hash="hashed_password",
            is_active=True,
            failed_login_attempts=0  # Explicitly set for in-memory test
        )
        
        assert user.email == "test@example.com"
        assert user.display_name == "Test User"
        assert user.password_hash == "hashed_password"
        assert user.is_active is True
        assert user.failed_login_attempts == 0
        assert user.locked_until is None
        assert user.last_login_at is None

    def test_user_repr(self):
        """Test user string representation."""
        user = User(email="test@example.com")
        assert repr(user) == "<User(email='test@example.com')>"

    def test_is_locked_property_when_not_locked(self):
        """Test is_locked property when user is not locked."""
        user = User(email="test@example.com", locked_until=None)
        assert user.is_locked is False

    def test_is_locked_property_when_locked_until_future(self):
        """Test is_locked property when user is locked until future date."""
        # Use utcnow() to match the model's implementation
        from datetime import datetime as dt
        future_date = dt.utcnow() + timedelta(hours=1)
        user = User(email="test@example.com", locked_until=future_date)
        assert user.is_locked is True

    def test_is_locked_property_when_locked_until_past(self):
        """Test is_locked property when locked_until is in the past."""
        from datetime import datetime as dt
        past_date = dt.utcnow() - timedelta(hours=1)
        user = User(email="test@example.com", locked_until=past_date)
        assert user.is_locked is False

    def test_role_names_property_empty(self):
        """Test role_names property when user has no roles."""
        user = User(email="test@example.com")
        user.roles = []
        assert user.role_names == []

    def test_role_names_property_with_roles(self):
        """Test role_names property when user has roles."""
        role1 = Role(name="admin", description="Administrator")
        role2 = Role(name="user", description="Regular user")
        
        user = User(email="test@example.com")
        user.roles = [role1, role2]
        
        assert set(user.role_names) == {"admin", "user"}

    def test_has_role_method_true(self):
        """Test has_role method when user has the role."""
        role = Role(name="admin", description="Administrator")
        user = User(email="test@example.com")
        user.roles = [role]
        
        assert user.has_role("admin") is True

    def test_has_role_method_false(self):
        """Test has_role method when user doesn't have the role."""
        user = User(email="test@example.com")
        user.roles = []
        
        assert user.has_role("admin") is False

    def test_is_admin_method_true(self):
        """Test is_admin method when user has user_admin role."""
        role = Role(name="user_admin", description="User Administrator")
        user = User(email="test@example.com")
        user.roles = [role]
        
        assert user.is_admin() is True

    def test_is_admin_method_false(self):
        """Test is_admin method when user doesn't have user_admin role."""
        role = Role(name="regular_user", description="Regular User")
        user = User(email="test@example.com")
        user.roles = [role]
        
        assert user.is_admin() is False

    def test_can_login_active_and_not_locked(self):
        """Test can_login when user is active and not locked."""
        user = User(
            email="test@example.com",
            is_active=True,
            locked_until=None
        )
        assert user.can_login() is True

    def test_can_login_inactive_user(self):
        """Test can_login when user is inactive."""
        user = User(
            email="test@example.com",
            is_active=False,
            locked_until=None
        )
        assert user.can_login() is False

    def test_can_login_locked_user(self):
        """Test can_login when user is locked."""
        from datetime import datetime as dt
        future_date = dt.utcnow() + timedelta(hours=1)
        user = User(
            email="test@example.com",
            is_active=True,
            locked_until=future_date
        )
        assert user.can_login() is False

    def test_can_login_inactive_and_locked(self):
        """Test can_login when user is both inactive and locked."""
        from datetime import datetime as dt
        future_date = dt.utcnow() + timedelta(hours=1)
        user = User(
            email="test@example.com",
            is_active=False,
            locked_until=future_date
        )
        assert user.can_login() is False
