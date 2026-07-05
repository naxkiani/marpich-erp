"""Loan Management tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.banking.container import (
    get_banking_customer_account_service,
    get_banking_loan_management_service,
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
    get_banking_loan_management_service()
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
        json={"email": "loan@bank.dev", "password": "SecurePass123!", "display_name": "Loan Ops"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "loan@bank.dev", "password": "SecurePass123!"},
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
    await get_banking_loan_management_service().handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {}}
    )


async def _onboard_and_open_loan_account(client: AsyncClient, headers: dict) -> str:
    customer = await client.post(
        "/api/v1/banking/customers",
        headers=headers,
        json={
            "customer_type": "individual",
            "display_name": "Loan Borrower",
            "legal_name": "Loan Borrower",
            "email": "borrower@test",
            "phone": "+15551238888",
            "auto_submit": True,
        },
    )
    assert customer.status_code == 201
    cid = customer.json()["data"]["id"]
    await client.post(f"/api/v1/banking/customers/{cid}/approve", headers=headers)

    kyc = await client.post(
        f"/api/v1/banking/customers/{cid}/kyc",
        headers=headers,
        json={"tier": "tier1", "document_type": "passport", "document_ref": "P777666"},
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
        json={"customer_id": cid, "product_code": "LOAN-PER", "opening_balance": 0.0},
    )
    assert account.status_code == 201
    account_id = account.json()["data"]["id"]
    approved = await client.post(f"/api/v1/banking/accounts/{account_id}/approve", headers=headers)
    assert approved.status_code == 200
    assert approved.json()["data"]["kernel_linked"] is True
    return account_id


@pytest.mark.asyncio
async def test_loan_catalog(client):
    slug = "loancat"
    headers = await _auth_headers(client, slug)
    resp = await client.get("/api/v1/banking/loans/catalog", headers=headers)
    assert resp.status_code == 200
    caps = {c["capability"] for c in resp.json()["data"]}
    assert "personal" in caps
    assert "business" in caps
    assert "education" in caps
    assert "construction" in caps
    assert "mortgage" in caps
    assert "microfinance" in caps
    assert "agriculture" in caps
    assert "loan_origination" in caps
    assert "approval_workflow" in caps
    assert "collateral" in caps
    assert "guarantors" in caps
    assert "repayment_schedule" in caps
    assert "installments" in caps
    assert "penalty_rules" in caps
    assert "restructuring" in caps
    assert "settlement" in caps
    assert "early_closure" in caps
    assert "automatic_gl_posting" in caps
    assert "ai_credit_risk_analysis" in caps
    assert "audit_trail" in caps


@pytest.mark.asyncio
async def test_personal_loan_lifecycle(client):
    slug = "loanlife"
    headers = await _auth_headers(client, slug)
    await _provision(slug)
    account_id = await _onboard_and_open_loan_account(client, headers)

    applied = await client.post(
        "/api/v1/banking/loans/apply",
        headers=headers,
        json={
            "account_id": account_id,
            "loan_type": "personal",
            "principal": 50000.0,
            "tenure_months": 12,
        },
    )
    assert applied.status_code == 201
    loan = applied.json()["data"]
    loan_id = loan["id"]
    assert loan["status"] == "draft"
    assert loan["emi_amount"] > 0

    submitted = await client.post(f"/api/v1/banking/loans/{loan_id}/submit", headers=headers)
    assert submitted.status_code == 200
    assert submitted.json()["data"]["status"] == "pending_approval"

    approved = await client.post(
        f"/api/v1/banking/loans/{loan_id}/approve",
        headers=headers,
        json={"approver_id": "credit-officer"},
    )
    assert approved.status_code == 200
    assert approved.json()["data"]["status"] == "approved"

    collateral = await client.post(
        f"/api/v1/banking/loans/{loan_id}/collateral",
        headers=headers,
        json={
            "collateral_type": "vehicle",
            "description": "2022 sedan",
            "estimated_value": 30000.0,
        },
    )
    assert collateral.status_code == 201

    guarantor = await client.post(
        f"/api/v1/banking/loans/{loan_id}/guarantors",
        headers=headers,
        json={
            "guarantor_name": "Jane Doe",
            "guarantor_id_ref": "ID-998877",
            "relationship": "spouse",
        },
    )
    assert guarantor.status_code == 201

    risk = await client.post(
        f"/api/v1/banking/loans/{loan_id}/credit-risk",
        headers=headers,
        json={"monthly_income": 8000.0, "existing_obligations": 500.0},
    )
    assert risk.status_code == 201
    analysis = risk.json()["data"]
    assert "risk_score" in analysis
    assert "risk_grade" in analysis
    assert "recommendation" in analysis

    disbursed = await client.post(
        f"/api/v1/banking/loans/{loan_id}/disburse",
        headers=headers,
        json={"approver_id": "disbursement-officer"},
    )
    assert disbursed.status_code == 200
    assert disbursed.json()["data"]["status"] == "active"

    schedule = await client.get(f"/api/v1/banking/loans/{loan_id}/schedule", headers=headers)
    assert schedule.status_code == 200
    installments = schedule.json()["data"]
    assert len(installments) == 12
    first = installments[0]

    paid = await client.post(
        f"/api/v1/banking/loans/{loan_id}/installments/pay",
        headers=headers,
        json={"installment_id": first["id"], "days_overdue": 5},
    )
    assert paid.status_code == 200
    assert paid.json()["data"]["penalty_amount"] > 0

    detail = await client.get(f"/api/v1/banking/loans/{loan_id}", headers=headers)
    assert detail.status_code == 200
    assert detail.json()["data"]["credit_risk"] is not None
    assert len(detail.json()["data"]["installments"]) == 12

    audit = await client.get(f"/api/v1/banking/loans/{loan_id}/audit", headers=headers)
    assert audit.status_code == 200
    actions = {e["action"] for e in audit.json()["data"]}
    assert "loan.applied" in actions
    assert "loan.disbursed" in actions
    assert "credit_risk.analyzed" in actions
    assert "installment.paid" in actions


@pytest.mark.asyncio
async def test_loan_dashboard(client):
    slug = "loandash"
    headers = await _auth_headers(client, slug)
    await _provision(slug)
    account_id = await _onboard_and_open_loan_account(client, headers)

    await client.post(
        "/api/v1/banking/loans/apply",
        headers=headers,
        json={
            "account_id": account_id,
            "loan_type": "microfinance",
            "principal": 5000.0,
            "tenure_months": 6,
        },
    )

    dash = await client.get("/api/v1/banking/loans/dashboard", headers=headers)
    assert dash.status_code == 200
    data = dash.json()["data"]
    assert data["summary"]["loan_count"] >= 1
    assert "total_outstanding" in data["summary"]
