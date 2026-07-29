"""P214-H Enterprise AI Governance / Responsible AI / Risk foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.ai.application.ai_governance_foundation import (
    validate_ai_governance_foundation,
)
from contexts.ai.container import get_ai_service, reset_ai_service
from contexts.ai.domain.services import ai_platform_governance as mod

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_ai_service()
    yield
    reset_ai_service()


@pytest.mark.unit
def test_ai_governance_foundation():
    result = validate_ai_governance_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P214-H"
    assert result["adr"] == 428
    assert result["sor"] == "ai"
    assert result["capability"] == "CAP-PLT-AI-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_ai_governance_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P214-H"
    assert cat["adr"] == 428
    assert cat["principle"] == mod.PRINCIPLE
    assert cat["fabric"] == mod.FABRIC
    assert "trust framework" in cat["principle"]
    assert cat["domain_model"]["core_domain"] == mod.CORE_DOMAIN
    assert cat["bounded_contexts"]["context_count"] >= 7
    assert cat["policies"]["lifecycle_stage_count"] >= 7
    assert cat["enterprise_ai_governance_platform_present_required"] is True
    assert cat["responsible_ai_platform_present_required"] is True
    assert cat["ai_risk_management_platform_present_required"] is True
    assert cat["ai_trust_management_present_required"] is True
    assert cat["sibling_ai_bc_forbidden"] is True
    assert cat["policies"]["via_policy_engine"] is True
    assert cat["explainability"]["via_p214_e"] is True
    assert cat["audit"]["via_audit"] is True
    assert cat["events"]["core_event_count"] >= 8
    assert cat["microservices"]["service_count"] >= 9
    assert cat["cursor_outputs"]["count"] >= 20
    assert (
        "enterprise_ai_governance_platform_is_missing"
        in cat["quality_gates"]["reject_if"]
    )
    assert "P214-G" in cat["builds_on"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /ai/governance" in mod.governance_surface()["routes"]
    assert "GET /ai/governance/risk" in mod.governance_surface()["routes"]
    assert "GET /ai/governance/trust" in mod.governance_surface()["routes"]


@pytest.mark.unit
def test_ai_governance_acl():
    from contexts.ai.infrastructure.acl import ai_governance_acl as acls

    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")[
        "via_policy_engine"
    ] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")[
        "via_workflow_engine"
    ] is True
    assert acls.to_audit(tenant_id="t1", entry_ref="a1")["via_audit"] is True
    assert acls.to_mlops(tenant_id="t1", model_ref="m1")[
        "via_p214_d"
    ] is True
    assert acls.to_genai(tenant_id="t1", model_ref="g1")[
        "via_p214_e"
    ] is True
    assert acls.to_agents(tenant_id="t1", agent_ref="ag1")[
        "via_p214_f"
    ] is True
    assert acls.to_knowledge(tenant_id="t1", knowledge_ref="k1")[
        "via_p214_g"
    ] is True
    assert acls.to_enterprise_ai(tenant_id="t1", governance_ref="gov1")[
        "module_local_governance_forbidden"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_governance():
    svc = get_ai_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_governance"]["prompt_id"] == "P214-H"
    assert catalog["platform_governance"]["adr"] == 428
    assert catalog["platform_governance"]["principle"] == mod.PRINCIPLE
    assert catalog["platform_governance"]["fabric"] == mod.FABRIC
    assert catalog["sor"] == "ai"
    summary = svc.platform_governance()
    assert summary["prompt_id"] == "P214-H"
    assert summary["fabric"] == mod.FABRIC
    assert "P214-G" in summary["builds_on"]
    assert summary["context_count"] >= 7
    assert summary["policy_lifecycle_stage_count"] >= 7
    assert summary["microservice_count"] >= 9
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.governance_readiness()["passed"] is True
    assert svc.governance_policies()["via_policy_engine"] is True
    assert svc.governance_risk()["present_required"] is True
    assert svc.governance_trust()["present_required"] is True
    assert svc.governance_digital_twin()["present_required"] is True
