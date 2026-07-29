"""AI P214-W civilization-layer foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/443-enterprise-ai-aicivilization.md",
    "docs/architecture/ENTERPRISE_AI_AICIVILIZATION.md",
    "docs/architecture/enterprise_ai/AI_AICIVILIZATION_CAPABILITIES.v1.yaml",
    "docs/architecture/enterprise_ai/AI_AICIVILIZATION_DDD_CQRS.v1.yaml",
    "docs/architecture/enterprise_ai/AI_AICIVILIZATION_SECURITY.v1.yaml",
    "docs/architecture/enterprise_ai/AI_AICIVILIZATION_VALIDATION.v1.yaml",
    "backend/contexts/ai/domain/services/ai_platform_aicivilization.py",
    "backend/contexts/ai/domain/aggregates/ai_aicivilization_aggregates.py",
    "backend/contexts/ai/infrastructure/acl/ai_aicivilization_acl.py",
    "backend/contexts/ai/application/ai_aicivilization_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/enterprise_ai_civilization_layer",
    "backend/contexts/collective_intelligence_network",
    "backend/contexts/future_intelligence_ecosystem",
    "backend/contexts/cognitive_civilization_platform",
    "backend/contexts/ai_knowledge_society",
    "backend/contexts/distributed_intelligence_network",
    "backend/contexts/collective_ai_consciousness_architecture",
)


def validate_ai_aicivilization_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.ai.domain.aggregates.ai_aicivilization_aggregates import (
        CivilizationDigitalTwinRoot,
        CivilizationRoot,
        CollectiveDecisionRoot,
        DistributedIntelligenceRoot,
        HumanCollaborationRoot,
        KnowledgeCivilizationRoot,
        LearningCivilizationRoot,
        NetworkRoot,
    )
    from contexts.ai.domain.services import ai_platform_aicivilization as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P214-W"
        and cat.get("adr") == 443
        and cat.get("sor") == "ai"
        and cat.get("capability") == "CAP-PLT-AI-004"
        and cat.get("principle") == catmod.PRINCIPLE
        and cat.get("fabric") == catmod.FABRIC
        and "living collective intelligence ecosystem" in cat["principle"]
        and cat["domain_model"]["core_domain"] == catmod.CORE_DOMAIN
        and cat["domain_model"]["supporting_count"] >= 9
        and cat["bounded_contexts"]["context_count"] >= 7
        and cat["enterprise_ai_civilization_layer_present_required"] is True
        and cat["collective_intelligence_network_present_required"] is True
        and cat["human_ai_collaboration_platform_present_required"] is True
        and cat["knowledge_civilization_platform_present_required"] is True
        and cat["distributed_intelligence_fabric_present_required"] is True
        and cat["collective_decision_intelligence_present_required"] is True
        and cat["learning_ecosystem_present_required"] is True
        and cat["knowledge_graph_integration_present_required"] is True
        and cat["digital_twin_integration_present_required"] is True
        and cat["cqrs_architecture_present_required"] is True
        and cat["event_architecture_present_required"] is True
        and cat["microservices_architecture_present_required"] is True
        and cat["api_first_architecture_present_required"] is True
        and cat["zero_trust_ai_security_present_required"] is True
        and cat["cloud_native_deployment_present_required"] is True
        and cat["sibling_ai_bc_forbidden"] is True
        and cat["deepens_p214_v_collective_ecosystem"] is True
        and cat["guarded_by_p214_u"] is True
        and cat["coordinated_by_p214_t"] is True
        and cat["collective_decision"]["via_p213"] is True
        and cat["knowledge_graph"]["via_p214_g"] is True
        and cat["cqrs"]["command_count"] >= 6
        and cat["events"]["core_event_count"] >= 7
        and cat["microservices"]["service_count"] >= 9
        and cat["cursor_outputs"]["count"] >= 20
        and "enterprise_ai_civilization_layer_is_missing" in cat["quality_gates"]["reject_if"]
        and "P214-V" in cat["builds_on"]
        and "P214-U" in cat["builds_on"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    def _bad(fn, **kwargs):
        try:
            fn(**kwargs)
            return True
        except ValueError:
            return False

    checks = [
        not _bad(CivilizationRoot.enable, tenant_id="t1", civilization_ref="c1", present=False) and CivilizationRoot.enable(tenant_id="t1", civilization_ref="c2").is_missing() is False,
        not _bad(NetworkRoot.enable, tenant_id="t1", network_ref="n1", present=False) and NetworkRoot.enable(tenant_id="t1", network_ref="n2").is_missing() is False,
        not _bad(KnowledgeCivilizationRoot.enable, tenant_id="t1", knowledge_ref="k1", present=False) and KnowledgeCivilizationRoot.enable(tenant_id="t1", knowledge_ref="k2").is_missing() is False,
        not _bad(HumanCollaborationRoot.enable, tenant_id="t1", collaboration_ref="h1", present=False) and HumanCollaborationRoot.enable(tenant_id="t1", collaboration_ref="h2").is_missing() is False,
        not _bad(DistributedIntelligenceRoot.enable, tenant_id="t1", distributed_ref="d1", present=False) and DistributedIntelligenceRoot.enable(tenant_id="t1", distributed_ref="d2").is_missing() is False,
        not _bad(CollectiveDecisionRoot.enable, tenant_id="t1", decision_ref="dc1", present=False) and CollectiveDecisionRoot.enable(tenant_id="t1", decision_ref="dc2").is_missing() is False,
        not _bad(LearningCivilizationRoot.enable, tenant_id="t1", learning_ref="l1", present=False) and LearningCivilizationRoot.enable(tenant_id="t1", learning_ref="l2").is_missing() is False,
        not _bad(CivilizationDigitalTwinRoot.enable, tenant_id="t1", twin_ref="tw1", present=False) and CivilizationDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw2").is_missing() is False,
    ]
    aggregates_ok = all(checks)

    acl_path = root / "backend/contexts/ai/infrastructure/acl/ai_aicivilization_acl.py"
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p212" in acl_text
        and "via_p213" in acl_text
        and "via_p214_g" in acl_text
        and "via_p214_q" in acl_text
        and "via_p214_s" in acl_text
        and "via_p214_t" in acl_text
        and "via_p214_u" in acl_text
        and "via_p214_v" in acl_text
        and "via_audit_platform" in acl_text
        and "via_policy_engine" in acl_text
        and "module_local_civilization_forbidden" in acl_text
    )

    router = (root / "backend/contexts/ai/presentation/router.py").read_text(encoding="utf-8")
    router_ok = (
        '@router.get("/aiciv")' in router
        and "/aiciv/readiness" in router
        and "/aiciv/network" in router
        and "/aiciv/knowledge" in router
        and "/aiciv/human-collaboration" in router
        and "/aiciv/distributed-intelligence" in router
        and "/aiciv/digital-twin" in router
    )

    law = (root / "docs/architecture/ENTERPRISE_AI_AICIVILIZATION.md").read_text(encoding="utf-8")
    doc_ok = (
        "Never Enterprise AI Civilization Layer is missing" in law
        and "Never Collective Intelligence Network is missing" in law
        and "Never Human-AI Collaboration Platform is missing" in law
        and "Never Knowledge Civilization Platform is missing" in law
        and "Never Distributed Intelligence Fabric is missing" in law
        and "Never Collective Decision Intelligence is missing" in law
        and "Never Learning Ecosystem is missing" in law
        and "Never Knowledge Graph Integration is missing" in law
        and "Never Digital Twin Integration is missing" in law
        and "Never CQRS architecture is missing" in law
        and "Never Event architecture is missing" in law
        and "Never Microservices architecture is missing" in law
        and "Never API first architecture is missing" in law
        and "Never Zero trust AI security is missing" in law
        and "Never Cloud native deployment is missing" in law
        and "Never Sibling AI BC" in law
        and "MEOS Collective Intelligence Civilization Fabric" in law
        and "living collective intelligence ecosystem" in law
        and "P214-U" in law
        and "P214-V" in law
    )

    passed = not missing and not sibling and catalog_ok and aggregates_ok and acl_ok and router_ok and doc_ok
    return {"prompt": "P214-W", "adr": 443, "passed": passed, "missing_artifacts": missing, "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": aggregates_ok, "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "ai", "capability": "CAP-PLT-AI-004", "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD"}
