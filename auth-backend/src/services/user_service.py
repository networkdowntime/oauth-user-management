"""User service for business logic related to user management."""

import secrets
import string
from datetime import datetime
from typing import List, Optional
from argon2 import PasswordHasher

from ..models.user import User
from ..models.role import Role
from ..repositories.user import UserRepository
from ..repositories.role import RoleRepository
from ..repositories.audit_log import AuditLogRepository
from ..schemas.user import UserResponse, UserCreate, UserUpdate, UserPasswordReset
from ..core.logging_config import get_logger

logger = get_logger(__name__)
ph = PasswordHasher()


class UserService:
    """Service for user-related business logic."""
    
    def __init__(
        self, 
        user_repo: UserRepository,
        role_repo: RoleRepository,
        audit_repo: AuditLogRepository
    ):
        self.user_repo = user_repo
        self.role_repo = role_repo
        self.audit_repo = audit_repo
    
    async def get_users(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        """Get all users."""
        users = await self.user_repo.get_all_with_roles(skip, limit)
        return [self._user_to_response(user) for user in users]
    
    async def create_user(self, user_data: UserCreate, performed_by: str) -> UserResponse:
        """Create a new user."""
        logger.info(f"Creating user: {user_data.email}")
        
        # Check if user already exists
        existing_user = await self.user_repo.get_by_email(user_data.email)
        if existing_user:
            raise ValueError(f"User with email {user_data.email} already exists")
        
        # Hash the password
        hashed_password = ph.hash(user_data.password)
        
        # Create user data dict
        user_dict = {
            "email": user_data.email,
            "display_name": user_data.display_name,
            "password_hash": hashed_password,
            "is_active": user_data.is_active,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        
        # Create user
        user = await self.user_repo.create(user_dict)
        
        # Log the action - temporarily disabled
        # await self.audit_repo.create_with_serialization(
        #     action="user_created",
        #     resource_type="user",
        #     resource_id=str(user.id),
        #     details={"email": user_data.email},
        #     performed_by=performed_by
        # )
        
        logger.info(f"User created: {user.email}")
        
        # Return response with roles loaded
        user_with_roles = await self.user_repo.get_by_id_with_roles(str(user.id))
        return self._user_to_response(user_with_roles)
    
    async def update_user(
        self, 
        user_id: str, 
        user_data: UserUpdate, 
        performed_by: str
    ) -> Optional[UserResponse]:
        """Update an existing user."""
        user = await self.user_repo.get_by_id_with_roles(user_id)
        if not user:
            return None
        
        # Prepare update data
        update_dict = {}
        if user_data.email is not None:
            update_dict["email"] = user_data.email
        if user_data.display_name is not None:
            update_dict["display_name"] = user_data.display_name
        if user_data.is_active is not None:
            update_dict["is_active"] = user_data.is_active
        if user_data.locked_until is not None:
            update_dict["locked_until"] = user_data.locked_until
        if user_data.password is not None:
            # Hash the new password
            update_dict["password_hash"] = ph.hash(user_data.password)
        
        update_dict["updated_at"] = datetime.utcnow()
        
        # Update user
        updated_user = await self.user_repo.update(user, update_dict)
        
        # Handle role assignments
        if user_data.role_ids is not None:
            await self._update_user_roles(user_id, user_data.role_ids, performed_by)
        
        # Log the action
        await self._log_action(
            action="user_updated",
            resource_type="user",
            resource_id=user_id,
            details={
                "email": user_data.email,
                "display_name": user_data.display_name,
                "is_active": user_data.is_active,
            },
            performed_by=performed_by
        )
        
        logger.info(f"User updated: {updated_user.email} by {performed_by}")
        
        # Return updated user with roles
        user_with_roles = await self.user_repo.get_by_id_with_roles(user_id)
        return self._user_to_response(user_with_roles)
    
    async def get_user_by_id(self, user_id: str) -> Optional[UserResponse]:
        """Get user by ID."""
        user = await self.user_repo.get_by_id_with_roles(user_id)
        if user:
            return self._user_to_response(user)
        return None
    
    async def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        """Get user by email."""
        user = await self.user_repo.get_by_email_with_roles(email)
        if user:
            return self._user_to_response(user)
        return None
    
    async def delete_user(self, user_id: str, performed_by: str) -> bool:
        """Delete a user and cascade delete all associated roles."""
        user = await self.user_repo.get_by_id_with_roles(user_id)
        if not user:
            return False
        
        # Log the action before deletion
        await self._log_action(
            action="user_deleted",
            resource_type="user",
            resource_id=user_id,
            details={"email": user.email},
            performed_by=performed_by
        )
        
        # Use the cascade delete method to remove user and all role relationships
        success = await self.user_repo.delete_user_with_roles(user_id)
        
        if success:
            logger.info(f"User deleted: {user.email} by {performed_by}")
        
        return success
    
    async def reset_user_password(
        self, 
        user_id: str, 
        password_data: UserPasswordReset,
        performed_by: str
    ) -> bool:
        """Reset user password."""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            return False
        
        # Create password hasher and hash new password
        password_hash = ph.hash(password_data.new_password)
        
        # Update password
        success = await self.user_repo.update_password(user_id, password_hash)
        
        if success:
            # Log the action
            await self._log_action(
                action="password_reset",
                resource_type="user",
                resource_id=user_id,
                details={"email": user.email},
                performed_by=performed_by
            )
            
            logger.info(f"Password reset for user: {user.email} by {performed_by}")
        
        return success
    
    async def assign_role_to_user(
        self, 
        user_id: str, 
        role_id: str,
        performed_by: str
    ) -> bool:
        """Assign a role to a user."""
        success = await self.user_repo.assign_role(user_id, role_id)
        
        if success:
            user = await self.user_repo.get_by_id(user_id)
            role = await self.role_repo.get_by_id(role_id)
            
            # Log the action
            await self._log_action(
                action="role_assigned",
                resource_type="user",
                resource_id=user_id,
                details={
                    "role_id": role_id,
                    "role_name": role.name if role else "unknown",
                    "user_email": user.email if user else "unknown"
                },
                performed_by=performed_by
            )
            
            logger.info(f"Role {role.name if role else role_id} assigned to user {user.email if user else user_id} by {performed_by}")
        
        return success
    
    async def remove_role_from_user(
        self, 
        user_id: str, 
        role_id: str,
        performed_by: str
    ) -> bool:
        """Remove a role from a user."""
        user = await self.user_repo.get_by_id(user_id)
        role = await self.role_repo.get_by_id(role_id)
        
        success = await self.user_repo.remove_role(user_id, role_id)
        
        if success:
            # Log the action
            await self._log_action(
                action="role_removed",
                resource_type="user",
                resource_id=user_id,
                details={
                    "role_id": role_id,
                    "role_name": role.name if role else "unknown",
                    "user_email": user.email if user else "unknown"
                },
                performed_by=performed_by
            )
            
            logger.info(f"Role {role.name if role else role_id} removed from user {user.email if user else user_id} by {performed_by}")
        
        return success
    
    def _user_to_response(self, user: User) -> UserResponse:
        """Convert User model to UserResponse schema."""
        return UserResponse(
            id=str(user.id),
            email=user.email,
            display_name=user.display_name,
            is_active=user.is_active,
            last_login_at=user.last_login_at,
            failed_login_attempts=user.failed_login_attempts,
            locked_until=user.locked_until,
            social_provider=user.social_provider,
            created_at=user.created_at,
            updated_at=user.updated_at,
            roles=[
                {
                    "id": str(role.id),
                    "name": role.name,
                    "description": role.description
                }
                for role in user.roles
            ]
        )
    
    def _generate_service_password(self) -> str:
        """Generate a secure random password for service accounts."""
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(secrets.choice(alphabet) for _ in range(24))
    
    async def _update_user_roles(self, user_id: str, role_ids: List[str], performed_by: str):
        """Update user role assignments."""
        # Get current roles
        user = await self.user_repo.get_by_id_with_roles(user_id)
        if not user:
            return  # User not found, nothing to update
            
        current_role_ids = {str(role.id) for role in user.roles}
        new_role_ids = set(role_ids)
        
        # Remove roles that are no longer assigned
        for role_id in current_role_ids - new_role_ids:
            await self.remove_role_from_user(user_id, role_id, performed_by)
        
        # Add new roles
        for role_id in new_role_ids - current_role_ids:
            await self.assign_role_to_user(user_id, role_id, performed_by)
    
    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate a user by email and password."""
        try:
            user = await self.user_repo.get_by_email(email)
            if not user:
                return None
            
            # Verify password using Argon2
            try:
                ph.verify(user.password_hash, password)
                
                # Successful login: update last_login_at and reset failed attempts
                await self.user_repo.update(user, {
                    "last_login_at": datetime.now(),
                    "failed_login_attempts": 0
                })
                
                logger.info(f"User authenticated successfully: {email}")
                return user
            except Exception:
                # Password verification failed: increment failed login attempts
                current_attempts = getattr(user, 'failed_login_attempts', 0) or 0
                await self.user_repo.update(user, {
                    "failed_login_attempts": current_attempts + 1
                })
                
                logger.warning(f"Password verification failed for user: {email}, failed attempts: {current_attempts + 1}")
                return None
                
        except Exception as e:
            logger.error(f"Error authenticating user {email}: {str(e)}")
            return None
    
    async def _log_action(
        self,
        action: str,
        resource_type: str,
        resource_id: str,
        details: dict,
        performed_by: str
    ):
        """Log an action to the audit trail."""
        try:
            await self.audit_repo.create_with_serialization(
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                details=details,
                performed_by=performed_by
            )
        except Exception as e:
            # Don't let audit failures break the main operation
            logger.warning(f"Failed to log audit action: {e}")
