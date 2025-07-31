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
    
    connection.execute(sa.text("""
        INSERT INTO scopes (id, name, description, applies_to, is_active, created_at, updated_at)
        VALUES (gen_random_uuid(), 'profile', 'Permits consent retrieval of the users profile from an OpenID server', 'Service-to-service,Browser', true, LOCALTIMESTAMP, LOCALTIMESTAMP)
        ON CONFLICT (name) DO NOTHING;
    """))

    connection.execute(sa.text("""
        INSERT INTO scopes (id, name, description, applies_to, is_active, created_at, updated_at)
        VALUES (gen_random_uuid(), 'email', 'Permits consent retrieval of the users email address from an OpenID server', 'Service-to-service,Browser', true, LOCALTIMESTAMP, LOCALTIMESTAMP)
        ON CONFLICT (name) DO NOTHING;
    """))

    connection.execute(sa.text("""
        INSERT INTO scopes (id, name, description, applies_to, is_active, created_at, updated_at)
        VALUES (gen_random_uuid(), 'address', 'Permits consent retrieval of the users address from an OpenID server', 'Service-to-service,Browser', true, LOCALTIMESTAMP, LOCALTIMESTAMP)
        ON CONFLICT (name) DO NOTHING;
    """))

    connection.execute(sa.text("""
        INSERT INTO scopes (id, name, description, applies_to, is_active, created_at, updated_at)
        VALUES (gen_random_uuid(), 'phone', 'Permits consent retrieval of the users phone number from an OpenID server', 'Service-to-service,Browser', true, LOCALTIMESTAMP, LOCALTIMESTAMP)
        ON CONFLICT (name) DO NOTHING;
    """))

    connection.execute(sa.text("""
        INSERT INTO scopes (id, name, description, applies_to, is_active, created_at, updated_at)
        VALUES (gen_random_uuid(), 'openid', 'Required scope in OpenID Connect (OIDC). It signals that an application is requesting authentication, not just authorization, and allows it to receive an ID token.', 'Service-to-service,Browser', true, LOCALTIMESTAMP, LOCALTIMESTAMP)
        ON CONFLICT (name) DO NOTHING;
    """))

    connection.execute(sa.text("""
        INSERT INTO scopes (id, name, description, applies_to, is_active, created_at, updated_at)
        VALUES (gen_random_uuid(), 'admin', 'Required scope to access OAuth2 admin functionality.', 'Service-to-service,Browser', true, LOCALTIMESTAMP, LOCALTIMESTAMP)
        ON CONFLICT (name) DO NOTHING;
    """))

    connection.execute(sa.text("""
        INSERT INTO public.service_accounts(
            id, client_id, client_secret, grant_types, response_types, token_endpoint_auth_method, audience, owner, client_metadata, token_endpoint_auth_signing_alg, client_name, redirect_uris, skip_consent, jwks, jwks_uri, id_token_signed_response_alg, account_type, is_active, description, last_used_at, created_by, created_at, updated_at)
            VALUES (
                gen_random_uuid(), -- id
                'auth-backend', -- client_id
                'auth-backend-secret-change-in-production', -- client_secret
                '["client_credentials","authorization_code"]', -- grant_types
                '["code"]', -- response_types
                'client_secret_basic', -- token_endpoint_auth_method
                '["auth-backend"]', -- audience
                'Ryan Wiles', -- owner
                null, -- client_metadata
                null, -- token_endpoint_auth_signing_alg
                'OAuth2 Authentication Backend', -- client_name
                '["http://localhost:8000/callback","http://localhost:8000/auth/callback"]', -- redirect_uris
                true, -- skip_consent
                null, -- jwks
                null, -- jwks_uri
                'RS256', -- id_token_signed_response_alg
                'Service-to-service', -- account_type
                true, -- is_active
                'Handles the Authorization Endpoints for Hydra and management of the User & Client Service Accounts', -- description
                null, -- last_used_at
                'system', -- created_by
                LOCALTIMESTAMP, -- created_at
                LOCALTIMESTAMP -- updated_at
            ) ON CONFLICT (client_id) DO NOTHING;
    """))

    connection.execute(sa.text("""
        INSERT INTO public.service_accounts(
            id, client_id, client_secret, grant_types, response_types, token_endpoint_auth_method, audience, owner, client_metadata, token_endpoint_auth_signing_alg, client_name, redirect_uris, skip_consent, jwks, jwks_uri, id_token_signed_response_alg, account_type, is_active, description, last_used_at, created_by, created_at, updated_at, post_logout_redirect_uris, allowed_cors_origins)
            VALUES (
                gen_random_uuid(), -- id
                'management-ui', -- client_id
                NULL, -- client_secret
                '["authorization_code", "refresh_token", "implicit"]', -- grant_types
                '["code", "id_token", "token"]', -- response_types
                'none', -- token_endpoint_auth_method
                '["management-ui", "auth-backend"]', -- audience
                'Ryan Wiles', -- owner
                '{"purpose": "User management interface", "environment": "development", "application_type": "web"}', -- client_metadata
                null, -- token_endpoint_auth_signing_alg
                'OAuth2 Management Interface', -- client_name
                '["http://localhost:3000/auth/callback", "http://localhost:3000/callback", "http://localhost:3000/"]', -- redirect_uris
                false, -- skip_consent
                null, -- jwks
                null, -- jwks_uri
                'RS256', -- id_token_signed_response_alg
                'Browser', -- account_type
                true, -- is_active
                'Management Interface for Users & Clients for OAuth2', -- description
                null, -- last_used_at
                'system', -- created_by
                LOCALTIMESTAMP, -- created_at
                LOCALTIMESTAMP, -- updated_at
                '["http://localhost:3000/","http://localhost:3000/login"]', -- post_logout_redirect_uris
                '["http://localhost:3000"]' -- allowed_cors_origins
            ) ON CONFLICT (client_id) DO NOTHING;
    """))

    connection.execute(sa.text("""
        INSERT INTO service_account_scopes(service_account_id, scope_id)
            SELECT sa.id, s.id FROM service_accounts sa, scopes s where sa.client_id='auth-backend' and s.name = 'openid'
            ON CONFLICT (service_account_id, scope_id) DO NOTHING;
    """))

    connection.execute(sa.text("""
        INSERT INTO service_account_scopes(service_account_id, scope_id)
            SELECT sa.id, s.id FROM service_accounts sa, scopes s where sa.client_id='auth-backend' and s.name = 'profile'
            ON CONFLICT (service_account_id, scope_id) DO NOTHING;
    """))

    connection.execute(sa.text("""
        INSERT INTO service_account_scopes(service_account_id, scope_id)
            SELECT sa.id, s.id FROM service_accounts sa, scopes s where sa.client_id='auth-backend' and s.name = 'email'
            ON CONFLICT (service_account_id, scope_id) DO NOTHING;
    """))

    connection.execute(sa.text("""
        INSERT INTO service_account_scopes(service_account_id, scope_id)
            SELECT sa.id, s.id FROM service_accounts sa, scopes s where sa.client_id='management-ui' and s.name = 'openid'
            ON CONFLICT (service_account_id, scope_id) DO NOTHING;
    """))

    connection.execute(sa.text("""
        INSERT INTO service_account_scopes(service_account_id, scope_id)
            SELECT sa.id, s.id FROM service_accounts sa, scopes s where sa.client_id='management-ui' and s.name = 'profile'
            ON CONFLICT (service_account_id, scope_id) DO NOTHING;
    """))

    connection.execute(sa.text("""
        INSERT INTO service_account_scopes(service_account_id, scope_id)
            SELECT sa.id, s.id FROM service_accounts sa, scopes s where sa.client_id='management-ui' and s.name = 'email'
            ON CONFLICT (service_account_id, scope_id) DO NOTHING;
    """))

    connection.execute(sa.text("""
        INSERT INTO service_account_scopes(service_account_id, scope_id)
            SELECT sa.id, s.id FROM service_accounts sa, scopes s where sa.client_id='management-ui' and s.name = 'admin'
            ON CONFLICT (service_account_id, scope_id) DO NOTHING;
    """))
def downgrade():
    """
    Add back the scope column and restore scope data from relationships.
    """
