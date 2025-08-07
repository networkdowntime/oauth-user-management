"""Role service for business logic."""

from datetime import datetime
from typing import List, Optional

from ..core.logging_config import get_logger
from ..models.role import Role
from ..models.service_account import ServiceAccount
from ..models.user import User
from ..repositories.audit_log import AuditLogRepository
from ..repositories.role import RoleRepository
from ..repositories.service_account import ServiceAccountRepository
from ..repositories.user import UserRepository
from ..schemas.role import RoleCreate, RoleResponse, RoleUpdate
from ..schemas.service_account import ServiceAccountResponse
from ..schemas.user import UserResponse

logger = get_logger(__name__)


class RoleService:
    """Service for role-related business logic."""

    def __init__(
        self,
        role_repo: RoleRepository,
        user_repo: UserRepository,
        service_account_repo: ServiceAccountRepository,
        audit_repo: AuditLogRepository,
    ):
        self.role_repo = role_repo
        self.user_repo = user_repo
        self.service_account_repo = service_account_repo
        self.audit_repo = audit_repo

    async def get_all_roles(self, skip: int = 0, limit: int = 100) -> List[RoleResponse]:
        """Get all roles."""
        roles = await self.role_repo.get_all_with_users(skip, limit)
        return [self._role_to_response(role) for role in roles]

    async def get_role_by_id(self, role_id: str) -> Optional[RoleResponse]:
        """Get role by ID."""
        role = await self.role_repo.get_by_id_with_users(role_id)
        return self._role_to_response(role) if role else None

    async def create_role(self, role_data: RoleCreate, performed_by: str) -> RoleResponse:
        """Create a new role."""
        # Check if role already exists
        existing_role = await self.role_repo.get_by_name(role_data.name)
        if existing_role:
            raise ValueError(f"Role with name {role_data.name} already exists")

        # Create role data dict
        role_dict = {
            "name": role_data.name,
            "description": role_data.description,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }

        # Create role
        role = await self.role_repo.create(role_dict)

        # Log the action
        await self._log_action(
            action="role_created",
            resource_type="role",
            resource_id=str(role.id),
            details={"name": role_data.name, "description": role_data.description},
            performed_by=performed_by,
        )

        logger.info(f"Role created: {role.name} by {performed_by}")

        return self._role_to_response(role)

    async def update_role(self, role_id: str, role_data: RoleUpdate, performed_by: str) -> Optional[RoleResponse]:
        """Update an existing role."""
        role = await self.role_repo.get_by_id_with_users(role_id)
        if not role:
            return None

        # Prepare update data
        update_dict = {}
        if role_data.name is not None:
            # Check if name already exists (if changing)
            if role_data.name != role.name:
                existing_role = await self.role_repo.get_by_name(role_data.name)
                if existing_role:
                    raise ValueError(f"Role with name {role_data.name} already exists")
            update_dict["name"] = role_data.name
        if role_data.description is not None:
            update_dict["description"] = role_data.description

        update_dict["updated_at"] = datetime.utcnow()

        # Update role
        updated_role = await self.role_repo.update(role, update_dict)

        # Log the action
        await self._log_action(
            action="role_updated",
            resource_type="role",
            resource_id=role_id,
            details=update_dict,
            performed_by=performed_by,
        )

        logger.info(f"Role updated: {updated_role.name} by {performed_by}")

        return self._role_to_response(updated_role)

    async def delete_role(self, role_id: str, performed_by: str) -> bool:
        """Delete a role."""
        role = await self.role_repo.get_by_id(role_id)
        if not role:
            return False

        name = role.name
        success = await self.role_repo.delete(role_id)

        if success:
            # Log the action
            await self._log_action(
                action="role_deleted",
                resource_type="role",
                resource_id=role_id,
                details={"name": name},
                performed_by=performed_by,
            )

            logger.info(f"Role deleted: {name} by {performed_by}")

        return success

    async def get_users_by_role(self, role_id: str) -> List[UserResponse]:
        """Get all users with a specific role."""
        users = await self.user_repo.get_users_by_role(role_id)
        return [self._user_to_response(user) for user in users]

    async def get_users_without_role(self, role_id: str) -> List[UserResponse]:
        """Get all users who don't have a specific role."""
        users = await self.user_repo.get_users_without_role(role_id)
        return [self._user_to_response(user) for user in users]

    async def get_service_accounts_by_role(self, role_id: str) -> List[ServiceAccountResponse]:
        """Get all service accounts with a specific role."""
        service_accounts = await self.service_account_repo.get_service_accounts_by_role(role_id)
        return [self._service_account_to_response(service_account) for service_account in service_accounts]

    async def get_service_accounts_without_role(self, role_id: str) -> List[ServiceAccountResponse]:
        """Get all service accounts who don't have a specific role."""
        service_accounts = await self.service_account_repo.get_service_accounts_without_role(role_id)
        return [self._service_account_to_response(service_account) for service_account in service_accounts]

    async def assign_user_to_role(self, user_id: str, role_id: str, performed_by: str) -> bool:
        """Assign a user to a role."""
        success = await self.user_repo.assign_role(user_id, role_id)

        if success:
            user = await self.user_repo.get_by_id(user_id)
            role = await self.role_repo.get_by_id(role_id)

            # Log the action
            await self._log_action(
                action="role_assigned",
                resource_type="user",
                resource_id=user_id,
                details={
                    "role_id": role_id,
                    "role_name": role.name if role else "unknown",
                    "user_email": user.email if user else "unknown",
                },
                performed_by=performed_by,
            )

            logger.info(
                f"Role {role.name if role else role_id} assigned to user {user.email if user else user_id} by {performed_by}"
            )

        return success

    async def remove_user_from_role(self, user_id: str, role_id: str, performed_by: str) -> bool:
        """Remove a user from a role."""
        user = await self.user_repo.get_by_id(user_id)
        role = await self.role_repo.get_by_id(role_id)

        success = await self.user_repo.remove_role(user_id, role_id)

        if success:
            # Log the action
            await self._log_action(
                action="role_removed",
                resource_type="user",
                resource_id=user_id,
                details={
                    "role_id": role_id,
                    "role_name": role.name if role else "unknown",
                    "user_email": user.email if user else "unknown",
                },
                performed_by=performed_by,
            )

            logger.info(
                f"Role {role.name if role else role_id} removed from user {user.email if user else user_id} by {performed_by}"
            )

        return success

    async def assign_service_to_role(self, service_id: str, role_id: str, performed_by: str) -> bool:
        """Assign a service account to a role."""
        success = await self.service_account_repo.assign_role(service_id, role_id)

        if success:
            service_account = await self.service_account_repo.get_by_id(service_id)
            role = await self.role_repo.get_by_id(role_id)

            # Log the action
            await self._log_action(
                action="role_assigned",
                resource_type="service_account",
                resource_id=service_id,
                details={
                    "role_id": role_id,
                    "role_name": role.name if role else "unknown",
                    "service_account_name": (service_account.client_name if service_account else "unknown"),
                },
                performed_by=performed_by,
            )

            logger.info(
                f"Role {role.name if role else role_id} assigned to service account {service_account.client_name if service_account else service_id} by {performed_by}"
            )

        return success

    async def remove_service_from_role(self, service_id: str, role_id: str, performed_by: str) -> bool:
        """Remove a service account from a role."""
        service_account = await self.service_account_repo.get_by_id(service_id)
        role = await self.role_repo.get_by_id(role_id)

        success = await self.service_account_repo.remove_role(service_id, role_id)

        if success:
            # Log the action
            await self._log_action(
                action="role_removed",
                resource_type="service_account",
                resource_id=service_id,
                details={
                    "role_id": role_id,
                    "role_name": role.name if role else "unknown",
                    "service_account_name": (service_account.client_name if service_account else "unknown"),
                },
                performed_by=performed_by,
            )

            logger.info(
                f"Role {role.name if role else role_id} removed from service account {service_account.client_name if service_account else service_id} by {performed_by}"
            )

        return success

    def _role_to_response(self, role: Role) -> RoleResponse:
        """Convert Role model to RoleResponse schema."""
        return RoleResponse(
            id=str(role.id),
            name=role.name,
            description=role.description,
            created_at=role.created_at,
            updated_at=role.updated_at,
            user_count=role.user_count,
        )

    def _user_to_response(self, user: User) -> UserResponse:
        """Convert User model to UserResponse schema."""
        return UserResponse(
            id=str(user.id),
            email=user.email,
            display_name=user.display_name,
            is_active=user.is_active,
            last_login_at=user.last_login_at,
            failed_login_attempts=user.failed_login_attempts,
            locked_until=user.locked_until,
            social_provider=user.social_provider,
            created_at=user.created_at,
            updated_at=user.updated_at,
            roles=[{"id": str(role.id), "name": role.name, "description": role.description} for role in user.roles],
        )

    def _service_account_to_response(self, service_account: ServiceAccount) -> ServiceAccountResponse:
        """Convert ServiceAccount model to ServiceAccountResponse schema."""
        return ServiceAccountResponse(
            id=service_account.id,
            client_id=service_account.client_id,
            client_name=service_account.client_name,
            description=service_account.description,
            grant_types=service_account.grant_types or ["client_credentials"],
            scope=(" ".join(scope.name for scope in service_account.scopes) if service_account.scopes else ""),
            token_endpoint_auth_method=service_account.token_endpoint_auth_method or "client_secret_basic",
            audience=service_account.audience,
            owner=service_account.owner,
            client_metadata=service_account.client_metadata,
            redirect_uris=service_account.redirect_uris or [],
            skip_consent=service_account.skip_consent or True,
            is_active=service_account.is_active,
            client_secret=service_account.client_secret,
            response_types=service_account.response_types or [],
            last_used_at=service_account.last_used_at,
            created_by=service_account.created_by,
            created_at=service_account.created_at,
            updated_at=service_account.updated_at,
            roles=[
                {
                    "id": role.id,
                    "name": role.name,
                    "description": role.description,
                    "permissions": [],  # placeholder
                    "created_at": role.created_at,
                    "updated_at": role.updated_at,
                }
                for role in service_account.roles
            ],
        )

    async def _log_action(
        self,
        action: str,
        resource_type: str,
        resource_id: str,
        details: dict,
        performed_by: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ):
        """Log an audit action."""
        # Use the specialized method that handles JSON serialization
        await self.audit_repo.create_with_serialization(
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            performed_by=performed_by,
            ip_address=ip_address,
            user_agent=user_agent,
        )
