"""Role repository for database operations."""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models.role import Role
from .base import BaseRepository


class RoleRepository(BaseRepository[Role]):
    """Repository for role-related database operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(Role, db)

    async def get_by_name(self, name: str) -> Optional[Role]:
        """Get role by name."""
        result = await self.db.execute(select(Role).where(Role.name == name))
        return result.scalar_one_or_none()

    async def get_by_id_with_users(self, role_id: str) -> Optional[Role]:
        """Get role by ID with users preloaded."""
        result = await self.db.execute(select(Role).options(selectinload(Role.users)).where(Role.id == role_id))
        return result.scalar_one_or_none()

    async def get_all_with_users(self, skip: int = 0, limit: int = 100) -> List[Role]:
        """Get all roles with users preloaded."""
        result = await self.db.execute(
            select(Role).options(selectinload(Role.users)).offset(skip).limit(limit).order_by(Role.created_at.desc())
        )
        return list(result.scalars().all())
