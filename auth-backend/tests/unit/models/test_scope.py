"""
Tests for the Scope model.

This module tests the Scope model functionality including properties,
methods, and enum handling.
"""
from src.models.scope import Scope, ScopeAppliesTo
from src.models.service_account import ServiceAccount, ServiceAccountType


class TestScope:
    """Test cases for the Scope model."""

    def test_scope_creation(self):
        """Test creating a new scope."""
        scope = Scope(
            name="read:users",
            description="Read user data",
            is_active=True
        )
        
        assert scope.name == "read:users"
        assert scope.description == "Read user data"
        assert scope.is_active is True

    def test_scope_repr(self):
        """Test scope string representation."""
        scope = Scope(name="write:data")
        assert repr(scope) == "<Scope(name='write:data')>"

    def test_service_account_count_property_empty(self):
        """Test service_account_count property when no service accounts assigned."""
        scope = Scope(name="test:scope")
        scope.service_accounts = []
        assert scope.service_account_count == 0

    def test_service_account_count_property_with_accounts(self):
        """Test service_account_count property when service accounts are assigned."""
        sa1 = ServiceAccount(client_id="client1", client_name="Client 1")
        sa2 = ServiceAccount(client_id="client2", client_name="Client 2")
        
        scope = Scope(name="test:scope")
        scope.service_accounts = [sa1, sa2]
        
        assert scope.service_account_count == 2

    def test_applies_to_list_property_empty(self):
        """Test applies_to_list property when applies_to is empty."""
        scope = Scope(name="test:scope", applies_to="")
        assert scope.applies_to_list == []

    def test_applies_to_list_property_single_value(self):
        """Test applies_to_list property with single value."""
        # Use the actual enum value string
        scope = Scope(name="test:scope", applies_to="Service-to-service")
        assert scope.applies_to_list == [ScopeAppliesTo.SERVICE_TO_SERVICE]

    def test_applies_to_list_property_multiple_values(self):
        """Test applies_to_list property with multiple values."""
        # Use the actual enum value strings
        scope = Scope(name="test:scope", applies_to="Service-to-service,Browser")
        applies_to = scope.applies_to_list
        assert ScopeAppliesTo.SERVICE_TO_SERVICE in applies_to
        assert ScopeAppliesTo.BROWSER in applies_to
        assert len(applies_to) == 2

    def test_applies_to_list_setter(self):
        """Test setting applies_to_list property."""
        scope = Scope(name="test:scope")
        scope.applies_to_list = [ScopeAppliesTo.SERVICE_TO_SERVICE, ScopeAppliesTo.BROWSER]
        
        # Check the actual enum value strings are used
        assert "Service-to-service" in scope.applies_to
        assert "Browser" in scope.applies_to

    def test_applies_to_list_setter_empty(self):
        """Test setting applies_to_list property to empty list."""
        scope = Scope(name="test:scope")
        scope.applies_to_list = []
        assert scope.applies_to == ""

    def test_applies_to_service_method_true(self):
        """Test applies_to_service method when it applies to service."""
        scope = Scope(name="test:scope")
        scope.applies_to_list = [ScopeAppliesTo.SERVICE_TO_SERVICE]
        assert scope.applies_to_service() is True

    def test_applies_to_service_method_false(self):
        """Test applies_to_service method when it doesn't apply to service."""
        scope = Scope(name="test:scope")
        scope.applies_to_list = [ScopeAppliesTo.BROWSER]
        assert scope.applies_to_service() is False

    def test_applies_to_browser_method_true(self):
        """Test applies_to_browser method when it applies to browser."""
        scope = Scope(name="test:scope")
        scope.applies_to_list = [ScopeAppliesTo.BROWSER]
        assert scope.applies_to_browser() is True

    def test_applies_to_browser_method_false(self):
        """Test applies_to_browser method when it doesn't apply to browser."""
        scope = Scope(name="test:scope")
        scope.applies_to_list = [ScopeAppliesTo.SERVICE_TO_SERVICE]
        assert scope.applies_to_browser() is False

    def test_is_applicable_to_account_type_service(self):
        """Test is_applicable_to_account_type method for service account type."""
        scope = Scope(name="test:scope")
        scope.applies_to_list = [ScopeAppliesTo.SERVICE_TO_SERVICE]
        
        assert scope.is_applicable_to_account_type(ServiceAccountType.SERVICE_TO_SERVICE.value) is True
        assert scope.is_applicable_to_account_type(ServiceAccountType.BROWSER.value) is False

    def test_is_applicable_to_account_type_browser(self):
        """Test is_applicable_to_account_type method for browser account type."""
        scope = Scope(name="test:scope")
        scope.applies_to_list = [ScopeAppliesTo.BROWSER]
        
        assert scope.is_applicable_to_account_type(ServiceAccountType.BROWSER.value) is True
        assert scope.is_applicable_to_account_type(ServiceAccountType.SERVICE_TO_SERVICE.value) is False

    def test_is_applicable_to_account_type_unknown(self):
        """Test is_applicable_to_account_type method for unknown account type."""
        scope = Scope(name="test:scope")
        scope.applies_to_list = [ScopeAppliesTo.SERVICE_TO_SERVICE]
        
        # Test with an unknown account type
        assert scope.is_applicable_to_account_type("unknown_type") is False

    def test_get_service_account_names_empty(self):
        """Test get_service_account_names method when no service accounts assigned."""
        scope = Scope(name="test:scope")
        scope.service_accounts = []
        assert scope.get_service_account_names() == []

    def test_get_service_account_names_with_accounts(self):
        """Test get_service_account_names method when service accounts are assigned."""
        sa1 = ServiceAccount(client_id="client1", client_name="Client One")
        sa2 = ServiceAccount(client_id="client2", client_name="Client Two")
        
        scope = Scope(name="test:scope")
        scope.service_accounts = [sa1, sa2]
        
        names = scope.get_service_account_names()
        assert set(names) == {"Client One", "Client Two"}

    def test_to_hydra_scope_method(self):
        """Test to_hydra_scope method."""
        scope = Scope(name="read:data")
        assert scope.to_hydra_scope() == "read:data"

    def test_from_hydra_scope_class_method_minimal(self):
        """Test from_hydra_scope class method with minimal parameters."""
        scope = Scope.from_hydra_scope("write:data")
        
        assert scope.name == "write:data"
        assert scope.description == "OAuth2 scope: write:data"
        assert scope.is_active is True
        
        # Default applies_to both types
        applies_to = scope.applies_to_list
        assert ScopeAppliesTo.SERVICE_TO_SERVICE in applies_to
        assert ScopeAppliesTo.BROWSER in applies_to

    def test_from_hydra_scope_class_method_full(self):
        """Test from_hydra_scope class method with all parameters."""
        scope = Scope.from_hydra_scope(
            "admin:users",
            description="Admin access to users",
            applies_to=[ScopeAppliesTo.SERVICE_TO_SERVICE]
        )
        
        assert scope.name == "admin:users"
        assert scope.description == "Admin access to users"
        assert scope.applies_to_list == [ScopeAppliesTo.SERVICE_TO_SERVICE]
