"""Deposit Management tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.banking.container import (
    get_banking_customer_account_service,
    get_banking_deposit_management_service,
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
    get_banking_deposit_management_service()
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
        json={"email": "dep@bank.dev", "password": "SecurePass123!", "display_name": "Deposit Ops"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "dep@bank.dev", "password": "SecurePass123!"},
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
    await get_banking_deposit_management_service().handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {}}
    )


async def _onboard_and_open_account(client: AsyncClient, headers: dict) -> str:
    customer = await client.post(
        "/api/v1/banking/customers",
        headers=headers,
        json={
            "customer_type": "individual",
            "display_name": "Deposit Holder",
            "legal_name": "Deposit Holder",
            "email": "dep.holder@test",
            "phone": "+15551239999",
            "auto_submit": True,
        },
    )
    assert customer.status_code == 201
    cid = customer.json()["data"]["id"]
    await client.post(f"/api/v1/banking/customers/{cid}/approve", headers=headers)

    kyc = await client.post(
        f"/api/v1/banking/customers/{cid}/kyc",
        headers=headers,
        json={"tier": "tier1", "document_type": "passport", "document_ref": "P999888"},
    )
    kyc_id = kyc.json()["data"]["id"]
    await client.post(
        f"/api/v1/banking/kyc/{kyc_id}/verify",
        headers=headers,
        json={"verified_by": "compliance"},
    )

    account = await client.post(
        "/api/v1/banking/accounts",
        headers=headers,
        json={"customer_id": cid, "product_code": "SAV-STD", "opening_balance": 20000.0},
    )
    assert account.status_code == 201
    account_id = account.json()["data"]["id"]
    approved = await client.post(f"/api/v1/banking/accounts/{account_id}/approve", headers=headers)
    assert approved.status_code == 200
    assert approved.json()["data"]["kernel_linked"] is True
    return account_id


@pytest.mark.asyncio
async def test_deposit_catalog(client):
    slug = "depcat"
    headers = await _auth_headers(client, slug)
    resp = await client.get("/api/v1/banking/deposits/catalog", headers=headers)
    assert resp.status_code == 200
    caps = {c["capability"] for c in resp.json()["data"]}
    assert "savings" in caps
    assert "current" in caps
    assert "term" in caps
    assert "recurring" in caps
    assert "profit_distribution_rules" in caps
    assert "interest_calculation" in caps
    assert "interest_accrual" in caps
    assert "maturity" in caps
    assert "renewal" in caps
    assert "early_withdrawal_rules" in caps
    assert "deposit_certificates" in caps
    assert "deposit_statements" in caps
    assert "automatic_gl_posting" in caps
    assert "approval_workflow" in caps
    assert "audit_trail" in caps


@pytest.mark.asyncio
async def test_open_savings_deposit_and_transaction(client):
    slug = "depsav"
    headers = await _auth_headers(client, slug)
    await _provision(slug)
    account_id = await _onboard_and_open_account(client, headers)

    opened = await client.post(
        "/api/v1/banking/deposits/open",
        headers=headers,
        json={"account_id": account_id, "deposit_type": "savings", "principal": 5000.0},
    )
    assert opened.status_code == 201
    deposit = opened.json()["data"]
    assert deposit["deposit_type"] == "savings"
    assert deposit["status"] == "active"
    deposit_id = deposit["id"]

    txn = await client.post(
        "/api/v1/banking/deposits/transactions",
        headers=headers,
        json={"deposit_id": deposit_id, "transaction_type": "deposit", "amount": 1000.0},
    )
    assert txn.status_code == 201
    assert txn.json()["data"]["status"] == "posted"
    assert txn.json()["data"]["kernel_journal_id"] is not None


@pytest.mark.asyncio
async def test_term_deposit_approval_and_maturity(client):
    slug = "depterm"
    headers = await _auth_headers(client, slug)
    await _provision(slug)
    account_id = await _onboard_and_open_account(client, headers)

    opened = await client.post(
        "/api/v1/banking/deposits/open",
        headers=headers,
        json={
            "account_id": account_id,
            "deposit_type": "term",
            "principal": 25000.0,
            "tenure_months": 12,
            "auto_renew": True,
        },
    )
    assert opened.status_code == 201
    assert opened.json()["data"]["status"] == "pending_approval"
    deposit_id = opened.json()["data"]["id"]

    approved = await client.post(
        f"/api/v1/banking/deposits/{deposit_id}/approve",
        headers=headers,
        json={"approver_id": "manager"},
    )
    assert approved.status_code == 200
    assert approved.json()["data"]["status"] == "active"
    assert approved.json()["data"]["maturity_date"] is not None

    matured = await client.post(
        f"/api/v1/banking/deposits/{deposit_id}/maturity",
        headers=headers,
    )
    assert matured.status_code == 200
    data = matured.json()["data"]
    assert data["status"] in {"matured", "active", "renewed"}


@pytest.mark.asyncio
async def test_interest_accrual_and_post(client):
    slug = "depint"
    headers = await _auth_headers(client, slug)
    await _provision(slug)
    account_id = await _onboard_and_open_account(client, headers)

    opened = await client.post(
        "/api/v1/banking/deposits/open",
        headers=headers,
        json={"account_id": account_id, "deposit_type": "savings", "principal": 9000.0},
    )
    deposit_id = opened.json()["data"]["id"]

    await client.post(
        "/api/v1/banking/deposits/transactions",
        headers=headers,
        json={"deposit_id": deposit_id, "transaction_type": "deposit", "amount": 5000.0},
    )

    accrual = await client.post(
        "/api/v1/banking/deposits/interest/accrue",
        headers=headers,
        json={"deposit_id": deposit_id, "days": 30},
    )
    assert accrual.status_code == 200
    assert accrual.json()["data"]["accrued_amount"] > 0

    posted = await client.post(
        "/api/v1/banking/deposits/interest/post",
        headers=headers,
        json={"deposit_id": deposit_id, "approver_id": "system"},
    )
    assert posted.status_code == 200
    assert posted.json()["data"]["status"] == "posted"


@pytest.mark.asyncio
async def test_early_withdrawal_penalty(client):
    slug = "deppen"
    headers = await _auth_headers(client, slug)
    await _provision(slug)
    account_id = await _onboard_and_open_account(client, headers)

    opened = await client.post(
        "/api/v1/banking/deposits/open",
        headers=headers,
        json={
            "account_id": account_id,
            "deposit_type": "term",
            "principal": 30000.0,
            "tenure_months": 6,
        },
    )
    deposit_id = opened.json()["data"]["id"]
    await client.post(
        f"/api/v1/banking/deposits/{deposit_id}/approve",
        headers=headers,
        json={"approver_id": "manager"},
    )

    txn = await client.post(
        "/api/v1/banking/deposits/transactions",
        headers=headers,
        json={"deposit_id": deposit_id, "transaction_type": "withdrawal", "amount": 5000.0},
    )
    assert txn.status_code == 201
    assert txn.json()["data"]["penalty_amount"] > 0
    assert txn.json()["data"]["status"] == "pending"

    approved = await client.post(
        f"/api/v1/banking/deposits/transactions/{txn.json()['data']['id']}/approve",
        headers=headers,
        json={"approver_id": "manager"},
    )
    assert approved.status_code == 200
    assert approved.json()["data"]["status"] == "posted"


@pytest.mark.asyncio
async def test_certificate_statement_audit(client):
    slug = "depdoc"
    headers = await _auth_headers(client, slug)
    await _provision(slug)
    account_id = await _onboard_and_open_account(client, headers)

    opened = await client.post(
        "/api/v1/banking/deposits/open",
        headers=headers,
        json={"account_id": account_id, "deposit_type": "savings", "principal": 8000.0},
    )
    deposit_id = opened.json()["data"]["id"]

    cert = await client.post(
        f"/api/v1/banking/deposits/{deposit_id}/certificate",
        headers=headers,
    )
    assert cert.status_code == 201
    assert cert.json()["data"]["certificate_number"]

    stmt = await client.post(
        f"/api/v1/banking/deposits/{deposit_id}/statement",
        headers=headers,
        json={"period_days": 30},
    )
    assert stmt.status_code == 201
    assert stmt.json()["data"]["statement_ref"]

    audit = await client.get(
        f"/api/v1/banking/deposits/{deposit_id}/audit",
        headers=headers,
    )
    assert audit.status_code == 200
    actions = {e["action"] for e in audit.json()["data"]}
    assert "deposit.opened" in actions
    assert "certificate.issued" in actions
    assert "statement.generated" in actions


@pytest.mark.asyncio
async def test_profit_rules_seeded(client):
    slug = "deprule"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    rules = await client.get("/api/v1/banking/deposits/profit-rules/list", headers=headers)
    assert rules.status_code == 200
    codes = {r["rule_code"] for r in rules.json()["data"]}
    assert "INT-SAV" in codes
    assert "INT-TERM" in codes
    assert "PROFIT-SAV" in codes


@pytest.mark.asyncio
async def test_deposit_dashboard(client):
    slug = "depdash"
    headers = await _auth_headers(client, slug)
    await _provision(slug)
    account_id = await _onboard_and_open_account(client, headers)
    await client.post(
        "/api/v1/banking/deposits/open",
        headers=headers,
        json={"account_id": account_id, "deposit_type": "current", "principal": 1000.0},
    )

    dash = await client.get("/api/v1/banking/deposits/dashboard", headers=headers)
    assert dash.status_code == 200
    summary = dash.json()["data"]["summary"]
    assert summary["deposit_count"] >= 1
