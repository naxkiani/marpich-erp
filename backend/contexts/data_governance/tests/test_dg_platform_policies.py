"""P212-H Data Governance policies foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.data_governance.application.dg_policy_foundation import (
    validate_dg_policy_foundation,
)
from contexts.data_governance.container import (
    get_data_governance_service,
    reset_data_governance_service,
)
from contexts.data_governance.domain.services import (
    dg_platform_policies as pol,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_data_governance_service()
    yield
    reset_data_governance_service()


@pytest.mark.unit
def test_dg_policy_foundation():
    result = validate_dg_policy_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P212-H"
    assert result["adr"] == 401
    assert result["sor"] == "data_governance"
    assert result["capability"] == "CAP-PLT-DG-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_dg_policy_catalog():
    cat = pol.catalog()
    assert cat["prompt_id"] == "P212-H"
    assert cat["adr"] == 401
    assert cat["sor"] == "data_governance"
    assert cat["capability"] == "CAP-PLT-DG-001"
    assert cat["data_policy_architecture_complete_required"] is True
    assert cat["policy_lifecycle_management_present_required"] is True
    assert cat["policy_rule_engine_present_required"] is True
    assert cat["governance_automation_present_required"] is True
    assert cat["policy_intelligence_present_required"] is True
    assert cat["ai_governance_integration_present_required"] is True
    assert cat["knowledge_graph_integration_present_required"] is True
    assert cat["digital_twin_integration_present_required"] is True
    assert cat["cqrs_architecture_present_required"] is True
    assert cat["event_sourcing_architecture_present_required"] is True
    assert cat["microservices_architecture_present_required"] is True
    assert cat["zero_trust_alignment_present_required"] is True
    assert cat["enterprise_scalability_present_required"] is True
    assert cat["policy_architecture"]["bc_count"] >= 5
    assert cat["policy_lifecycle"]["stage_count"] >= 8
    assert cat["policy_framework"]["category_count"] >= 6
    assert cat["policy_rule_engine"]["via_policy_engine"] is True
    assert cat["governance_automation"]["step_count"] >= 5
    assert cat["microservices"]["service_count"] >= 6
    assert cat["cqrs"]["event_count"] >= 7
    assert cat["cursor_outputs"]["count"] >= 18
    assert (
        "data_policy_architecture_is_incomplete"
        in cat["quality_gates"]["reject_if"]
    )
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /data-governance/policies" in pol.policies_surface()["routes"]
    assert (
        "GET /data-governance/policies/readiness"
        in pol.policies_surface()["routes"]
    )


@pytest.mark.unit
def test_dg_policy_acl():
    from contexts.data_governance.infrastructure.acl import dg_policy_acl as acls

    assert acls.to_ownership(tenant_id="t1", owner_ref="o1")[
        "via_p212_d"
    ] is True
    assert acls.to_quality(tenant_id="t1", policy_ref="p1")[
        "via_p212_e"
    ] is True
    assert acls.to_mesh(tenant_id="t1", product_ref="p1")[
        "via_p212_f"
    ] is True
    assert acls.to_marketplace(tenant_id="t1", product_ref="p1")[
        "via_p212_g"
    ] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="pol1")[
        "via_policy_engine"
    ] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="pol1")[
        "module_local_pdp_forbidden"
    ] is True
    assert acls.to_enterprise_ai(tenant_id="t1", model_ref="m1")[
        "ai_governance_integration_present_required"
    ] is True
    assert acls.to_authorization(
        tenant_id="t1", principal_ref="u1", action="activate_policy"
    )["via_p208"] is True
    assert acls.to_workflow(tenant_id="t1", approval_ref="a1")[
        "via_workflow"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_policies():
    svc = get_data_governance_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_policies"]["prompt_id"] == "P212-H"
    assert catalog["platform_policies"]["adr"] == 401
    assert catalog["sor"] == "data_governance"
    summary = svc.platform_policies()
    assert summary["prompt_id"] == "P212-H"
    assert summary["capability"] == "CAP-PLT-DG-001"
    assert "P212-G" in summary["builds_on"]
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.policies_readiness()["passed"] is True
