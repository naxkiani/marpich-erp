"""P212-D Data Governance ownership/stewardship foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.data_governance.application.dg_ownership_foundation import (
    validate_dg_ownership_foundation,
)
from contexts.data_governance.container import (
    get_data_governance_service,
    reset_data_governance_service,
)
from contexts.data_governance.domain.services import (
    dg_platform_ownership as own,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_data_governance_service()
    yield
    reset_data_governance_service()


@pytest.mark.unit
def test_dg_ownership_foundation():
    result = validate_dg_ownership_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P212-D"
    assert result["adr"] == 397
    assert result["sor"] == "data_governance"
    assert result["capability"] == "CAP-PLT-DG-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_dg_ownership_catalog():
    cat = own.catalog()
    assert cat["prompt_id"] == "P212-D"
    assert cat["adr"] == 397
    assert cat["sor"] == "data_governance"
    assert cat["capability"] == "CAP-PLT-DG-001"
    assert cat["ownership_architecture_complete_required"] is True
    assert cat["stewardship_architecture_complete_required"] is True
    assert cat["accountability_framework_present_required"] is True
    assert cat["ddd_domain_model_present_required"] is True
    assert cat["cqrs_design_present_required"] is True
    assert cat["event_sourcing_design_present_required"] is True
    assert cat["data_mesh_alignment_present_required"] is True
    assert cat["knowledge_graph_integration_present_required"] is True
    assert cat["digital_twin_integration_present_required"] is True
    assert cat["ai_ownership_intelligence_present_required"] is True
    assert cat["zero_trust_alignment_present_required"] is True
    assert cat["enterprise_scalability_present_required"] is True
    assert cat["accountability_framework"]["dimension_count"] >= 4
    assert cat["microservices"]["service_count"] >= 5
    assert cat["cqrs"]["event_count"] >= 10
    assert cat["cursor_outputs"]["count"] >= 18
    assert (
        "data_ownership_architecture_is_incomplete"
        in cat["quality_gates"]["reject_if"]
    )
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /data-governance/ownership" in own.ownership_surface()["routes"]
    assert (
        "GET /data-governance/ownership/readiness"
        in own.ownership_surface()["routes"]
    )


@pytest.mark.unit
def test_dg_ownership_acl():
    from contexts.data_governance.infrastructure.acl import (
        dg_ownership_acl as acls,
    )

    assert acls.to_identity(tenant_id="t1", identity_ref="i1")[
        "via_p207"
    ] is True
    assert acls.to_authorization(
        tenant_id="t1", principal_ref="u1", action="assign"
    )["via_p208"] is True
    assert acls.to_data_security(tenant_id="t1", asset_ref="a1")[
        "via_p211"
    ] is True
    assert acls.to_enterprise_ai(tenant_id="t1", model_ref="m1")[
        "ai_ownership_intelligence_present_required"
    ] is True
    assert acls.to_workflow(tenant_id="t1", approval_ref="ap1")[
        "via_workflow"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_ownership():
    svc = get_data_governance_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_ownership"]["prompt_id"] == "P212-D"
    assert catalog["platform_ownership"]["adr"] == 397
    assert catalog["sor"] == "data_governance"
    summary = svc.platform_ownership()
    assert summary["prompt_id"] == "P212-D"
    assert summary["capability"] == "CAP-PLT-DG-001"
    assert "P212-A" in summary["builds_on"]
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.ownership_readiness()["passed"] is True
