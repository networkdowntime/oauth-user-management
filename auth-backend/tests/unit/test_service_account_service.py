"""
Unit tests for ServiceAccountService business logic.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
from src.services.service_account_service import ServiceAccountService
from src.core.exceptions import (
    ServiceAccountNotFoundError,
    ServiceAccountAlreadyExistsError,
    RoleNotFoundError,
    HydraIntegrationError
)

@pytest.fixture
def service_account_repo():
    repo = MagicMock()
    repo.get_by_client_id = AsyncMock()
    repo.create = AsyncMock()
    repo.get_by_id_with_roles = AsyncMock()
    repo.get_by_id = AsyncMock()
    repo.update = AsyncMock()
    repo.delete = AsyncMock()
    repo.search = AsyncMock()
    repo.assign_role = AsyncMock()
    repo.remove_role = AsyncMock()
    repo.activate = AsyncMock()
    repo.deactivate = AsyncMock()
    return repo

@pytest.fixture
def role_repo():
    repo = MagicMock()
    repo.get_by_id = AsyncMock()
    return repo

@pytest.fixture
def hydra_client():
    client = MagicMock()
    client.create_client = AsyncMock()
    client.update_client = AsyncMock()
    client.delete_client = AsyncMock()
    client.get_client = AsyncMock()
    return client

@pytest.fixture
def service(service_account_repo, role_repo, hydra_client):
    return ServiceAccountService(service_account_repo, role_repo, hydra_client)

def make_service_account(**kwargs):
    mock = MagicMock()
    mock.id = kwargs.get('id', uuid4())
    mock.client_id = kwargs.get('client_id', 'svc-123')
    mock.to_hydra_client = MagicMock(return_value={"client_id": mock.client_id})
    mock.roles = kwargs.get('roles', [])
    return mock

@pytest.mark.asyncio
async def test_create_service_account_success(service, service_account_repo, hydra_client):
    data = {"client_id": "svc-abc"}
    service_account_repo.get_by_client_id.return_value = None
    created = make_service_account(client_id="svc-abc")
    service_account_repo.create.return_value = created
    service_account_repo.get_by_id_with_roles.return_value = created
    hydra_client.create_client.return_value = None

    result = await service.create_service_account(data)
    assert result.client_id == "svc-abc"
    hydra_client.create_client.assert_called_once()

@pytest.mark.asyncio
async def test_create_service_account_already_exists(service, service_account_repo):
    data = {"client_id": "svc-dup"}
    service_account_repo.get_by_client_id.return_value = make_service_account(client_id="svc-dup")
    with pytest.raises(ServiceAccountAlreadyExistsError):
        await service.create_service_account(data)

@pytest.mark.asyncio
async def test_create_service_account_hydra_failure(service, service_account_repo, hydra_client):
    data = {"client_id": "svc-fail"}
    service_account_repo.get_by_client_id.return_value = None
    created = make_service_account(client_id="svc-fail")
    service_account_repo.create.return_value = created
    service_account_repo.get_by_id_with_roles.return_value = created
    hydra_client.create_client.side_effect = Exception("hydra error")
    service_account_repo.delete = AsyncMock()
    with pytest.raises(HydraIntegrationError):
        await service.create_service_account(data)
    service_account_repo.delete.assert_called_once()

@pytest.mark.asyncio
async def test_get_service_account_success(service, service_account_repo):
    acc = make_service_account()
    service_account_repo.get_by_id.return_value = acc
    result = await service.get_service_account(acc.id)
    assert result is acc

@pytest.mark.asyncio
async def test_get_service_account_not_found(service, service_account_repo):
    service_account_repo.get_by_id.return_value = None
    with pytest.raises(ServiceAccountNotFoundError):
        await service.get_service_account(uuid4())

@pytest.mark.asyncio
async def test_update_service_account_success(service, service_account_repo, hydra_client):
    acc = make_service_account()
    service_account_repo.get_by_id.return_value = acc
    updated = make_service_account(client_id=acc.client_id)
    service_account_repo.update.return_value = updated
    hydra_client.update_client.return_value = None
    result = await service.update_service_account(acc.id, {"foo": "bar"})
    assert result.client_id == acc.client_id
    hydra_client.update_client.assert_called_once()

@pytest.mark.asyncio
async def test_delete_service_account_success(service, service_account_repo, hydra_client):
    acc = make_service_account()
    service_account_repo.get_by_id.return_value = acc
    hydra_client.delete_client.return_value = None
    service_account_repo.delete.return_value = None
    await service.delete_service_account(acc.id)
    hydra_client.delete_client.assert_called_once()
    service_account_repo.delete.assert_called_once()

@pytest.mark.asyncio
async def test_assign_role_to_service_account_success(service, service_account_repo, role_repo):
    acc = make_service_account()
    role = MagicMock()
    service_account_repo.get_by_id.return_value = acc
    role_repo.get_by_id.return_value = role
    service_account_repo.assign_role.return_value = True
    service_account_repo.get_by_id.return_value = acc
    result = await service.assign_role_to_service_account(acc.id, uuid4())
    assert result is acc

@pytest.mark.asyncio
async def test_remove_role_from_service_account_success(service, service_account_repo):
    acc = make_service_account()
    service_account_repo.get_by_id.return_value = acc
    service_account_repo.remove_role.return_value = True
    service_account_repo.get_by_id.return_value = acc
    result = await service.remove_role_from_service_account(acc.id, uuid4())
    assert result is acc

@pytest.mark.asyncio
async def test_activate_service_account_success(service, service_account_repo):
    acc = make_service_account()
    service_account_repo.activate.return_value = True
    service_account_repo.get_by_id.return_value = acc
    result = await service.activate_service_account(acc.id)
    assert result is acc

@pytest.mark.asyncio
async def test_deactivate_service_account_success(service, service_account_repo):
    acc = make_service_account()
    service_account_repo.deactivate.return_value = True
    service_account_repo.get_by_id.return_value = acc
    result = await service.deactivate_service_account(acc.id)
    assert result is acc

@pytest.mark.asyncio
async def test_sync_with_hydra_success(service, service_account_repo, hydra_client):
    acc = make_service_account()
    service_account_repo.get_by_id.return_value = acc
    hydra_client.get_client.return_value = {"client_id": acc.client_id}
    hydra_client.update_client.return_value = None
    result = await service.sync_with_hydra(acc.id)
    assert result is acc
    hydra_client.update_client.assert_called_once()

@pytest.mark.asyncio
async def test_sync_with_hydra_create_if_missing(service, service_account_repo, hydra_client):
    acc = make_service_account()
    service_account_repo.get_by_id.return_value = acc
    hydra_client.get_client.return_value = None
    hydra_client.create_client.return_value = None
    result = await service.sync_with_hydra(acc.id)
    assert result is acc
    hydra_client.create_client.assert_called_once()

@pytest.mark.asyncio
async def test_sync_with_hydra_failure(service, service_account_repo, hydra_client):
    acc = make_service_account()
    service_account_repo.get_by_id.return_value = acc
    hydra_client.get_client.side_effect = Exception("hydra error")
    with pytest.raises(HydraIntegrationError):
        await service.sync_with_hydra(acc.id)
