"""
Tests for the AuditLog model.

This module tests the AuditLog model functionality including properties,
methods, and class methods.
"""
import json
from datetime import datetime

from src.models.audit_log import AuditLog


class TestAuditLog:
    """Test cases for the AuditLog model."""

    def test_audit_log_creation(self):
        """Test creating a new audit log."""
        log = AuditLog(
            action="CREATE",
            resource_type="User",
            resource_id="123",
            details={"field": "value"},
            performed_by="admin@example.com",
            ip_address="192.168.1.1",
            user_agent="Test Agent"
        )
        
        assert log.action == "CREATE"
        assert log.resource_type == "User"
        assert log.resource_id == "123"
        assert log.details == {"field": "value"}
        assert log.performed_by == "admin@example.com"
        assert log.ip_address == "192.168.1.1"
        assert log.user_agent == "Test Agent"

    def test_audit_log_repr(self):
        """Test audit log string representation."""
        log = AuditLog(action="DELETE", resource_type="ServiceAccount")
        assert repr(log) == "<AuditLog(action='DELETE', resource_type='ServiceAccount')>"

    def test_details_str_property_with_details(self):
        """Test details_str property when details exist."""
        details = {"user_id": "123", "email": "test@example.com"}
        log = AuditLog(
            action="UPDATE",
            resource_type="User",
            details=details,
            performed_by="admin@example.com"
        )
        
        details_str = log.details_str
        assert details_str == json.dumps(details, indent=2)

    def test_details_str_property_no_details(self):
        """Test details_str property when no details exist."""
        log = AuditLog(
            action="UPDATE",
            resource_type="User",
            details=None,
            performed_by="admin@example.com"
        )
        
        assert log.details_str == ""

    def test_create_log_class_method_minimal(self):
        """Test create_log class method with minimal parameters."""
        log = AuditLog.create_log(
            action="VIEW",
            resource_type="Role",
            performed_by="user@example.com"
        )
        
        assert log.action == "VIEW"
        assert log.resource_type == "Role"
        assert log.performed_by == "user@example.com"
        assert log.resource_id is None
        assert log.details is None
        assert log.ip_address is None
        assert log.user_agent is None

    def test_create_log_class_method_full(self):
        """Test create_log class method with all parameters."""
        details = {"previous_value": "old", "new_value": "new"}
        log = AuditLog.create_log(
            action="UPDATE",
            resource_type="ServiceAccount",
            performed_by="admin@example.com",
            resource_id="sa-123",
            details=details,
            ip_address="10.0.0.1",
            user_agent="Mozilla/5.0"
        )
        
        assert log.action == "UPDATE"
        assert log.resource_type == "ServiceAccount"
        assert log.performed_by == "admin@example.com"
        assert log.resource_id == "sa-123"
        assert log.details == details
        assert log.ip_address == "10.0.0.1"
        assert log.user_agent == "Mozilla/5.0"
