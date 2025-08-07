"""
Tests for the ServiceAccount model.

This module tests the ServiceAccount model functionality including properties,
methods, and relationships.
"""
from typing import Dict, Any

from src.models.service_account import ServiceAccount, ServiceAccountType
from src.models.scope import Scope


class TestServiceAccount:
    """Test cases for the ServiceAccount model."""

    def test_service_account_creation(self):
        """Test creating a new service account."""
        sa = ServiceAccount(
            client_id="test-client",
            client_name="Test Client",
            description="Test service account"
        )
        
        assert sa.client_id == "test-client"
        assert sa.client_name == "Test Client"
        assert sa.description == "Test service account"

    def test_service_account_repr(self):
        """Test service account string representation."""
        sa = ServiceAccount(client_id="test-client", client_name="Test Client")
        assert repr(sa) == "<ServiceAccount(client_id='test-client', name='Test Client')>"

    def test_to_hydra_client_basic(self):
        """Test converting service account to Hydra client format."""
        sa = ServiceAccount(
            client_id="test-client",
            client_secret="test-secret",
            client_name="Test Client",
            grant_types=["client_credentials"],
            response_types=[],
            token_endpoint_auth_method="client_secret_basic",
            audience=["https://api.example.com"],
            owner="test-owner",
            client_metadata={"app_type": "test"},
            redirect_uris=[],
            skip_consent=True,
            account_type="service_to_service"
        )
        
        hydra_client = sa.to_hydra_client()
        
        assert hydra_client["client_id"] == "test-client"
        assert hydra_client["client_secret"] == "test-secret"
        assert hydra_client["client_name"] == "Test Client"
        assert hydra_client["grant_types"] == ["client_credentials"]
        assert hydra_client["audience"] == ["https://api.example.com"]
        assert hydra_client["owner"] == "test-owner"
        assert hydra_client["skip_consent"] is True
        assert hydra_client["account_type"] == "service_to_service"

    def test_to_hydra_client_with_scopes(self):
        """Test converting service account to Hydra client format with scopes."""
        scope1 = Scope(name="read", description="Read access")
        scope2 = Scope(name="write", description="Write access")
        
        sa = ServiceAccount(
            client_id="test-client",
            client_name="Test Client"
        )
        sa.scopes = [scope1, scope2]
        
        hydra_client = sa.to_hydra_client()
        
        assert hydra_client["scope"] == "read write"

    def test_to_hydra_client_no_secret_for_public(self):
        """Test that public clients don't include client_secret."""
        sa = ServiceAccount(
            client_id="test-client",
            client_name="Test Client",
            token_endpoint_auth_method="none",
            client_secret="should-not-appear"
        )
        
        hydra_client = sa.to_hydra_client()
        
        assert "client_secret" not in hydra_client

    def test_from_hydra_client_basic(self):
        """Test creating service account from Hydra client data."""
        hydra_data = {
            "client_id": "hydra-client",
            "client_secret": "hydra-secret",
            "grant_types": ["authorization_code"],
            "response_types": ["code"],
            "client_name": "Hydra Client"
        }
        
        sa = ServiceAccount.from_hydra_client(hydra_data, "admin@example.com")
        
        assert sa.client_id == "hydra-client"
        assert sa.client_secret == "hydra-secret"
        assert sa.grant_types == ["authorization_code"]
        assert sa.response_types == ["code"]
        assert sa.created_by == "admin@example.com"

    def test_from_hydra_client_with_defaults(self):
        """Test creating service account from minimal Hydra client data."""
        hydra_data = {
            "client_id": "minimal-client"
        }
        
        sa = ServiceAccount.from_hydra_client(hydra_data, "admin@example.com")
        
        assert sa.client_id == "minimal-client"
        assert sa.grant_types == ["client_credentials"]  # Default
        assert sa.response_types == []  # Default
