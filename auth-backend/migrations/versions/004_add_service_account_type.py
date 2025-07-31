"""Add account_type field to service_accounts

Revision ID: 004_add_service_account_type
Revises: 003_add_service_accounts
Create Date: 2025-07-29 22:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '004_add_service_account_type'
down_revision = '003_add_service_accounts'
branch_labels = None
depends_on = None


def upgrade():
    """Add account_type field to service_accounts table."""
    # Add the account_type column with default value
    op.add_column(
        'service_accounts',
        sa.Column(
            'account_type',
            sa.String(50),
            nullable=False,
            default='Service-to-service',
            server_default='Service-to-service'
        )
    )


def downgrade():
    """Remove account_type field from service_accounts table."""
    op.drop_column('service_accounts', 'account_type')
