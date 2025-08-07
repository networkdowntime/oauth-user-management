"""User repository for database operations."""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models.role import Role
from ..models.user import User
from .base import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for user-related database operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(User, db)

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email address."""
        result = await self.db.execute(select(User).options(selectinload(User.roles)).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_id_with_roles(self, user_id: str) -> Optional[User]:
        """Get user by ID with roles preloaded."""
        result = await self.db.execute(select(User).options(selectinload(User.roles)).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_all_with_roles(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with roles preloaded."""
        result = await self.db.execute(
            select(User).options(selectinload(User.roles)).offset(skip).limit(limit).order_by(User.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_users_by_role(self, role_id: str) -> List[User]:
        """Get all users with a specific role."""
        result = await self.db.execute(
            select(User)
            .options(selectinload(User.roles))
            .join(User.roles)
            .where(Role.id == role_id)
            .order_by(User.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_users_without_role(self, role_id: str) -> List[User]:
        """Get all users who don't have a specific role."""
        # Get all users
        all_users_result = await self.db.execute(
            select(User).options(selectinload(User.roles)).order_by(User.created_at.desc())
        )
        all_users = list(all_users_result.scalars().all())

        # Filter out users who have the role
        users_without_role = [user for user in all_users if not any(role.id == role_id for role in user.roles)]

        return users_without_role

    async def assign_role(self, user_id: str, role_id: str) -> bool:
        """Assign a role to a user."""
        user = await self.get_by_id_with_roles(user_id)
        if not user:
            return False

        role_result = await self.db.execute(select(Role).where(Role.id == role_id))
        role = role_result.scalar_one_or_none()
        if not role:
            return False

        # Check if user already has this role
        if any(str(r.id) == role_id for r in user.roles):
            return True  # Already has role

        user.roles.append(role)
        await self.db.commit()
        return True

    async def remove_role(self, user_id: str, role_id: str) -> bool:
        """Remove a role from a user."""
        user = await self.get_by_id_with_roles(user_id)
        if not user:
            return False

        # Find and remove the role
        for i, role in enumerate(user.roles):
            if str(role.id) == role_id:
                user.roles.pop(i)
                await self.db.commit()
                return True

        return False  # Role not found

    async def update_password(self, user_id: str, password_hash: str) -> bool:
        """Update user's password hash."""
        user = await self.get_by_id(user_id)
        if not user:
            return False

        user.password_hash = password_hash
        await self.db.commit()
        return True

    async def delete_user_with_roles(self, user_id: str) -> bool:
        """Delete a user and cascade delete all associated user-role relationships."""
        # First get the user with roles to verify it exists
        user = await self.get_by_id_with_roles(user_id)
        if not user:
            return False

        # Clear all role relationships first
        user.roles.clear()

        # Now delete the user
        await self.db.delete(user)
        await self.db.commit()
        return True
