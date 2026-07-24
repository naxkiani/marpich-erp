"""Plugin platform tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from contexts.plugins.container import get_plugin_runtime, get_plugin_service, reset_plugin_service
from core.presentation.api.app_factory import create_app
from core.presentation.api.startup_registry import configure_application


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    reset_plugin_service()
    get_plugin_service()
    yield


@pytest.fixture
async def client():
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


@pytest.mark.asyncio
async def test_invoke_sandboxed_extension(client):
    slug = "plugins-invoke"
    headers = await _auth_headers(client, slug)

    await client.post(
        "/api/v1/plugins/com.marpich.demo-sales-widget/install",
        headers=headers,
        json={"granted_permissions": ["analytics.read", "sales.orders.read"]},
    )

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
