"""Enterprise account type tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.financial_kernel.container import get_financial_kernel_service, reset_financial_kernel_service
from contexts.financial_kernel.domain.services.account_type_engine import (
    apply_credit_to_balance,
    apply_debit_to_balance,
    get_posting_rule,
    list_account_types,
)
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from core.presentation.api.main import app


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    reset_financial_kernel_service()
    get_financial_kernel_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "types@kernel.dev", "password": "SecurePass123!", "display_name": "Types Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "types@kernel.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


def test_all_account_types_registered():
    types = {t["account_type"] for t in list_account_types()}
    expected = {
        "asset", "liability", "equity", "revenue", "expense",
        "contra_asset", "contra_liability", "contra_revenue", "contra_expense",
        "memorandum", "suspense", "control", "bank", "cash", "tax", "payroll",
        "project", "grant", "student", "patient", "customer", "vendor",
    }
    assert expected == types


def test_contra_asset_credit_normal_balance():
    rule = get_posting_rule("contra_asset")
    assert rule.normal_balance == "credit"
    assert rule.is_contra is True
    bal = apply_credit_to_balance("contra_asset", 0, 100)
    assert bal == 100
    bal = apply_debit_to_balance("contra_asset", bal, 25)
    assert bal == 75


def test_memorandum_blocks_gl_posting():
    rule = get_posting_rule("memorandum")
    assert rule.gl_posting_allowed is False


@pytest.mark.asyncio
async def test_account_types_api(client):
    headers = await _auth_headers(client, "types-api")
    resp = await client.get("/api/v1/financial-kernel/coa/account-types", headers=headers)
    assert resp.status_code == 200
    assert len(resp.json()["data"]) == 22


@pytest.mark.asyncio
async def test_bank_account_type_posting_rules(client):
    headers = await _auth_headers(client, "types-bank")
    resp = await client.get(
        "/api/v1/financial-kernel/coa/account-types/bank/posting-rules",
        headers=headers,
    )
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["reconciliation_required"] is True
    assert data["is_control_account"] is True
    assert data["requires_subledger"] is True


@pytest.mark.asyncio
async def test_create_patient_account_type(client):
    slug = "types-patient"
    headers = await _auth_headers(client, slug)
    await client.post(
        "/api/v1/financial-kernel/coa/templates/apply",
        headers=headers,
        json={"template_key": "coa.enterprise", "template_type": "industry"},
    )
    tree = (await client.get("/api/v1/financial-kernel/coa/tree", headers=headers)).json()["data"]
    from contexts.financial_kernel.domain.services.coa_tree_service import flatten_tree

    receivables = next(n for n in flatten_tree(tree) if n["account_key"] == "receivables")
    resp = await client.post(
        "/api/v1/financial-kernel/coa/accounts",
        headers=headers,
        json={
            "code": "1101",
            "name": "Patient AR Sub",
            "account_category": "asset",
            "account_type": "patient",
            "parent_account_id": receivables["id"],
        },
    )
    assert resp.status_code == 201
    data = resp.json()["data"]
    assert data["account_type"] == "patient"
    assert data["posting_rule"]["requires_subledger"] is True


@pytest.mark.asyncio
async def test_memorandum_account_rejects_posting(client):
    slug = "types-memo"
    headers = await _auth_headers(client, slug)
    svc = get_financial_kernel_service()
    await svc.handle_tenant_provisioned({"tenant_id": slug, "payload": {"industry_pack": "hospital"}})
    rev = (await svc.resolve_account_code(slug, "patient_service_revenue")).unwrap()
    create = await svc.create_account(
        tenant_id=slug,
        code="MEMO-01",
        name="Memo Account",
        account_category="off_balance",
        account_type="memorandum",
        is_posting=False,
    )
    assert create.succeeded
    memo_code = create.unwrap()["code"]
    assert "non_posting" in (
        await client.post(
            "/api/v1/financial-kernel/ledger/journals/automatic",
            headers=headers,
            json={
                "source_context": "test",
                "source_document_id": "memo-post",
                "lines": [
                    {"account_code": memo_code, "debit": 50, "credit": 0},
                    {"account_code": rev, "debit": 0, "credit": 50},
                ],
            },
        )
    ).json()["detail"]
