"""P214-I Enterprise AI Security / Adversarial Defense foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.ai.application.ai_security_foundation import (
    validate_ai_security_foundation,
)
from contexts.ai.container import get_ai_service, reset_ai_service
from contexts.ai.domain.services import ai_platform_security as mod

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_ai_service()
    yield
    reset_ai_service()


@pytest.mark.unit
def test_ai_security_foundation():
    result = validate_ai_security_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P214-I"
    assert result["adr"] == 429
    assert result["sor"] == "ai"
    assert result["capability"] == "CAP-PLT-AI-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_ai_security_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P214-I"
    assert cat["adr"] == 429
    assert cat["principle"] == mod.PRINCIPLE
    assert cat["fabric"] == mod.FABRIC
    assert "intelligence layer" in cat["principle"]
    assert cat["domain_model"]["core_domain"] == mod.CORE_DOMAIN
    assert cat["bounded_contexts"]["context_count"] >= 8
    assert cat["enterprise_ai_security_platform_present_required"] is True
    assert cat["llm_security_present_required"] is True
    assert cat["prompt_security_present_required"] is True
    assert cat["agent_security_present_required"] is True
    assert cat["adversarial_defense_present_required"] is True
    assert cat["sibling_ai_bc_forbidden"] is True
    assert cat["models"]["via_p209"] is True
    assert cat["llm"]["via_p214_e"] is True
    assert cat["agents"]["via_p214_f"] is True
    assert cat["threats"]["via_p210"] is True
    assert cat["events"]["core_event_count"] >= 8
    assert cat["microservices"]["service_count"] >= 10
    assert cat["cursor_outputs"]["count"] >= 20
    assert (
        "enterprise_ai_security_platform_is_missing"
        in cat["quality_gates"]["reject_if"]
    )
    assert "P214-H" in cat["builds_on"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /ai/aisec" in mod.aisec_surface()["routes"]
    assert "GET /ai/aisec/llm" in mod.aisec_surface()["routes"]
    assert "GET /ai/aisec/adversarial" in mod.aisec_surface()["routes"]


@pytest.mark.unit
def test_ai_security_acl():
    from contexts.ai.infrastructure.acl import ai_security_acl as acls

    assert acls.to_cryptographic_trust(tenant_id="t1", secret_ref="s1")[
        "via_p209"
    ] is True
    assert acls.to_cyber_security(tenant_id="t1", control_ref="c1")[
        "via_p210"
    ] is True
    assert acls.to_genai(tenant_id="t1", model_ref="m1")[
        "via_p214_e"
    ] is True
    assert acls.to_agents(tenant_id="t1", agent_ref="a1")[
        "via_p214_f"
    ] is True
    assert acls.to_knowledge(tenant_id="t1", knowledge_ref="k1")[
        "via_p214_g"
    ] is True
    assert acls.to_governance(tenant_id="t1", policy_ref="p1")[
        "via_p214_h"
    ] is True
    assert acls.to_enterprise_ai(tenant_id="t1", security_ref="sec1")[
        "module_local_ai_security_forbidden"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_aisec():
    svc = get_ai_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_aisec"]["prompt_id"] == "P214-I"
    assert catalog["platform_aisec"]["adr"] == 429
    assert catalog["platform_aisec"]["principle"] == mod.PRINCIPLE
    assert catalog["platform_aisec"]["fabric"] == mod.FABRIC
    assert catalog["sor"] == "ai"
    summary = svc.platform_aisec()
    assert summary["prompt_id"] == "P214-I"
    assert summary["fabric"] == mod.FABRIC
    assert "P214-H" in summary["builds_on"]
    assert summary["context_count"] >= 8
    assert summary["microservice_count"] >= 10
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.aisec_readiness()["passed"] is True
    assert svc.aisec_llm()["via_p214_e"] is True
    assert svc.aisec_agents()["via_p214_f"] is True
    assert svc.aisec_threats()["via_p210"] is True
    assert svc.aisec_adversarial()["present_required"] is True
    assert svc.aisec_soc()["present_required"] is True
