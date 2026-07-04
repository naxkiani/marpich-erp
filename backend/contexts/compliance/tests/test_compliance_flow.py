"""Compliance Framework tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.compliance.container import get_compliance_service, reset_compliance_service
from contexts.compliance.infrastructure.persistence.memory_store import ComplianceMemoryStore
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from core.presentation.api.main import app
from shared.infrastructure.messaging.event_bus import InProcessEventBus


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    ComplianceMemoryStore.reset()
    InProcessEventBus.reset()
    reset_compliance_service()
    get_compliance_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "admin@compliance.dev", "password": "SecurePass123!", "display_name": "Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "admin@compliance.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_seed_controls_on_tenant_provision():
    await get_compliance_service().handle_tenant_provisioned(
        {"tenant_id": "hosp", "payload": {"industry_pack": "hospital"}}
    )
    controls = await get_compliance_service().list_controls("hosp")
    assert controls.succeeded
    assert any(c["control_id"] == "HIPAA-164.312-b" for c in controls.unwrap())


@pytest.mark.asyncio
async def test_policy_denied_creates_violation():
    await get_compliance_service().handle_tenant_provisioned(
        {"tenant_id": "acme", "payload": {"industry_pack": "bank"}}
    )
    await get_compliance_service().handle_integration_event(
        {
            "tenant_id": "acme",
            "event_name": "policy.evaluation.denied",
            "correlation_id": "c1",
            "payload": {"policy_key": "lending.limit"},
        }
    )
    result = await get_compliance_service().query_violations("acme", domain="internal_policies")
    assert result.unwrap()["total"] >= 1


@pytest.mark.asyncio
async def test_dashboard_and_report(client):
    slug = "compliance-dash"
    await get_compliance_service().handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {"industry_pack": "hospital"}}
    )
    headers = await _auth_headers(client, slug)

    dashboard = await client.get("/api/v1/compliance/dashboard", headers=headers)
    assert dashboard.status_code == 200
    assert "compliance_score" in dashboard.json()["data"]

    report = await client.post(
        "/api/v1/compliance/reports",
        headers=headers,
        json={"report_type": "full", "format": "json"},
    )
    assert report.status_code == 202
    report_id = report.json()["data"]["id"]

    fetched = await client.get(f"/api/v1/compliance/reports/{report_id}", headers=headers)
    assert fetched.status_code == 200
    assert fetched.json()["data"]["status"] == "completed"


@pytest.mark.asyncio
async def test_resolve_violation(client):
    slug = "compliance-resolve"
    await get_compliance_service().handle_integration_event(
        {
            "tenant_id": slug,
            "event_name": "policy.evaluation.denied",
            "correlation_id": "c2",
            "payload": {},
        }
    )
    headers = await _auth_headers(client, slug)
    violations = await client.get("/api/v1/compliance/violations", headers=headers)
    vid = violations.json()["data"]["items"][0]["id"]

    resolved = await client.post(
        f"/api/v1/compliance/violations/{vid}/resolve",
        headers=headers,
        json={"notes": "Policy activated — false alarm"},
    )
    assert resolved.status_code == 200
    assert resolved.json()["data"]["status"] == "resolved"
