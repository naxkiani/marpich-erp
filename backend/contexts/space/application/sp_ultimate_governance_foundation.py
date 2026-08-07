"""Space P218-Y Ultimate Intelligence Governance foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/551-enterprise-space-intelligence-ultimate-governance.md",
    "docs/architecture/ENTERPRISE_SPACE_INTELLIGENCE_ULTIMATE_GOVERNANCE.md",
    "docs/architecture/space/ULTIMATE_GOVERNANCE_ARCHITECTURE.v1.yaml",
    "docs/architecture/space/ULTIMATE_GOVERNANCE_LIFECYCLE.v1.yaml",
    "docs/architecture/space/ULTIMATE_GOVERNANCE_DDD_CQRS.v1.yaml",
    "docs/architecture/space/ULTIMATE_GOVERNANCE_CONTROLS.v1.yaml",
    "docs/architecture/space/ULTIMATE_GOVERNANCE_VALIDATION.v1.yaml",
    "docs/architecture/space/P218_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/space/domain/services/sp_platform_ultimate_governance.py",
    "backend/contexts/space/domain/aggregates/sp_ultimate_governance_aggregates.py",
    "backend/contexts/space/infrastructure/acl/sp_ultimate_governance_acl.py",
    "backend/contexts/space/application/sp_ultimate_governance_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/ultimate_governance_platform",
    "backend/contexts/intelligence_alignment_bc",
    "backend/contexts/future_trust_bc",
)


def validate_sp_ultimate_governance_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.space.domain.aggregates.sp_ultimate_governance_aggregates import (
        CivilizationTrustRoot, EthicsFrameworkRoot, FutureTrustRoot,
        GovernanceDigitalTwinRoot, GovernanceKnowledgeGraphRoot, IntelligenceAlignmentRoot,
        SafetyGovernanceRoot, UltimateGovernanceCoreRoot, UltimateGovernanceRoot,
    )
    from contexts.space.domain.services import sp_platform_ultimate_governance as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P218-Y" and cat["adr"] == 551 and cat["sor"] == "space"
        and cat["capability"] == "CAP-PLT-SP-001"
        and cat["fabric"] == "meos_ultimate_intelligence_governance_fabric"
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
        and cat["singularity_gate"] == "P218-X"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["ultimate_intelligence_governance_present_required"] is True
        and cat["intelligence_alignment_present_required"] is True
        and cat["future_trust_architecture_present_required"] is True
        and cat["ethics_framework_present_required"] is True
        and cat["safety_governance_present_required"] is True
        and cat["digital_twin_governance_present_required"] is True
        and cat["knowledge_graph_present_required"] is True
        and cat["domain_model_present_required"] is True
        and cat["civilization_trust_present_required"] is True
        and cat["governance_present_required"] is True
        and cat["architecture"]["layer_count"] == 5
        and cat["lifecycle"]["stage_count"] == 10
        and cat["ultimate_governance"]["capability_count"] == 7
        and cat["alignment"]["domain_count"] == 5
        and cat["alignment"]["agent_count"] == 5
        and cat["trust"]["trust_model_count"] == 5
        and cat["trust"]["domain_count"] == 5
        and cat["ethics"]["domain_count"] == 7
        and cat["ethics"]["component_count"] == 5
        and cat["safety"]["domain_count"] == 5
        and cat["safety"]["agent_count"] == 5
        and cat["knowledge_graph"]["entity_count"] == 9
        and cat["knowledge_graph"]["relationship_count"] == 5
        and cat["operating_model"]["layer_count"] == 5
        and cat["governance"]["domain_count"] == 8
        and cat["governance"]["approval_gate_count"] == 7
        and cat["bounded_contexts"]["context_count"] == 6
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 10
        and cat["never_replace_p218_x_singularity"] is True
        and cat["never_replace_p218_w_collective_si"] is True
        and cat["never_replace_p218_v_human_gi"] is True
        and cat["never_replace_p218_u_human_evolution"] is True
        and cat["never_replace_p218_t_civilization"] is True
        and cat["never_ungated_governance_decision"] is True
        and cat["never_skip_intelligence_alignment"] is True
        and cat["never_violate_human_sovereignty"] is True
        and cat["never_skip_ethical_validation"] is True
        and cat["never_opaque_unexplainable_intelligence_decisions"] is True
        and cat["never_skip_human_authority_preservation"] is True
        and cat["space_ai_via_p214z_acl_only"] is True
        and cat["no_module_local_llm"] is True
        and cat["foundation_for_p218_z"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        UltimateGovernanceCoreRoot.enable(tenant_id="t1", core_ref="c1").is_missing() is False,
        IntelligenceAlignmentRoot.enable(tenant_id="t1", alignment_ref="a1").is_missing() is False,
        FutureTrustRoot.enable(tenant_id="t1", trust_ref="tr1").is_missing() is False,
        EthicsFrameworkRoot.enable(tenant_id="t1", ethics_ref="e1").is_missing() is False,
        SafetyGovernanceRoot.enable(tenant_id="t1", safety_ref="s1").is_missing() is False,
        GovernanceDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        GovernanceKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="kg1").is_missing() is False,
        CivilizationTrustRoot.enable(tenant_id="t1", civilization_trust_ref="ct1").is_missing() is False,
        UltimateGovernanceRoot.enable(tenant_id="t1", governance_ref="g1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/space/infrastructure/acl/sp_ultimate_governance_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "to_space_foundation", "to_space_mission", "to_space_strategy", "to_space_domain",
        "to_space_infrastructure", "to_space_ai", "to_satellite", "to_orbital",
        "to_communications", "to_navigation", "to_mission_intel", "to_scientific",
        "to_exploration", "to_manufacturing", "to_resources", "to_logistics",
        "to_security", "to_sustainability", "to_commerce", "to_education", "to_civilization",
        "to_human_evolution", "to_human_gi", "to_collective_si", "to_singularity",
        "to_biotechnology", "to_robotics_supreme", "to_quantum_supreme", "to_master_ai",
        "to_integration", "to_policy_engine", "to_workflow", "to_audit", "to_identity",
        "to_core_platform", "to_enterprise_space",
        "never_replace_p218_x_singularity", "never_replace_p218_w_collective_si",
        "never_replace_p218_v_human_gi", "never_replace_p218_u_human_evolution",
        "never_replace_p218_t_civilization", "never_ungated_governance_decision",
        "never_skip_intelligence_alignment", "never_violate_human_sovereignty",
        "never_skip_ethical_validation", "never_opaque_unexplainable_intelligence_decisions",
        "never_skip_human_authority_preservation", "module_local_ultimate_governance_forbidden",
        "space_ai_via_p214z_acl_only", "no_module_local_llm",
    ))
    router = (root / "backend/contexts/space/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@space_router.get("/ultimate-governance")', "/ultimate-governance/vision",
        "/ultimate-governance/architecture", "/ultimate-governance/lifecycle",
        "/ultimate-governance/core", "/ultimate-governance/alignment",
        "/ultimate-governance/trust", "/ultimate-governance/ethics",
        "/ultimate-governance/safety", "/ultimate-governance/knowledge-graph",
        "/ultimate-governance/digital-twin", "/ultimate-governance/civilization-trust",
        "/ultimate-governance/operating-model", "/ultimate-governance/governance",
        "/ultimate-governance/observability", "/ultimate-governance/security",
        "/ultimate-governance/integration", "/ultimate-governance/deployment",
        "/ultimate-governance/testing", "/ultimate-governance/cqrs",
        "/ultimate-governance/events", "/ultimate-governance/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_SPACE_INTELLIGENCE_ULTIMATE_GOVERNANCE.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Ultimate Intelligence Governance is missing",
        "Never Intelligence Alignment is missing",
        "Never Future Trust Architecture is missing",
        "Never Ethics Framework is missing",
        "Never Safety Governance is missing",
        "Never Digital Twin Governance is missing",
        "Never Knowledge Graph is missing",
        "Never Domain Model is missing",
        "Never Civilization Trust is missing",
        "Never Governance is missing",
        "Never Observability is missing", "Never Deployment Architecture is missing",
        "Never CQRS architecture is missing", "Never Event Architecture is missing",
        "Never Microservices Architecture is missing", "Never Sibling Space BC",
        "Never Replace P218-X Singularity",
        "Never Replace P218-W Collective Intelligence",
        "Never Replace P218-V Human General Intelligence",
        "Never Replace P218-U Human Evolution",
        "Never Replace P218-T Civilization",
        "Never Module-Local LLM", "Never Opaque Unexplainable Intelligence Decisions",
        "Never Ungated Governance Decision",
        "Never Skip Intelligence Alignment",
        "Never Violate Human Sovereignty",
        "Never Skip Ethical Validation",
        "Never Skip Human Authority Preservation",
        "civilization-scale governance platform capable of ensuring",
        "P218-Y", "P218-Z",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P218-Y", "adr": 551, "passed": passed,
        "missing_artifacts": missing, "forbidden_sibling_present": sibling,
        "catalog": catalog_ok, "aggregates": all(checks), "acl": acl_ok,
        "router": router_ok, "documentation": doc_ok, "sor": "space",
        "capability": "CAP-PLT-SP-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
