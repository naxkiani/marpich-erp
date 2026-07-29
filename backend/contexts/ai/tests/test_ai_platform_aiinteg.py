"""P214-M Enterprise AI Integration / Gateway / Service Mesh foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.ai.application.ai_aiinteg_foundation import (
    validate_ai_aiinteg_foundation,
)
from contexts.ai.container import get_ai_service, reset_ai_service
from contexts.ai.domain.services import ai_platform_aiinteg as mod

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_ai_service()
    yield
    reset_ai_service()


@pytest.mark.unit
def test_ai_aiinteg_foundation():
    result = validate_ai_aiinteg_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P214-M"
    assert result["adr"] == 433
    assert result["sor"] == "ai"
    assert result["capability"] == "CAP-PLT-AI-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_ai_aiinteg_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P214-M"
    assert cat["adr"] == 433
    assert cat["principle"] == mod.PRINCIPLE
    assert cat["fabric"] == mod.FABRIC
    assert "secure, intelligent" in cat["principle"]
    assert "autonomous communication fabric" in cat["principle"]
    assert cat["domain_model"]["core_domain"] == mod.CORE_DOMAIN
    assert cat["bounded_contexts"]["context_count"] >= 7
    assert cat["enterprise_ai_api_gateway_present_required"] is True
    assert cat["intelligent_service_mesh_present_required"] is True
    assert cat["model_serving_gateway_present_required"] is True
    assert cat["digital_twin_integration_present_required"] is True
    assert cat["sibling_ai_bc_forbidden"] is True
    assert cat["platform_api_gateway_owns_edge"] is True
    assert cat["platform_event_fabric_owns_bus"] is True
    assert cat["gateway"]["via_api_gateway"] is True
    assert cat["serving"]["via_p214_l"] is True
    assert cat["agents"]["via_p214_f"] is True
    assert cat["events_fabric"]["via_event_fabric"] is True
    assert cat["workflows"]["via_workflow_engine"] is True
    assert cat["events"]["core_event_count"] >= 7
    assert cat["microservices"]["service_count"] >= 10
    assert cat["cursor_outputs"]["count"] >= 20
    assert (
        "enterprise_ai_api_gateway_is_missing"
        in cat["quality_gates"]["reject_if"]
    )
    assert "P214-L" in cat["builds_on"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /ai/aiinteg" in mod.aiinteg_surface()["routes"]
    assert "GET /ai/aiinteg/mesh" in mod.aiinteg_surface()["routes"]
    assert "GET /ai/aiinteg/serving" in mod.aiinteg_surface()["routes"]


@pytest.mark.unit
def test_ai_aiinteg_acl():
    from contexts.ai.infrastructure.acl import ai_aiinteg_acl as acls

    assert acls.to_api_gateway(tenant_id="t1", route_ref="r1")[
        "via_api_gateway"
    ] is True
    assert acls.to_event_fabric(tenant_id="t1", channel_ref="c1")[
        "via_event_fabric"
    ] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")[
        "via_workflow_engine"
    ] is True
    assert acls.to_agents(tenant_id="t1", agent_ref="a1")[
        "via_p214_f"
    ] is True
    assert acls.to_modelintel(tenant_id="t1", model_ref="m1")[
        "via_p214_l"
    ] is True
    assert acls.to_aiops(tenant_id="t1", ops_ref="o1")[
        "via_p214_j"
    ] is True
    assert acls.to_enterprise_ai(tenant_id="t1", integ_ref="i1")[
        "module_local_ai_gateway_forbidden"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_aiinteg():
    svc = get_ai_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_aiinteg"]["prompt_id"] == "P214-M"
    assert catalog["platform_aiinteg"]["adr"] == 433
    assert catalog["platform_aiinteg"]["principle"] == mod.PRINCIPLE
    assert catalog["platform_aiinteg"]["fabric"] == mod.FABRIC
    assert catalog["sor"] == "ai"
    summary = svc.platform_aiinteg()
    assert summary["prompt_id"] == "P214-M"
    assert summary["fabric"] == mod.FABRIC
    assert "P214-L" in summary["builds_on"]
    assert summary["context_count"] >= 7
    assert summary["microservice_count"] >= 10
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.aiinteg_readiness()["passed"] is True
    assert svc.aiinteg_gateway()["via_api_gateway"] is True
    assert svc.aiinteg_serving()["via_p214_l"] is True
    assert svc.aiinteg_agents()["via_p214_f"] is True
    assert svc.aiinteg_events_fabric()["via_event_fabric"] is True
    assert svc.aiinteg_digital_twin()["present_required"] is True
