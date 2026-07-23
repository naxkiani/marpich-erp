"""Identity bounded context tests."""
import pytest
from httpx import ASGITransport, AsyncClient

from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from core.presentation.api.app_factory import create_app
from core.presentation.api.startup_registry import configure_application


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
    application = create_app(profile="core", startup_mode="lazy")
    configure_application(application, profile="core", startup_mode="lazy")
    transport = ASGITransport(app=application)
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
async def test_mfa_setup_and_verify(client):
    import pyotp

    tenant = "mfa-tenant"
    headers = {"X-Tenant-ID": tenant}

    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "mfa@acme.com",
            "password": "SecurePass123!",
            "display_name": "MFA User",
        },
        headers=headers,
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "mfa@acme.com", "password": "SecurePass123!"},
        headers=headers,
    )
    assert login.status_code == 200
    token = login.json()["data"]["access_token"]
    auth = {**headers, "Authorization": f"Bearer {token}"}

    setup = await client.post("/api/v1/users/me/mfa/setup", headers=auth)
    assert setup.status_code == 200
    secret = setup.json()["data"]["secret"]
    assert setup.json()["data"]["provisioning_uri"]
    code = pyotp.TOTP(secret).now()

    verify = await client.post(
        "/api/v1/users/me/mfa/verify",
        json={"code": code},
        headers=auth,
    )
    assert verify.status_code == 200
    body = verify.json()["data"]
    assert body["mfa_enabled"] is True
    assert len(body["backup_codes"]) >= 1

    me = await client.get("/api/v1/users/me", headers=auth)
    assert me.status_code == 200
    assert me.json()["data"]["mfa_enabled"] is True


@pytest.mark.asyncio
async def test_change_password(client):
    tenant = "pwd-tenant"
    headers = {"X-Tenant-ID": tenant}

    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "pwd@acme.com",
            "password": "SecurePass123!",
            "display_name": "Pwd User",
        },
        headers=headers,
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "pwd@acme.com", "password": "SecurePass123!"},
        headers=headers,
    )
    assert login.status_code == 200
    token = login.json()["data"]["access_token"]
    auth = {**headers, "Authorization": f"Bearer {token}"}

    bad = await client.post(
        "/api/v1/users/me/password",
        json={
            "current_password": "WrongPass123!",
            "new_password": "AnotherPass123!",
            "revoke_other_sessions": False,
        },
        headers=auth,
    )
    assert bad.status_code == 400

    changed = await client.post(
        "/api/v1/users/me/password",
        json={
            "current_password": "SecurePass123!",
            "new_password": "AnotherPass123!",
            "revoke_other_sessions": False,
        },
        headers=auth,
    )
    assert changed.status_code == 200
    body = changed.json()["data"]
    assert body["password_changed"] is True
    assert body["other_sessions_revoked"] is False

    old_login = await client.post(
        "/api/v1/auth/login",
        json={"email": "pwd@acme.com", "password": "SecurePass123!"},
        headers=headers,
    )
    assert old_login.status_code == 400

    new_login = await client.post(
        "/api/v1/auth/login",
        json={"email": "pwd@acme.com", "password": "AnotherPass123!"},
        headers=headers,
    )
    assert new_login.status_code == 200
    assert new_login.json()["data"]["access_token"]


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
