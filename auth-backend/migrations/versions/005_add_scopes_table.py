"""Add scopes table and service account scopes association

Revision ID: 005_add_scopes_table
Revises: 004_add_service_account_type
Create Date: 2025-01-29 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '005_add_scopes_table'
down_revision = '004_add_service_account_type'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add scopes table and service account scopes association table."""
    
    # Create scopes table
    op.create_table(
        'scopes',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, primary_key=True, default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.String(length=100), nullable=False, unique=True, index=True),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('applies_to', sa.String(length=20), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create service_account_scopes association table
    op.create_table(
        'service_account_scopes',
        sa.Column('service_account_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('scope_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(['service_account_id'], ['service_accounts.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['scope_id'], ['scopes.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('service_account_id', 'scope_id')
    )
    
    # Create indexes for better performance
    op.create_index('ix_scopes_name', 'scopes', ['name'])
    op.create_index('ix_scopes_is_active', 'scopes', ['is_active'])
    op.create_index('ix_scopes_applies_to', 'scopes', ['applies_to'])
    op.create_index('ix_service_account_scopes_service_account_id', 'service_account_scopes', ['service_account_id'])
    op.create_index('ix_service_account_scopes_scope_id', 'service_account_scopes', ['scope_id'])


def downgrade() -> None:
    """Remove scopes table and service account scopes association table."""
    
    # Drop indexes
    op.drop_index('ix_service_account_scopes_scope_id', table_name='service_account_scopes')
    op.drop_index('ix_service_account_scopes_service_account_id', table_name='service_account_scopes')
    op.drop_index('ix_scopes_applies_to', table_name='scopes')
    op.drop_index('ix_scopes_is_active', table_name='scopes')
    op.drop_index('ix_scopes_name', table_name='scopes')
    
    # Drop tables
    op.drop_table('service_account_scopes')
    op.drop_table('scopes')
