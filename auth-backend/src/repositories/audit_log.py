"""Audit log repository for database operations."""

from typing import List, Optional

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.audit_log import AuditLog
from .base import BaseRepository


class AuditLogRepository(BaseRepository[AuditLog]):
    """Repository for audit log-related database operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(AuditLog, db)

    async def get_by_resource(
        self,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        limit: int = 100,
    ) -> List[AuditLog]:
        """Get audit logs filtered by resource type and/or ID."""
        query = select(AuditLog)

        filters = []
        if resource_type:
            filters.append(AuditLog.resource_type == resource_type)
        if resource_id:
            filters.append(AuditLog.resource_id == resource_id)

        if filters:
            query = query.where(and_(*filters))

        query = query.order_by(AuditLog.timestamp.desc()).limit(limit)

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_user_logs(self, user_id: str, limit: int = 10) -> List[AuditLog]:
        """Get the last N audit logs for a specific user."""
        result = await self.db.execute(
            select(AuditLog)
            .where(and_(AuditLog.resource_type == "user", AuditLog.resource_id == user_id))
            .order_by(AuditLog.timestamp.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def create_with_serialization(
        self,
        action: str,
        resource_type: str,
        resource_id: str,
        details: dict,
        performed_by: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> AuditLog:
        """Create an audit log entry with proper JSON serialization."""
        import json
        from datetime import datetime
        from enum import Enum

        def clean_for_json(obj):
            """Convert all non-JSON-serializable objects to strings."""
            if isinstance(obj, dict):
                return {key: clean_for_json(value) for key, value in obj.items()}
            elif isinstance(obj, list):
                return [clean_for_json(item) for item in obj]
            elif isinstance(obj, Enum):
                return obj.value
            elif isinstance(obj, datetime):
                return obj.isoformat()
            elif hasattr(obj, "__dict__"):
                # Handle objects with attributes
                return str(obj)
            else:
                return obj

        # Clean all objects to ensure JSON serializability
        cleaned_details = clean_for_json(details) if details else {}

        # Now this should work without issues
        details_json = json.dumps(cleaned_details) if cleaned_details else None

        # Use raw SQL with explicit JSON casting to avoid SQLAlchemy serialization issues
        import uuid

        from sqlalchemy import text

        now = datetime.now()
        audit_id = uuid.uuid4()

        await self.db.execute(
            text(
                """
                INSERT INTO audit_logs (
                    id, action, resource_type, resource_id, details,
                    performed_by, ip_address, user_agent, timestamp,
                    created_at, updated_at
                ) VALUES (
                    :id, :action, :resource_type, :resource_id, :details,
                    :performed_by, :ip_address, :user_agent, :timestamp,
                    :created_at, :updated_at
                )
            """
            ),
            {
                "id": audit_id,
                "action": action,
                "resource_type": resource_type,
                "resource_id": resource_id,
                "details": details_json,
                "performed_by": performed_by,
                "ip_address": ip_address,
                "user_agent": user_agent,
                "timestamp": now,
                "created_at": now,
                "updated_at": now,
            },
        )

        await self.db.commit()

        # Return a simple audit log-like object
        return type(
            "AuditLog",
            (),
            {
                "id": audit_id,
                "action": action,
                "resource_type": resource_type,
                "resource_id": resource_id,
                "details": cleaned_details,
                "performed_by": performed_by,
                "ip_address": ip_address,
                "user_agent": user_agent,
                "timestamp": now,
                "created_at": now,
                "updated_at": now,
            },
        )()
