"""P212-L Data Governance digital twin foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.data_governance.application.dg_twin_foundation import (
    validate_dg_twin_foundation,
)
from contexts.data_governance.container import (
    get_data_governance_service,
    reset_data_governance_service,
)
from contexts.data_governance.domain.services import (
    dg_platform_twin as twin,
)

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_data_governance_service()
    yield
    reset_data_governance_service()


@pytest.mark.unit
def test_dg_twin_foundation():
    result = validate_dg_twin_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P212-L"
    assert result["adr"] == 404
    assert result["sor"] == "data_governance"
    assert result["capability"] == "CAP-PLT-DG-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_dg_twin_catalog():
    cat = twin.catalog()
    assert cat["prompt_id"] == "P212-L"
    assert cat["adr"] == 404
    assert cat["sor"] == "data_governance"
    assert cat["capability"] == "CAP-PLT-DG-001"
    assert cat["digital_twin_architecture_complete_required"] is True
    assert cat["governance_state_model_present_required"] is True
    assert cat["simulation_engine_present_required"] is True
    assert cat["what_if_analysis_present_required"] is True
    assert cat["risk_prediction_intelligence_present_required"] is True
    assert cat["optimization_engine_present_required"] is True
    assert cat["ai_governance_integration_present_required"] is True
    assert cat["knowledge_graph_integration_present_required"] is True
    assert cat["data_mesh_integration_present_required"] is True
    assert cat["policy_simulation_present_required"] is True
    assert cat["cqrs_architecture_present_required"] is True
    assert cat["event_sourcing_architecture_present_required"] is True
    assert cat["microservices_architecture_present_required"] is True
    assert cat["zero_trust_security_present_required"] is True
    assert cat["enterprise_scalability_present_required"] is True
    assert cat["twin_architecture"]["bc_count"] >= 5
    assert cat["governance_state_model"]["layer_count"] >= 4
    assert cat["simulation_engine"]["type_count"] >= 4
    assert cat["what_if_analysis"]["capability_count"] >= 4
    assert cat["microservices"]["service_count"] >= 6
    assert cat["cqrs"]["event_count"] >= 6
    assert cat["cursor_outputs"]["count"] >= 18
    assert (
        "data_governance_digital_twin_architecture_is_incomplete"
        in cat["quality_gates"]["reject_if"]
    )
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /data-governance/twin" in twin.twin_surface()["routes"]
    assert (
        "GET /data-governance/twin/readiness"
        in twin.twin_surface()["routes"]
    )


@pytest.mark.unit
def test_dg_twin_acl():
    from contexts.data_governance.infrastructure.acl import dg_twin_acl as acls

    assert acls.to_quality(tenant_id="t1", quality_ref="q1")[
        "via_p212_e"
    ] is True
    assert acls.to_mesh(tenant_id="t1", product_ref="p1")[
        "via_p212_f"
    ] is True
    assert acls.to_policies(tenant_id="t1", policy_ref="pol1")[
        "via_p212_h"
    ] is True
    assert acls.to_graph(tenant_id="t1", entity_ref="e1")[
        "via_p212_j"
    ] is True
    assert acls.to_ai_readiness(tenant_id="t1", dataset_ref="d1")[
        "via_p212_k"
    ] is True
    assert acls.to_enterprise_ai(tenant_id="t1", model_ref="m1")[
        "via_enterprise_ai"
    ] is True
    assert acls.to_authorization(
        tenant_id="t1", principal_ref="u1", action="execute_simulation"
    )["via_p208"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_twin():
    svc = get_data_governance_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_twin"]["prompt_id"] == "P212-L"
    assert catalog["platform_twin"]["adr"] == 404
    assert catalog["sor"] == "data_governance"
    summary = svc.platform_twin()
    assert summary["prompt_id"] == "P212-L"
    assert summary["capability"] == "CAP-PLT-DG-001"
    assert "P212-J" in summary["builds_on"]
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.twin_readiness()["passed"] is True
