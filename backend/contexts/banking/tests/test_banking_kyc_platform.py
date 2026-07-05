"""Enterprise KYC Platform tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.banking.container import (
    get_banking_customer_account_service,
    get_banking_kyc_platform_service,
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
    get_banking_kyc_platform_service()
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
        json={"email": "kyc@bank.dev", "password": "SecurePass123!", "display_name": "KYC Ops"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "kyc@bank.dev", "password": "SecurePass123!"},
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


async def _create_customer(client: AsyncClient, headers: dict) -> str:
    resp = await client.post(
        "/api/v1/banking/customers",
        headers=headers,
        json={
            "customer_type": "individual",
            "display_name": "John Smith",
            "legal_name": "John Smith",
            "email": "john@kyc.test",
            "phone": "+15551230001",
            "auto_submit": True,
        },
    )
    cid = resp.json()["data"]["id"]
    await client.post(f"/api/v1/banking/customers/{cid}/approve", headers=headers)
    return cid


async def _open_case(client: AsyncClient, headers: dict, customer_id: str) -> dict:
    resp = await client.post(
        "/api/v1/banking/kyc/cases",
        headers=headers,
        json={"customer_id": customer_id},
    )
    assert resp.status_code == 201
    return resp.json()["data"]


@pytest.mark.asyncio
async def test_kyc_catalog(client):
    slug = "kyccat"
    headers = await _auth_headers(client, slug)
    resp = await client.get("/api/v1/banking/kyc/catalog", headers=headers)
    assert resp.status_code == 200
    caps = {c["capability"] for c in resp.json()["data"]}
    assert "identity_verification" in caps
    assert "passport" in caps
    assert "national_id" in caps
    assert "business_registration" in caps
    assert "tax_number" in caps
    assert "address_verification" in caps
    assert "risk_classification" in caps
    assert "standard" in caps
    assert "enhanced" in caps
    assert "pep_flag" in caps
    assert "sanctions_screening" in caps
    assert "document_verification" in caps
    assert "biometric_extension" in caps
    assert "workflow_approval" in caps
    assert "periodic_review" in caps
    assert "audit_trail" in caps
    assert "policy_engine_rules" in caps


@pytest.mark.asyncio
async def test_kyc_policy_keys_seeded(client):
    slug = "kycpol"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    keys_resp = await client.get("/api/v1/banking/kyc/policy-keys", headers=headers)
    assert keys_resp.status_code == 200
    keys = {k["key"] for k in keys_resp.json()["data"]}
    assert "kyc.risk.classification" in keys
    assert "kyc.pep.screening" in keys
    assert "kyc.sanctions.screening" in keys

    eval_resp = await client.post(
        "/api/v1/banking/kyc/policies/evaluate",
        headers=headers,
        json={
            "policy_key": "kyc.pep.screening",
            "facts": {"match_score": 0.0, "customer_type": "individual", "role": ""},
        },
    )
    assert eval_resp.status_code == 200


@pytest.mark.asyncio
async def test_full_kyc_case_lifecycle(client):
    slug = "kyclife"
    headers = await _auth_headers(client, slug)
    await _provision(slug)
    customer_id = await _create_customer(client, headers)
    case = await _open_case(client, headers, customer_id)
    case_id = case["id"]

    passport = await client.post(
        f"/api/v1/banking/kyc/cases/{case_id}/documents",
        headers=headers,
        json={
            "document_type": "passport",
            "document_ref": "P9876543",
            "issuing_country": "US",
            "expiry_date": "2030-12-31",
        },
    )
    assert passport.status_code == 201
    doc_id = passport.json()["data"]["id"]

    await client.post(
        f"/api/v1/banking/kyc/documents/{doc_id}/verify",
        headers=headers,
        json={"verified_by": "compliance_officer"},
    )

    address = await client.post(
        f"/api/v1/banking/kyc/cases/{case_id}/addresses",
        headers=headers,
        json={
            "address_line": "123 Main St",
            "city": "New York",
            "country": "US",
            "postal_code": "10001",
        },
    )
    assert address.status_code == 201
    addr_id = address.json()["data"]["id"]
    await client.post(
        f"/api/v1/banking/kyc/addresses/{addr_id}/verify",
        headers=headers,
        json={"verified_by": "compliance_officer"},
    )

    pep = await client.post(
        f"/api/v1/banking/kyc/cases/{case_id}/screening/pep",
        headers=headers,
        json={"match_score": 0.1, "provider_ref": "PEP-SCREEN-1"},
    )
    assert pep.status_code == 200
    assert pep.json()["data"]["status"] == "clear"

    sanctions = await client.post(
        f"/api/v1/banking/kyc/cases/{case_id}/screening/sanctions",
        headers=headers,
        json={"match_score": 0.0, "provider_ref": "SAN-SCREEN-1"},
    )
    assert sanctions.status_code == 200

    risk = await client.post(
        f"/api/v1/banking/kyc/cases/{case_id}/classify-risk", headers=headers
    )
    assert risk.status_code == 200
    assert risk.json()["data"]["risk_class"] == "low"

    submit = await client.post(f"/api/v1/banking/kyc/cases/{case_id}/submit", headers=headers)
    assert submit.status_code == 200
    assert submit.json()["data"]["status"] == "pending_approval"

    approved = await client.post(
        f"/api/v1/banking/kyc/cases/{case_id}/approve",
        headers=headers,
        json={"approver_id": "chief_compliance_officer"},
    )
    assert approved.status_code == 200
    assert approved.json()["data"]["status"] == "approved"
    assert "review" in approved.json()["data"]

    audit = await client.get(f"/api/v1/banking/kyc/cases/{case_id}/audit", headers=headers)
    assert audit.status_code == 200
    actions = {e["action"] for e in audit.json()["data"]}
    assert "case.opened" in actions
    assert "document.verified" in actions
    assert "case.approved" in actions


@pytest.mark.asyncio
async def test_pep_flag_triggers_edd(client):
    slug = "kycpep"
    headers = await _auth_headers(client, slug)
    await _provision(slug)
    customer_id = await _create_customer(client, headers)
    case = await _open_case(client, headers, customer_id)
    case_id = case["id"]

    pep = await client.post(
        f"/api/v1/banking/kyc/cases/{case_id}/screening/pep",
        headers=headers,
        json={"match_score": 0.88, "match_details": {"role": "senior_official"}},
    )
    assert pep.status_code == 200
    assert pep.json()["data"]["status"] == "confirmed"
    assert pep.json()["data"]["case"]["requires_edd"] is True
    assert pep.json()["data"]["case"]["due_diligence_level"] == "enhanced"


@pytest.mark.asyncio
async def test_sanctions_block(client):
    slug = "kycsan"
    headers = await _auth_headers(client, slug)
    await _provision(slug)
    customer_id = await _create_customer(client, headers)
    case = await _open_case(client, headers, customer_id)
    case_id = case["id"]

    doc = await client.post(
        f"/api/v1/banking/kyc/cases/{case_id}/documents",
        headers=headers,
        json={"document_type": "national_id", "document_ref": "NID123"},
    )
    doc_id = doc.json()["data"]["id"]
    await client.post(
        f"/api/v1/banking/kyc/documents/{doc_id}/verify",
        headers=headers,
        json={"verified_by": "officer"},
    )

    await client.post(
        f"/api/v1/banking/kyc/cases/{case_id}/screening/sanctions",
        headers=headers,
        json={"match_score": 0.95, "match_details": {"list_name": "OFAC"}},
    )

    case_detail = await client.get(f"/api/v1/banking/kyc/cases/{case_id}", headers=headers)
    assert case_detail.json()["data"]["sanctions_status"] == "blocked"

    submit = await client.post(f"/api/v1/banking/kyc/cases/{case_id}/submit", headers=headers)
    assert submit.status_code == 400


@pytest.mark.asyncio
async def test_biometric_hook(client):
    slug = "kycbio"
    headers = await _auth_headers(client, slug)
    await _provision(slug)
    customer_id = await _create_customer(client, headers)
    case = await _open_case(client, headers, customer_id)
    case_id = case["id"]

    hook = await client.post(
        f"/api/v1/banking/kyc/cases/{case_id}/biometric",
        headers=headers,
        json={
            "provider": "FaceVerify",
            "hook_ref": "BIO-001",
            "callback_url": "https://example.com/kyc/callback",
        },
    )
    assert hook.status_code == 201
    hook_id = hook.json()["data"]["id"]
    assert hook.json()["data"]["status"] == "pending"

    completed = await client.post(
        f"/api/v1/banking/kyc/biometric/{hook_id}/complete",
        headers=headers,
        json={"status": "verified", "result_payload": {"confidence": 0.98}},
    )
    assert completed.status_code == 200
    assert completed.json()["data"]["status"] == "verified"


@pytest.mark.asyncio
async def test_business_documents(client):
    slug = "kycbiz"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    biz = await client.post(
        "/api/v1/banking/customers",
        headers=headers,
        json={
            "customer_type": "business",
            "display_name": "Acme Ltd",
            "legal_name": "Acme Limited",
            "email": "biz@kyc.test",
            "phone": "+15551230002",
            "auto_submit": True,
        },
    )
    cid = biz.json()["data"]["id"]
    await client.post(f"/api/v1/banking/customers/{cid}/approve", headers=headers)
    case = await _open_case(client, headers, cid)

    for doc_type, ref in [
        ("business_registration", "BR-12345"),
        ("tax_number", "TAX-98765"),
    ]:
        resp = await client.post(
            f"/api/v1/banking/kyc/cases/{case['id']}/documents",
            headers=headers,
            json={"document_type": doc_type, "document_ref": ref},
        )
        assert resp.status_code == 201


@pytest.mark.asyncio
async def test_kyc_dashboard(client):
    slug = "kycdash"
    headers = await _auth_headers(client, slug)
    await _provision(slug)
    customer_id = await _create_customer(client, headers)
    await _open_case(client, headers, customer_id)

    resp = await client.get("/api/v1/banking/kyc/dashboard", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["data"]["summary"]["case_count"] >= 1
    assert "policy_keys" in resp.json()["data"]
