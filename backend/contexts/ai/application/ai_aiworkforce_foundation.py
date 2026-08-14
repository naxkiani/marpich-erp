"""AI P214-Q Autonomous AI Ecosystem / Digital Workforce foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/437-enterprise-ai-aiworkforce.md",
    "docs/architecture/ENTERPRISE_AI_AIWORKFORCE.md",
    "docs/architecture/enterprise_ai/AI_AIWORKFORCE_CAPABILITIES.v1.yaml",
    "docs/architecture/enterprise_ai/AI_AIWORKFORCE_DDD_CQRS.v1.yaml",
    "docs/architecture/enterprise_ai/AI_AIWORKFORCE_SECURITY.v1.yaml",
    "docs/architecture/enterprise_ai/AI_AIWORKFORCE_VALIDATION.v1.yaml",
    "backend/contexts/ai/domain/services/ai_platform_aiworkforce.py",
    "backend/contexts/ai/domain/aggregates/ai_aiworkforce_aggregates.py",
    "backend/contexts/ai/infrastructure/acl/ai_aiworkforce_acl.py",
    "backend/contexts/ai/application/ai_aiworkforce_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/autonomous_ai_ecosystem",
    "backend/contexts/ai_digital_workforce",
    "backend/contexts/digital_workforce_platform",
    "backend/contexts/autonomous_agent_ecosystem",
    "backend/contexts/ai_organization_platform",
    "backend/contexts/self_improving_intelligence",
    "backend/contexts/agent_runtime",
)


def validate_ai_aiworkforce_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.ai.domain.aggregates.ai_aiworkforce_aggregates import (
        DecisionRoot,
        EcosystemRoot,
        EvolutionRoot,
        LearningRoot,
        MemoryRoot,
        OrganizationRoot,
        WorkforceDigitalTwinRoot,
        WorkforcePlatformRoot,
        WorkflowRoot,
    )
    from contexts.ai.domain.services import ai_platform_aiworkforce as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P214-Q"
        and cat.get("adr") == 437
        and cat.get("sor") == "ai"
        and cat.get("capability") == "CAP-PLT-AI-001"
        and cat.get("principle") == catmod.PRINCIPLE
        and cat.get("fabric") == catmod.FABRIC
        and "self-improving intelligent enterprise operating system" in cat["principle"]
        and cat["domain_model"]["core_domain"] == catmod.CORE_DOMAIN
        and cat["domain_model"]["supporting_count"] >= 9
        and cat["bounded_contexts"]["context_count"] >= 7
        and cat["enterprise_autonomous_ai_ecosystem_present_required"] is True
        and cat["ai_digital_workforce_present_required"] is True
        and cat["multi_agent_platform_present_required"] is True
        and cat["ai_organization_model_present_required"] is True
        and cat["autonomous_workflow_platform_present_required"] is True
        and cat["self_learning_intelligence_present_required"] is True
        and cat["autonomous_decision_framework_present_required"] is True
        and cat["ai_memory_platform_present_required"] is True
        and cat["ai_evolution_management_present_required"] is True
        and cat["knowledge_graph_integration_present_required"] is True
        and cat["digital_twin_integration_present_required"] is True
        and cat["cqrs_architecture_present_required"] is True
        and cat["event_architecture_present_required"] is True
        and cat["microservices_architecture_present_required"] is True
        and cat["api_first_architecture_present_required"] is True
        and cat["zero_trust_ai_security_present_required"] is True
        and cat["cloud_native_deployment_present_required"] is True
        and cat["sibling_ai_bc_forbidden"] is True
        and cat["deepens_p214_f_digital_workforce"] is True
        and cat["governed_by_p214_p"] is True
        and cat["ecosystem"]["via_p214_f"] is True
        and cat["workflows"]["via_workflow_engine"] is True
        and cat["learning"]["via_p214_o"] is True
        and cat["learning"]["via_p214_l"] is True
        and cat["decision_autonomy"]["via_p214_p"] is True
        and cat["memory"]["via_p214_g"] is True
        and cat["evolution"]["via_p214_j"] is True
        and cat["cqrs"]["command_count"] >= 6
        and cat["events"]["core_event_count"] >= 8
        and cat["microservices"]["service_count"] >= 10
        and cat["cursor_outputs"]["count"] >= 20
        and "enterprise_autonomous_ai_ecosystem_is_missing" in cat["quality_gates"]["reject_if"]
        and "P214-P" in cat["builds_on"]
        and "P214-F" in cat["builds_on"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    def _bad(fn, **kwargs):
        try:
            fn(**kwargs)
            return True
        except ValueError:
            return False

    checks = [
        not _bad(WorkforcePlatformRoot.enable, tenant_id="t1", workforce_ref="w1", present=False)
        and WorkforcePlatformRoot.enable(tenant_id="t1", workforce_ref="w2").is_missing() is False,
        not _bad(EcosystemRoot.enable, tenant_id="t1", ecosystem_ref="e1", present=False)
        and EcosystemRoot.enable(tenant_id="t1", ecosystem_ref="e2").is_missing() is False,
        not _bad(OrganizationRoot.enable, tenant_id="t1", organization_ref="o1", present=False)
        and OrganizationRoot.enable(tenant_id="t1", organization_ref="o2").is_missing() is False,
        not _bad(WorkflowRoot.enable, tenant_id="t1", workflow_ref="wf1", present=False)
        and WorkflowRoot.enable(tenant_id="t1", workflow_ref="wf2").is_missing() is False,
        not _bad(LearningRoot.enable, tenant_id="t1", learning_ref="l1", present=False)
        and LearningRoot.enable(tenant_id="t1", learning_ref="l2").is_missing() is False,
        not _bad(DecisionRoot.enable, tenant_id="t1", decision_ref="d1", present=False)
        and DecisionRoot.enable(tenant_id="t1", decision_ref="d2").is_missing() is False,
        not _bad(MemoryRoot.enable, tenant_id="t1", memory_ref="m1", present=False)
        and MemoryRoot.enable(tenant_id="t1", memory_ref="m2").is_missing() is False,
        not _bad(EvolutionRoot.enable, tenant_id="t1", evolution_ref="ev1", present=False)
        and EvolutionRoot.enable(tenant_id="t1", evolution_ref="ev2").is_missing() is False,
        not _bad(WorkforceDigitalTwinRoot.enable, tenant_id="t1", twin_ref="tw1", present=False)
        and WorkforceDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw2").is_missing() is False,
    ]
    aggregates_ok = all(checks)

    acl_path = root / "backend/contexts/ai/infrastructure/acl/ai_aiworkforce_acl.py"
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p207" in acl_text
        and "via_p208" in acl_text
        and "via_p209" in acl_text
        and "via_p210" in acl_text
        and "via_p211" in acl_text
        and "via_p212" in acl_text
        and "via_p213" in acl_text
        and "via_audit_platform" in acl_text
        and "via_policy_engine" in acl_text
        and "via_workflow_engine" in acl_text
        and "via_p214_f" in acl_text
        and "via_p214_g" in acl_text
        and "via_p214_j" in acl_text
        and "via_p214_l" in acl_text
        and "via_p214_m" in acl_text
        and "via_p214_n" in acl_text
        and "via_p214_o" in acl_text
        and "via_p214_p" in acl_text
        and "module_local_ai_workforce_forbidden" in acl_text
    )

    router = (root / "backend/contexts/ai/presentation/router.py").read_text(encoding="utf-8")
    router_ok = (
        '@router.get("/aiworkforce")' in router
        and "/aiworkforce/readiness" in router
        and "/aiworkforce/workforce" in router
        and "/aiworkforce/ecosystem" in router
        and "/aiworkforce/decisions" in router
        and "/aiworkforce/memory" in router
        and "/aiworkforce/evolution" in router
        and "/aiworkforce/digital-twin" in router
    )

    law = (root / "docs/architecture/ENTERPRISE_AI_AIWORKFORCE.md").read_text(encoding="utf-8")
    doc_ok = (
        "Never Enterprise Autonomous AI Ecosystem is missing" in law
        and "Never AI Digital Workforce is missing" in law
        and "Never Multi-Agent Platform is missing" in law
        and "Never AI Organization Model is missing" in law
        and "Never Autonomous Workflow Platform is missing" in law
        and "Never Self-Learning Intelligence is missing" in law
        and "Never Autonomous Decision Framework is missing" in law
        and "Never AI Memory Platform is missing" in law
        and "Never AI Evolution Management is missing" in law
        and "Never Knowledge Graph Integration is missing" in law
        and "Never Digital Twin Integration is missing" in law
        and "Never CQRS architecture is missing" in law
        and "Never Event architecture is missing" in law
        and "Never Microservices architecture is missing" in law
        and "Never API first architecture is missing" in law
        and "Never Zero trust AI security is missing" in law
        and "Never Cloud native deployment is missing" in law
        and "Never Sibling AI BC" in law
        and "MEOS Autonomous Intelligence Ecosystem" in law
        and "self-improving intelligent enterprise operating system" in law
        and "P214-F" in law
        and "P214-P" in law
    )

    passed = (
        not missing
        and not sibling
        and catalog_ok
        and aggregates_ok
        and acl_ok
        and router_ok
        and doc_ok
    )
    return {
        "prompt": "P214-Q",
        "adr": 437,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "catalog": catalog_ok,
        "aggregates": aggregates_ok,
        "acl": acl_ok,
        "router": router_ok,
        "documentation": doc_ok,
        "sor": "ai",
        "capability": "CAP-PLT-AI-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
