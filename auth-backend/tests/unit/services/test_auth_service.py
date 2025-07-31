"""
Unit tests for AuthService.

Tests password hashing and verification functionality using Argon2.
Validates security and correctness of authentication operations.
"""
import pytest
from argon2.exceptions import VerifyMismatchError

from src.services.auth_service import AuthService


class TestAuthService:
    """Test suite for AuthService password operations."""

    @pytest.fixture
    def auth_service(self):
        """Create an AuthService instance for testing."""
        return AuthService()

    def test_hash_password_creates_hash(self, auth_service):
        """Test that hash_password creates a valid Argon2 hash."""
        password = "test_password_123"
        
        password_hash = auth_service.hash_password(password)
        
        assert password_hash is not None
        assert isinstance(password_hash, str)
        assert password_hash != password  # Hash should be different from password
        assert password_hash.startswith("$argon2")  # Argon2 hash format

    def test_hash_password_different_passwords_different_hashes(self, auth_service):
        """Test that different passwords produce different hashes."""
        password1 = "test_password_123"
        password2 = "test_password_456"
        
        hash1 = auth_service.hash_password(password1)
        hash2 = auth_service.hash_password(password2)
        
        assert hash1 != hash2

    def test_hash_password_same_password_different_hashes(self, auth_service):
        """Test that same password produces different hashes due to salt."""
        password = "test_password_123"
        
        hash1 = auth_service.hash_password(password)
        hash2 = auth_service.hash_password(password)
        
        # Due to salting, same password should produce different hashes
        assert hash1 != hash2

    def test_hash_password_empty_password_raises_error(self, auth_service):
        """Test that hash_password raises error for empty password."""
        with pytest.raises(ValueError, match="Password cannot be empty"):
            auth_service.hash_password("")

    def test_hash_password_none_password_raises_error(self, auth_service):
        """Test that hash_password raises error for None password."""
        with pytest.raises(ValueError, match="Password cannot be empty"):
            auth_service.hash_password(None)

    def test_verify_password_correct_password_returns_true(self, auth_service):
        """Test that verify_password returns True for correct password."""
        password = "test_password_123"
        password_hash = auth_service.hash_password(password)
        
        result = auth_service.verify_password(password, password_hash)
        
        assert result is True

    def test_verify_password_incorrect_password_returns_false(self, auth_service):
        """Test that verify_password returns False for incorrect password."""
        password = "test_password_123"
        wrong_password = "wrong_password_456"
        password_hash = auth_service.hash_password(password)
        
        result = auth_service.verify_password(wrong_password, password_hash)
        
        assert result is False

    def test_verify_password_empty_password_returns_false(self, auth_service):
        """Test that verify_password returns False for empty password."""
        password = "test_password_123"
        password_hash = auth_service.hash_password(password)
        
        result = auth_service.verify_password("", password_hash)
        
        assert result is False

    def test_verify_password_empty_hash_returns_false(self, auth_service):
        """Test that verify_password returns False for empty hash."""
        password = "test_password_123"
        
        result = auth_service.verify_password(password, "")
        
        assert result is False

    def test_verify_password_invalid_hash_returns_false(self, auth_service):
        """Test that verify_password returns False for invalid hash format."""
        password = "test_password_123"
        invalid_hash = "not_a_valid_hash"
        
        result = auth_service.verify_password(password, invalid_hash)
        
        assert result is False

    def test_verify_password_none_values_returns_false(self, auth_service):
        """Test that verify_password handles None values gracefully."""
        password = "test_password_123"
        password_hash = auth_service.hash_password(password)
        
        # Test None password
        result = auth_service.verify_password(None, password_hash)
        assert result is False
        
        # Test None hash
        result = auth_service.verify_password(password, None)
        assert result is False
        
        # Test both None
        result = auth_service.verify_password(None, None)
        assert result is False

    def test_hash_and_verify_round_trip(self, auth_service):
        """Test complete hash and verify round trip."""
        test_passwords = [
            "simple",
            "complex_P@ssw0rd!",
            "unicode_测试密码",
            "numbers_123456789",
            "symbols_!@#$%^&*()",
            " spaces around ",
        ]
        
        for password in test_passwords:
            # Hash the password
            password_hash = auth_service.hash_password(password)
            
            # Verify it works
            assert auth_service.verify_password(password, password_hash) is True
            
            # Verify wrong password fails
            assert auth_service.verify_password(password + "wrong", password_hash) is False

    def test_hash_password_consistent_format(self, auth_service):
        """Test that all generated hashes follow Argon2 format."""
        passwords = ["test1", "test2", "test3"]
        
        for password in passwords:
            password_hash = auth_service.hash_password(password)
            
            # All Argon2 hashes should start with $argon2
            assert password_hash.startswith("$argon2")
            
            # Should contain the expected number of $ separators
            parts = password_hash.split("$")
            assert len(parts) >= 5  # At least 5 parts in Argon2 hash

    def test_verify_password_case_sensitive(self, auth_service):
        """Test that password verification is case sensitive."""
        password = "TestPassword123"
        password_hash = auth_service.hash_password(password)
        
        # Correct case should work
        assert auth_service.verify_password(password, password_hash) is True
        
        # Different case should fail
        assert auth_service.verify_password(password.lower(), password_hash) is False
        assert auth_service.verify_password(password.upper(), password_hash) is False
