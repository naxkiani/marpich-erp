"""Branch Banking Platform tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.banking.container import (
    get_banking_branch_platform_service,
    get_banking_customer_account_service,
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
    get_banking_branch_platform_service()
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
        json={"email": "branch@bank.dev", "password": "SecurePass123!", "display_name": "Branch Ops"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "branch@bank.dev", "password": "SecurePass123!"},
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
    await get_banking_branch_platform_service().handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {}}
    )


async def _head_office(client: AsyncClient, headers: dict) -> str:
    offices = await client.get("/api/v1/banking/branches/offices", headers=headers)
    assert offices.status_code == 200
    ho = next(o for o in offices.json()["data"] if o["office_type"] == "head_office")
    return ho["id"]


@pytest.mark.asyncio
async def test_branch_catalog(client):
    slug = "brcat"
    headers = await _auth_headers(client, slug)
    resp = await client.get("/api/v1/banking/branches/catalog", headers=headers)
    assert resp.status_code == 200
    caps = {c["capability"] for c in resp.json()["data"]}
    assert "head_office" in caps
    assert "regional_office" in caps
    assert "cash_counter" in caps
    assert "branch_opening" in caps
    assert "vault_management" in caps
    assert "branch_analytics" in caps


@pytest.mark.asyncio
async def test_branch_hierarchy_and_extensions(client):
    slug = "brhier"
    headers = await _auth_headers(client, slug)
    await _provision(slug)
    ho_id = await _head_office(client, headers)

    regional = await client.post(
        "/api/v1/banking/branches/offices",
        headers=headers,
        json={
            "office_type": "regional_office",
            "name": "North Region",
            "code": "REG-N",
            "parent_office_id": ho_id,
            "region": "north",
        },
    )
    assert regional.status_code == 201
    reg_id = regional.json()["data"]["id"]

    branch = await client.post(
        "/api/v1/banking/branches/offices",
        headers=headers,
        json={
            "office_type": "branch",
            "name": "Downtown Branch",
            "code": "BR-DT",
            "parent_office_id": reg_id,
            "region": "north",
        },
    )
    assert branch.status_code == 201
    branch_id = branch.json()["data"]["id"]

    counter = await client.post(
        f"/api/v1/banking/branches/offices/{branch_id}/extensions",
        headers=headers,
        json={"extension_type": "cash_counter", "label": "Counter 1"},
    )
    assert counter.status_code == 201

    atm = await client.post(
        f"/api/v1/banking/branches/offices/{branch_id}/extensions",
        headers=headers,
        json={"extension_type": "atm_extension", "label": "ATM-01", "terminal_id": "ATM001"},
    )
    assert atm.status_code == 201


@pytest.mark.asyncio
async def test_branch_open_close_and_vault(client):
    slug = "brops"
    headers = await _auth_headers(client, slug)
    await _provision(slug)
    branch = await client.post(
        "/api/v1/banking/branches/offices",
        headers=headers,
        json={
            "office_type": "branch",
            "name": "Ops Branch",
            "code": "BR-OPS",
            "parent_office_id": await _head_office(client, headers),
        },
    )
    branch_id = branch.json()["data"]["id"]

    opened = await client.post(
        f"/api/v1/banking/branches/offices/{branch_id}/open",
        headers=headers,
        json={"operator_id": "teller-1", "opening_balance": 5000.0},
    )
    assert opened.status_code == 200
    assert opened.json()["data"]["status"] == "open"

    vault_dep = await client.post(
        f"/api/v1/banking/branches/offices/{branch_id}/vault/movements",
        headers=headers,
        json={"movement_type": "deposit", "amount": 10000.0, "operator_id": "vault-1"},
    )
    assert vault_dep.status_code == 200
    assert vault_dep.json()["data"]["balance"] == 10000.0

    closed = await client.post(
        f"/api/v1/banking/branches/offices/{branch_id}/close",
        headers=headers,
        json={"operator_id": "teller-1", "closing_balance": 15000.0},
    )
    assert closed.status_code == 200
    assert closed.json()["data"]["status"] == "closed"


@pytest.mark.asyncio
async def test_cash_limits_and_assignments(client):
    slug = "brlim"
    headers = await _auth_headers(client, slug)
    await _provision(slug)
    ho_id = await _head_office(client, headers)
    parent_branch = await client.post(
        "/api/v1/banking/branches/offices",
        headers=headers,
        json={
            "office_type": "branch",
            "name": "Parent Branch",
            "code": "BR-PAR",
            "parent_office_id": ho_id,
        },
    )
    parent_id = parent_branch.json()["data"]["id"]

    limit = await client.post(
        f"/api/v1/banking/branches/offices/{parent_id}/cash-limits",
        headers=headers,
        json={"limit_type": "drawer", "max_amount": 8000.0},
    )
    assert limit.status_code == 201

    assign = await client.post(
        f"/api/v1/banking/branches/offices/{parent_id}/assignments",
        headers=headers,
        json={"employee_id": "emp-101", "role": "teller"},
    )
    assert assign.status_code == 201
    assert assign.json()["data"]["active"] is True


@pytest.mark.asyncio
async def test_kpis_dashboard_and_analytics(client):
    slug = "brdash"
    headers = await _auth_headers(client, slug)
    await _provision(slug)
    branch_id = (
        await client.post(
            "/api/v1/banking/branches/offices",
            headers=headers,
            json={
                "office_type": "branch",
                "name": "KPI Branch",
                "code": "BR-KPI",
                "parent_office_id": await _head_office(client, headers),
                "region": "central",
            },
        )
    ).json()["data"]["id"]

    kpi = await client.post(
        f"/api/v1/banking/branches/offices/{branch_id}/kpis",
        headers=headers,
        json={"metric_key": "transaction_volume", "metric_value": 850.0},
    )
    assert kpi.status_code == 201
    assert kpi.json()["data"]["achievement_pct"] is not None

    dash = await client.get("/api/v1/banking/branches/dashboard", headers=headers)
    assert dash.status_code == 200
    assert dash.json()["data"]["office_count"] >= 2
    assert "kpi_summary" in dash.json()["data"]

    analytics = await client.get("/api/v1/banking/branches/analytics", headers=headers)
    assert analytics.status_code == 200
    assert "regional_performance" in analytics.json()["data"]

    audit = await client.get(
        f"/api/v1/banking/branches/offices/{branch_id}/audit", headers=headers
    )
    assert audit.status_code == 200
    actions = {e["action"] for e in audit.json()["data"]}
    assert "office.created" in actions
    assert "kpi.recorded" in actions
