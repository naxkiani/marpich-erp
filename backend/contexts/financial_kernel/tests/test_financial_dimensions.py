"""Enterprise financial dimensions tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.financial_kernel.container import get_financial_kernel_service, reset_financial_kernel_service
from contexts.financial_kernel.domain.services.financial_dimension_engine import (
    DIMENSION_CATALOG,
    enrich_journal_line,
    extract_line_dimensions,
    merge_header_dimensions,
    validate_line_dimensions,
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
        json={"email": "dim@kernel.dev", "password": "SecurePass123!", "display_name": "Dim Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "dim@kernel.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


def test_dimension_catalog_has_all_types():
    assert len(DIMENSION_CATALOG) == 16
    types = set(DIMENSION_CATALOG.keys())
    assert "company" in types
    assert "cost_center" in types
    assert "fund" in types
    assert "grant" in types
    assert "hospital" in types
    assert "ward" in types
    assert "construction_site" in types
    assert "business_unit" in types


def test_enrich_line_merges_legacy_and_unlimited_dimensions():
    line = {
        "account_code": "1000",
        "debit": 100,
        "cost_center": "CC-01",
        "dimensions": {
            "fund": "FUND-A",
            "grant": "G-2025",
            "faculty": "ENG",
            "hospital": "MAIN",
            "ward": "ICU",
            "construction_site": "SITE-1",
            "warehouse": "WH-EAST",
            "country": "US",
            "currency": "USD",
            "business_unit": "BU-RETAIL",
        },
    }
    enriched = enrich_journal_line(line)
    dims = enriched["dimensions"]
    assert dims["cost_center"] == "CC-01"
    assert dims["fund"] == "FUND-A"
    assert dims["grant"] == "G-2025"
    assert len(dims) >= 10


def test_merge_header_dimensions_injects_company_and_branch():
    lines = [{"account_code": "1000", "debit": 50, "credit": 0}]
    merged = merge_header_dimensions(
        lines, organization_id="ACME-CO", branch_id="BR-NYC"
    )
    dims = merged[0]["dimensions"]
    assert dims["company"] == "ACME-CO"
    assert dims["branch"] == "BR-NYC"


def test_validate_line_dimensions_rejects_unknown_code():
    lines = [{"account_code": "1000", "dimensions": {"cost_center": "UNKNOWN"}}]
    lookup = {
        "cost_center": {
            "CC-MAIN": {"code": "CC-MAIN", "is_active": True},
        }
    }
    valid, issues = validate_line_dimensions(lines, lookup=lookup)
    assert valid is False
    assert issues[0]["error"] == "unknown_dimension_code"


@pytest.mark.asyncio
async def test_create_dimension_values_and_list(client):
    slug = "dim-crud"
    headers = await _auth_headers(client, slug)

    catalog = await client.get(
        "/api/v1/financial-kernel/dimensions/catalog", headers=headers
    )
    assert catalog.status_code == 200
    assert len(catalog.json()["data"]) == 16

    for dim_type, code, name in (
        ("cost_center", "CC-MAIN", "Main Cost Center"),
        ("profit_center", "PC-RETAIL", "Retail Profit Center"),
        ("fund", "FUND-OPS", "Operations Fund"),
        ("grant", "GRANT-NIH", "NIH Research Grant"),
        ("faculty", "FAC-ENG", "Engineering Faculty"),
        ("hospital", "HOSP-MAIN", "Main Hospital"),
        ("ward", "WARD-ICU", "ICU Ward"),
    ):
        resp = await client.post(
            "/api/v1/financial-kernel/dimensions/values",
            headers=headers,
            json={"dimension_type": dim_type, "code": code, "name": name},
        )
        assert resp.status_code == 201, resp.text

    listed = await client.get(
        "/api/v1/financial-kernel/dimensions/values",
        headers=headers,
    )
    assert listed.status_code == 200
    assert len(listed.json()["data"]) == 7


@pytest.mark.asyncio
async def test_journal_post_with_unlimited_dimensions(client):
    slug = "dim-journal"
    headers = await _auth_headers(client, slug)
    svc = get_financial_kernel_service()
    await svc.handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {"industry_pack": "hospital"}}
    )
    periods = (await svc.list_periods(slug)).unwrap()
    expense = (await svc.resolve_account_code(slug, "clinical_staff")).unwrap()
    cash = (await svc.resolve_account_code(slug, "cash")).unwrap()

    await svc.create_dimension_value(
        tenant_id=slug,
        dimension_type="cost_center",
        code="CC-CLINIC",
        name="Clinical Cost Center",
    )
    await svc.create_dimension_value(
        tenant_id=slug,
        dimension_type="fund",
        code="FUND-OPS",
        name="Operations Fund",
    )

    post = await client.post(
        "/api/v1/financial-kernel/journals",
        headers=headers,
        json={
            "source_context": "manual",
            "source_document_id": "dim-post-001",
            "lines": [
                {
                    "account_code": expense,
                    "debit": 100,
                    "credit": 0,
                    "dimensions": {
                        "company": "ACME",
                        "branch": "NYC",
                        "department": "CLINICAL",
                        "project": "PRJ-001",
                        "cost_center": "CC-CLINIC",
                        "profit_center": "PC-MAIN",
                        "fund": "FUND-OPS",
                        "grant": "GRANT-A",
                        "faculty": "MED",
                        "hospital": "HOSP-1",
                        "ward": "WARD-A",
                        "construction_site": "SITE-1",
                        "warehouse": "WH-1",
                        "country": "US",
                        "currency": "USD",
                        "business_unit": "BU-HEALTH",
                    },
                },
                {"account_code": cash, "debit": 0, "credit": 100},
            ],
        },
    )
    assert post.status_code == 201, post.text
    journal = post.json()["data"]
    line_dims = journal["lines"][0]["dimensions"]
    assert line_dims["cost_center"] == "CC-CLINIC"
    assert line_dims["fund"] == "FUND-OPS"
    assert line_dims["hospital"] == "HOSP-1"
    assert len(line_dims) >= 15


@pytest.mark.asyncio
async def test_dimension_validation_rejects_unknown_on_post(client):
    slug = "dim-reject"
    headers = await _auth_headers(client, slug)
    svc = get_financial_kernel_service()
    await svc.handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {"industry_pack": "hospital"}}
    )
    expense = (await svc.resolve_account_code(slug, "clinical_staff")).unwrap()
    cash = (await svc.resolve_account_code(slug, "cash")).unwrap()

    await svc.create_dimension_value(
        tenant_id=slug,
        dimension_type="cost_center",
        code="CC-VALID",
        name="Valid Center",
    )

    post = await client.post(
        "/api/v1/financial-kernel/journals",
        headers=headers,
        json={
            "source_context": "manual",
            "source_document_id": "dim-bad-001",
            "lines": [
                {
                    "account_code": expense,
                    "debit": 50,
                    "credit": 0,
                    "cost_center": "CC-INVALID",
                },
                {"account_code": cash, "debit": 0, "credit": 50},
            ],
        },
    )
    assert post.status_code == 400
    assert "dimension" in post.json()["detail"].lower()


@pytest.mark.asyncio
async def test_validate_endpoint_and_audit(client):
    slug = "dim-audit"
    headers = await _auth_headers(client, slug)

    create = await client.post(
        "/api/v1/financial-kernel/dimensions/values",
        headers=headers,
        json={"dimension_type": "department", "code": "DEPT-HR", "name": "Human Resources"},
    )
    value_id = create.json()["data"]["id"]

    validate = await client.post(
        "/api/v1/financial-kernel/dimensions/validate",
        headers=headers,
        json={
            "lines": [
                {
                    "account_code": "5000",
                    "debit": 10,
                    "dimensions": {"department": "DEPT-HR", "project": "PRJ-X"},
                }
            ]
        },
    )
    assert validate.status_code == 200
    data = validate.json()["data"]
    assert data["valid"] is True
    assert data["summary"]["unlimited_supported"] is True

    deactivate = await client.post(
        f"/api/v1/financial-kernel/dimensions/values/{value_id}/deactivate",
        headers=headers,
    )
    assert deactivate.status_code == 200

    audit = await client.get(
        f"/api/v1/financial-kernel/dimensions/values/{value_id}/audit",
        headers=headers,
    )
    assert audit.status_code == 200
    actions = [e["action"] for e in audit.json()["data"]]
    assert "created" in actions
    assert "deactivated" in actions
