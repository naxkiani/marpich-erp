"""P214-N Enterprise AI Infrastructure / Cloud / Compute foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.ai.application.ai_aiinfra_foundation import (
    validate_ai_aiinfra_foundation,
)
from contexts.ai.container import get_ai_service, reset_ai_service
from contexts.ai.domain.services import ai_platform_aiinfra as mod

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_ai_service()
    yield
    reset_ai_service()


@pytest.mark.unit
def test_ai_aiinfra_foundation():
    result = validate_ai_aiinfra_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P214-N"
    assert result["adr"] == 434
    assert result["sor"] == "ai"
    assert result["capability"] == "CAP-PLT-AI-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_ai_aiinfra_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P214-N"
    assert cat["adr"] == 434
    assert cat["principle"] == mod.PRINCIPLE
    assert cat["fabric"] == mod.FABRIC
    assert "scalable, secure" in cat["principle"]
    assert "intelligent compute foundation" in cat["principle"]
    assert cat["domain_model"]["core_domain"] == mod.CORE_DOMAIN
    assert cat["bounded_contexts"]["context_count"] >= 7
    assert cat["enterprise_ai_cloud_platform_present_required"] is True
    assert cat["gpu_infrastructure_platform_present_required"] is True
    assert cat["kubernetes_ai_platform_present_required"] is True
    assert cat["infrastructure_digital_twin_present_required"] is True
    assert cat["sibling_ai_bc_forbidden"] is True
    assert cat["cloud"]["via_p213_o"] is True
    assert cat["kubernetes"]["via_p214_m"] is True
    assert cat["resources"]["via_p214_j"] is True
    assert cat["knowledge_graph"]["via_p214_g"] is True
    assert cat["events"]["core_event_count"] >= 8
    assert cat["microservices"]["service_count"] >= 9
    assert cat["cursor_outputs"]["count"] >= 20
    assert (
        "enterprise_ai_cloud_platform_is_missing"
        in cat["quality_gates"]["reject_if"]
    )
    assert "P214-M" in cat["builds_on"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /ai/aiinfra" in mod.aiinfra_surface()["routes"]
    assert "GET /ai/aiinfra/gpu" in mod.aiinfra_surface()["routes"]
    assert "GET /ai/aiinfra/kubernetes" in mod.aiinfra_surface()["routes"]


@pytest.mark.unit
def test_ai_aiinfra_acl():
    from contexts.ai.infrastructure.acl import ai_aiinfra_acl as acls

    assert acls.to_ops_deploy(tenant_id="t1", release_ref="r1")[
        "via_p213_o"
    ] is True
    assert acls.to_aiinteg(tenant_id="t1", mesh_ref="m1")[
        "via_p214_m"
    ] is True
    assert acls.to_aiops(tenant_id="t1", ops_ref="o1")[
        "via_p214_j"
    ] is True
    assert acls.to_knowledge(tenant_id="t1", knowledge_ref="k1")[
        "via_p214_g"
    ] is True
    assert acls.to_aisec(tenant_id="t1", security_ref="s1")[
        "via_p214_i"
    ] is True
    assert acls.to_mlops(tenant_id="t1", model_ref="m1")[
        "via_p214_d"
    ] is True
    assert acls.to_enterprise_ai(tenant_id="t1", infra_ref="i1")[
        "module_local_gpu_scheduler_forbidden"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_aiinfra():
    svc = get_ai_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_aiinfra"]["prompt_id"] == "P214-N"
    assert catalog["platform_aiinfra"]["adr"] == 434
    assert catalog["platform_aiinfra"]["principle"] == mod.PRINCIPLE
    assert catalog["platform_aiinfra"]["fabric"] == mod.FABRIC
    assert catalog["sor"] == "ai"
    summary = svc.platform_aiinfra()
    assert summary["prompt_id"] == "P214-N"
    assert summary["fabric"] == mod.FABRIC
    assert "P214-M" in summary["builds_on"]
    assert summary["context_count"] >= 7
    assert summary["microservice_count"] >= 9
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.aiinfra_readiness()["passed"] is True
    assert svc.aiinfra_cloud()["via_p213_o"] is True
    assert svc.aiinfra_kubernetes()["via_p214_m"] is True
    assert svc.aiinfra_resources()["via_p214_j"] is True
    assert svc.aiinfra_gpu()["present_required"] is True
    assert svc.aiinfra_digital_twin()["present_required"] is True
