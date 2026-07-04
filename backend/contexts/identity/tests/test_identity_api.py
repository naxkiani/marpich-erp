"""Identity bounded context tests."""
import pytest
from httpx import ASGITransport, AsyncClient

from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from core.presentation.api.main import app


@pytest.fixture(autouse=True)
def reset_store():
    import contexts.identity.container as c

    c._container = None
    InMemoryStore.reset()
    yield
    c._container = None
    InMemoryStore.reset()


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_register_and_login(client):
    tenant = "acme-hospital"
    headers = {"X-Tenant-ID": tenant}

    reg = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "admin@acme.com",
            "password": "SecurePass123!",
            "display_name": "Admin",
        },
        headers=headers,
    )
    assert reg.status_code == 201
    assert reg.json()["data"]["email"] == "admin@acme.com"

    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "admin@acme.com", "password": "SecurePass123!"},
        headers=headers,
    )
    assert login.status_code == 200
    data = login.json()["data"]
    assert data["access_token"]
    assert data["mfa_required"] is False

    me = await client.get(
        "/api/v1/users/me",
        headers={**headers, "Authorization": f"Bearer {data['access_token']}"},
    )
    assert me.status_code == 200
    assert me.json()["data"]["permissions"] == ["*"]


@pytest.mark.asyncio
async def test_refresh_rotates_token(client):
    tenant = "test-tenant"
    headers = {"X-Tenant-ID": tenant}

    await client.post(
        "/api/v1/auth/register",
        json={"email": "u@test.com", "password": "SecurePass123!", "display_name": "User"},
        headers=headers,
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "u@test.com", "password": "SecurePass123!"},
        headers=headers,
    )
    refresh_token = login.json()["data"]["refresh_token"]

    refreshed = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token},
        headers=headers,
    )
    assert refreshed.status_code == 200
    assert refreshed.json()["data"]["refresh_token"] != refresh_token


@pytest.mark.asyncio
async def test_user_aggregate_locks_after_failures():
    from contexts.identity.domain.aggregates.user import User

    user, _ = User.register(
        tenant_id="test-tenant",
        email="a@b.com",
        password_hash="hash",
        display_name="Test",
        correlation_id="c1",
    )
    for _ in range(5):
        user.record_failed_login()
    assert user.is_locked()
