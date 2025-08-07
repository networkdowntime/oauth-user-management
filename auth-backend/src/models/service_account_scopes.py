"""Association table for service account scopes."""

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID

from ..core.database import Base

# Association table for many-to-many relationship between service accounts and scopes
service_account_scopes = Table(
    "service_account_scopes",
    Base.metadata,
    Column(
        "service_account_id",
        UUID(as_uuid=True),
        ForeignKey("service_accounts.id"),
        primary_key=True,
    ),
    Column("scope_id", UUID(as_uuid=True), ForeignKey("scopes.id"), primary_key=True),
)
