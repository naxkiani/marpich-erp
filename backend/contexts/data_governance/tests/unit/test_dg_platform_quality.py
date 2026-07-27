"""P212-E Data Governance quality intelligence foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.data_governance.application.dg_quality_foundation import (
    validate_dg_quality_foundation,
)
from contexts.data_governance.container import (
    get_data_governance_service,
    reset_data_governance_service,
)
from contexts.data_governance.domain.services import (
    dg_platform_quality as qual,
)

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_data_governance_service()
    yield
    reset_data_governance_service()


@pytest.mark.unit
def test_dg_quality_foundation():
    result = validate_dg_quality_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P212-E"
    assert result["adr"] == 398
    assert result["sor"] == "data_governance"
    assert result["capability"] == "CAP-PLT-DG-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_dg_quality_catalog():
    cat = qual.catalog()
    assert cat["prompt_id"] == "P212-E"
    assert cat["adr"] == 398
    assert cat["sor"] == "data_governance"
    assert cat["capability"] == "CAP-PLT-DG-001"
    assert cat["quality_intelligence_architecture_complete_required"] is True
    assert cat["ddd_domain_model_present_required"] is True
    assert cat["quality_rule_architecture_present_required"] is True
    assert cat["quality_measurement_architecture_present_required"] is True
    assert cat["ai_quality_intelligence_present_required"] is True
    assert cat["data_mesh_alignment_present_required"] is True
    assert cat["knowledge_graph_integration_present_required"] is True
    assert cat["digital_twin_integration_present_required"] is True
    assert cat["cqrs_architecture_present_required"] is True
    assert cat["event_sourcing_architecture_present_required"] is True
    assert cat["microservices_architecture_present_required"] is True
    assert cat["enterprise_scalability_present_required"] is True
    assert cat["quality_dimensions"]["dimension_count"] >= 8
    assert cat["ddd_model"]["context_count"] >= 5
    assert cat["microservices"]["service_count"] >= 6
    assert cat["cqrs"]["event_count"] >= 9
    assert cat["cursor_outputs"]["count"] >= 18
    assert (
        "data_quality_intelligence_architecture_is_incomplete"
        in cat["quality_gates"]["reject_if"]
    )
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /data-governance/quality" in qual.quality_surface()["routes"]
    assert (
        "GET /data-governance/quality/readiness"
        in qual.quality_surface()["routes"]
    )


@pytest.mark.unit
def test_dg_quality_acl():
    from contexts.data_governance.infrastructure.acl import (
        dg_quality_acl as acls,
    )

    assert acls.to_ownership(tenant_id="t1", owner_ref="o1")[
        "via_p212_d"
    ] is True
    assert acls.to_data_security(tenant_id="t1", asset_ref="a1")[
        "via_p211"
    ] is True
    assert acls.to_identity(tenant_id="t1", identity_ref="i1")[
        "via_p207"
    ] is True
    assert acls.to_enterprise_ai(tenant_id="t1", model_ref="m1")[
        "ai_quality_intelligence_present_required"
    ] is True
    assert acls.to_authorization(
        tenant_id="t1", principal_ref="u1", action="check"
    )["via_p208"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_quality():
    svc = get_data_governance_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_quality"]["prompt_id"] == "P212-E"
    assert catalog["platform_quality"]["adr"] == 398
    assert catalog["sor"] == "data_governance"
    summary = svc.platform_quality()
    assert summary["prompt_id"] == "P212-E"
    assert summary["capability"] == "CAP-PLT-DG-001"
    assert "P212-D" in summary["builds_on"]
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.quality_readiness()["passed"] is True
