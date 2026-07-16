"""Banking Settlement Engine tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.banking.container import (
    get_banking_customer_account_service,
    get_banking_payment_platform_service,
    get_banking_settlement_engine_service,
    reset_banking_customer_account_service,
)
from contexts.financial_kernel.container import (
    get_financial_kernel_service,
    reset_financial_kernel_service,
)
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from contexts.policy.container import get_policy_service, reset_policy_service
from contexts.policy.infrastructure.persistence.memory_store import PolicyMemoryStore
from core.presentation.api.main import app


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    PolicyMemoryStore.reset()
    reset_financial_kernel_service()
    reset_banking_customer_account_service()
    reset_policy_service()
    get_financial_kernel_service()
    get_banking_customer_account_service()
    get_banking_payment_platform_service()
    get_banking_settlement_engine_service()
    get_policy_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "settle@bank.dev", "password": "SecurePass123!", "display_name": "Settlement Ops"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "settle@bank.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


async def _provision(slug: str) -> None:
    kernel = get_financial_kernel_service()
    await kernel.handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {"industry_pack": "bank"}}
    )
    await get_policy_service().handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {"industry_pack": "bank"}}
    )
    await get_banking_customer_account_service().handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {}}
    )
    await get_banking_payment_platform_service().handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {}}
    )
    await get_banking_settlement_engine_service().handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {}}
    )


@pytest.mark.asyncio
async def test_settlement_catalog(client):
    slug = "setcat"
    headers = await _auth_headers(client, slug)
    resp = await client.get("/api/v1/banking/settlement/catalog", headers=headers)
    assert resp.status_code == 200
    caps = {c["capability"] for c in resp.json()["data"]}
    assert "internal_settlement" in caps
    assert "interbank_settlement" in caps
    assert "clearing" in caps
    assert "bank_reconciliation" in caps
    assert "automatic_matching" in caps
    assert "settlement_dashboard" in caps
    assert "reconciliation_audit" in caps


@pytest.mark.asyncio
async def test_internal_settlement_lifecycle(client):
    slug = "setint"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    batch = await client.post(
        "/api/v1/banking/settlement/batches",
        headers=headers,
        json={
            "settlement_type": "internal_settlement",
            "items": [
                {"source_ref": "TXN-001", "amount": 1500.0, "counterparty": "BR-A"},
                {"source_ref": "TXN-002", "amount": 2500.0, "counterparty": "BR-B"},
            ],
        },
    )
    assert batch.status_code == 201
    batch_id = batch.json()["data"]["id"]
    assert batch.json()["data"]["total_amount"] == 4000.0

    submit = await client.post(
        f"/api/v1/banking/settlement/batches/{batch_id}/submit", headers=headers
    )
    assert submit.status_code == 200
    assert submit.json()["data"]["status"] == "pending_settlement"

    settle = await client.post(
        f"/api/v1/banking/settlement/batches/{batch_id}/settle", headers=headers
    )
    assert settle.status_code == 200
    assert settle.json()["data"]["status"] == "completed"


@pytest.mark.asyncio
async def test_clearing_settlement_lifecycle(client):
    slug = "setclr"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    batch = await client.post(
        "/api/v1/banking/settlement/batches",
        headers=headers,
        json={
            "settlement_type": "clearing",
            "items": [{"source_ref": "CLR-001", "amount": 8000.0}],
        },
    )
    assert batch.status_code == 201
    batch_id = batch.json()["data"]["id"]

    settle = await client.post(
        f"/api/v1/banking/settlement/batches/{batch_id}/settle", headers=headers
    )
    assert settle.status_code == 200
    data = settle.json()["data"]
    assert data["status"] == "completed"
    assert data["clearing_ref"].startswith("CLR-")


@pytest.mark.asyncio
async def test_reconciliation_auto_match_and_audit(client):
    slug = "setrec"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    run = await client.post(
        "/api/v1/banking/settlement/reconciliation/runs",
        headers=headers,
        json={
            "settlement_account": "NOSTRO-001",
            "statement_items": [
                {"id": "s1", "reference": "TXN100", "amount": 500.0},
                {"id": "s2", "reference": "TXN200", "amount": 300.0},
            ],
            "book_items": [
                {"id": "b1", "reference": "TXN100", "amount": 500.0},
                {"id": "b2", "reference": "TXN200", "amount": 300.0},
            ],
        },
    )
    assert run.status_code == 201
    run_id = run.json()["data"]["id"]

    match = await client.post(
        f"/api/v1/banking/settlement/reconciliation/runs/{run_id}/match", headers=headers
    )
    assert match.status_code == 200
    assert match.json()["data"]["status"] == "matched"
    assert match.json()["data"]["matched_count"] == 2

    audit = await client.get(
        f"/api/v1/banking/settlement/reconciliation/runs/{run_id}/audit", headers=headers
    )
    assert audit.status_code == 200
    actions = {e["action"] for e in audit.json()["data"]}
    assert "reconciliation.started" in actions
    assert "reconciliation.matched" in actions


@pytest.mark.asyncio
async def test_difference_analysis_and_adjustment(client):
    slug = "setdif"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    run = await client.post(
        "/api/v1/banking/settlement/reconciliation/runs",
        headers=headers,
        json={
            "statement_items": [{"id": "s1", "reference": "A1", "amount": 1000.0}],
            "book_items": [{"id": "b1", "reference": "A2", "amount": 950.0}],
        },
    )
    run_id = run.json()["data"]["id"]
    await client.post(
        f"/api/v1/banking/settlement/reconciliation/runs/{run_id}/match", headers=headers
    )

    diff = await client.post(
        f"/api/v1/banking/settlement/reconciliation/runs/{run_id}/analyze-differences",
        headers=headers,
    )
    assert diff.status_code == 200
    assert diff.json()["data"]["difference_amount"] == 50.0
    assert len(diff.json()["data"]["analysis"]) >= 3

    adj = await client.post(
        "/api/v1/banking/settlement/adjustments",
        headers=headers,
        json={"run_id": run_id, "amount": 50.0, "reason": "timing_difference"},
    )
    assert adj.status_code == 201
    adj_id = adj.json()["data"]["id"]

    approved = await client.post(
        f"/api/v1/banking/settlement/adjustments/{adj_id}/approve",
        headers=headers,
        json={"approver_id": "settlement-manager"},
    )
    assert approved.status_code == 200
    assert approved.json()["data"]["status"] == "posted"


@pytest.mark.asyncio
async def test_exception_retry_and_dashboard(client):
    slug = "setexc"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    batch = await client.post(
        "/api/v1/banking/settlement/batches",
        headers=headers,
        json={
            "settlement_type": "interbank_settlement",
            "items": [{"source_ref": "IB-001", "amount": 12000.0}],
        },
    )
    batch_id = batch.json()["data"]["id"]

    exc = await client.post(
        "/api/v1/banking/settlement/exceptions",
        headers=headers,
        json={
            "source_type": "batch",
            "source_id": batch_id,
            "reason": "nostro_position_insufficient",
        },
    )
    assert exc.status_code == 201
    exc_id = exc.json()["data"]["id"]

    retry = await client.post(
        f"/api/v1/banking/settlement/exceptions/{exc_id}/retry", headers=headers
    )
    assert retry.status_code == 200

    report = await client.post(
        "/api/v1/banking/settlement/reports",
        headers=headers,
        json={"report_type": "settlement_summary"},
    )
    assert report.status_code == 201
    assert "completed_batches" in report.json()["data"]["summary"]

    dash = await client.get("/api/v1/banking/settlement/dashboard", headers=headers)
    assert dash.status_code == 200
    assert "batch_count" in dash.json()["data"]
    assert "open_exceptions" in dash.json()["data"]
