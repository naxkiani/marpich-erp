"""Treasury Workflow tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.treasury.container import (
    get_treasury_workflow_service,
    reset_treasury_service,
)
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from core.presentation.api.main import app


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    reset_treasury_service()
    get_treasury_workflow_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "wf@treasury.dev", "password": "SecurePass123!", "display_name": "WF Mgr"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "wf@treasury.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


async def _provision(slug: str) -> None:
    await get_treasury_workflow_service().handle_tenant_provisioned({"tenant_id": slug, "payload": {}})


@pytest.mark.asyncio
async def test_workflow_catalog(client):
    slug = "wfcat"
    headers = await _auth_headers(client, slug)
    resp = await client.get("/api/v1/treasury/workflows/catalog", headers=headers)
    assert resp.status_code == 200
    caps = {c["capability"] for c in resp.json()["data"]}
    assert "transfer_approval" in caps
    assert "payment_approval" in caps
    assert "fund_request" in caps
    assert "cash_request" in caps
    assert "cash_transfer" in caps
    assert "investment_approval" in caps
    assert "bank_account_approval" in caps
    assert "treasury_limits" in caps
    assert "escalation" in caps
    assert "delegation" in caps
    assert "parallel" in caps
    assert "sequential" in caps
    assert "sla_monitoring" in caps
    assert "audit_trail" in caps
    assert "digital_signature" in caps
    assert "workflow_designer" in caps
    assert len(caps) == 16


@pytest.mark.asyncio
async def test_seed_definitions_and_limits(client):
    slug = "wfseed"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    defs = await client.get("/api/v1/treasury/workflows/definitions", headers=headers)
    assert defs.status_code == 200
    types = {d["workflow_type"] for d in defs.json()["data"]}
    assert "transfer_approval" in types
    assert "investment_approval" in types
    assert len(defs.json()["data"]) == 7

    limits = await client.get("/api/v1/treasury/workflows/limits", headers=headers)
    assert limits.status_code == 200
    assert len(limits.json()["data"]) == 5


@pytest.mark.asyncio
async def test_workflow_designer(client):
    slug = "wfdesign"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    designer = await client.get("/api/v1/treasury/workflows/designer", headers=headers)
    assert designer.status_code == 200
    data = designer.json()["data"]
    assert data["definition_count"] == 7
    assert "approval_modes" in data
    assert "workflow_types" in data


@pytest.mark.asyncio
async def test_sequential_transfer_approval_flow(client):
    slug = "wfseq"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    create = await client.post(
        "/api/v1/treasury/workflows/requests",
        headers=headers,
        json={
            "workflow_type": "transfer_approval",
            "amount": 15000,
            "currency": "USD",
            "subject_ref": "xfer-001",
            "subject_type": "transfer",
            "title": "Wire transfer to vendor",
        },
    )
    assert create.status_code == 201
    request_id = create.json()["data"]["id"]
    step_id = create.json()["data"]["steps"][0]["step_id"]

    submit = await client.post(
        f"/api/v1/treasury/workflows/requests/{request_id}/submit",
        headers=headers,
    )
    assert submit.status_code == 200
    assert submit.json()["data"]["status"] == "pending_approval"

    approve = await client.post(
        f"/api/v1/treasury/workflows/requests/{request_id}/approve",
        headers=headers,
        json={"step_id": step_id, "with_signature": True},
    )
    assert approve.status_code == 200
    assert approve.json()["data"]["status"] == "approved"
    assert len(approve.json()["data"]["digital_signatures"]) == 1

    execute = await client.post(
        f"/api/v1/treasury/workflows/requests/{request_id}/execute",
        headers=headers,
    )
    assert execute.status_code == 200
    assert execute.json()["data"]["status"] == "executed"


@pytest.mark.asyncio
async def test_parallel_investment_approval(client):
    slug = "wfpar"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    create = await client.post(
        "/api/v1/treasury/workflows/requests",
        headers=headers,
        json={
            "workflow_type": "investment_approval",
            "amount": 75000,
            "currency": "USD",
            "subject_ref": "inv-001",
            "subject_type": "investment",
            "title": "Bond purchase approval",
        },
    )
    assert create.status_code == 201
    request_id = create.json()["data"]["id"]
    assert create.json()["data"]["approval_mode"] == "parallel"

    await client.post(f"/api/v1/treasury/workflows/requests/{request_id}/submit", headers=headers)

    steps = create.json()["data"]["steps"]
    for step in steps:
        resp = await client.post(
            f"/api/v1/treasury/workflows/requests/{request_id}/approve",
            headers=headers,
            json={"step_id": step["step_id"]},
        )
        assert resp.status_code == 200

    final = await client.get(f"/api/v1/treasury/workflows/requests/{request_id}", headers=headers)
    assert final.json()["data"]["status"] == "approved"


@pytest.mark.asyncio
async def test_delegation_escalation_and_audit(client):
    slug = "wfdeleg"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    create = await client.post(
        "/api/v1/treasury/workflows/requests",
        headers=headers,
        json={
            "workflow_type": "payment_approval",
            "amount": 5000,
            "currency": "USD",
            "subject_ref": "pay-001",
            "subject_type": "payment",
            "title": "Vendor payment",
        },
    )
    request_id = create.json()["data"]["id"]
    step_id = create.json()["data"]["steps"][0]["step_id"]
    await client.post(f"/api/v1/treasury/workflows/requests/{request_id}/submit", headers=headers)

    delegate = await client.post(
        f"/api/v1/treasury/workflows/requests/{request_id}/delegate",
        headers=headers,
        json={"step_id": step_id, "to_user": "delegate-user", "reason": "OOO"},
    )
    assert delegate.status_code == 200
    assert len(delegate.json()["data"]["delegations"]) == 1

    escalate = await client.post(
        f"/api/v1/treasury/workflows/requests/{request_id}/escalate",
        headers=headers,
        json={"escalated_to": "treasury-director", "reason": "sla_breach"},
    )
    assert escalate.status_code == 200
    assert escalate.json()["data"]["status"] == "escalated"

    audit = await client.get(
        f"/api/v1/treasury/workflows/requests/{request_id}/audit",
        headers=headers,
    )
    assert audit.status_code == 200
    actions = {e["action"] for e in audit.json()["data"]}
    assert "created" in actions
    assert "submitted" in actions
    assert "delegated" in actions
    assert "escalated" in actions


@pytest.mark.asyncio
async def test_reject_and_sla_monitoring(client):
    slug = "wfsla"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    create = await client.post(
        "/api/v1/treasury/workflows/requests",
        headers=headers,
        json={
            "workflow_type": "cash_request",
            "amount": 2000,
            "currency": "USD",
            "subject_ref": "cash-001",
            "subject_type": "cash",
            "title": "Petty cash top-up",
        },
    )
    request_id = create.json()["data"]["id"]
    await client.post(f"/api/v1/treasury/workflows/requests/{request_id}/submit", headers=headers)

    reject = await client.post(
        f"/api/v1/treasury/workflows/requests/{request_id}/reject",
        headers=headers,
        json={"comment": "Insufficient justification"},
    )
    assert reject.status_code == 200
    assert reject.json()["data"]["status"] == "rejected"

    sla = await client.get("/api/v1/treasury/workflows/sla", headers=headers)
    assert sla.status_code == 200
    assert "pending_count" in sla.json()["data"]


@pytest.mark.asyncio
async def test_workflow_dashboard(client):
    slug = "wfdash"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    dash = await client.get("/api/v1/treasury/workflows/dashboard", headers=headers)
    assert dash.status_code == 200
    data = dash.json()["data"]
    assert "summary" in data
    assert data["summary"]["active_definitions"] == 7
    assert "workflow_states" in data
