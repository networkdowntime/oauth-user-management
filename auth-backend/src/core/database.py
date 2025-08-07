"""
Database configuration and connection management.

This module handles SQLAlchemy setup, database connections,
and provides utilities for database operations.
"""

import uuid
from datetime import datetime
from typing import AsyncGenerator

from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from .config import settings


class Base(DeclarativeBase):
    """Base class for all database models."""

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)


# Create async engine
async_engine = create_async_engine(
    settings.database_url.replace("postgresql://", "postgresql+asyncpg://"),
    echo=settings.environment == "development",
    pool_pre_ping=True,
    pool_recycle=300,
)

# Create async session maker
AsyncSessionLocal = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get database session.

    Yields:
        AsyncSession: Database session
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def create_tables() -> None:
    """Create all database tables."""
    # Import all models to ensure they're registered with SQLAlchemy
    # These imports are necessary for metadata registration, even if they appear unused
    from ..models import (  # noqa: F401
        AuditLog,
        Role,
        Scope,
        ServiceAccount,
        User,
        service_account_roles,
        service_account_scopes,
        user_roles,
    )

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def initialize_default_data() -> None:
    """Initialize default data including admin user and user_admin role."""
    from sqlalchemy import select

    from ..models.audit_log import AuditLog
    from ..models.role import Role
    from ..models.user import User
    from ..services.auth_service import AuthService

    async with AsyncSessionLocal() as session:
        try:
            # Check if user_admin role exists
            role_result = await session.execute(select(Role).where(Role.name == "user_admin"))
            admin_role = role_result.scalar_one_or_none()

            if not admin_role:
                # Create user_admin role
                admin_role = Role(name="user_admin", description="Administrator role with full system access")
                session.add(admin_role)
                await session.flush()  # Get the ID

                # Log role creation
                audit_log = AuditLog(
                    action="role_created",
                    resource_type="role",
                    resource_id=str(admin_role.id),
                    details={"role_name": "user_admin"},
                    performed_by="system",
                    timestamp=datetime.now(),
                )
                session.add(audit_log)

            # Check if default admin user exists
            user_result = await session.execute(select(User).where(User.email == settings.default_admin_email))
            admin_user = user_result.scalar_one_or_none()

            if not admin_user:
                # Create default admin user
                auth_service = AuthService()
                hashed_password = auth_service.hash_password(settings.default_admin_password)

                admin_user = User(
                    email=settings.default_admin_email,
                    password_hash=hashed_password,
                    is_active=True,
                    display_name="Default Administrator",
                )
                session.add(admin_user)
                await session.flush()  # Get the ID

                # Assign user_admin role to admin user using raw SQL to avoid async issues
                if admin_role:
                    from sqlalchemy import text

                    await session.execute(
                        text("INSERT INTO user_roles (user_id, role_id) VALUES (:user_id, :role_id)"),
                        {"user_id": admin_user.id, "role_id": admin_role.id},
                    )

                # Log user creation
                audit_log = AuditLog(
                    action="user_created",
                    resource_type="user",
                    resource_id=str(admin_user.id),
                    details={"email": settings.default_admin_email, "created_by": "system"},
                    performed_by="system",
                    timestamp=datetime.now(),
                )
                session.add(audit_log)

            await session.commit()

        except Exception as e:
            await session.rollback()
            raise e
