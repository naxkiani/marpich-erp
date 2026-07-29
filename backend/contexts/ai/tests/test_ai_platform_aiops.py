"""P214-J Enterprise AIOps / Autonomous AI Management foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.ai.application.ai_aiops_foundation import (
    validate_ai_aiops_foundation,
)
from contexts.ai.container import get_ai_service, reset_ai_service
from contexts.ai.domain.services import ai_platform_aiops as mod

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_ai_service()
    yield
    reset_ai_service()


@pytest.mark.unit
def test_ai_aiops_foundation():
    result = validate_ai_aiops_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P214-J"
    assert result["adr"] == 430
    assert result["sor"] == "ai"
    assert result["capability"] == "CAP-PLT-AI-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_ai_aiops_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P214-J"
    assert cat["adr"] == 430
    assert cat["principle"] == mod.PRINCIPLE
    assert cat["fabric"] == mod.FABRIC
    assert "self-optimizing" in cat["principle"]
    assert cat["domain_model"]["core_domain"] == mod.CORE_DOMAIN
    assert cat["bounded_contexts"]["context_count"] >= 7
    assert cat["enterprise_aiops_platform_present_required"] is True
    assert cat["ai_observability_present_required"] is True
    assert cat["autonomous_remediation_present_required"] is True
    assert cat["operational_digital_twin_present_required"] is True
    assert cat["sibling_ai_bc_forbidden"] is True
    assert cat["observability"]["via_observability"] is True
    assert cat["rca"]["via_p213_o"] is True
    assert cat["remediation"]["via_workflow_engine"] is True
    assert cat["events"]["core_event_count"] >= 8
    assert cat["microservices"]["service_count"] >= 10
    assert cat["cursor_outputs"]["count"] >= 20
    assert (
        "enterprise_aiops_platform_is_missing"
        in cat["quality_gates"]["reject_if"]
    )
    assert "P214-I" in cat["builds_on"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /ai/aiops" in mod.aiops_surface()["routes"]
    assert "GET /ai/aiops/remediation" in mod.aiops_surface()["routes"]
    assert "GET /ai/aiops/digital-twin" in mod.aiops_surface()["routes"]


@pytest.mark.unit
def test_ai_aiops_acl():
    from contexts.ai.infrastructure.acl import ai_aiops_acl as acls

    assert acls.to_observability(tenant_id="t1", signal_ref="s1")[
        "via_observability"
    ] is True
    assert acls.to_ops_deploy(tenant_id="t1", release_ref="r1")[
        "via_p213_o"
    ] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")[
        "via_workflow_engine"
    ] is True
    assert acls.to_mlops(tenant_id="t1", model_ref="m1")[
        "via_p214_d"
    ] is True
    assert acls.to_aisec(tenant_id="t1", security_ref="sec1")[
        "via_p214_i"
    ] is True
    assert acls.to_knowledge(tenant_id="t1", knowledge_ref="k1")[
        "via_p214_g"
    ] is True
    assert acls.to_enterprise_ai(tenant_id="t1", ops_ref="o1")[
        "module_local_aiops_forbidden"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_aiops():
    svc = get_ai_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_aiops"]["prompt_id"] == "P214-J"
    assert catalog["platform_aiops"]["adr"] == 430
    assert catalog["platform_aiops"]["principle"] == mod.PRINCIPLE
    assert catalog["platform_aiops"]["fabric"] == mod.FABRIC
    assert catalog["sor"] == "ai"
    summary = svc.platform_aiops()
    assert summary["prompt_id"] == "P214-J"
    assert summary["fabric"] == mod.FABRIC
    assert "P214-I" in summary["builds_on"]
    assert summary["context_count"] >= 7
    assert summary["microservice_count"] >= 10
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.aiops_readiness()["passed"] is True
    assert svc.aiops_observability()["via_observability"] is True
    assert svc.aiops_remediation()["via_workflow_engine"] is True
    assert svc.aiops_rca()["via_p213_o"] is True
    assert svc.aiops_digital_twin()["present_required"] is True
