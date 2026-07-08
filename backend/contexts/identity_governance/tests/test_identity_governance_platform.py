"""Enterprise Identity Governance Platform tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from contexts.identity_governance.container import get_identity_governance_service, reset_identity_governance_service
from contexts.identity_governance.domain.aggregates.identity_governance_platform import (
    IdentityGovernanceCapability,
    RequestStatus,
)
from contexts.identity_governance.domain.services import identity_governance_engine
from contexts.identity_governance.infrastructure.persistence.identity_governance_memory_store import (
    InMemoryAccessRequestRepository,
    InMemoryAccessReviewRepository,
    InMemoryEmergencyAccessGrantRepository,
    InMemoryGovernanceAuditEntryRepository,
    InMemoryIdentityGovernanceProfileRepository,
    InMemoryPrivilegeCertificationRepository,
    InMemoryTemporaryAccessGrantRepository,
)
from contexts.policy.container import get_policy_service, reset_policy_service
from core.presentation.api.main import app
from shared.infrastructure.messaging.event_bus import InProcessEventBus


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    InMemoryIdentityGovernanceProfileRepository.reset()
    InMemoryAccessRequestRepository.reset()
    InMemoryAccessReviewRepository.reset()
    InMemoryPrivilegeCertificationRepository.reset()
    InMemoryTemporaryAccessGrantRepository.reset()
    InMemoryEmergencyAccessGrantRepository.reset()
    InMemoryGovernanceAuditEntryRepository.reset()
    InProcessEventBus.reset()
    reset_policy_service()
    reset_identity_governance_service()
    get_policy_service()
    get_identity_governance_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "iga@enterprise.dev", "password": "SecurePass123!", "display_name": "IGA"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "iga@enterprise.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_catalog_lists_identity_governance_capabilities(client):
    headers = await _auth_headers(client, "igacat")
    resp = await client.get("/api/v1/identity-governance/catalog", headers=headers)
    assert resp.status_code == 200
    data = resp.json()["data"]
    caps = {c["capability"] for c in data["capabilities"]}
    assert IdentityGovernanceCapability.ACCESS_REQUEST.value in caps
    assert IdentityGovernanceCapability.SEGREGATION_OF_DUTIES.value in caps
    assert IdentityGovernanceCapability.EMERGENCY_ACCESS.value in caps
    assert IdentityGovernanceCapability.IDENTITY_DASHBOARD.value in caps
    assert len(caps) == 12
    assert data["delegation"]["local_identity_duplication"] is False
    assert len(data["sod_rules"]) >= 4


@pytest.mark.asyncio
async def test_access_request_approval_and_dashboard(client):
    slug = "igaseed"
    headers = await _auth_headers(client, slug)

    seed = await client.post("/api/v1/identity-governance/seed", headers=headers)
    assert seed.status_code == 200
    body = seed.json()["data"]
    assert body["seeded"] is True
    assert body["access_requests_seeded"] == 2

    requests = await client.get("/api/v1/identity-governance/access-requests", headers=headers)
    request_ref = requests.json()["data"][0]["request_ref"]

    approve = await client.post(
        f"/api/v1/identity-governance/access-requests/{request_ref}/approve",
        headers=headers,
    )
    assert approve.status_code == 200
    assert approve.json()["data"]["status"] == RequestStatus.APPROVED.value

    temp = await client.post(
        "/api/v1/identity-governance/temporary-access",
        headers=headers,
        json={"user_id": "user-temp", "roles": ["finance_viewer"], "justification": "Month-end"},
    )
    assert temp.status_code == 201

    emergency = await client.post(
        "/api/v1/identity-governance/emergency-access",
        headers=headers,
        json={"user_id": "user-emg", "roles": ["admin"], "incident_ref": "INC-001", "justification": "Incident response"},
    )
    assert emergency.status_code == 201

    audit = await client.get("/api/v1/identity-governance/audit", headers=headers)
    assert audit.status_code == 200
    assert len(audit.json()["data"]) >= 2

    dash = await client.get("/api/v1/identity-governance/dashboard", headers=headers)
    assert dash.status_code == 200
    d = dash.json()["data"]
    assert d["summary"]["capabilities"] == 12
    assert d["summary"]["active_temporary_grants"] >= 1
    assert d["delegation"]["local_identity_duplication"] is False


@pytest.mark.asyncio
async def test_sod_blocks_conflicting_roles(client):
    slug = "igasod"
    headers = await _auth_headers(client, slug)
    await client.post("/api/v1/identity-governance/seed", headers=headers)

    check = await client.post(
        "/api/v1/identity-governance/sod/check",
        headers=headers,
        json={
            "existing_roles": ["finance_approver"],
            "requested_roles": ["finance_poster"],
        },
    )
    assert check.status_code == 200
    assert check.json()["data"]["valid"] is False

    submit = await client.post(
        "/api/v1/identity-governance/access-requests",
        headers=headers,
        json={
            "target_user_id": "user-sod",
            "requested_roles": ["finance_poster"],
            "justification": "Test SoD",
            "existing_roles": ["finance_approver"],
        },
    )
    assert submit.status_code == 400


@pytest.mark.asyncio
async def test_certification_and_access_review(client):
    slug = "igacert"
    headers = await _auth_headers(client, slug)
    await client.post("/api/v1/identity-governance/seed", headers=headers)

    certs = await client.get("/api/v1/identity-governance/certifications", headers=headers)
    cert_ref = certs.json()["data"][0]["certification_ref"]

    certify = await client.post(
        f"/api/v1/identity-governance/certifications/{cert_ref}/certify",
        headers=headers,
        json={"notes": "Privileges verified"},
    )
    assert certify.status_code == 200
    assert certify.json()["data"]["status"] == "certified"

    reviews = await client.get("/api/v1/identity-governance/access-reviews", headers=headers)
    review_ref = reviews.json()["data"][0]["review_ref"]

    complete = await client.post(
        f"/api/v1/identity-governance/access-reviews/{review_ref}/complete",
        headers=headers,
        json={"findings": [{"user_id": "user-finance-1", "action": "retain"}]},
    )
    assert complete.status_code == 200
    assert complete.json()["data"]["status"] == "completed"


def test_engine_sod_and_dashboard():
    sod = identity_governance_engine.check_segregation_of_duties(
        existing_roles=["finance_approver"],
        requested_roles=["finance_poster"],
    )
    assert sod["valid"] is False
    assert len(sod["conflicts"]) >= 1

    dashboard = identity_governance_engine.build_dashboard(
        profile={"sod_enforcement": True},
        access_requests=[{"status": "pending", "created_at": "2026-01-01"}],
        access_reviews=[],
        certifications=[],
        temporary_grants=[],
        emergency_grants=[],
        audit_entries=[],
    )
    assert dashboard["summary"]["pending_access_requests"] == 1

    dm = identity_governance_engine.dependency_map()
    assert dm["no_identity_duplication"] is True
