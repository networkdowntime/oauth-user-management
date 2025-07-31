"""Add service accounts table

Revision ID: 003_add_service_accounts
Revises: 002_add_audit_logs
Create Date: 2025-07-28 20:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid

# revision identifiers, used by Alembic.
revision = '003_add_service_accounts'
down_revision = '002_add_audit_logs'
branch_labels = None
depends_on = None


def upgrade():
    """Add service accounts table and service_account_roles association table."""
    # Create service_accounts table
    op.create_table(
        'service_accounts',
        
        # Primary key
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        
        # OAuth2 Required Fields
        sa.Column('client_id', sa.String(255), nullable=False, unique=True),
        sa.Column('client_secret', sa.String(512), nullable=True),
        sa.Column('grant_types', sa.JSON(), nullable=False, default=['client_credentials']),
        sa.Column('response_types', sa.JSON(), nullable=False, default=[]),
        sa.Column('scope', sa.String(1000), nullable=False, default=''),
        sa.Column('token_endpoint_auth_method', sa.String(50), nullable=False, default='client_secret_basic'),
        
        # OAuth2 Optional Fields
        sa.Column('audience', sa.JSON(), nullable=True),
        sa.Column('owner', sa.String(255), nullable=True),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.Column('token_endpoint_auth_signing_alg', sa.String(50), nullable=True),
        sa.Column('client_name', sa.String(255), nullable=False),
        sa.Column('redirect_uris', sa.JSON(), nullable=True, default=[]),
        sa.Column('skip_consent', sa.Boolean(), nullable=False, default=True),
        sa.Column('jwks', sa.JSON(), nullable=True),
        sa.Column('jwks_uri', sa.String(500), nullable=True),
        sa.Column('id_token_signed_response_alg', sa.String(50), nullable=True, default='RS256'),
        
        # Management Fields
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('last_used_at', sa.DateTime(), nullable=True),
        sa.Column('created_by', sa.String(255), nullable=False),
        
        # Audit fields
        sa.Column('created_at', sa.DateTime(), nullable=False, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, default=sa.func.now(), onupdate=sa.func.now())
    )
    
    # Create indexes
    op.create_index('ix_service_accounts_id', 'service_accounts', ['id'])
    op.create_index('ix_service_accounts_client_id', 'service_accounts', ['client_id'])
    op.create_index('ix_service_accounts_is_active', 'service_accounts', ['is_active'])
    
    # Create service_account_roles association table
    op.create_table(
        'service_account_roles',
        sa.Column('service_account_id', UUID(as_uuid=True), nullable=False),
        sa.Column('role_id', UUID(as_uuid=True), nullable=False),
        sa.PrimaryKeyConstraint('service_account_id', 'role_id')
    )
    
    # Add foreign key constraints
    op.create_foreign_key(
        'fk_service_account_roles_service_account_id',
        'service_account_roles', 'service_accounts',
        ['service_account_id'], ['id'],
        ondelete='CASCADE'
    )
    
    op.create_foreign_key(
        'fk_service_account_roles_role_id',
        'service_account_roles', 'roles',
        ['role_id'], ['id'],
        ondelete='CASCADE'
    )


def downgrade():
    """Remove service accounts table and associations."""
    # Drop foreign keys first
    op.drop_constraint('fk_service_account_roles_role_id', 'service_account_roles', type_='foreignkey')
    op.drop_constraint('fk_service_account_roles_service_account_id', 'service_account_roles', type_='foreignkey')
    
    # Drop association table
    op.drop_table('service_account_roles')
    
    # Drop indexes
    op.drop_index('ix_service_accounts_is_active', 'service_accounts')
    op.drop_index('ix_service_accounts_client_id', 'service_accounts')
    op.drop_index('ix_service_accounts_id', 'service_accounts')
    
    # Drop main table
    op.drop_table('service_accounts')
