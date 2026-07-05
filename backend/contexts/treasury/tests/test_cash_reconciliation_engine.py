"""Enterprise Cash Reconciliation tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.treasury.container import (
    get_cash_management_service,
    get_cash_reconciliation_service,
    reset_treasury_service,
)
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from core.presentation.api.main import app


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    reset_treasury_service()
    get_cash_management_service()
    get_cash_reconciliation_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "cashrecon@treasury.dev", "password": "SecurePass123!", "display_name": "Cash Recon"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "cashrecon@treasury.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


async def _provision(slug: str) -> dict[str, dict]:
    svc = get_cash_management_service()
    await svc.handle_tenant_provisioned({"tenant_id": slug, "payload": {}})
    locs = (await svc.list_locations(slug)).unwrap()
    return {l["location_type"]: l for l in locs}


@pytest.mark.asyncio
async def test_cash_reconciliation_catalog(client):
    slug = "cashreconcat"
    headers = await _auth_headers(client, slug)
    resp = await client.get("/api/v1/treasury/cash-reconciliation/catalog", headers=headers)
    assert resp.status_code == 200
    caps = {c["capability"] for c in resp.json()["data"]}
    assert "cash_count" in caps
    assert "cash_difference" in caps
    assert "cash_over" in caps
    assert "cash_short" in caps
    assert "cash_verification" in caps
    assert "cash_approval" in caps
    assert "cash_closing" in caps
    assert "shift_closing" in caps
    assert "branch_closing" in caps
    assert "discrepancy_report" in caps
    assert "ai_anomaly_detection" in caps
    assert len(caps) == 11


@pytest.mark.asyncio
async def test_balanced_count_no_manager_approval(client):
    slug = "cashreconbal"
    headers = await _auth_headers(client, slug)
    locs = await _provision(slug)
    register = locs["cash_register"]

    count = await client.post(
        "/api/v1/treasury/cash-reconciliation/counts",
        headers=headers,
        json={"location_id": register["id"], "counted_amount": register["balance"]},
    )
    assert count.status_code == 201
    data = count.json()["data"]
    assert data["variance_type"] == "balanced"
    assert data["requires_manager_approval"] is False
    run_id = data["id"]

    verify = await client.post(
        f"/api/v1/treasury/cash-reconciliation/runs/{run_id}/verify",
        headers=headers,
    )
    assert verify.status_code == 200
    assert verify.json()["data"]["status"] == "approved"

    close = await client.post(
        f"/api/v1/treasury/cash-reconciliation/runs/{run_id}/close",
        headers=headers,
    )
    assert close.status_code == 200
    assert close.json()["data"]["status"] == "closed"


@pytest.mark.asyncio
async def test_cash_short_requires_manager_approval(client):
    slug = "cashreconshort"
    headers = await _auth_headers(client, slug)
    locs = await _provision(slug)
    register = locs["cash_register"]
    system_balance = register["balance"]

    count = await client.post(
        "/api/v1/treasury/cash-reconciliation/counts",
        headers=headers,
        json={"location_id": register["id"], "counted_amount": system_balance - 50},
    )
    assert count.status_code == 201
    data = count.json()["data"]
    assert data["variance_type"] == "cash_short"
    assert data["variance"] == -50
    assert data["requires_manager_approval"] is True
    run_id = data["id"]

    verify = await client.post(
        f"/api/v1/treasury/cash-reconciliation/runs/{run_id}/verify",
        headers=headers,
    )
    assert verify.status_code == 200
    assert verify.json()["data"]["status"] == "pending_manager_approval"

    close_before_approve = await client.post(
        f"/api/v1/treasury/cash-reconciliation/runs/{run_id}/close",
        headers=headers,
    )
    assert close_before_approve.status_code == 400

    approve = await client.post(
        f"/api/v1/treasury/cash-reconciliation/runs/{run_id}/approve",
        headers=headers,
    )
    assert approve.status_code == 200
    assert approve.json()["data"]["status"] == "approved"

    close = await client.post(
        f"/api/v1/treasury/cash-reconciliation/runs/{run_id}/close",
        headers=headers,
    )
    assert close.status_code == 200
    assert close.json()["data"]["status"] == "closed"


@pytest.mark.asyncio
async def test_cash_over_and_discrepancy_report(client):
    slug = "cashreconover"
    headers = await _auth_headers(client, slug)
    locs = await _provision(slug)
    register = locs["cash_register"]

    count = await client.post(
        "/api/v1/treasury/cash-reconciliation/counts",
        headers=headers,
        json={"location_id": register["id"], "counted_amount": register["balance"] + 25},
    )
    assert count.status_code == 201
    run_id = count.json()["data"]["id"]

    report = await client.get(
        f"/api/v1/treasury/cash-reconciliation/runs/{run_id}/discrepancy-report",
        headers=headers,
    )
    assert report.status_code == 200
    rpt = report.json()["data"]
    assert rpt["variance_type"] == "cash_over"
    assert rpt["cash_over"] == 25
    assert rpt["requires_manager_approval"] is True


@pytest.mark.asyncio
async def test_shift_closing_and_ai_anomalies(client):
    slug = "cashreconshift"
    headers = await _auth_headers(client, slug)
    locs = await _provision(slug)
    register = locs["cash_register"]

    shift = await client.post(
        "/api/v1/treasury/cash-reconciliation/shift-closing",
        headers=headers,
        json={"location_id": register["id"], "counted_amount": register["balance"] - 100},
    )
    assert shift.status_code == 201
    data = shift.json()["data"]
    assert data["closing_type"] == "shift_closing"
    run_id = data["id"]

    anomalies = await client.get(
        f"/api/v1/treasury/cash-reconciliation/runs/{run_id}/ai-anomalies",
        headers=headers,
    )
    assert anomalies.status_code == 200
    items = anomalies.json()["data"]
    assert len(items) >= 1
    assert any(a.get("autonomous_execution") is False for a in items)


@pytest.mark.asyncio
async def test_branch_closing_and_audit_trail(client):
    slug = "cashreconbranch"
    headers = await _auth_headers(client, slug)
    locs = await _provision(slug)
    register = locs["cash_register"]
    petty = locs["petty_cash"]

    branch = await client.post(
        "/api/v1/treasury/cash-reconciliation/branch-closing",
        headers=headers,
        json={
            "branch_id": register.get("branch_id") or "main",
            "location_counts": [
                {"location_id": register["id"], "counted_amount": register["balance"]},
                {"location_id": petty["id"], "counted_amount": petty["balance"]},
            ],
        },
    )
    assert branch.status_code == 201
    runs = branch.json()["data"]
    assert len(runs) == 2
    assert all(r["closing_type"] == "branch_closing" for r in runs)

    audit = await client.get(
        f"/api/v1/treasury/cash-reconciliation/runs/{runs[0]['id']}/audit",
        headers=headers,
    )
    assert audit.status_code == 200
    actions = {e["action"] for e in audit.json()["data"]}
    assert "cash_count" in actions


@pytest.mark.asyncio
async def test_reject_variance(client):
    slug = "cashreconreject"
    headers = await _auth_headers(client, slug)
    locs = await _provision(slug)
    register = locs["cash_register"]

    count = await client.post(
        "/api/v1/treasury/cash-reconciliation/counts",
        headers=headers,
        json={"location_id": register["id"], "counted_amount": register["balance"] - 10},
    )
    run_id = count.json()["data"]["id"]

    await client.post(
        f"/api/v1/treasury/cash-reconciliation/runs/{run_id}/verify",
        headers=headers,
    )

    reject = await client.post(
        f"/api/v1/treasury/cash-reconciliation/runs/{run_id}/reject",
        headers=headers,
        json={"reason": "Recount required"},
    )
    assert reject.status_code == 200
    assert reject.json()["data"]["status"] == "rejected"
    assert reject.json()["data"]["rejection_reason"] == "Recount required"


@pytest.mark.asyncio
async def test_dashboard(client):
    slug = "cashrecondash"
    headers = await _auth_headers(client, slug)
    locs = await _provision(slug)
    register = locs["cash_register"]

    await client.post(
        "/api/v1/treasury/cash-reconciliation/counts",
        headers=headers,
        json={"location_id": register["id"], "counted_amount": register["balance"] - 5},
    )

    dash = await client.get("/api/v1/treasury/cash-reconciliation/dashboard", headers=headers)
    assert dash.status_code == 200
    data = dash.json()["data"]
    assert data["summary"]["run_count"] >= 1
    assert "by_status" in data
    assert "workflow_states" in data
