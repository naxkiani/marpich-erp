"""Analytics — metrics, dashboards, alerts tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.analytics.container import get_analytics_service, reset_analytics_service
from contexts.analytics.infrastructure.persistence.memory_store import AnalyticsMemoryStore
from contexts.audit.container import get_audit_service, reset_audit_service
from contexts.audit.infrastructure.persistence.memory_store import AuditMemoryStore
from contexts.core_platform.container import reset_platform_service
from contexts.core_platform.infrastructure.persistence.memory_store import PlatformMemoryStore
from contexts.documents.container import get_documents_service, reset_documents_service
from contexts.documents.infrastructure.persistence.memory_store import DocumentsMemoryStore
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from contexts.integration.container import get_integration_service, reset_integration_service
from contexts.integration.infrastructure.persistence.memory_store import IntegrationMemoryStore
from contexts.media.container import get_media_service, reset_media_service
from contexts.media.infrastructure.persistence.memory_store import MediaMemoryStore
from contexts.notifications.container import get_notification_service, reset_notification_service
from contexts.notifications.infrastructure.persistence.memory_store import NotificationMemoryStore
from contexts.organization.container import get_organization_service, reset_organization_service
from contexts.organization.infrastructure.persistence.memory_store import OrganizationMemoryStore
from contexts.settings.container import get_settings_service, reset_settings_service
from contexts.settings.infrastructure.persistence.memory_store import SettingsMemoryStore
from contexts.workflow.container import get_workflow_service, reset_workflow_service
from contexts.workflow.infrastructure.persistence.memory_store import WorkflowMemoryStore
from core.presentation.api.main import app
from shared.infrastructure.messaging.event_bus import InProcessEventBus


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    PlatformMemoryStore.reset()
    OrganizationMemoryStore.reset()
    SettingsMemoryStore.reset()
    NotificationMemoryStore.reset()
    AuditMemoryStore.reset()
    DocumentsMemoryStore.reset()
    WorkflowMemoryStore.reset()
    IntegrationMemoryStore.reset()
    MediaMemoryStore.reset()
    AnalyticsMemoryStore.reset()
    InProcessEventBus.reset()
    reset_platform_service()
    reset_organization_service()
    reset_settings_service()
    reset_notification_service()
    reset_audit_service()
    reset_documents_service()
    reset_workflow_service()
    reset_integration_service()
    reset_media_service()
    reset_analytics_service()
    get_analytics_service()
    get_organization_service()
    get_settings_service()
    get_notification_service()
    get_audit_service()
    get_documents_service()
    get_workflow_service()
    get_integration_service()
    get_media_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "admin@analytics.dev", "password": "SecurePass123!", "display_name": "Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "admin@analytics.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_tenant_provision_seeds_dashboard_and_metrics(client):
    slug = "analytics-provision"
    await client.post(
        "/api/v1/platform/tenants",
        json={"name": "Analytics Co", "slug": slug, "industry_pack": "hospital"},
    )
    headers = await _auth_headers(client, slug)

    metrics = await client.get("/api/v1/analytics/metrics", headers=headers)
    assert metrics.status_code == 200
    keys = {m["key"] for m in metrics.json()["data"]}
    assert "events.total" in keys
    assert "users.created" in keys

    dashboards = await client.get("/api/v1/analytics/dashboards", headers=headers)
    assert dashboards.status_code == 200
    assert len(dashboards.json()["data"]) >= 1


@pytest.mark.asyncio
async def test_events_increment_metrics(client):
    slug = "analytics-metrics"
    await client.post(
        "/api/v1/platform/tenants",
        json={"name": "Metrics Co", "slug": slug, "industry_pack": "hospital"},
    )
    headers = await _auth_headers(client, slug)

    metrics = await client.get("/api/v1/analytics/metrics", headers=headers)
    data = {m["key"]: m["current_value"] for m in metrics.json()["data"]}
    assert data.get("users.created", 0) >= 1
    assert data.get("events.total", 0) >= 1


@pytest.mark.asyncio
async def test_dashboard_widget_values(client):
    slug = "analytics-dashboard"
    await client.post(
        "/api/v1/platform/tenants",
        json={"name": "Dash Co", "slug": slug, "industry_pack": "clinic"},
    )
    headers = await _auth_headers(client, slug)

    dashboards = await client.get("/api/v1/analytics/dashboards", headers=headers)
    dashboard_id = dashboards.json()["data"][0]["id"]

    detail = await client.get(f"/api/v1/analytics/dashboards/{dashboard_id}", headers=headers)
    assert detail.status_code == 200
    widgets = detail.json()["data"]["widgets"]
    assert len(widgets) >= 1
    assert all("value" in w for w in widgets)


@pytest.mark.asyncio
async def test_events_summary(client):
    slug = "analytics-summary"
    headers = await _auth_headers(client, slug)

    summary = await client.get("/api/v1/analytics/events/summary", headers=headers)
    assert summary.status_code == 200
    data = summary.json()["data"]
    assert data["total_events"] >= 1
    assert len(data["top_events"]) >= 1


@pytest.mark.asyncio
async def test_alert_triggers_on_threshold(client):
    slug = "analytics-alert"
    await client.post(
        "/api/v1/platform/tenants",
        json={"name": "Alert Co", "slug": slug, "industry_pack": "school"},
    )
    headers = await _auth_headers(client, slug)

    alert = await client.post(
        "/api/v1/analytics/alerts",
        json={"metric_key": "users.created", "name": "User spike", "threshold": 1, "operator": "gte"},
        headers=headers,
    )
    assert alert.status_code == 201

    await client.post(
        "/api/v1/auth/register",
        json={"email": "user2@analytics.dev", "password": "SecurePass123!", "display_name": "User2"},
        headers={"X-Tenant-ID": slug},
    )

    entries = await client.get(
        "/api/v1/audit/entries",
        params={"event_name": "analytics.alert.triggered"},
        headers=headers,
    )
    assert entries.status_code == 200
    assert len(entries.json()["data"]["items"]) >= 1
