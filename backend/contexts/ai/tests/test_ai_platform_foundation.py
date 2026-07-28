"""P214-A Enterprise AI platform foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.ai.application.ai_foundation_foundation import (
    validate_ai_foundation_foundation,
)
from contexts.ai.container import get_ai_service, reset_ai_service
from contexts.ai.domain.services import ai_platform_foundation as mod

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_ai_service()
    yield
    reset_ai_service()


@pytest.mark.unit
def test_ai_foundation_foundation():
    result = validate_ai_foundation_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P214-A"
    assert result["adr"] == 421
    assert result["sor"] == "ai"
    assert result["capability"] == "CAP-PLT-AI-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_ai_foundation_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P214-A"
    assert cat["adr"] == 421
    assert cat["principle"] == mod.PRINCIPLE
    assert cat["fabric"] == mod.FABRIC
    assert "intelligence foundation" in cat["principle"]
    assert cat["core_domain"] == "enterprise_artificial_intelligence_management"
    assert cat["aggregate"] == "EnterpriseAIAggregate"
    assert cat["enterprise_ai_platform_foundation_present_required"] is True
    assert cat["machine_learning_platform_present_required"] is True
    assert cat["generative_ai_platform_present_required"] is True
    assert cat["llm_platform_present_required"] is True
    assert cat["vector_intelligence_present_required"] is True
    assert cat["ai_governance_foundation_present_required"] is True
    assert cat["ai_agent_foundation_present_required"] is True
    assert cat["sibling_ai_bc_forbidden"] is True
    assert cat["module_local_llm_sdk_forbidden"] is True
    assert cat["bounded_contexts"]["context_count"] >= 6
    assert cat["ai_paas"]["capability_count"] >= 10
    assert cat["ml_platform"]["lifecycle_step_count"] >= 10
    assert cat["ai_agent_foundation"]["via_p213_m"] is True
    assert cat["knowledge_integration"]["via_p213_l"] is True
    assert cat["digital_twin_integration"]["via_p212_l"] is True
    assert cat["cqrs"]["command_count"] >= 6
    assert cat["events"]["core_event_count"] >= 7
    assert cat["microservices"]["service_count"] >= 10
    assert cat["api_first"]["via_api_gateway"] is True
    assert cat["deployment"]["via_p213_o"] is True
    assert cat["cursor_outputs"]["count"] >= 20
    assert (
        "enterprise_ai_platform_foundation_is_missing"
        in cat["quality_gates"]["reject_if"]
    )
    assert "P213" in cat["builds_on"]
    assert "P212" in cat["builds_on"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /ai/foundation" in mod.foundation_surface()["routes"]
    assert "GET /ai/foundation/ml" in mod.foundation_surface()["routes"]
    assert "GET /ai/foundation/agents" in mod.foundation_surface()["routes"]


@pytest.mark.unit
def test_ai_foundation_acl():
    from contexts.ai.infrastructure.acl import ai_foundation_acl as acls

    assert acls.to_identity(tenant_id="t1", identity_ref="i1")[
        "via_p207"
    ] is True
    assert acls.to_authorization(
        tenant_id="t1", principal_ref="u1", action="ai.read"
    )["via_p208"] is True
    assert acls.to_cryptographic_trust(tenant_id="t1", secret_ref="s1")[
        "via_p209"
    ] is True
    assert acls.to_cyber_security(tenant_id="t1", control_ref="c1")[
        "via_p210"
    ] is True
    assert acls.to_data_security(tenant_id="t1", asset_ref="a1")[
        "via_p211"
    ] is True
    assert acls.to_data_governance(tenant_id="t1", product_ref="p1")[
        "via_p212"
    ] is True
    assert acls.to_graph(tenant_id="t1", entity_ref="e1")["via_p213_l"] is True
    assert acls.to_twin(tenant_id="t1", twin_ref="tw1")["via_p212_l"] is True
    assert acls.to_autonomous_di(tenant_id="t1", decision_ref="d1")[
        "via_p213_m"
    ] is True
    assert acls.to_ops_deploy(tenant_id="t1", release_ref="r1")[
        "via_p213_o"
    ] is True
    assert acls.to_enterprise_ai(tenant_id="t1", model_ref="m1")[
        "module_local_llm_sdk_forbidden"
    ] is True
    assert acls.to_api_gateway(tenant_id="t1", route_ref="rt1")[
        "via_api_gateway"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_foundation():
    svc = get_ai_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_foundation"]["prompt_id"] == "P214-A"
    assert catalog["platform_foundation"]["adr"] == 421
    assert catalog["platform_foundation"]["principle"] == mod.PRINCIPLE
    assert catalog["platform_foundation"]["fabric"] == mod.FABRIC
    assert catalog["sor"] == "ai"
    summary = svc.platform_foundation()
    assert summary["prompt_id"] == "P214-A"
    assert summary["principle"] == mod.PRINCIPLE
    assert summary["fabric"] == mod.FABRIC
    assert "P213" in summary["builds_on"]
    assert summary["context_count"] >= 6
    assert summary["ai_paas_count"] >= 10
    assert summary["microservice_count"] >= 10
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.foundation_readiness()["passed"] is True
    assert svc.foundation_ml()["lifecycle_step_count"] >= 10
    assert svc.foundation_vectors()["present_required"] is True
    assert svc.foundation_agents()["via_p213_m"] is True
    assert svc.foundation_api()["via_api_gateway"] is True
