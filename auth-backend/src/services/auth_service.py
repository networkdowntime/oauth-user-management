"""Authentication service for password hashing and verification."""

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError

from ..core.logging_config import get_logger

logger = get_logger(__name__)
ph = PasswordHasher()


class AuthService:
    """Service for authentication-related operations."""
    
    def hash_password(self, password: str) -> str:
        """Hash a password using Argon2."""
        if not password:
            raise ValueError("Password cannot be empty")
        return ph.hash(password)
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify a password against its hash."""
        if not password or not password_hash:
            return False
        
        try:
            ph.verify(password_hash, password)
            return True
        except (VerifyMismatchError, VerificationError, Exception):
            # Catch all Argon2 exceptions and any other errors
            return False
