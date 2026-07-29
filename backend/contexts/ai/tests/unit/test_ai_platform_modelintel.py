"""P214-L Enterprise AI Model Intelligence / Lifecycle / Governance foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.ai.application.ai_modelintel_foundation import (
    validate_ai_modelintel_foundation,
)
from contexts.ai.container import get_ai_service, reset_ai_service
from contexts.ai.domain.services import ai_platform_modelintel as mod

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_ai_service()
    yield
    reset_ai_service()


@pytest.mark.unit
def test_ai_modelintel_foundation():
    result = validate_ai_modelintel_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P214-L"
    assert result["adr"] == 432
    assert result["sor"] == "ai"
    assert result["capability"] == "CAP-PLT-AI-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_ai_modelintel_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P214-L"
    assert cat["adr"] == 432
    assert cat["principle"] == mod.PRINCIPLE
    assert cat["fabric"] == mod.FABRIC
    assert "lifecycle visibility" in cat["principle"]
    assert "governance and intelligence" in cat["principle"]
    assert cat["domain_model"]["core_domain"] == mod.CORE_DOMAIN
    assert cat["bounded_contexts"]["context_count"] >= 7
    assert cat["enterprise_ai_model_platform_present_required"] is True
    assert cat["model_registry_present_required"] is True
    assert cat["drift_detection_present_required"] is True
    assert cat["model_digital_twin_present_required"] is True
    assert cat["sibling_ai_bc_forbidden"] is True
    assert cat["approval"]["via_p214_h"] is True
    assert cat["approval"]["via_workflow_engine"] is True
    assert cat["knowledge_graph"]["via_p214_g"] is True
    assert cat["events"]["core_event_count"] >= 8
    assert cat["microservices"]["service_count"] >= 10
    assert cat["cursor_outputs"]["count"] >= 20
    assert (
        "enterprise_ai_model_platform_is_missing"
        in cat["quality_gates"]["reject_if"]
    )
    assert "P214-K" in cat["builds_on"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /ai/modelintel" in mod.modelintel_surface()["routes"]
    assert "GET /ai/modelintel/drift" in mod.modelintel_surface()["routes"]
    assert "GET /ai/modelintel/digital-twin" in mod.modelintel_surface()["routes"]


@pytest.mark.unit
def test_ai_modelintel_acl():
    from contexts.ai.infrastructure.acl import ai_modelintel_acl as acls

    assert acls.to_mlops(tenant_id="t1", model_ref="m1")[
        "via_p214_d"
    ] is True
    assert acls.to_governance(tenant_id="t1", policy_ref="p1")[
        "via_p214_h"
    ] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")[
        "via_workflow_engine"
    ] is True
    assert acls.to_knowledge(tenant_id="t1", knowledge_ref="k1")[
        "via_p214_g"
    ] is True
    assert acls.to_aidata(tenant_id="t1", dataset_ref="d1")[
        "via_p214_k"
    ] is True
    assert acls.to_aiops(tenant_id="t1", ops_ref="o1")[
        "via_p214_j"
    ] is True
    assert acls.to_enterprise_ai(tenant_id="t1", modelintel_ref="mi1")[
        "module_local_model_registry_forbidden"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_modelintel():
    svc = get_ai_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_modelintel"]["prompt_id"] == "P214-L"
    assert catalog["platform_modelintel"]["adr"] == 432
    assert catalog["platform_modelintel"]["principle"] == mod.PRINCIPLE
    assert catalog["platform_modelintel"]["fabric"] == mod.FABRIC
    assert catalog["sor"] == "ai"
    summary = svc.platform_modelintel()
    assert summary["prompt_id"] == "P214-L"
    assert summary["fabric"] == mod.FABRIC
    assert "P214-K" in summary["builds_on"]
    assert summary["context_count"] >= 7
    assert summary["microservice_count"] >= 10
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.modelintel_readiness()["passed"] is True
    assert svc.modelintel_approval()["via_p214_h"] is True
    assert svc.modelintel_knowledge_graph()["via_p214_g"] is True
    assert svc.modelintel_drift()["present_required"] is True
    assert svc.modelintel_digital_twin()["present_required"] is True
