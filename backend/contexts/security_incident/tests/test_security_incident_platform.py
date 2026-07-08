"""Enterprise Security Incident Platform tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from contexts.policy.container import get_policy_service, reset_policy_service
from contexts.security_incident.container import get_security_incident_service, reset_security_incident_service
from contexts.security_incident.domain.aggregates.incident_platform import (
    IncidentCapability,
    IncidentClassification,
    IncidentStatus,
)
from contexts.security_incident.domain.services import incident_engine
from contexts.security_incident.infrastructure.persistence.incident_memory_store import (
    InMemoryIncidentEvidenceRepository,
    InMemoryIncidentLessonLearnedRepository,
    InMemoryIncidentNotificationRepository,
    InMemoryIncidentTenantProfileRepository,
    InMemorySecurityIncidentRepository,
)
from core.presentation.api.main import app
from shared.infrastructure.messaging.event_bus import InProcessEventBus


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    InMemoryIncidentTenantProfileRepository.reset()
    InMemorySecurityIncidentRepository.reset()
    InMemoryIncidentEvidenceRepository.reset()
    InMemoryIncidentNotificationRepository.reset()
    InMemoryIncidentLessonLearnedRepository.reset()
    InProcessEventBus.reset()
    reset_policy_service()
    reset_security_incident_service()
    get_policy_service()
    get_security_incident_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "soc@enterprise.dev", "password": "SecurePass123!", "display_name": "SOC"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "soc@enterprise.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_catalog_lists_incident_capabilities(client):
    headers = await _auth_headers(client, "inccat")
    resp = await client.get("/api/v1/security-incidents/catalog", headers=headers)
    assert resp.status_code == 200
    data = resp.json()["data"]
    caps = {c["capability"] for c in data["capabilities"]}
    assert IncidentCapability.INCIDENT_DETECTION.value in caps
    assert IncidentCapability.DIGITAL_FORENSICS.value in caps
    assert IncidentCapability.INCIDENT_DASHBOARD.value in caps
    assert IncidentCapability.SLA.value in caps
    assert len(caps) == 13
    assert data["delegation"]["local_incident_duplication"] is False
    classifications = {c["classification"] for c in data["classifications"]}
    assert IncidentClassification.CYBER.value in classifications
    assert len(classifications) == 9


@pytest.mark.asyncio
async def test_seed_incident_lifecycle_and_dashboard(client):
    slug = "incseed"
    headers = await _auth_headers(client, slug)

    seed = await client.post("/api/v1/security-incidents/seed", headers=headers)
    assert seed.status_code == 200
    body = seed.json()["data"]
    assert body["seeded"] is True
    assert body["incidents_seeded"] == 6
    assert body["enabled_classifications"] == 9

    detect = await client.post(
        "/api/v1/security-incidents/incidents",
        headers=headers,
        json={
            "title": "Suspicious API key usage",
            "description": "API key used from unexpected geography",
            "classification": "unauthorized_access",
            "severity": "high",
        },
    )
    assert detect.status_code == 201
    incident_ref = detect.json()["data"]["incident_ref"]

    investigate = await client.post(
        f"/api/v1/security-incidents/incidents/{incident_ref}/investigate",
        headers=headers,
        json={"assigned_to": "analyst-1"},
    )
    assert investigate.status_code == 200
    assert investigate.json()["data"]["status"] == IncidentStatus.INVESTIGATING.value

    contain = await client.post(
        f"/api/v1/security-incidents/incidents/{incident_ref}/contain",
        headers=headers,
        json={"actions": ["Revoke API key", "Block source IP"]},
    )
    assert contain.status_code == 200
    assert contain.json()["data"]["status"] == IncidentStatus.CONTAINED.value

    evidence = await client.post(
        f"/api/v1/security-incidents/incidents/{incident_ref}/evidence",
        headers=headers,
        json={"evidence_type": "log", "description": "API access logs from gateway"},
    )
    assert evidence.status_code == 201
    assert evidence.json()["data"]["hash_digest"]

    forensics = await client.post(
        f"/api/v1/security-incidents/incidents/{incident_ref}/forensics",
        headers=headers,
    )
    assert forensics.status_code == 200
    assert forensics.json()["data"]["explainable"] is True

    root_cause = await client.post(
        f"/api/v1/security-incidents/incidents/{incident_ref}/root-cause",
        headers=headers,
        json={"root_cause": "Compromised API key from leaked credentials"},
    )
    assert root_cause.status_code == 200

    resolve = await client.post(
        f"/api/v1/security-incidents/incidents/{incident_ref}/resolve",
        headers=headers,
        json={"root_cause": "Compromised API key from leaked credentials"},
    )
    assert resolve.status_code == 200
    assert resolve.json()["data"]["status"] == IncidentStatus.RESOLVED.value

    lesson = await client.post(
        f"/api/v1/security-incidents/incidents/{incident_ref}/lessons",
        headers=headers,
        json={
            "title": "Rotate API keys regularly",
            "summary": "Key was not rotated after employee departure",
            "recommendations": ["Enforce 90-day key rotation", "Enable geo-fencing"],
        },
    )
    assert lesson.status_code == 201

    sla = await client.get("/api/v1/security-incidents/sla", headers=headers)
    assert sla.status_code == 200
    assert sla.json()["data"]["summary"]["total"] >= 7

    dash = await client.get("/api/v1/security-incidents/dashboard", headers=headers)
    assert dash.status_code == 200
    d = dash.json()["data"]
    assert d["summary"]["capabilities"] == 13
    assert d["summary"]["total_incidents"] >= 7
    assert d["delegation"]["local_incident_duplication"] is False


@pytest.mark.asyncio
async def test_escalate_incident(client):
    slug = "incesc"
    headers = await _auth_headers(client, slug)
    await client.post("/api/v1/security-incidents/seed", headers=headers)

    incidents = await client.get("/api/v1/security-incidents/incidents", headers=headers)
    incident_ref = incidents.json()["data"][0]["incident_ref"]

    esc = await client.post(
        f"/api/v1/security-incidents/incidents/{incident_ref}/escalate",
        headers=headers,
    )
    assert esc.status_code == 200
    assert esc.json()["data"]["status"] == IncidentStatus.ESCALATED.value


def test_engine_sla_and_forensics():
    deadlines = incident_engine.compute_sla_deadlines(response_hours=4, resolution_hours=72)
    assert "response_due_at" in deadlines
    assert "resolution_due_at" in deadlines

    incident = {
        "incident_ref": "INC-1",
        "classification": "malware",
        "severity": "critical",
        "status": "investigating",
        "resolution_due_at": deadlines["resolution_due_at"],
        "response_due_at": deadlines["response_due_at"],
    }
    sla = incident_engine.evaluate_sla(incident=incident, response_hours=4, resolution_hours=72)
    assert sla in ("on_track", "at_risk", "breached")

    forensics = incident_engine.digital_forensics_analysis(
        incident=incident,
        evidence=[{"incident_ref": "INC-1", "evidence_type": "disk_image"}],
    )
    assert forensics["explainable"] is True
    assert forensics["autonomous_execution"] is False

    dm = incident_engine.dependency_map()
    assert dm["no_incident_duplication"] is True
