"""Association table for service account roles."""

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID

from ..core.database import Base

# Association table for many-to-many relationship between service accounts and roles
service_account_roles = Table(
    "service_account_roles",
    Base.metadata,
    Column(
        "service_account_id",
        UUID(as_uuid=True),
        ForeignKey("service_accounts.id"),
        primary_key=True,
    ),
    Column("role_id", UUID(as_uuid=True), ForeignKey("roles.id"), primary_key=True),
)
