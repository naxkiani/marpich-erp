"""P212-M Data Governance ops foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.data_governance.application.dg_ops_foundation import (
    validate_dg_ops_foundation,
)
from contexts.data_governance.container import (
    get_data_governance_service,
    reset_data_governance_service,
)
from contexts.data_governance.domain.services import dg_platform_ops as ops

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_data_governance_service()
    yield
    reset_data_governance_service()


@pytest.mark.unit
def test_dg_ops_foundation():
    result = validate_dg_ops_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P212-M"
    assert result["adr"] == 405
    assert result["sor"] == "data_governance"
    assert result["capability"] == "CAP-PLT-DG-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_dg_ops_catalog():
    cat = ops.catalog()
    assert cat["prompt_id"] == "P212-M"
    assert cat["adr"] == 405
    assert cat["sor"] == "data_governance"
    assert cat["capability"] == "CAP-PLT-DG-001"
    assert cat["cqrs_architecture_complete_required"] is True
    assert cat["command_side_design_present_required"] is True
    assert cat["query_side_design_present_required"] is True
    assert cat["event_sourcing_architecture_present_required"] is True
    assert cat["event_bus_architecture_present_required"] is True
    assert cat["event_contract_governance_present_required"] is True
    assert cat["microservice_architecture_present_required"] is True
    assert cat["api_first_architecture_present_required"] is True
    assert cat["hexagonal_architecture_present_required"] is True
    assert cat["data_governance_integration_present_required"] is True
    assert cat["ai_governance_integration_present_required"] is True
    assert cat["digital_twin_integration_present_required"] is True
    assert cat["multi_tenant_architecture_present_required"] is True
    assert cat["observability_architecture_present_required"] is True
    assert cat["enterprise_scalability_present_required"] is True
    assert cat["command_side"]["category_count"] >= 5
    assert cat["query_side"]["read_model_count"] >= 7
    assert cat["microservices"]["service_count"] >= 11
    assert cat["event_sourcing"]["event_count"] >= 4
    assert cat["hexagonal"]["layer_count"] >= 5
    assert cat["cursor_outputs"]["count"] >= 18
    assert cat["event_bus"]["via_enterprise_event_bus"] is True
    assert cat["api_first"]["via_api_gateway"] is True
    assert (
        "cqrs_architecture_is_incomplete"
        in cat["quality_gates"]["reject_if"]
    )
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /data-governance/ops" in ops.ops_surface()["routes"]
    assert (
        "GET /data-governance/ops/readiness" in ops.ops_surface()["routes"]
    )


@pytest.mark.unit
def test_dg_ops_acl():
    from contexts.data_governance.infrastructure.acl import dg_ops_acl as acls

    assert acls.to_event_bus(tenant_id="t1", topic_ref="t1")[
        "via_enterprise_event_bus"
    ] is True
    assert acls.to_api_gateway(tenant_id="t1", route_ref="r1")[
        "via_api_gateway"
    ] is True
    assert acls.to_graph(tenant_id="t1", entity_ref="e1")[
        "via_p212_j"
    ] is True
    assert acls.to_ai_readiness(tenant_id="t1", dataset_ref="d1")[
        "via_p212_k"
    ] is True
    assert acls.to_twin(tenant_id="t1", twin_ref="tw1")[
        "via_p212_l"
    ] is True
    assert acls.to_authorization(
        tenant_id="t1", principal_ref="u1", action="execute_command"
    )["via_p208"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_ops():
    svc = get_data_governance_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_ops"]["prompt_id"] == "P212-M"
    assert catalog["platform_ops"]["adr"] == 405
    assert catalog["sor"] == "data_governance"
    summary = svc.platform_ops()
    assert summary["prompt_id"] == "P212-M"
    assert summary["capability"] == "CAP-PLT-DG-001"
    assert "P212-L" in summary["builds_on"]
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.ops_readiness()["passed"] is True
