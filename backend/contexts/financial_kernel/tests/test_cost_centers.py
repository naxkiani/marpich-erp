"""Enterprise Cost Centers tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.financial_kernel.container import get_cost_center_service, get_financial_kernel_service, reset_financial_kernel_service
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from core.presentation.api.main import app


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    reset_financial_kernel_service()
    get_cost_center_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "cc@kernel.dev", "password": "SecurePass123!", "display_name": "CC Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "cc@kernel.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_create_all_center_types(client):
    slug = "cc-types"
    headers = await _auth_headers(client, slug)
    for center_type in (
        "department",
        "project",
        "branch",
        "faculty",
        "hospital_ward",
        "construction_site",
        "warehouse",
        "business_unit",
    ):
        resp = await client.post(
            "/api/v1/financial-kernel/cost-centers",
            headers=headers,
            json={"code": center_type[:3].upper(), "name": center_type.replace("_", " ").title(), "center_type": center_type},
        )
        assert resp.status_code == 201, center_type
        assert resp.json()["data"]["center_type"] == center_type


@pytest.mark.asyncio
async def test_profit_center_and_hierarchy(client):
    slug = "cc-hierarchy"
    headers = await _auth_headers(client, slug)

    bu = await client.post(
        "/api/v1/financial-kernel/cost-centers",
        headers=headers,
        json={"code": "BU01", "name": "Retail Division", "center_type": "business_unit"},
    )
    bu_id = bu.json()["data"]["id"]

    pc = await client.post(
        "/api/v1/financial-kernel/cost-centers/profit-centers",
        headers=headers,
        json={"code": "PC01", "name": "Store Profit", "business_unit_id": bu_id},
    )
    assert pc.status_code == 201
    pc_id = pc.json()["data"]["id"]

    dept = await client.post(
        "/api/v1/financial-kernel/cost-centers",
        headers=headers,
        json={
            "code": "DEPT01",
            "name": "Sales Dept",
            "center_type": "department",
            "parent_id": bu_id,
            "profit_center_id": pc_id,
        },
    )
    assert dept.status_code == 201
    assert dept.json()["data"]["parent_id"] == bu_id

    list_pc = await client.get("/api/v1/financial-kernel/cost-centers/profit-centers/list", headers=headers)
    assert list_pc.status_code == 200
    assert len(list_pc.json()["data"]) == 1


@pytest.mark.asyncio
async def test_budget_expense_revenue_allocations(client):
    slug = "cc-alloc"
    headers = await _auth_headers(client, slug)

    await client.post(
        "/api/v1/financial-kernel/cost-centers",
        headers=headers,
        json={"code": "WARD1", "name": "ICU Ward", "center_type": "hospital_ward"},
    )

    for alloc_type in ("budget", "expense", "revenue"):
        resp = await client.post(
            "/api/v1/financial-kernel/cost-centers/allocations",
            headers=headers,
            json={
                "allocation_type": alloc_type,
                "source_context": "hospital",
                "source_document_id": f"enc-{alloc_type}",
                "cost_center_code": "WARD1",
                "account_code": "5100",
                "amount": 1000,
            },
        )
        assert resp.status_code == 201, alloc_type
        assert resp.json()["data"]["allocation_type"] == alloc_type

    split = await client.post(
        "/api/v1/financial-kernel/cost-centers/allocations/split",
        headers=headers,
        json={
            "allocation_type": "expense",
            "source_context": "construction",
            "source_document_id": "proj-1",
            "account_code": "5200",
            "total_amount": 300,
            "cost_center_codes": ["WARD1"],
            "weights": [1],
        },
    )
    assert split.status_code == 201


@pytest.mark.asyncio
async def test_split_allocation_across_centers(client):
    slug = "cc-split"
    headers = await _auth_headers(client, slug)

    for code, ctype in (("SITE1", "construction_site"), ("WH01", "warehouse")):
        await client.post(
            "/api/v1/financial-kernel/cost-centers",
            headers=headers,
            json={"code": code, "name": code, "center_type": ctype},
        )

    split = await client.post(
        "/api/v1/financial-kernel/cost-centers/allocations/split",
        headers=headers,
        json={
            "allocation_type": "budget",
            "source_context": "finance",
            "source_document_id": "budget-q1",
            "account_code": "5000",
            "total_amount": 1000,
            "cost_center_codes": ["SITE1", "WH01"],
            "weights": [60, 40],
        },
    )
    assert split.status_code == 201
    parts = split.json()["data"]
    assert len(parts) == 2
    assert parts[0]["amount"] == 600
    assert parts[1]["amount"] == 400


@pytest.mark.asyncio
async def test_profitability_analysis(client):
    slug = "cc-profit"
    headers = await _auth_headers(client, slug)

    svc = get_financial_kernel_service()
    await svc.handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {"industry_pack": "hospital"}}
    )
    expense = (await svc.resolve_account_code(slug, "clinical_staff")).unwrap()
    revenue = (await svc.resolve_account_code(slug, "patient_service_revenue")).unwrap()
    cash = (await svc.resolve_account_code(slug, "cash")).unwrap()

    await client.post(
        "/api/v1/financial-kernel/cost-centers",
        headers=headers,
        json={"code": "ER", "name": "Emergency Room", "center_type": "hospital_ward"},
    )

    await client.post(
        "/api/v1/financial-kernel/journals",
        headers=headers,
        json={
            "source_context": "hospital",
            "source_document_id": "enc-1",
            "lines": [
                {"account_code": expense, "debit": 200, "credit": 0, "cost_center": "ER"},
                {"account_code": cash, "debit": 0, "credit": 200},
            ],
        },
    )
    await client.post(
        "/api/v1/financial-kernel/journals",
        headers=headers,
        json={
            "source_context": "hospital",
            "source_document_id": "bill-1",
            "lines": [
                {"account_code": cash, "debit": 500, "credit": 0, "cost_center": "ER"},
                {"account_code": revenue, "debit": 0, "credit": 500, "cost_center": "ER"},
            ],
        },
    )

    analysis = await client.get(
        "/api/v1/financial-kernel/cost-centers/profitability",
        headers=headers,
        params={"cost_center_code": "ER"},
    )
    assert analysis.status_code == 200
    data = analysis.json()["data"]
    assert data["revenue"] == 500
    assert data["expenses"] == 200
    assert data["profit"] == 300

    rollup = await client.get("/api/v1/financial-kernel/cost-centers/profitability", headers=headers)
    assert rollup.status_code == 200
    assert "summary" in rollup.json()["data"]
    assert "centers" in rollup.json()["data"]
