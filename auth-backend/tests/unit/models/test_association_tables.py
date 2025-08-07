"""
Tests for association tables.

This module tests that association tables are properly defined.
"""
from src.models.user_roles import user_roles
from src.models.service_account_roles import service_account_roles
from src.models.service_account_scopes import service_account_scopes


class TestAssociationTables:
    """Test cases for association tables."""

    def test_user_roles_table_exists(self):
        """Test that user_roles table is defined."""
        assert user_roles is not None
        assert user_roles.name == "user_roles"
        assert len(user_roles.columns) == 2
        
        # Check column names
        column_names = [col.name for col in user_roles.columns]
        assert "user_id" in column_names
        assert "role_id" in column_names

    def test_service_account_roles_table_exists(self):
        """Test that service_account_roles table is defined."""
        assert service_account_roles is not None
        assert service_account_roles.name == "service_account_roles"
        assert len(service_account_roles.columns) == 2
        
        # Check column names
        column_names = [col.name for col in service_account_roles.columns]
        assert "service_account_id" in column_names
        assert "role_id" in column_names

    def test_service_account_scopes_table_exists(self):
        """Test that service_account_scopes table is defined."""
        assert service_account_scopes is not None
        assert service_account_scopes.name == "service_account_scopes"
        assert len(service_account_scopes.columns) == 2
        
        # Check column names
        column_names = [col.name for col in service_account_scopes.columns]
        assert "service_account_id" in column_names
        assert "scope_id" in column_names
