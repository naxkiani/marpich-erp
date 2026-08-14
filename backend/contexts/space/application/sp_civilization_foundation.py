"""Space P218-T Civilization Intelligence foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/546-enterprise-space-intelligence-civilization.md",
    "docs/architecture/ENTERPRISE_SPACE_INTELLIGENCE_CIVILIZATION.md",
    "docs/architecture/space/CIVILIZATION_ARCHITECTURE.v1.yaml",
    "docs/architecture/space/CIVILIZATION_LIFECYCLE.v1.yaml",
    "docs/architecture/space/CIVILIZATION_DDD_CQRS.v1.yaml",
    "docs/architecture/space/CIVILIZATION_CONTROLS.v1.yaml",
    "docs/architecture/space/CIVILIZATION_VALIDATION.v1.yaml",
    "docs/architecture/space/P218_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/space/domain/services/sp_platform_civilization.py",
    "backend/contexts/space/domain/aggregates/sp_civilization_aggregates.py",
    "backend/contexts/space/infrastructure/acl/sp_civilization_acl.py",
    "backend/contexts/space/application/sp_civilization_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/space_civilization_platform",
    "backend/contexts/interplanetary_governance_bc",
    "backend/contexts/human_space_society_bc",
)


def validate_sp_civilization_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.space.domain.aggregates.sp_civilization_aggregates import (
        CivilizationAiRoot, CivilizationDigitalTwinRoot, CivilizationGovernanceRoot,
        CivilizationKnowledgeGraphRoot, CivilizationPlatformRoot, EthicsFrameworkRoot,
        FutureArchitectureRoot, HumanSocietyRoot, InterplanetaryGovernanceRoot,
    )
    from contexts.space.domain.services import sp_platform_civilization as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P218-T" and cat["adr"] == 546 and cat["sor"] == "space"
        and cat["capability"] == "CAP-PLT-SP-001"
        and cat["fabric"] == "meos_space_civilization_intelligence_fabric"
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
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["space_civilization_platform_present_required"] is True
        and cat["human_society_intelligence_present_required"] is True
        and cat["interplanetary_governance_present_required"] is True
        and cat["future_civilization_architecture_present_required"] is True
        and cat["civilization_ai_present_required"] is True
        and cat["digital_civilization_twin_present_required"] is True
        and cat["knowledge_graph_present_required"] is True
        and cat["ethics_framework_present_required"] is True
        and cat["governance_present_required"] is True
        and cat["architecture"]["layer_count"] == 5
        and cat["lifecycle"]["stage_count"] == 10
        and cat["society"]["domain_count"] == 5
        and cat["society"]["capability_count"] == 6
        and cat["governance_platform"]["domain_count"] == 6
        and cat["governance_platform"]["agent_count"] == 5
        and cat["future_architecture"]["component_count"] == 6
        and cat["future_architecture"]["architecture_domain_count"] == 6
        and cat["civilization_ai"]["capability_count"] == 7
        and cat["civilization_ai"]["model_count"] == 5
        and cat["knowledge_graph"]["entity_count"] == 9
        and cat["knowledge_graph"]["relationship_count"] == 5
        and cat["ethics"]["domain_count"] == 5
        and cat["governance"]["domain_count"] == 8
        and cat["governance"]["approval_gate_count"] == 7
        and cat["bounded_contexts"]["context_count"] == 7
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 10
        and cat["never_replace_p218_s_education"] is True
        and cat["never_ungated_governance_decision"] is True
        and cat["never_skip_ethical_ai_review"] is True
        and cat["never_skip_human_rights_protection"] is True
        and cat["never_opaque_unexplainable_civilization_decisions"] is True
        and cat["space_ai_via_p214z_acl_only"] is True
        and cat["no_module_local_llm"] is True
        and cat["foundation_for_p218_u"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        CivilizationPlatformRoot.enable(tenant_id="t1", platform_ref="p1").is_missing() is False,
        HumanSocietyRoot.enable(tenant_id="t1", society_ref="s1").is_missing() is False,
        InterplanetaryGovernanceRoot.enable(tenant_id="t1", governance_ref="g1").is_missing() is False,
        FutureArchitectureRoot.enable(tenant_id="t1", future_arch_ref="f1").is_missing() is False,
        CivilizationAiRoot.enable(tenant_id="t1", civilization_ai_ref="a1").is_missing() is False,
        CivilizationDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        CivilizationKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="kg1").is_missing() is False,
        EthicsFrameworkRoot.enable(tenant_id="t1", ethics_ref="e1").is_missing() is False,
        CivilizationGovernanceRoot.enable(tenant_id="t1", civ_gov_ref="cg1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/space/infrastructure/acl/sp_civilization_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "to_space_foundation", "to_space_mission", "to_space_strategy", "to_space_domain",
        "to_space_infrastructure", "to_space_ai", "to_satellite", "to_orbital",
        "to_communications", "to_navigation", "to_mission_intel", "to_scientific",
        "to_exploration", "to_manufacturing", "to_resources", "to_logistics",
        "to_security", "to_sustainability", "to_commerce", "to_education",
        "to_biotechnology", "to_robotics_supreme", "to_quantum_supreme", "to_master_ai",
        "to_integration", "to_policy_engine", "to_workflow", "to_audit", "to_identity",
        "to_core_platform", "to_enterprise_space", "never_replace_p218_s_education",
        "never_ungated_governance_decision", "never_skip_ethical_ai_review",
        "never_skip_human_rights_protection", "never_opaque_unexplainable_civilization_decisions",
        "module_local_civilization_forbidden", "space_ai_via_p214z_acl_only", "no_module_local_llm",
    ))
    router = (root / "backend/contexts/space/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@space_router.get("/civilization")', "/civilization/vision",
        "/civilization/architecture", "/civilization/lifecycle", "/civilization/society",
        "/civilization/governance", "/civilization/future-architecture",
        "/civilization/civilization-ai", "/civilization/digital-twin", "/civilization/culture",
        "/civilization/knowledge-graph", "/civilization/economy", "/civilization/observability",
        "/civilization/ethics", "/civilization/security", "/civilization/integration",
        "/civilization/deployment", "/civilization/testing", "/civilization/cqrs",
        "/civilization/events", "/civilization/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_SPACE_INTELLIGENCE_CIVILIZATION.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Space Civilization Platform is missing",
        "Never Human Society Intelligence is missing",
        "Never Interplanetary Governance is missing",
        "Never Future Civilization Architecture is missing",
        "Never Civilization AI is missing",
        "Never Digital Civilization Twin is missing",
        "Never Knowledge Graph is missing",
        "Never Ethics Framework is missing",
        "Never Governance is missing", "Never Civilization Architecture is missing",
        "Never Observability is missing", "Never Deployment Architecture is missing",
        "Never CQRS architecture is missing", "Never Event Architecture is missing",
        "Never Microservices Architecture is missing", "Never Sibling Space BC",
        "Never Replace P218-S Education",
        "Never Module-Local LLM", "Never Ungated Governance Decision",
        "Never Skip Ethical AI Review",
        "Never Skip Human Rights Protection",
        "Never Opaque Unexplainable Civilization Decisions",
        "intelligent civilization operating platform capable of modeling",
        "P218-T", "P218-U",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P218-T", "adr": 546, "passed": passed,
        "missing_artifacts": missing, "forbidden_sibling_present": sibling,
        "catalog": catalog_ok, "aggregates": all(checks), "acl": acl_ok,
        "router": router_ok, "documentation": doc_ok, "sor": "space",
        "capability": "CAP-PLT-SP-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
