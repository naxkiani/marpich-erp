"""AI P214-V AGI cognitive-core foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/442-enterprise-ai-agi.md",
    "docs/architecture/ENTERPRISE_AI_AGI.md",
    "docs/architecture/enterprise_ai/AI_AGI_CAPABILITIES.v1.yaml",
    "docs/architecture/enterprise_ai/AI_AGI_DDD_CQRS.v1.yaml",
    "docs/architecture/enterprise_ai/AI_AGI_SECURITY.v1.yaml",
    "docs/architecture/enterprise_ai/AI_AGI_VALIDATION.v1.yaml",
    "backend/contexts/ai/domain/services/ai_platform_agi.py",
    "backend/contexts/ai/domain/aggregates/ai_agi_aggregates.py",
    "backend/contexts/ai/infrastructure/acl/ai_agi_acl.py",
    "backend/contexts/ai/application/ai_agi_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/enterprise_agi_platform",
    "backend/contexts/cognitive_enterprise_intelligence",
    "backend/contexts/next_generation_intelligence_core",
    "backend/contexts/agi_architecture_platform",
    "backend/contexts/cognitive_computing_platform",
    "backend/contexts/general_intelligence_orchestration",
    "backend/contexts/future_meos_intelligence_core",
)


def validate_ai_agi_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.ai.domain.aggregates.ai_agi_aggregates import (
        AGICoreRoot,
        AGIDigitalTwinRoot,
        DecisionIntelligenceRoot,
        LearningCoreRoot,
        MemoryRoot,
        ReasoningRoot,
        StrategicIntelligenceRoot,
        UnderstandingRoot,
    )
    from contexts.ai.domain.services import ai_platform_agi as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P214-V"
        and cat.get("adr") == 442
        and cat.get("sor") == "ai"
        and cat.get("capability") == "CAP-PLT-AI-003"
        and cat.get("principle") == catmod.PRINCIPLE
        and cat.get("fabric") == catmod.FABRIC
        and "cognitive enterprise intelligence platform" in cat["principle"]
        and cat["domain_model"]["core_domain"] == catmod.CORE_DOMAIN
        and cat["domain_model"]["supporting_count"] >= 9
        and cat["bounded_contexts"]["context_count"] >= 7
        and cat["enterprise_agi_platform_present_required"] is True
        and cat["cognitive_intelligence_core_present_required"] is True
        and cat["universal_reasoning_engine_present_required"] is True
        and cat["enterprise_memory_architecture_present_required"] is True
        and cat["strategic_intelligence_engine_present_required"] is True
        and cat["autonomous_learning_core_present_required"] is True
        and cat["cognitive_decision_intelligence_present_required"] is True
        and cat["knowledge_graph_integration_present_required"] is True
        and cat["digital_twin_integration_present_required"] is True
        and cat["cqrs_architecture_present_required"] is True
        and cat["event_architecture_present_required"] is True
        and cat["microservices_architecture_present_required"] is True
        and cat["api_first_architecture_present_required"] is True
        and cat["zero_trust_ai_security_present_required"] is True
        and cat["cloud_native_deployment_present_required"] is True
        and cat["sibling_ai_bc_forbidden"] is True
        and cat["deepens_p214_u_cognitive_core"] is True
        and cat["coordinated_by_p214_t"] is True
        and cat["agi_core"]["via_p214_t"] is True
        and cat["agi_core"]["via_p214_u"] is True
        and cat["memory"]["via_p214_g"] is True
        and cat["strategic_intelligence"]["via_p213"] is True
        and cat["cqrs"]["command_count"] >= 6
        and cat["events"]["core_event_count"] >= 7
        and cat["microservices"]["service_count"] >= 9
        and cat["cursor_outputs"]["count"] >= 20
        and "enterprise_agi_platform_is_missing" in cat["quality_gates"]["reject_if"]
        and "P214-U" in cat["builds_on"]
        and "P214-T" in cat["builds_on"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    def _bad(fn, **kwargs):
        try:
            fn(**kwargs)
            return True
        except ValueError:
            return False

    checks = [
        not _bad(AGICoreRoot.enable, tenant_id="t1", core_ref="c1", present=False) and AGICoreRoot.enable(tenant_id="t1", core_ref="c2").is_missing() is False,
        not _bad(ReasoningRoot.enable, tenant_id="t1", reasoning_ref="r1", present=False) and ReasoningRoot.enable(tenant_id="t1", reasoning_ref="r2").is_missing() is False,
        not _bad(MemoryRoot.enable, tenant_id="t1", memory_ref="m1", present=False) and MemoryRoot.enable(tenant_id="t1", memory_ref="m2").is_missing() is False,
        not _bad(UnderstandingRoot.enable, tenant_id="t1", understanding_ref="u1", present=False) and UnderstandingRoot.enable(tenant_id="t1", understanding_ref="u2").is_missing() is False,
        not _bad(StrategicIntelligenceRoot.enable, tenant_id="t1", strategic_ref="s1", present=False) and StrategicIntelligenceRoot.enable(tenant_id="t1", strategic_ref="s2").is_missing() is False,
        not _bad(LearningCoreRoot.enable, tenant_id="t1", learning_ref="l1", present=False) and LearningCoreRoot.enable(tenant_id="t1", learning_ref="l2").is_missing() is False,
        not _bad(DecisionIntelligenceRoot.enable, tenant_id="t1", decision_ref="d1", present=False) and DecisionIntelligenceRoot.enable(tenant_id="t1", decision_ref="d2").is_missing() is False,
        not _bad(AGIDigitalTwinRoot.enable, tenant_id="t1", twin_ref="tw1", present=False) and AGIDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw2").is_missing() is False,
    ]
    aggregates_ok = all(checks)

    acl_path = root / "backend/contexts/ai/infrastructure/acl/ai_agi_acl.py"
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p210" in acl_text
        and "via_p212" in acl_text
        and "via_p213" in acl_text
        and "via_p214_g" in acl_text
        and "via_p214_q" in acl_text
        and "via_p214_t" in acl_text
        and "via_p214_u" in acl_text
        and "via_audit_platform" in acl_text
        and "via_policy_engine" in acl_text
        and "module_local_agi_forbidden" in acl_text
    )

    router = (root / "backend/contexts/ai/presentation/router.py").read_text(encoding="utf-8")
    router_ok = (
        '@router.get("/agi")' in router
        and "/agi/readiness" in router
        and "/agi/core" in router
        and "/agi/reasoning" in router
        and "/agi/memory" in router
        and "/agi/strategic-intelligence" in router
        and "/agi/digital-twin" in router
    )

    law = (root / "docs/architecture/ENTERPRISE_AI_AGI.md").read_text(encoding="utf-8")
    doc_ok = (
        "Never Enterprise AGI Platform is missing" in law
        and "Never Cognitive Intelligence Core is missing" in law
        and "Never Universal Reasoning Engine is missing" in law
        and "Never Enterprise Memory Architecture is missing" in law
        and "Never Strategic Intelligence Engine is missing" in law
        and "Never Autonomous Learning Core is missing" in law
        and "Never Cognitive Decision Intelligence is missing" in law
        and "Never Knowledge Graph Integration is missing" in law
        and "Never Digital Twin Integration is missing" in law
        and "Never CQRS architecture is missing" in law
        and "Never Event architecture is missing" in law
        and "Never Microservices architecture is missing" in law
        and "Never API first architecture is missing" in law
        and "Never Zero trust AI security is missing" in law
        and "Never Cloud native deployment is missing" in law
        and "Never Sibling AI BC" in law
        and "MEOS Cognitive Intelligence Core" in law
        and "cognitive enterprise intelligence platform" in law
        and "P214-T" in law
        and "P214-U" in law
    )

    passed = not missing and not sibling and catalog_ok and aggregates_ok and acl_ok and router_ok and doc_ok
    return {"prompt": "P214-V", "adr": 442, "passed": passed, "missing_artifacts": missing, "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": aggregates_ok, "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "ai", "capability": "CAP-PLT-AI-003", "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD"}
