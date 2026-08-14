"""AI P214-S Research / Innovation Lab / Future Evolution foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/439-enterprise-ai-airesearch.md",
    "docs/architecture/ENTERPRISE_AI_AIRESEARCH.md",
    "docs/architecture/enterprise_ai/AI_AIRESEARCH_CAPABILITIES.v1.yaml",
    "docs/architecture/enterprise_ai/AI_AIRESEARCH_DDD_CQRS.v1.yaml",
    "docs/architecture/enterprise_ai/AI_AIRESEARCH_SECURITY.v1.yaml",
    "docs/architecture/enterprise_ai/AI_AIRESEARCH_VALIDATION.v1.yaml",
    "backend/contexts/ai/domain/services/ai_platform_airesearch.py",
    "backend/contexts/ai/domain/aggregates/ai_airesearch_aggregates.py",
    "backend/contexts/ai/infrastructure/acl/ai_airesearch_acl.py",
    "backend/contexts/ai/application/ai_airesearch_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/ai_research_platform",
    "backend/contexts/innovation_lab",
    "backend/contexts/future_intelligence_evolution",
    "backend/contexts/ai_discovery_platform",
    "backend/contexts/ai_experimentation_platform",
    "backend/contexts/prototype_factory",
    "backend/contexts/emerging_technology_platform",
)


def validate_ai_airesearch_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.ai.domain.aggregates.ai_airesearch_aggregates import (
        BreakthroughRoot,
        ExperimentRoot,
        InnovationLabRoot,
        KnowledgePlatformRoot,
        PrototypeRoot,
        ResearchDigitalTwinRoot,
        ResearchPlatformRoot,
        RoadmapRoot,
        TechnologyObservatoryRoot,
    )
    from contexts.ai.domain.services import ai_platform_airesearch as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P214-S"
        and cat.get("adr") == 439
        and cat.get("sor") == "ai"
        and cat.get("capability") == "CAP-PLT-AI-001"
        and cat.get("principle") == catmod.PRINCIPLE
        and cat.get("fabric") == catmod.FABRIC
        and "continuously evolving intelligent enterprise capable of discovering and creating future AI capabilities" in cat["principle"]
        and cat["domain_model"]["core_domain"] == catmod.CORE_DOMAIN
        and cat["domain_model"]["supporting_count"] >= 9
        and cat["bounded_contexts"]["context_count"] >= 7
        and cat["enterprise_ai_research_platform_present_required"] is True
        and cat["ai_innovation_lab_present_required"] is True
        and cat["experimentation_platform_present_required"] is True
        and cat["prototype_factory_present_required"] is True
        and cat["future_intelligence_observatory_present_required"] is True
        and cat["scientific_knowledge_platform_present_required"] is True
        and cat["breakthrough_management_present_required"] is True
        and cat["ai_evolution_roadmap_present_required"] is True
        and cat["knowledge_graph_integration_present_required"] is True
        and cat["digital_twin_integration_present_required"] is True
        and cat["cqrs_architecture_present_required"] is True
        and cat["event_architecture_present_required"] is True
        and cat["microservices_architecture_present_required"] is True
        and cat["api_first_architecture_present_required"] is True
        and cat["zero_trust_security_present_required"] is True
        and cat["cloud_native_deployment_present_required"] is True
        and cat["sibling_ai_bc_forbidden"] is True
        and cat["deepens_p214_r_future_evolution"] is True
        and cat["governed_by_p214_p"] is True
        and cat["experimentation"]["via_p214_o"] is True
        and cat["experimentation"]["via_p214_l"] is True
        and cat["prototypes"]["via_p214_n"] is True
        and cat["knowledge"]["via_p214_g"] is True
        and cat["roadmap"]["via_p214_r"] is True
        and cat["knowledge_graph"]["via_p214_g"] is True
        and cat["cqrs"]["command_count"] >= 6
        and cat["events"]["core_event_count"] >= 8
        and cat["microservices"]["service_count"] >= 9
        and cat["cursor_outputs"]["count"] >= 20
        and "enterprise_ai_research_platform_is_missing" in cat["quality_gates"]["reject_if"]
        and "P214-R" in cat["builds_on"]
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
        not _bad(ResearchPlatformRoot.enable, tenant_id="t1", research_ref="r1", present=False) and ResearchPlatformRoot.enable(tenant_id="t1", research_ref="r2").is_missing() is False,
        not _bad(InnovationLabRoot.enable, tenant_id="t1", innovation_ref="i1", present=False) and InnovationLabRoot.enable(tenant_id="t1", innovation_ref="i2").is_missing() is False,
        not _bad(ExperimentRoot.enable, tenant_id="t1", experiment_ref="e1", present=False) and ExperimentRoot.enable(tenant_id="t1", experiment_ref="e2").is_missing() is False,
        not _bad(PrototypeRoot.enable, tenant_id="t1", prototype_ref="p1", present=False) and PrototypeRoot.enable(tenant_id="t1", prototype_ref="p2").is_missing() is False,
        not _bad(TechnologyObservatoryRoot.enable, tenant_id="t1", tech_ref="t1", present=False) and TechnologyObservatoryRoot.enable(tenant_id="t1", tech_ref="t2").is_missing() is False,
        not _bad(KnowledgePlatformRoot.enable, tenant_id="t1", knowledge_ref="k1", present=False) and KnowledgePlatformRoot.enable(tenant_id="t1", knowledge_ref="k2").is_missing() is False,
        not _bad(BreakthroughRoot.enable, tenant_id="t1", breakthrough_ref="b1", present=False) and BreakthroughRoot.enable(tenant_id="t1", breakthrough_ref="b2").is_missing() is False,
        not _bad(RoadmapRoot.enable, tenant_id="t1", roadmap_ref="rm1", present=False) and RoadmapRoot.enable(tenant_id="t1", roadmap_ref="rm2").is_missing() is False,
        not _bad(ResearchDigitalTwinRoot.enable, tenant_id="t1", twin_ref="tw1", present=False) and ResearchDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw2").is_missing() is False,
    ]
    aggregates_ok = all(checks)

    acl_path = root / "backend/contexts/ai/infrastructure/acl/ai_airesearch_acl.py"
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p207" in acl_text
        and "via_p208" in acl_text
        and "via_p209" in acl_text
        and "via_p210" in acl_text
        and "via_p214_f" in acl_text
        and "via_p214_g" in acl_text
        and "via_p214_j" in acl_text
        and "via_p214_l" in acl_text
        and "via_p214_m" in acl_text
        and "via_p214_n" in acl_text
        and "via_p214_o" in acl_text
        and "via_p214_p" in acl_text
        and "via_p214_q" in acl_text
        and "via_p214_r" in acl_text
        and "via_audit_platform" in acl_text
        and "via_policy_engine" in acl_text
        and "module_local_ai_research_forbidden" in acl_text
    )

    router = (root / "backend/contexts/ai/presentation/router.py").read_text(encoding="utf-8")
    router_ok = (
        '@router.get("/airesearch")' in router
        and "/airesearch/readiness" in router
        and "/airesearch/research" in router
        and "/airesearch/innovation" in router
        and "/airesearch/experiments" in router
        and "/airesearch/prototypes" in router
        and "/airesearch/roadmap" in router
        and "/airesearch/digital-twin" in router
    )

    law = (root / "docs/architecture/ENTERPRISE_AI_AIRESEARCH.md").read_text(encoding="utf-8")
    doc_ok = (
        "Never Enterprise AI Research Platform is missing" in law
        and "Never AI Innovation Lab is missing" in law
        and "Never Experimentation Platform is missing" in law
        and "Never Prototype Factory is missing" in law
        and "Never Future Intelligence Observatory is missing" in law
        and "Never Scientific Knowledge Platform is missing" in law
        and "Never Breakthrough Management is missing" in law
        and "Never AI Evolution Roadmap is missing" in law
        and "Never Knowledge Graph Integration is missing" in law
        and "Never Digital Twin Integration is missing" in law
        and "Never CQRS architecture is missing" in law
        and "Never Event architecture is missing" in law
        and "Never Microservices architecture is missing" in law
        and "Never API first architecture is missing" in law
        and "Never Zero trust security is missing" in law
        and "Never Cloud native deployment is missing" in law
        and "Never Sibling AI BC" in law
        and "MEOS Future Intelligence Evolution Fabric" in law
        and "continuously evolving intelligent enterprise capable of discovering and creating future AI capabilities" in law
        and "P214-P" in law
        and "P214-R" in law
    )

    passed = not missing and not sibling and catalog_ok and aggregates_ok and acl_ok and router_ok and doc_ok
    return {"prompt": "P214-S", "adr": 439, "passed": passed, "missing_artifacts": missing, "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": aggregates_ok, "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "ai", "capability": "CAP-PLT-AI-001", "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD"}
