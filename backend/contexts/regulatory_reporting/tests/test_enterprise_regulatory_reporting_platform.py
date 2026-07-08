"""Enterprise Regulatory Reporting Platform tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from contexts.policy.container import get_policy_service, reset_policy_service
from contexts.policy.infrastructure.persistence.memory_store import PolicyMemoryStore
from contexts.regulatory_reporting.container import (
    get_enterprise_regulatory_reporting_service,
    reset_enterprise_regulatory_reporting_service,
)
from contexts.regulatory_reporting.domain.aggregates.regulatory_reporting_platform import (
    RegulatoryCapability,
    SubmissionStatus,
)
from contexts.regulatory_reporting.domain.services import regulatory_reporting_engine
from contexts.regulatory_reporting.infrastructure.persistence.regulatory_reporting_memory_store import (
    InMemoryCountryAdapterRepository,
    InMemoryDigitalSubmissionRepository,
    InMemoryRegulatoryTenantProfileRepository,
)
from contexts.reporting.container import get_regulatory_reporting_service, reset_reporting_service
from contexts.tax.container import reset_tax_engine_service
from core.presentation.api.main import app


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    PolicyMemoryStore.reset()
    InMemoryRegulatoryTenantProfileRepository.reset()
    InMemoryCountryAdapterRepository.reset()
    InMemoryDigitalSubmissionRepository.reset()
    reset_policy_service()
    reset_tax_engine_service()
    reset_reporting_service()
    reset_enterprise_regulatory_reporting_service()
    get_policy_service()
    get_regulatory_reporting_service()
    get_enterprise_regulatory_reporting_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "reg2@enterprise.dev", "password": "SecurePass123!", "display_name": "REG2"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "reg2@enterprise.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


async def _provision_tax(slug: str) -> None:
    await get_policy_service().handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {"industry_pack": "tax_consulting"}}
    )


@pytest.mark.asyncio
async def test_catalog_lists_regulatory_capabilities(client):
    headers = await _auth_headers(client, "eregcat")
    resp = await client.get("/api/v1/regulatory-reporting/catalog", headers=headers)
    assert resp.status_code == 200
    data = resp.json()["data"]
    caps = {c["capability"] for c in data["capabilities"]}
    assert RegulatoryCapability.CENTRAL_BANK.value in caps
    assert RegulatoryCapability.FINANCIAL_INTELLIGENCE_UNIT.value in caps
    assert RegulatoryCapability.AML_REPORTS.value in caps
    assert RegulatoryCapability.KYC_REPORTS.value in caps
    assert RegulatoryCapability.COUNTRY_ADAPTERS.value in caps
    assert RegulatoryCapability.XML_EXPORT.value in caps
    assert len(caps) == 16
    assert data["delegation"]["hardcoded_regulatory_formats"] is False
    formats = {f["format"] for f in data["export_formats"]}
    assert formats == {"xml", "json", "pdf"}


@pytest.mark.asyncio
async def test_seed_adapters_generate_and_submit(client):
    slug = "eregseed"
    headers = await _auth_headers(client, slug)
    await _provision_tax(slug)
    await client.post("/api/v1/reports/seed", headers=headers)
    await client.post(
        "/api/v1/tax/calculation/compute",
        headers=headers,
        json={"amount": 1000, "tax_type": "vat", "jurisdiction": "EXAMPLE", "record_audit": True},
    )

    seed = await client.post("/api/v1/regulatory-reporting/seed", headers=headers)
    assert seed.status_code == 200
    body = seed.json()["data"]
    assert body["seeded"] is True
    assert body["adapters_seeded"] == 4

    adapters = await client.get("/api/v1/regulatory-reporting/adapters", headers=headers)
    assert adapters.status_code == 200
    assert len(adapters.json()["data"]) == 4
    countries = {a["country_code"] for a in adapters.json()["data"]}
    assert "EXAMPLE" in countries
    assert "IR" in countries

    gen = await client.post(
        "/api/v1/regulatory-reporting/reports/generate",
        headers=headers,
        json={
            "country_code": "EXAMPLE",
            "regulator_type": "tax_authority",
            "export_format": "xml",
            "parameters": {"period": "2026-Q1", "jurisdiction": "EXAMPLE"},
        },
    )
    assert gen.status_code == 201
    g = gen.json()["data"]
    assert g["manifest_driven"] is True
    assert g["hardcoded_regulatory_formats"] is False
    submission_ref = g["submission"]["submission_ref"]

    submit = await client.post(
        f"/api/v1/regulatory-reporting/submissions/{submission_ref}/submit",
        headers=headers,
    )
    assert submit.status_code == 200
    assert submit.json()["data"]["submission"]["status"] == SubmissionStatus.SUBMITTED.value
    assert submit.json()["data"]["portal_reference"]

    dash = await client.get("/api/v1/regulatory-reporting/dashboard", headers=headers)
    assert dash.status_code == 200
    d = dash.json()["data"]
    assert d["summary"]["capabilities"] == 16
    assert d["summary"]["country_adapters"] == 4
    assert d["delegation"]["manifest_driven_formats"] is True


@pytest.mark.asyncio
async def test_configure_custom_country_adapter(client):
    slug = "eregadp"
    headers = await _auth_headers(client, slug)
    await client.post("/api/v1/regulatory-reporting/seed", headers=headers)

    adapter = await client.post(
        "/api/v1/regulatory-reporting/adapters",
        headers=headers,
        json={
            "country_code": "DE",
            "country_name": "Germany",
            "regulator_types": ["government", "audit_authority"],
            "supported_formats": ["xml", "pdf"],
            "package_plugin_id": "regulatory-banking-oecd",
        },
    )
    assert adapter.status_code == 201
    assert adapter.json()["data"]["country_code"] == "DE"


def test_engine_report_type_and_dashboard():
    assert regulatory_reporting_engine.resolve_report_type(
        regulator_type="tax_authority"
    ) == "tax_authority"
    assert regulatory_reporting_engine.resolve_report_type(
        report_category="aml"
    ) == "financial_institution"

    dashboard = regulatory_reporting_engine.build_dashboard(
        profile={"enabled_regulators": ["tax_authority"]},
        adapters=[{"country_code": "EXAMPLE", "active": True}],
        submissions=[{"country_code": "EXAMPLE", "regulator_type": "tax_authority", "export_format": "xml", "status": "submitted", "created_at": "2026-01-01"}],
    )
    assert dashboard["summary"]["country_adapters"] == 1
    assert dashboard["delegation"]["hardcoded_regulatory_formats"] is False

    dm = regulatory_reporting_engine.dependency_map()
    assert dm["manifest_driven"] is True
