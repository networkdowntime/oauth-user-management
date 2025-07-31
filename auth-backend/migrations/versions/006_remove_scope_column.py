"""Remove scope column from service_accounts table

Revision ID: 006
Revises: 005
Create Date: 2025-07-30 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '006'
down_revision = '005'
branch_labels = None
depends_on = None


def upgrade():
    """
    Migrate existing scope data to scope relationships and drop the scope column.
    """
    # Create a connection to execute raw SQL
    connection = op.get_bind()
    
    # First, migrate existing scope data to the relationship table
    # This query will:
    # 1. Split the space-separated scope string
    # 2. Match scope names to scope IDs
    # 3. Insert records into service_account_scopes table
    connection.execute(sa.text("""
        INSERT INTO service_account_scopes (service_account_id, scope_id)
        SELECT DISTINCT 
            sa.id as service_account_id,
            s.id as scope_id
        FROM service_accounts sa
        CROSS JOIN LATERAL unnest(string_to_array(sa.scope, ' ')) AS scope_name
        JOIN scopes s ON s.name = scope_name
        WHERE sa.scope IS NOT NULL 
        AND sa.scope != ''
        AND scope_name != ''
        ON CONFLICT (service_account_id, scope_id) DO NOTHING;
    """))
    
    # Now drop the scope column
    op.drop_column('service_accounts', 'scope')


def downgrade():
    """
    Add back the scope column and restore scope data from relationships.
    """
    # Add the scope column back
    op.add_column('service_accounts', 
                  sa.Column('scope', sa.String(1000), nullable=False, default=""))
    
    # Create a connection to execute raw SQL
    connection = op.get_bind()
    
    # Restore scope data from relationships
    # This query will:
    # 1. Get all scopes for each service account from the relationship table
    # 2. Join scope names with spaces
    # 3. Update the scope column
    connection.execute(sa.text("""
        UPDATE service_accounts 
        SET scope = COALESCE(scope_names.scope_list, '')
        FROM (
            SELECT 
                sa.id,
                string_agg(s.name, ' ' ORDER BY s.name) as scope_list
            FROM service_accounts sa
            LEFT JOIN service_account_scopes sas ON sa.id = sas.service_account_id
            LEFT JOIN scopes s ON sas.scope_id = s.id
            GROUP BY sa.id
        ) AS scope_names
        WHERE service_accounts.id = scope_names.id;
    """))
