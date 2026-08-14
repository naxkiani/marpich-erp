"""Space P218-V Human General Intelligence foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/548-enterprise-space-intelligence-human-gi.md",
    "docs/architecture/ENTERPRISE_SPACE_INTELLIGENCE_HUMAN_GI.md",
    "docs/architecture/space/HUMAN_GI_ARCHITECTURE.v1.yaml",
    "docs/architecture/space/HUMAN_GI_LIFECYCLE.v1.yaml",
    "docs/architecture/space/HUMAN_GI_DDD_CQRS.v1.yaml",
    "docs/architecture/space/HUMAN_GI_CONTROLS.v1.yaml",
    "docs/architecture/space/HUMAN_GI_VALIDATION.v1.yaml",
    "docs/architecture/space/P218_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/space/domain/services/sp_platform_human_gi.py",
    "backend/contexts/space/domain/aggregates/sp_human_gi_aggregates.py",
    "backend/contexts/space/infrastructure/acl/sp_human_gi_acl.py",
    "backend/contexts/space/application/sp_human_gi_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/human_gi_platform",
    "backend/contexts/collective_intelligence_bc",
    "backend/contexts/cognitive_civilization_bc",
)


def validate_sp_human_gi_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.space.domain.aggregates.sp_human_gi_aggregates import (
        CognitiveCivilizationRoot, CollectiveIntelligenceRoot, GiEthicsRoot,
        GiGovernanceRoot, HumanAiCollaborationRoot, HumanGiCoreRoot,
        HumanGiKnowledgeGraphRoot, HumanIntelligenceTwinRoot, ReasoningArchitectureRoot,
    )
    from contexts.space.domain.services import sp_platform_human_gi as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P218-V" and cat["adr"] == 548 and cat["sor"] == "space"
        and cat["capability"] == "CAP-PLT-SP-001"
        and cat["fabric"] == "meos_human_general_intelligence_fabric"
        and cat["foundation_gate"] == "P218" and cat["mission_gate"] == "P218-A"
        and cat["strategy_gate"] == "P218-B" and cat["domain_gate"] == "P218-C"
        and cat["infrastructure_gate"] == "P218-D" and cat["space_ai_gate"] == "P218-E"
        and cat["satellite_gate"] == "P218-F" and cat["orbital_gate"] == "P218-G"
        and cat["communications_gate"] == "P218-H" and cat["navigation_gate"] == "P218-I"
        and cat["mission_intel_gate"] == "P218-J" and cat["scientific_gate"] == "P218-K"
        and cat["exploration_gate"] == "P218-L" and cat["manufacturing_gate"] == "P218-M"
        and cat["resources_gate"] == "P218-N" and cat["logistics_gate"] == "P218-O"
        and cat["security_gate"] == "P218-P" and cat["sustainability_gate"] == "P218-Q"
        and cat["commerce_gate"] == "P218-R" and cat["education_gate"] == "P218-S"
        and cat["civilization_gate"] == "P218-T" and cat["human_evolution_gate"] == "P218-U"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["human_gi_architecture_present_required"] is True
        and cat["advanced_cognitive_civilization_present_required"] is True
        and cat["collective_intelligence_present_required"] is True
        and cat["reasoning_architecture_present_required"] is True
        and cat["knowledge_graph_present_required"] is True
        and cat["human_intelligence_digital_twin_present_required"] is True
        and cat["ethical_governance_present_required"] is True
        and cat["human_ai_collaboration_present_required"] is True
        and cat["governance_present_required"] is True
        and cat["architecture"]["layer_count"] == 5
        and cat["lifecycle"]["stage_count"] == 10
        and cat["human_gi_core"]["capability_count"] == 8
        and cat["human_gi_core"]["cognitive_domain_count"] == 8
        and cat["cognitive_civilization"]["domain_count"] == 6
        and cat["collective"]["architecture_layer_count"] == 5
        and cat["collective"]["agent_count"] == 5
        and cat["reasoning"]["capability_count"] == 6
        and cat["reasoning"]["framework_count"] == 5
        and cat["knowledge_graph"]["entity_count"] == 9
        and cat["knowledge_graph"]["relationship_count"] == 5
        and cat["collaboration"]["human_role_count"] == 6
        and cat["collaboration"]["ai_role_count"] == 5
        and cat["ethics"]["domain_count"] == 6
        and cat["governance"]["domain_count"] == 8
        and cat["governance"]["approval_gate_count"] == 7
        and cat["bounded_contexts"]["context_count"] == 7
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 10
        and cat["never_replace_p218_u_human_evolution"] is True
        and cat["never_replace_p218_t_civilization"] is True
        and cat["never_ungated_collective_decision"] is True
        and cat["never_skip_cognitive_privacy"] is True
        and cat["never_violate_cognitive_sovereignty"] is True
        and cat["never_skip_ethical_intelligence_review"] is True
        and cat["never_opaque_unexplainable_intelligence_decisions"] is True
        and cat["never_skip_human_authority_preservation"] is True
        and cat["space_ai_via_p214z_acl_only"] is True
        and cat["no_module_local_llm"] is True
        and cat["foundation_for_p218_w"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        HumanGiCoreRoot.enable(tenant_id="t1", core_ref="c1").is_missing() is False,
        CognitiveCivilizationRoot.enable(tenant_id="t1", civilization_intel_ref="cc1").is_missing() is False,
        CollectiveIntelligenceRoot.enable(tenant_id="t1", collective_ref="col1").is_missing() is False,
        ReasoningArchitectureRoot.enable(tenant_id="t1", reasoning_ref="r1").is_missing() is False,
        HumanGiKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="kg1").is_missing() is False,
        HumanIntelligenceTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        HumanAiCollaborationRoot.enable(tenant_id="t1", collaboration_ref="colab1").is_missing() is False,
        GiEthicsRoot.enable(tenant_id="t1", ethics_ref="e1").is_missing() is False,
        GiGovernanceRoot.enable(tenant_id="t1", governance_ref="g1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/space/infrastructure/acl/sp_human_gi_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "to_space_foundation", "to_space_mission", "to_space_strategy", "to_space_domain",
        "to_space_infrastructure", "to_space_ai", "to_satellite", "to_orbital",
        "to_communications", "to_navigation", "to_mission_intel", "to_scientific",
        "to_exploration", "to_manufacturing", "to_resources", "to_logistics",
        "to_security", "to_sustainability", "to_commerce", "to_education", "to_civilization",
        "to_human_evolution", "to_biotechnology", "to_robotics_supreme", "to_quantum_supreme",
        "to_master_ai", "to_integration", "to_policy_engine", "to_workflow", "to_audit",
        "to_identity", "to_core_platform", "to_enterprise_space",
        "never_replace_p218_u_human_evolution", "never_replace_p218_t_civilization",
        "never_ungated_collective_decision", "never_skip_cognitive_privacy",
        "never_violate_cognitive_sovereignty", "never_skip_ethical_intelligence_review",
        "never_opaque_unexplainable_intelligence_decisions", "never_skip_human_authority_preservation",
        "module_local_human_gi_forbidden", "space_ai_via_p214z_acl_only", "no_module_local_llm",
    ))
    router = (root / "backend/contexts/space/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@space_router.get("/human-gi")', "/human-gi/vision",
        "/human-gi/architecture", "/human-gi/lifecycle",
        "/human-gi/core", "/human-gi/cognitive-civilization",
        "/human-gi/collective", "/human-gi/reasoning",
        "/human-gi/knowledge-graph", "/human-gi/digital-twin",
        "/human-gi/collaboration", "/human-gi/ethics",
        "/human-gi/governance", "/human-gi/observability",
        "/human-gi/security", "/human-gi/integration",
        "/human-gi/deployment", "/human-gi/testing",
        "/human-gi/cqrs", "/human-gi/events",
        "/human-gi/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_SPACE_INTELLIGENCE_HUMAN_GI.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Human-GI Architecture is missing",
        "Never Advanced Cognitive Civilization is missing",
        "Never Collective Intelligence is missing",
        "Never Reasoning Architecture is missing",
        "Never Knowledge Graph is missing",
        "Never Human Intelligence Digital Twin is missing",
        "Never Ethical Governance is missing",
        "Never Human-AI Collaboration is missing",
        "Never Governance is missing",
        "Never Observability is missing", "Never Deployment Architecture is missing",
        "Never CQRS architecture is missing", "Never Event Architecture is missing",
        "Never Microservices Architecture is missing", "Never Sibling Space BC",
        "Never Replace P218-U Human Evolution",
        "Never Replace P218-T Civilization",
        "Never Module-Local LLM", "Never Opaque Unexplainable Intelligence Decisions",
        "Never Skip Cognitive Privacy",
        "Never Violate Cognitive Sovereignty",
        "Never Skip Ethical Intelligence Review",
        "Never Ungated Collective Decision",
        "Never Skip Human Authority Preservation",
        "enterprise intelligence architecture that expands human reasoning",
        "P218-V", "P218-W",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P218-V", "adr": 548, "passed": passed,
        "missing_artifacts": missing, "forbidden_sibling_present": sibling,
        "catalog": catalog_ok, "aggregates": all(checks), "acl": acl_ok,
        "router": router_ok, "documentation": doc_ok, "sor": "space",
        "capability": "CAP-PLT-SP-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
