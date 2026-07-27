"""P212-F Data Governance mesh/product foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.data_governance.application.dg_mesh_foundation import (
    validate_dg_mesh_foundation,
)
from contexts.data_governance.container import (
    get_data_governance_service,
    reset_data_governance_service,
)
from contexts.data_governance.domain.services import dg_platform_mesh as mesh

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_data_governance_service()
    yield
    reset_data_governance_service()


@pytest.mark.unit
def test_dg_mesh_foundation():
    result = validate_dg_mesh_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P212-F"
    assert result["adr"] == 399
    assert result["sor"] == "data_governance"
    assert result["capability"] == "CAP-PLT-DG-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_dg_mesh_catalog():
    cat = mesh.catalog()
    assert cat["prompt_id"] == "P212-F"
    assert cat["adr"] == 399
    assert cat["sor"] == "data_governance"
    assert cat["capability"] == "CAP-PLT-DG-001"
    assert cat["data_mesh_architecture_complete_required"] is True
    assert cat["data_product_platform_complete_required"] is True
    assert cat["ddd_domain_model_present_required"] is True
    assert cat["data_domain_model_present_required"] is True
    assert cat["data_product_lifecycle_present_required"] is True
    assert cat["data_contract_architecture_present_required"] is True
    assert cat["data_quality_integration_present_required"] is True
    assert cat["knowledge_graph_integration_present_required"] is True
    assert cat["digital_twin_integration_present_required"] is True
    assert cat["ai_native_intelligence_present_required"] is True
    assert cat["cqrs_architecture_present_required"] is True
    assert cat["event_sourcing_architecture_present_required"] is True
    assert cat["microservices_architecture_present_required"] is True
    assert cat["enterprise_scalability_present_required"] is True
    assert cat["mesh_architecture"]["principle_count"] >= 4
    assert cat["domain_model"]["domain_count"] >= 10
    assert cat["product_lifecycle"]["stage_count"] >= 9
    assert cat["microservices"]["service_count"] >= 6
    assert cat["cqrs"]["event_count"] >= 10
    assert cat["cursor_outputs"]["count"] >= 18
    assert (
        "data_mesh_architecture_is_incomplete"
        in cat["quality_gates"]["reject_if"]
    )
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /data-governance/mesh" in mesh.mesh_surface()["routes"]
    assert (
        "GET /data-governance/mesh/readiness" in mesh.mesh_surface()["routes"]
    )


@pytest.mark.unit
def test_dg_mesh_acl():
    from contexts.data_governance.infrastructure.acl import dg_mesh_acl as acls

    assert acls.to_ownership(tenant_id="t1", owner_ref="o1")[
        "via_p212_d"
    ] is True
    assert acls.to_quality(tenant_id="t1", product_ref="p1")[
        "via_p212_e"
    ] is True
    assert acls.to_identity(tenant_id="t1", identity_ref="i1")[
        "via_p207"
    ] is True
    assert acls.to_enterprise_ai(tenant_id="t1", model_ref="m1")[
        "ai_native_intelligence_present_required"
    ] is True
    assert acls.to_authorization(
        tenant_id="t1", principal_ref="u1", action="publish"
    )["via_p208"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_mesh():
    svc = get_data_governance_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_mesh"]["prompt_id"] == "P212-F"
    assert catalog["platform_mesh"]["adr"] == 399
    assert catalog["sor"] == "data_governance"
    summary = svc.platform_mesh()
    assert summary["prompt_id"] == "P212-F"
    assert summary["capability"] == "CAP-PLT-DG-001"
    assert "P212-E" in summary["builds_on"]
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.mesh_readiness()["passed"] is True
