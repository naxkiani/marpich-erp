"""Enterprise Chart of Accounts tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.financial_kernel.container import get_financial_kernel_service, reset_financial_kernel_service
from contexts.financial_kernel.domain.services.coa_tree_service import flatten_tree
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
        json={"email": "coa@kernel.dev", "password": "SecurePass123!", "display_name": "COA Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "coa@kernel.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_hierarchical_coa_on_provision():
    svc = get_financial_kernel_service()
    await svc.handle_tenant_provisioned(
        {"tenant_id": "coa-hosp", "payload": {"industry_pack": "hospital"}}
    )
    tree = (await svc.get_account_tree("coa-hosp")).unwrap()
    flat = flatten_tree(tree)
    keys = {n["account_key"] for n in flat}
    assert "assets" in keys
    assert "patient_receivables" in keys
    assert "patient_service_revenue" in keys
    assert any(n["level"] == 0 for n in flat)
    assert any(n["level"] == 1 for n in flat)


@pytest.mark.asyncio
async def test_apply_template_with_custom_codes(client):
    slug = "coa-custom"
    headers = await _auth_headers(client, slug)
    resp = await client.post(
        "/api/v1/financial-kernel/coa/templates/apply",
        headers=headers,
        json={
            "template_key": "coa.retail",
            "template_type": "industry",
            "code_overrides": {
                "sales_revenue": "REV-CUSTOM",
                "pos_cash": "CASH-POS",
            },
        },
    )
    assert resp.status_code == 201
    data = resp.json()["data"]
    flat = flatten_tree(data["tree"])
    codes = {n["code"] for n in flat if n.get("account_key")}
    assert "REV-CUSTOM" in codes
    assert "CASH-POS" in codes


@pytest.mark.asyncio
async def test_unlimited_depth_child_accounts(client):
    slug = "coa-depth"
    headers = await _auth_headers(client, slug)
    await client.post(
        "/api/v1/financial-kernel/coa/templates/apply",
        headers=headers,
        json={"template_key": "coa.retail", "template_type": "industry"},
    )
    tree = (await client.get("/api/v1/financial-kernel/coa/tree", headers=headers)).json()["data"]
    assets = next(n for n in tree if n["account_key"] == "assets")
    level1 = await client.post(
        "/api/v1/financial-kernel/coa/accounts",
        headers=headers,
        json={
            "code": "SUB1",
            "name": "Sub Group",
            "account_category": "asset",
            "account_key": "sub_group",
            "parent_account_id": assets["id"],
            "is_posting": False,
        },
    )
    assert level1.status_code == 201
    level2 = await client.post(
        "/api/v1/financial-kernel/coa/accounts",
        headers=headers,
        json={
            "code": "LEAF1",
            "name": "Deep Leaf",
            "account_category": "asset",
            "account_key": "deep_leaf",
            "parent_account_id": level1.json()["data"]["id"],
        },
    )
    assert level2.status_code == 201
    assert level2.json()["data"]["level"] == 2


@pytest.mark.asyncio
async def test_country_template_overlay(client):
    slug = "coa-country"
    headers = await _auth_headers(client, slug)
    await client.post(
        "/api/v1/financial-kernel/coa/templates/apply",
        headers=headers,
        json={"template_key": "coa.retail", "template_type": "industry"},
    )
    overlay = await client.post(
        "/api/v1/financial-kernel/coa/templates/apply",
        headers=headers,
        json={
            "template_key": "coa.country.us_gaap",
            "template_type": "country",
            "merge": True,
        },
    )
    assert overlay.status_code == 201
    resolve = await client.get(
        "/api/v1/financial-kernel/coa/resolve/retained_earnings",
        headers=headers,
    )
    assert resolve.status_code == 200
    assert resolve.json()["data"]["code"] == "RE-US"


@pytest.mark.asyncio
async def test_posting_blocked_on_summary_account(client):
    slug = "coa-summary"
    headers = await _auth_headers(client, slug)
    await get_financial_kernel_service().handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {"industry_pack": "hospital"}}
    )
    tree = (await get_financial_kernel_service().get_account_tree(slug)).unwrap()
    assets = next(n for n in tree if n["account_key"] == "assets")
    cash_code = (
        await get_financial_kernel_service().resolve_account_code(slug, "cash")
    ).unwrap()
    rev_code = (
        await get_financial_kernel_service().resolve_account_code(slug, "patient_service_revenue")
    ).unwrap()

    blocked = await client.post(
        "/api/v1/financial-kernel/ledger/journals/automatic",
        headers=headers,
        json={
            "source_context": "hospital",
            "source_document_id": "bad-post",
            "lines": [
                {"account_code": assets["code"], "debit": 100, "credit": 0},
                {"account_code": rev_code, "debit": 0, "credit": 100},
            ],
        },
    )
    assert blocked.status_code == 400
    assert "non_posting_account" in blocked.json()["detail"]

    ok = await client.post(
        "/api/v1/financial-kernel/ledger/journals/automatic",
        headers=headers,
        json={
            "source_context": "hospital",
            "source_document_id": "good-post",
            "lines": [
                {"account_code": cash_code, "debit": 100, "credit": 0},
                {"account_code": rev_code, "debit": 0, "credit": 100},
            ],
        },
    )
    assert ok.status_code == 201


@pytest.mark.asyncio
async def test_list_templates(client):
    headers = await _auth_headers(client, "coa-tmpl")
    resp = await client.get("/api/v1/financial-kernel/coa/templates", headers=headers)
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert any(t["template_key"] == "coa.healthcare" for t in data["industry"])
    assert any(t["template_key"] == "coa.country.ir_ifrs" for t in data["country"])
