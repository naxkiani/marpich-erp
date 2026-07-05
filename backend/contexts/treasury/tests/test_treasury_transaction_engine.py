"""Treasury Transaction Engine tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.financial_kernel.container import (
    get_financial_kernel_service,
    reset_financial_kernel_service,
)
from contexts.treasury.container import (
    get_treasury_service,
    get_treasury_transaction_service,
    reset_treasury_service,
)
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from core.presentation.api.main import app


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    reset_financial_kernel_service()
    reset_treasury_service()
    get_financial_kernel_service()
    get_treasury_service()
    get_treasury_transaction_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "txn@treasury.dev", "password": "SecurePass123!", "display_name": "Txn Mgr"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "txn@treasury.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


async def _provision_accounts(slug: str) -> dict[str, dict]:
    await get_treasury_service().handle_tenant_provisioned({"tenant_id": slug, "payload": {}})
    accounts = (await get_treasury_service().list_accounts(slug)).unwrap()
    return {a["code"]: a for a in accounts}


@pytest.mark.asyncio
async def test_transaction_catalog_lists_twelve_types(client):
    slug = "txncat"
    headers = await _auth_headers(client, slug)
    resp = await client.get("/api/v1/treasury/transactions/catalog", headers=headers)
    assert resp.status_code == 200
    types = {c["transaction_type"] for c in resp.json()["data"]}
    assert "internal_transfer" in types
    assert "wire_transfer" in types
    assert "loan_disbursement" in types
    assert len(types) == 12


@pytest.mark.asyncio
async def test_workflow_and_posting_rules(client):
    slug = "txnwf"
    headers = await _auth_headers(client, slug)

    workflow = await client.get("/api/v1/treasury/transactions/workflow", headers=headers)
    assert workflow.status_code == 200
    states = {w["status"] for w in workflow.json()["data"]}
    assert "draft" in states
    assert "pending_approval" in states
    assert "executed" in states

    rules = await client.get("/api/v1/treasury/transactions/posting-rules", headers=headers)
    assert rules.status_code == 200
    rule_map = {r["transaction_type"]: r["rule_id"] for r in rules.json()["data"]}
    assert rule_map["bank_transfer"] == "treasury_bank_transfer"
    assert rule_map["investment_purchase"] == "treasury_investment_purchase"


@pytest.mark.asyncio
async def test_internal_transfer_auto_executes(client):
    slug = "txnauto"
    headers = await _auth_headers(client, slug)
    accts = await _provision_accounts(slug)
    cash = accts["MAIN-CASH"]["id"]
    bank = accts["OPERATING-BANK"]["id"]

    resp = await client.post(
        "/api/v1/treasury/transactions",
        headers=headers,
        json={
            "transaction_type": "internal_transfer",
            "amount": 500,
            "currency": "USD",
            "reference": "INT-001",
            "from_account_id": cash,
            "to_account_id": bank,
            "auto_submit": True,
        },
    )
    assert resp.status_code == 201
    data = resp.json()["data"]
    assert data["status"] == "executed"
    assert data["posting_rule_id"] == "treasury_internal_transfer"


@pytest.mark.asyncio
async def test_wire_transfer_requires_approval(client):
    slug = "txnwire"
    headers = await _auth_headers(client, slug)
    accts = await _provision_accounts(slug)
    bank = accts["OPERATING-BANK"]["id"]
    cash = accts["MAIN-CASH"]["id"]

    create = await client.post(
        "/api/v1/treasury/transactions",
        headers=headers,
        json={
            "transaction_type": "wire_transfer",
            "amount": 5000,
            "currency": "USD",
            "reference": "WIRE-001",
            "from_account_id": bank,
            "to_account_id": cash,
        },
    )
    assert create.status_code == 201
    txn_id = create.json()["data"]["id"]

    submit = await client.post(
        f"/api/v1/treasury/transactions/{txn_id}/submit",
        headers=headers,
    )
    assert submit.status_code == 200
    assert submit.json()["data"]["status"] == "pending_approval"

    approve = await client.post(
        f"/api/v1/treasury/transactions/{txn_id}/approve",
        headers=headers,
        json={"comment": "Approved wire"},
    )
    assert approve.status_code == 200
    assert approve.json()["data"]["status"] == "executed"


@pytest.mark.asyncio
async def test_transaction_gl_posting(client):
    slug = "txnpost"
    headers = await _auth_headers(client, slug)
    kernel = get_financial_kernel_service()
    await kernel.handle_tenant_provisioned({"tenant_id": slug, "payload": {"industry_pack": "hospital"}})
    accts = await _provision_accounts(slug)
    cash = accts["MAIN-CASH"]["id"]
    bank = accts["OPERATING-BANK"]["id"]

    resp = await client.post(
        "/api/v1/treasury/transactions",
        headers=headers,
        json={
            "transaction_type": "cash_movement",
            "amount": 250,
            "currency": "USD",
            "reference": "CASH-001",
            "from_account_id": cash,
            "to_account_id": bank,
            "auto_submit": True,
        },
    )
    assert resp.status_code == 201
    txn_id = resp.json()["data"]["id"]

    journals = await client.get("/api/v1/financial-kernel/ledger/journals", headers=headers)
    posted = [
        j for j in journals.json()["data"]
        if j.get("source_context") == "treasury" and j.get("source_document_id") == txn_id
    ]
    assert len(posted) == 1
    assert posted[0]["status"] == "posted"


@pytest.mark.asyncio
async def test_transaction_dashboard(client):
    slug = "txndash"
    headers = await _auth_headers(client, slug)
    accts = await _provision_accounts(slug)
    cash = accts["MAIN-CASH"]["id"]
    bank = accts["OPERATING-BANK"]["id"]

    await client.post(
        "/api/v1/treasury/transactions",
        headers=headers,
        json={
            "transaction_type": "fund_allocation",
            "amount": 100,
            "currency": "USD",
            "reference": "ALLOC-1",
            "from_account_id": cash,
            "to_account_id": bank,
            "auto_submit": True,
        },
    )

    dash = await client.get("/api/v1/treasury/transactions/dashboard", headers=headers)
    assert dash.status_code == 200
    data = dash.json()["data"]
    assert data["summary"]["transaction_count"] >= 1
    assert "posting_rules" in data
    assert "workflow_states" in data


@pytest.mark.asyncio
async def test_loan_disbursement_and_repayment(client):
    slug = "txnloan"
    headers = await _auth_headers(client, slug)
    accts = await _provision_accounts(slug)
    bank = accts["OPERATING-BANK"]["id"]

    disburse = await client.post(
        "/api/v1/treasury/transactions",
        headers=headers,
        json={
            "transaction_type": "loan_disbursement",
            "amount": 10000,
            "currency": "USD",
            "reference": "LOAN-DISB-1",
            "to_account_id": bank,
            "auto_submit": True,
        },
    )
    assert disburse.status_code == 201
    assert disburse.json()["data"]["posting_rule_id"] == "treasury_loan_disbursement"

    repay = await client.post(
        "/api/v1/treasury/transactions",
        headers=headers,
        json={
            "transaction_type": "loan_repayment",
            "amount": 2000,
            "currency": "USD",
            "reference": "LOAN-REP-1",
            "from_account_id": bank,
            "auto_submit": True,
        },
    )
    assert repay.status_code == 201
    assert repay.json()["data"]["posting_rule_id"] == "treasury_loan_repayment"
