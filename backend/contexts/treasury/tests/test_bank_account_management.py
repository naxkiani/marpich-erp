"""Enterprise Bank Account Management tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.treasury.container import get_bank_account_service, reset_treasury_service
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from core.presentation.api.main import app


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    reset_treasury_service()
    get_bank_account_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "bank@treasury.dev", "password": "SecurePass123!", "display_name": "Bank Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "bank@treasury.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_bank_account_catalog(client):
    slug = "bankcat"
    headers = await _auth_headers(client, slug)
    resp = await client.get("/api/v1/treasury/bank-accounts/catalog", headers=headers)
    assert resp.status_code == 200
    caps = {c["capability"] for c in resp.json()["data"]}
    assert "unlimited_banks" in caps
    assert "account_types" in caps
    assert "secure_masking" in caps


@pytest.mark.asyncio
async def test_bank_branch_account_lifecycle(client):
    slug = "banklife"
    headers = await _auth_headers(client, slug)
    org_id = "org-hq"

    bank = await client.post(
        "/api/v1/treasury/banks",
        headers=headers,
        json={
            "code": "CHASE",
            "name": "Chase Bank",
            "country": "US",
            "organization_id": org_id,
            "swift_bic": "CHASUS33",
        },
    )
    assert bank.status_code == 201
    bank_id = bank.json()["data"]["id"]

    branch = await client.post(
        f"/api/v1/treasury/banks/{bank_id}/branches",
        headers=headers,
        json={
            "code": "NYC-01",
            "name": "New York Main",
            "routing_number": "021000021",
            "organization_id": org_id,
        },
    )
    assert branch.status_code == 201
    branch_id = branch.json()["data"]["id"]

    account = await client.post(
        "/api/v1/treasury/bank-accounts",
        headers=headers,
        json={
            "bank_id": bank_id,
            "branch_id": branch_id,
            "code": "OP-CURRENT-01",
            "name": "Operating Current",
            "account_type": "current",
            "currency": "USD",
            "organization_id": org_id,
            "iban": "US64SVBKUS6S3300958879",
            "account_number": "1234567890",
            "gl_account_code": "1100",
        },
    )
    assert account.status_code == 201
    acct = account.json()["data"]
    assert acct["status"] == "draft"
    assert acct["iban"].startswith("*")
    account_id = acct["id"]

    submit = await client.post(
        f"/api/v1/treasury/bank-accounts/{account_id}/submit",
        headers=headers,
    )
    assert submit.status_code == 200
    assert submit.json()["data"]["status"] == "pending_approval"

    approve = await client.post(
        f"/api/v1/treasury/bank-accounts/{account_id}/approve",
        headers=headers,
        json={},
    )
    assert approve.status_code == 200
    assert approve.json()["data"]["status"] == "active"


@pytest.mark.asyncio
async def test_signatories_and_documents(client):
    slug = "banksig"
    headers = await _auth_headers(client, slug)

    bank = await client.post(
        "/api/v1/treasury/banks",
        headers=headers,
        json={"code": "HSBC", "name": "HSBC", "swift_bic": "HBUKGB4B"},
    )
    bank_id = bank.json()["data"]["id"]

    account = await client.post(
        "/api/v1/treasury/bank-accounts",
        headers=headers,
        json={
            "bank_id": bank_id,
            "code": "ESCROW-01",
            "name": "Escrow Account",
            "account_type": "escrow",
            "currency": "EUR",
            "require_approval": False,
        },
    )
    account_id = account.json()["data"]["id"]

    sig = await client.post(
        f"/api/v1/treasury/bank-accounts/{account_id}/signatories",
        headers=headers,
        json={"name": "Jane CFO", "role": "primary_signatory", "authority_limit": 50000},
    )
    assert sig.status_code == 201
    sig_id = sig.json()["data"]["id"]

    sig_approve = await client.post(
        f"/api/v1/treasury/bank-accounts/signatories/{sig_id}/approve",
        headers=headers,
    )
    assert sig_approve.status_code == 200
    assert sig_approve.json()["data"]["status"] == "approved"

    doc = await client.post(
        f"/api/v1/treasury/bank-accounts/{account_id}/documents",
        headers=headers,
        json={"document_type": "kyc", "reference": "KYC-2025-001", "file_name": "kyc.pdf"},
    )
    assert doc.status_code == 201
    doc_id = doc.json()["data"]["id"]

    verify = await client.post(
        f"/api/v1/treasury/bank-accounts/documents/{doc_id}/verify",
        headers=headers,
    )
    assert verify.status_code == 200
    assert verify.json()["data"]["status"] == "verified"


@pytest.mark.asyncio
async def test_multi_organization_filter(client):
    slug = "bankorg"
    headers = await _auth_headers(client, slug)

    await client.post(
        "/api/v1/treasury/banks",
        headers=headers,
        json={"code": "BANK-A", "name": "Bank A", "organization_id": "org-a"},
    )
    await client.post(
        "/api/v1/treasury/banks",
        headers=headers,
        json={"code": "BANK-B", "name": "Bank B", "organization_id": "org-b"},
    )

    all_banks = await client.get("/api/v1/treasury/banks", headers=headers)
    assert len(all_banks.json()["data"]) == 2

    org_a = await client.get("/api/v1/treasury/banks?organization_id=org-a", headers=headers)
    assert len(org_a.json()["data"]) == 1
    assert org_a.json()["data"][0]["code"] == "BANK-A"


@pytest.mark.asyncio
async def test_invalid_iban_rejected(client):
    slug = "bankbad"
    headers = await _auth_headers(client, slug)

    bank = await client.post(
        "/api/v1/treasury/banks",
        headers=headers,
        json={"code": "BAD", "name": "Bad Bank"},
    )
    bank_id = bank.json()["data"]["id"]

    resp = await client.post(
        "/api/v1/treasury/bank-accounts",
        headers=headers,
        json={
            "bank_id": bank_id,
            "code": "BAD-01",
            "name": "Bad Account",
            "account_type": "current",
            "iban": "NOT-A-VALID-IBAN",
        },
    )
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_account_types_supported(client):
    slug = "banktypes"
    headers = await _auth_headers(client, slug)
    bank = await client.post(
        "/api/v1/treasury/banks",
        headers=headers,
        json={"code": "TYPE", "name": "Type Bank"},
    )
    bank_id = bank.json()["data"]["id"]

    for atype in ("current", "savings", "investment", "loan", "escrow", "virtual"):
        resp = await client.post(
            "/api/v1/treasury/bank-accounts",
            headers=headers,
            json={
                "bank_id": bank_id,
                "code": f"ACC-{atype[:4].upper()}",
                "name": f"{atype} account",
                "account_type": atype,
                "require_approval": False,
            },
        )
        assert resp.status_code == 201, atype
        assert resp.json()["data"]["account_type"] == atype
