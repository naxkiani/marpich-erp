"""Plugin platform tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from contexts.plugins.container import get_plugin_runtime, get_plugin_service, reset_plugin_service
from core.presentation.api.app_factory import create_app
from core.presentation.api.startup_registry import configure_application
from shared.infrastructure.messaging.event_fabric import EventFabric
from shared.infrastructure.settings import settings


@pytest.fixture(autouse=True)
def reset_all(monkeypatch):
    monkeypatch.setattr(settings, "persistence_backend", "memory")
    monkeypatch.setattr("shared.infrastructure.settings.use_postgres", lambda: False)
    monkeypatch.setattr("contexts.identity.container.use_postgres", lambda: False)
    identity_container._container = None
    InMemoryStore.reset()
    EventFabric.reset_dev_state()
    reset_plugin_service()
    get_plugin_service()
    yield
    reset_plugin_service()
    identity_container._container = None
    EventFabric.reset_dev_state()


@pytest.fixture
async def client(reset_all):
    application = create_app(profile="full", startup_mode="lazy")
    configure_application(application, profile="full", startup_mode="lazy")
    transport = ASGITransport(app=application)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "admin@plugins.dev", "password": "SecurePass123!", "display_name": "Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "admin@plugins.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    assert login.status_code == 200, login.text
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_seed_marketplace_listings():
    listings = (await get_plugin_service().list_marketplace()).unwrap()
    ids = {l["plugin_id"] for l in listings}
    assert "com.marpich.demo-sales-widget" in ids
    assert "com.marpich.demo-report-pack" in ids


@pytest.mark.asyncio
async def test_install_with_permissions(client):
    slug = "plugins-tenant"
    headers = await _auth_headers(client, slug)

    install = await client.post(
        "/api/v1/plugins/com.marpich.demo-sales-widget/install",
        headers=headers,
        json={
            "granted_permissions": ["analytics.read", "sales.orders.read"],
            "config": {"refresh_interval": 60},
        },
    )
    assert install.status_code == 201
    assert install.json()["data"]["plugin_id"] == "com.marpich.demo-sales-widget"
    assert install.json()["data"]["sandbox_profile"] == "strict"
    assert install.json()["data"]["enabled"] is False


@pytest.mark.asyncio
async def test_invoke_requires_enable_after_install(client):
    slug = "plugins-invoke"
    headers = await _auth_headers(client, slug)

    await client.post(
        "/api/v1/plugins/com.marpich.demo-sales-widget/install",
        headers=headers,
        json={"granted_permissions": ["analytics.read", "sales.orders.read"]},
    )
    blocked = await client.post(
        "/api/v1/plugins/invoke",
        headers=headers,
        json={
            "plugin_id": "com.marpich.demo-sales-widget",
            "extension_point": "ui.dashboard.widget",
            "payload": {"dashboard_id": "sales"},
        },
    )
    assert blocked.status_code == 400

    enabled = await client.post(
        "/api/v1/plugins/com.marpich.demo-sales-widget/enable",
        headers=headers,
    )
    assert enabled.status_code == 200
    assert enabled.json()["data"]["enabled"] is True

    invoke = await client.post(
        "/api/v1/plugins/invoke",
        headers=headers,
        json={
            "plugin_id": "com.marpich.demo-sales-widget",
            "extension_point": "ui.dashboard.widget",
            "payload": {"dashboard_id": "sales"},
        },
    )
    assert invoke.status_code == 200
    data = invoke.json()["data"]
    assert data["sandbox_profile"] == "strict"
    assert data["result"]["status"] == "ok"


@pytest.mark.asyncio
async def test_marketplace_dashboard_and_runtime_port(client):
    slug = "plugins-dash"
    headers = await _auth_headers(client, slug)

    await client.post(
        "/api/v1/plugins/com.marpich.demo-report-pack/install",
        headers=headers,
        json={"granted_permissions": ["finance.reports.read"]},
    )
    enabled = await client.post(
        "/api/v1/plugins/com.marpich.demo-report-pack/enable",
        headers=headers,
    )
    assert enabled.status_code == 200

    dashboard = await client.get("/api/v1/plugins/marketplace/dashboard", headers=headers)
    assert dashboard.status_code == 200
    body = dashboard.json()["data"]
    assert body["installed_count"] >= 1
    assert "report" in body["listings_by_type"]

    runtime = get_plugin_runtime()
    extensions = await runtime.list_extensions(
        tenant_id=slug, extension_point="analytics.report.template"
    )
    assert any(e.plugin_id == "com.marpich.demo-report-pack" for e in extensions)


@pytest.mark.asyncio
async def test_install_denied_without_required_permissions(client):
    slug = "plugins-deny"
    headers = await _auth_headers(client, slug)
    denied = await client.post(
        "/api/v1/plugins/com.marpich.demo-sales-widget/install",
        headers=headers,
        json={"granted_permissions": ["analytics.read"]},
    )
    assert denied.status_code == 400
    assert "missing_permissions" in denied.text


@pytest.mark.asyncio
async def test_tenant_installations_are_isolated(client):
    headers_a = await _auth_headers(client, "plugins-tenant-a")
    await client.post(
        "/api/v1/auth/register",
        json={"email": "admin-b@plugins.dev", "password": "SecurePass123!", "display_name": "Admin B"},
        headers={"X-Tenant-ID": "plugins-tenant-b"},
    )
    login_b = await client.post(
        "/api/v1/auth/login",
        json={"email": "admin-b@plugins.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": "plugins-tenant-b"},
    )
    assert login_b.status_code == 200, login_b.text
    headers_b = {
        "X-Tenant-ID": "plugins-tenant-b",
        "Authorization": f"Bearer {login_b.json()['data']['access_token']}",
    }

    installed_a = await client.post(
        "/api/v1/plugins/com.marpich.demo-sales-widget/install",
        headers=headers_a,
        json={"granted_permissions": ["analytics.read", "sales.orders.read"]},
    )
    assert installed_a.status_code == 201

    list_b = await client.get("/api/v1/plugins/installed", headers=headers_b)
    assert list_b.status_code == 200
    assert list_b.json()["data"] == []


@pytest.mark.asyncio
async def test_disable_blocks_invoke_after_enable(client):
    slug = "plugins-disable"
    headers = await _auth_headers(client, slug)
    await client.post(
        "/api/v1/plugins/com.marpich.demo-sales-widget/install",
        headers=headers,
        json={"granted_permissions": ["analytics.read", "sales.orders.read"]},
    )
    await client.post(
        "/api/v1/plugins/com.marpich.demo-sales-widget/enable",
        headers=headers,
    )
    disabled = await client.post(
        "/api/v1/plugins/com.marpich.demo-sales-widget/disable",
        headers=headers,
    )
    assert disabled.status_code == 200
    assert disabled.json()["data"]["enabled"] is False

    invoke = await client.post(
        "/api/v1/plugins/invoke",
        headers=headers,
        json={
            "plugin_id": "com.marpich.demo-sales-widget",
            "extension_point": "ui.dashboard.widget",
            "payload": {"dashboard_id": "sales"},
        },
    )
    assert invoke.status_code == 400
    assert "not_enabled" in invoke.text
