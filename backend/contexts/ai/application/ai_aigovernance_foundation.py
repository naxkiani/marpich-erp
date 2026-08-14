"""AI P214-U Autonomous Governance guardian-layer foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/441-enterprise-ai-aigovernance.md",
    "docs/architecture/ENTERPRISE_AI_AIGOVERNANCE.md",
    "docs/architecture/enterprise_ai/AI_AIGOVERNANCE_CAPABILITIES.v1.yaml",
    "docs/architecture/enterprise_ai/AI_AIGOVERNANCE_DDD_CQRS.v1.yaml",
    "docs/architecture/enterprise_ai/AI_AIGOVERNANCE_SECURITY.v1.yaml",
    "docs/architecture/enterprise_ai/AI_AIGOVERNANCE_VALIDATION.v1.yaml",
    "backend/contexts/ai/domain/services/ai_platform_aigovernance.py",
    "backend/contexts/ai/domain/aggregates/ai_aigovernance_aggregates.py",
    "backend/contexts/ai/infrastructure/acl/ai_aigovernance_acl.py",
    "backend/contexts/ai/application/ai_aigovernance_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/autonomous_ai_governance",
    "backend/contexts/self_healing_intelligence",
    "backend/contexts/ai_alignment_platform",
    "backend/contexts/ai_singularity_readiness",
    "backend/contexts/advanced_ai_safety",
    "backend/contexts/ai_recursive_improvement_governance",
    "backend/contexts/future_intelligence_platform",
)


def validate_ai_aigovernance_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.ai.domain.aggregates.ai_aigovernance_aggregates import (
        AGIReadinessRoot,
        AlignmentRoot,
        AutonomousGovernanceRoot,
        EvolutionControlRoot,
        GuardianDigitalTwinRoot,
        HumanCompatibilityRoot,
        SafetyRoot,
        SelfHealingRoot,
    )
    from contexts.ai.domain.services import ai_platform_aigovernance as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P214-U"
        and cat.get("adr") == 441
        and cat.get("sor") == "ai"
        and cat.get("capability") == "CAP-PLT-AI-002"
        and cat.get("principle") == catmod.PRINCIPLE
        and cat.get("fabric") == catmod.FABRIC
        and "safely manage, govern and evolve increasingly autonomous intelligence systems" in cat["principle"]
        and cat["domain_model"]["core_domain"] == catmod.CORE_DOMAIN
        and cat["domain_model"]["supporting_count"] >= 9
        and cat["bounded_contexts"]["context_count"] >= 7
        and cat["autonomous_ai_governance_present_required"] is True
        and cat["self_healing_intelligence_present_required"] is True
        and cat["ai_alignment_platform_present_required"] is True
        and cat["ai_safety_framework_present_required"] is True
        and cat["evolution_control_present_required"] is True
        and cat["agi_readiness_model_present_required"] is True
        and cat["human_compatibility_layer_present_required"] is True
        and cat["knowledge_graph_integration_present_required"] is True
        and cat["digital_twin_integration_present_required"] is True
        and cat["cqrs_architecture_present_required"] is True
        and cat["event_architecture_present_required"] is True
        and cat["microservices_architecture_present_required"] is True
        and cat["api_first_architecture_present_required"] is True
        and cat["zero_trust_ai_security_present_required"] is True
        and cat["cloud_native_deployment_present_required"] is True
        and cat["sibling_ai_bc_forbidden"] is True
        and cat["deepens_p214_t_guardian_layer"] is True
        and cat["governed_by_p214_p"] is True
        and cat["autonomous_governance"]["via_p214_p"] is True
        and cat["autonomous_governance"]["via_p214_t"] is True
        and cat["knowledge_graph"]["via_p214_g"] is True
        and cat["cqrs"]["command_count"] >= 6
        and cat["events"]["core_event_count"] >= 7
        and cat["microservices"]["service_count"] >= 9
        and cat["cursor_outputs"]["count"] >= 20
        and "autonomous_ai_governance_is_missing" in cat["quality_gates"]["reject_if"]
        and "P214-T" in cat["builds_on"]
        and "P214-P" in cat["builds_on"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    def _bad(fn, **kwargs):
        try:
            fn(**kwargs)
            return True
        except ValueError:
            return False

    checks = [
        not _bad(AutonomousGovernanceRoot.enable, tenant_id="t1", governance_ref="g1", present=False) and AutonomousGovernanceRoot.enable(tenant_id="t1", governance_ref="g2").is_missing() is False,
        not _bad(SelfHealingRoot.enable, tenant_id="t1", healing_ref="h1", present=False) and SelfHealingRoot.enable(tenant_id="t1", healing_ref="h2").is_missing() is False,
        not _bad(AlignmentRoot.enable, tenant_id="t1", alignment_ref="a1", present=False) and AlignmentRoot.enable(tenant_id="t1", alignment_ref="a2").is_missing() is False,
        not _bad(SafetyRoot.enable, tenant_id="t1", safety_ref="s1", present=False) and SafetyRoot.enable(tenant_id="t1", safety_ref="s2").is_missing() is False,
        not _bad(EvolutionControlRoot.enable, tenant_id="t1", evolution_ref="e1", present=False) and EvolutionControlRoot.enable(tenant_id="t1", evolution_ref="e2").is_missing() is False,
        not _bad(AGIReadinessRoot.enable, tenant_id="t1", readiness_ref="r1", present=False) and AGIReadinessRoot.enable(tenant_id="t1", readiness_ref="r2").is_missing() is False,
        not _bad(HumanCompatibilityRoot.enable, tenant_id="t1", compatibility_ref="c1", present=False) and HumanCompatibilityRoot.enable(tenant_id="t1", compatibility_ref="c2").is_missing() is False,
        not _bad(GuardianDigitalTwinRoot.enable, tenant_id="t1", twin_ref="tw1", present=False) and GuardianDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw2").is_missing() is False,
    ]
    aggregates_ok = all(checks)

    acl_path = root / "backend/contexts/ai/infrastructure/acl/ai_aigovernance_acl.py"
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p210" in acl_text
        and "via_p211" in acl_text
        and "via_p213" in acl_text
        and "via_p214_g" in acl_text
        and "via_p214_p" in acl_text
        and "via_p214_q" in acl_text
        and "via_p214_s" in acl_text
        and "via_p214_t" in acl_text
        and "via_audit_platform" in acl_text
        and "via_policy_engine" in acl_text
        and "module_local_guardian_forbidden" in acl_text
    )

    router = (root / "backend/contexts/ai/presentation/router.py").read_text(encoding="utf-8")
    router_ok = (
        '@router.get("/aigov")' in router
        and "/aigov/readiness" in router
        and "/aigov/autonomous-governance" in router
        and "/aigov/self-healing" in router
        and "/aigov/alignment" in router
        and "/aigov/agi-readiness" in router
        and "/aigov/digital-twin" in router
    )

    law = (root / "docs/architecture/ENTERPRISE_AI_AIGOVERNANCE.md").read_text(encoding="utf-8")
    doc_ok = (
        "Never Autonomous AI Governance is missing" in law
        and "Never Self-Healing Intelligence is missing" in law
        and "Never AI Alignment Platform is missing" in law
        and "Never AI Safety Framework is missing" in law
        and "Never Evolution Control is missing" in law
        and "Never AGI Readiness Model is missing" in law
        and "Never Human Compatibility Layer is missing" in law
        and "Never Knowledge Graph Integration is missing" in law
        and "Never Digital Twin Integration is missing" in law
        and "Never CQRS architecture is missing" in law
        and "Never Event architecture is missing" in law
        and "Never Microservices architecture is missing" in law
        and "Never API first architecture is missing" in law
        and "Never Zero trust AI security is missing" in law
        and "Never Cloud native deployment is missing" in law
        and "Never Sibling AI BC" in law
        and "MEOS Autonomous Intelligence Guardian Layer" in law
        and "safely manage, govern and evolve increasingly autonomous intelligence systems" in law
        and "P214-P" in law
        and "P214-T" in law
    )

    passed = not missing and not sibling and catalog_ok and aggregates_ok and acl_ok and router_ok and doc_ok
    return {"prompt": "P214-U", "adr": 441, "passed": passed, "missing_artifacts": missing, "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": aggregates_ok, "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "ai", "capability": "CAP-PLT-AI-002", "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD"}
