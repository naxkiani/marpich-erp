"""Space P218-U Human Evolution Intelligence foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/547-enterprise-space-intelligence-human-evolution.md",
    "docs/architecture/ENTERPRISE_SPACE_INTELLIGENCE_HUMAN_EVOLUTION.md",
    "docs/architecture/space/HUMAN_EVOLUTION_ARCHITECTURE.v1.yaml",
    "docs/architecture/space/HUMAN_EVOLUTION_LIFECYCLE.v1.yaml",
    "docs/architecture/space/HUMAN_EVOLUTION_DDD_CQRS.v1.yaml",
    "docs/architecture/space/HUMAN_EVOLUTION_CONTROLS.v1.yaml",
    "docs/architecture/space/HUMAN_EVOLUTION_VALIDATION.v1.yaml",
    "docs/architecture/space/P218_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/space/domain/services/sp_platform_human_evolution.py",
    "backend/contexts/space/domain/aggregates/sp_human_evolution_aggregates.py",
    "backend/contexts/space/infrastructure/acl/sp_human_evolution_acl.py",
    "backend/contexts/space/application/sp_human_evolution_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/human_evolution_platform",
    "backend/contexts/human_augmentation_bc",
    "backend/contexts/neural_intelligence_bc",
)


def validate_sp_human_evolution_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.space.domain.aggregates.sp_human_evolution_aggregates import (
        CapabilityDigitalTwinRoot, CognitiveEnhancementRoot, EvolutionAiRoot,
        EvolutionEthicsRoot, EvolutionGovernanceRoot, EvolutionKnowledgeGraphRoot,
        HumanAugmentationRoot, HumanMachineSymbiosisRoot, NeuralIntelligenceRoot,
    )
    from contexts.space.domain.services import sp_platform_human_evolution as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P218-U" and cat["adr"] == 547 and cat["sor"] == "space"
        and cat["capability"] == "CAP-PLT-SP-001"
        and cat["fabric"] == "meos_human_evolution_intelligence_fabric"
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
        and cat["civilization_gate"] == "P218-T"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["human_augmentation_platform_present_required"] is True
        and cat["human_machine_symbiosis_present_required"] is True
        and cat["cognitive_enhancement_present_required"] is True
        and cat["neural_intelligence_present_required"] is True
        and cat["human_capability_digital_twin_present_required"] is True
        and cat["evolution_ai_present_required"] is True
        and cat["ethics_framework_present_required"] is True
        and cat["governance_present_required"] is True
        and cat["knowledge_graph_present_required"] is True
        and cat["architecture"]["layer_count"] == 5
        and cat["lifecycle"]["stage_count"] == 10
        and cat["augmentation"]["capability_count"] == 5
        and cat["symbiosis"]["domain_count"] == 7
        and cat["symbiosis"]["collaboration_model_count"] == 5
        and cat["cognitive"]["domain_count"] == 6
        and cat["cognitive"]["ai_component_count"] == 5
        and cat["neural"]["architecture_domain_count"] == 5
        and cat["neural"]["security_principle_count"] == 4
        and cat["evolution_ai"]["model_count"] == 5
        and cat["knowledge_graph"]["entity_count"] == 9
        and cat["knowledge_graph"]["relationship_count"] == 5
        and cat["ethics"]["domain_count"] == 5
        and cat["governance"]["domain_count"] == 8
        and cat["governance"]["approval_gate_count"] == 7
        and cat["bounded_contexts"]["context_count"] == 7
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 10
        and cat["never_replace_p218_t_civilization"] is True
        and cat["never_ungated_augmentation_approval"] is True
        and cat["never_skip_human_consent"] is True
        and cat["never_skip_ethical_augmentation_review"] is True
        and cat["never_violate_human_sovereignty"] is True
        and cat["never_opaque_unexplainable_evolution_decisions"] is True
        and cat["never_skip_neural_data_privacy"] is True
        and cat["space_ai_via_p214z_acl_only"] is True
        and cat["no_module_local_llm"] is True
        and cat["foundation_for_p218_v"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        HumanAugmentationRoot.enable(tenant_id="t1", augmentation_ref="a1").is_missing() is False,
        HumanMachineSymbiosisRoot.enable(tenant_id="t1", symbiosis_ref="s1").is_missing() is False,
        CognitiveEnhancementRoot.enable(tenant_id="t1", cognitive_ref="c1").is_missing() is False,
        NeuralIntelligenceRoot.enable(tenant_id="t1", neural_ref="n1").is_missing() is False,
        CapabilityDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        EvolutionAiRoot.enable(tenant_id="t1", evolution_ai_ref="ai1").is_missing() is False,
        EvolutionEthicsRoot.enable(tenant_id="t1", ethics_ref="e1").is_missing() is False,
        EvolutionKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="kg1").is_missing() is False,
        EvolutionGovernanceRoot.enable(tenant_id="t1", governance_ref="g1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/space/infrastructure/acl/sp_human_evolution_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "to_space_foundation", "to_space_mission", "to_space_strategy", "to_space_domain",
        "to_space_infrastructure", "to_space_ai", "to_satellite", "to_orbital",
        "to_communications", "to_navigation", "to_mission_intel", "to_scientific",
        "to_exploration", "to_manufacturing", "to_resources", "to_logistics",
        "to_security", "to_sustainability", "to_commerce", "to_education", "to_civilization",
        "to_biotechnology", "to_robotics_supreme", "to_quantum_supreme", "to_master_ai",
        "to_integration", "to_policy_engine", "to_workflow", "to_audit", "to_identity",
        "to_core_platform", "to_enterprise_space", "never_replace_p218_t_civilization",
        "never_ungated_augmentation_approval", "never_skip_human_consent",
        "never_skip_ethical_augmentation_review", "never_violate_human_sovereignty",
        "never_opaque_unexplainable_evolution_decisions", "never_skip_neural_data_privacy",
        "module_local_human_evolution_forbidden", "space_ai_via_p214z_acl_only", "no_module_local_llm",
    ))
    router = (root / "backend/contexts/space/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@space_router.get("/human-evolution")', "/human-evolution/vision",
        "/human-evolution/architecture", "/human-evolution/lifecycle",
        "/human-evolution/augmentation", "/human-evolution/symbiosis",
        "/human-evolution/cognitive", "/human-evolution/neural",
        "/human-evolution/evolution-ai", "/human-evolution/digital-twin",
        "/human-evolution/knowledge-graph", "/human-evolution/ethics",
        "/human-evolution/governance", "/human-evolution/observability",
        "/human-evolution/security", "/human-evolution/integration",
        "/human-evolution/deployment", "/human-evolution/testing",
        "/human-evolution/cqrs", "/human-evolution/events",
        "/human-evolution/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_SPACE_INTELLIGENCE_HUMAN_EVOLUTION.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Human Augmentation Platform is missing",
        "Never Human-Machine Symbiosis is missing",
        "Never Cognitive Enhancement is missing",
        "Never Neural Intelligence is missing",
        "Never Human Capability Digital Twin is missing",
        "Never Evolution AI is missing",
        "Never Ethics Framework is missing",
        "Never Governance is missing",
        "Never Knowledge Graph is missing",
        "Never Human Evolution Architecture is missing",
        "Never Observability is missing", "Never Deployment Architecture is missing",
        "Never CQRS architecture is missing", "Never Event Architecture is missing",
        "Never Microservices Architecture is missing", "Never Sibling Space BC",
        "Never Replace P218-T Civilization",
        "Never Module-Local LLM", "Never Ungated Augmentation Approval",
        "Never Skip Human Consent",
        "Never Skip Ethical Augmentation Review",
        "Never Violate Human Sovereignty",
        "Never Opaque Unexplainable Evolution Decisions",
        "Never Skip Neural Data Privacy",
        "intelligent platform that enables humanity to safely extend",
        "P218-U", "P218-V",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P218-U", "adr": 547, "passed": passed,
        "missing_artifacts": missing, "forbidden_sibling_present": sibling,
        "catalog": catalog_ok, "aggregates": all(checks), "acl": acl_ok,
        "router": router_ok, "documentation": doc_ok, "sor": "space",
        "capability": "CAP-PLT-SP-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
