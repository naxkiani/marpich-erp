"""Space P218-Z Final Intelligence Nexus foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/552-enterprise-space-intelligence-intelligence-nexus.md",
    "docs/architecture/ENTERPRISE_SPACE_INTELLIGENCE_INTELLIGENCE_NEXUS.md",
    "docs/architecture/space/INTELLIGENCE_NEXUS_ARCHITECTURE.v1.yaml",
    "docs/architecture/space/INTELLIGENCE_NEXUS_LIFECYCLE.v1.yaml",
    "docs/architecture/space/INTELLIGENCE_NEXUS_DDD_CQRS.v1.yaml",
    "docs/architecture/space/INTELLIGENCE_NEXUS_CONTROLS.v1.yaml",
    "docs/architecture/space/INTELLIGENCE_NEXUS_VALIDATION.v1.yaml",
    "docs/architecture/space/P218_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/space/domain/services/sp_platform_intelligence_nexus.py",
    "backend/contexts/space/domain/aggregates/sp_intelligence_nexus_aggregates.py",
    "backend/contexts/space/infrastructure/acl/sp_intelligence_nexus_acl.py",
    "backend/contexts/space/application/sp_intelligence_nexus_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/intelligence_nexus_platform",
    "backend/contexts/supreme_control_plane_bc",
    "backend/contexts/final_intelligence_bc",
)


def validate_sp_intelligence_nexus_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.space.domain.aggregates.sp_intelligence_nexus_aggregates import (
        AgentEcosystemRoot, AutonomousCivilizationRoot, CivilizationDigitalTwinRoot,
        DecisionIntelligenceRoot, FinalArchitectureRoot, IntelligenceGovernanceRoot,
        IntelligenceNexusCoreRoot, SupremeControlPlaneRoot, UniversalKnowledgeGraphRoot,
    )
    from contexts.space.domain.services import sp_platform_intelligence_nexus as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P218-Z" and cat["adr"] == 552 and cat["sor"] == "space"
        and cat["capability"] == "CAP-PLT-SP-001"
        and cat["fabric"] == "meos_final_intelligence_nexus_fabric"
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
        and cat["human_gi_gate"] == "P218-V" and cat["collective_si_gate"] == "P218-W"
        and cat["singularity_gate"] == "P218-X" and cat["ultimate_governance_gate"] == "P218-Y"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["ultimate_intelligence_civilization_nexus_present_required"] is True
        and cat["meos_supreme_control_plane_present_required"] is True
        and cat["autonomous_civilization_intelligence_present_required"] is True
        and cat["final_enterprise_intelligence_architecture_present_required"] is True
        and cat["universal_knowledge_graph_present_required"] is True
        and cat["civilization_digital_twin_present_required"] is True
        and cat["intelligence_governance_present_required"] is True
        and cat["agent_ecosystem_present_required"] is True
        and cat["decision_intelligence_present_required"] is True
        and cat["governance_present_required"] is True
        and cat["architecture"]["layer_count"] == 6
        and cat["lifecycle"]["stage_count"] == 10
        and cat["nexus_core"]["capability_count"] == 7
        and cat["control_plane"]["domain_count"] == 7
        and cat["autonomous"]["domain_count"] == 7
        and cat["orchestration"]["agent_ecosystem_count"] == 8
        and cat["orchestration"]["agent_lifecycle_count"] == 7
        and cat["decision_engine"]["model_count"] == 6
        and cat["decision_engine"]["principle_count"] == 4
        and cat["knowledge_graph"]["entity_count"] == 11
        and cat["knowledge_graph"]["relationship_count"] == 6
        and cat["digital_twin"]["representation_count"] == 8
        and cat["agent_ecosystem"]["agent_count"] == 8
        and cat["governance"]["domain_count"] == 8
        and cat["governance"]["approval_gate_count"] == 7
        and cat["governance"]["layer_count"] == 5
        and cat["bounded_contexts"]["context_count"] == 7
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 10
        and cat["never_replace_p218_y_ultimate_governance"] is True
        and cat["never_replace_p218_x_singularity"] is True
        and cat["never_replace_p218_w_collective_si"] is True
        and cat["never_replace_p218_v_human_gi"] is True
        and cat["never_replace_p218_u_human_evolution"] is True
        and cat["never_replace_p218_t_civilization"] is True
        and cat["never_ungated_supreme_decision"] is True
        and cat["never_skip_intelligence_alignment"] is True
        and cat["never_violate_human_sovereignty"] is True
        and cat["never_skip_ethical_validation"] is True
        and cat["never_opaque_unexplainable_intelligence_decisions"] is True
        and cat["never_skip_human_authority_preservation"] is True
        and cat["space_ai_via_p214z_acl_only"] is True
        and cat["no_module_local_llm"] is True
        and cat["series_complete"] is True
        and cat["meos_final_intelligence_nexus_complete"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
        and cat["production_readiness"]["series_complete"] is True
    )
    checks = [
        IntelligenceNexusCoreRoot.enable(tenant_id="t1", core_ref="c1").is_missing() is False,
        SupremeControlPlaneRoot.enable(tenant_id="t1", control_plane_ref="cp1").is_missing() is False,
        AutonomousCivilizationRoot.enable(tenant_id="t1", autonomous_ref="a1").is_missing() is False,
        DecisionIntelligenceRoot.enable(tenant_id="t1", decision_ref="d1").is_missing() is False,
        AgentEcosystemRoot.enable(tenant_id="t1", agent_ref="ag1").is_missing() is False,
        UniversalKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="kg1").is_missing() is False,
        CivilizationDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        IntelligenceGovernanceRoot.enable(tenant_id="t1", governance_ref="g1").is_missing() is False,
        FinalArchitectureRoot.enable(tenant_id="t1", architecture_ref="fa1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/space/infrastructure/acl/sp_intelligence_nexus_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "to_space_foundation", "to_space_mission", "to_space_strategy", "to_space_domain",
        "to_space_infrastructure", "to_space_ai", "to_satellite", "to_orbital",
        "to_communications", "to_navigation", "to_mission_intel", "to_scientific",
        "to_exploration", "to_manufacturing", "to_resources", "to_logistics",
        "to_security", "to_sustainability", "to_commerce", "to_education", "to_civilization",
        "to_human_evolution", "to_human_gi", "to_collective_si", "to_singularity",
        "to_ultimate_governance", "to_biotechnology", "to_robotics_supreme", "to_quantum_supreme",
        "to_master_ai", "to_integration", "to_policy_engine", "to_workflow", "to_audit",
        "to_identity", "to_core_platform", "to_enterprise_space",
        "never_replace_p218_y_ultimate_governance", "never_replace_p218_x_singularity",
        "never_replace_p218_w_collective_si", "never_replace_p218_v_human_gi",
        "never_replace_p218_u_human_evolution", "never_replace_p218_t_civilization",
        "never_ungated_supreme_decision", "never_skip_intelligence_alignment",
        "never_violate_human_sovereignty", "never_skip_ethical_validation",
        "never_opaque_unexplainable_intelligence_decisions", "never_skip_human_authority_preservation",
        "module_local_intelligence_nexus_forbidden", "space_ai_via_p214z_acl_only",
        "no_module_local_llm", "series_complete",
    ))
    router = (root / "backend/contexts/space/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@space_router.get("/intelligence-nexus")', "/intelligence-nexus/vision",
        "/intelligence-nexus/architecture", "/intelligence-nexus/lifecycle",
        "/intelligence-nexus/core", "/intelligence-nexus/control-plane",
        "/intelligence-nexus/autonomous", "/intelligence-nexus/orchestration",
        "/intelligence-nexus/decision-engine", "/intelligence-nexus/knowledge-graph",
        "/intelligence-nexus/digital-twin", "/intelligence-nexus/agents",
        "/intelligence-nexus/ethics", "/intelligence-nexus/governance",
        "/intelligence-nexus/observability", "/intelligence-nexus/security",
        "/intelligence-nexus/integration", "/intelligence-nexus/deployment",
        "/intelligence-nexus/testing", "/intelligence-nexus/cqrs",
        "/intelligence-nexus/events", "/intelligence-nexus/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_SPACE_INTELLIGENCE_INTELLIGENCE_NEXUS.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Ultimate Intelligence Civilization Nexus is missing",
        "Never MEOS Supreme Control Plane is missing",
        "Never Autonomous Civilization Intelligence is missing",
        "Never Final Enterprise Intelligence Architecture is missing",
        "Never Universal Knowledge Graph is missing",
        "Never Civilization Digital Twin is missing",
        "Never Intelligence Governance is missing",
        "Never Agent Ecosystem is missing",
        "Never Decision Intelligence is missing",
        "Never Governance is missing",
        "Never Observability is missing", "Never Deployment Architecture is missing",
        "Never CQRS architecture is missing", "Never Event Architecture is missing",
        "Never Microservices Architecture is missing", "Never Sibling Space BC",
        "Never Replace P218-Y Ultimate Governance",
        "Never Replace P218-X Singularity",
        "Never Replace P218-W Collective Intelligence",
        "Never Replace P218-V Human General Intelligence",
        "Never Replace P218-U Human Evolution",
        "Never Replace P218-T Civilization",
        "Never Module-Local LLM", "Never Opaque Unexplainable Intelligence Decisions",
        "Never Ungated Supreme Decision",
        "Never Skip Intelligence Alignment",
        "Never Violate Human Sovereignty",
        "Never Skip Ethical Validation",
        "Never Skip Human Authority Preservation",
        "final intelligence coordination architecture capable of integrating",
        "P218-Z", "SERIES COMPLETE",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P218-Z", "adr": 552, "passed": passed,
        "missing_artifacts": missing, "forbidden_sibling_present": sibling,
        "catalog": catalog_ok, "aggregates": all(checks), "acl": acl_ok,
        "router": router_ok, "documentation": doc_ok, "sor": "space",
        "capability": "CAP-PLT-SP-001",
        "series_complete": True,
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
