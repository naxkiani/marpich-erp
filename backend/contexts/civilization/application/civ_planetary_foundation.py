"""Civilization P219-D planetary infrastructure intelligence foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/557-enterprise-civilization-operating-system-planetary.md",
    "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_PLANETARY.md",
    "docs/architecture/civilization/CIVILIZATION_PLANETARY_CAPABILITIES.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_PLANETARY_ARCHITECTURE.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_PLANETARY_DDD_CQRS.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_PLANETARY_SECURITY.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_PLANETARY_VALIDATION.v1.yaml",
    "docs/architecture/civilization/P219_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/civilization/domain/services/civ_platform_planetary.py",
    "backend/contexts/civilization/domain/aggregates/civ_planetary_aggregates.py",
    "backend/contexts/civilization/infrastructure/acl/civ_planetary_acl.py",
    "backend/contexts/civilization/application/civ_planetary_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/planetary_intelligence_platform",
    "backend/contexts/earth_digital_twin_bc",
    "backend/contexts/smart_planet_os_bc",
)


def validate_civ_planetary_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.civilization.domain.aggregates.civ_planetary_aggregates import (
        AutonomousPlanetaryOpsRoot,
        EarthDigitalTwinRoot,
        GlobalInfrastructureIntelligenceRoot,
        MeosPlanetaryIntelligenceCoreRoot,
        PlanetaryAiEngineRoot,
        PlanetaryEventArchitectureRoot,
        PlanetaryIntelligencePlatformRoot,
        PlanetaryKnowledgeGraphRoot,
        SmartPlanetArchitectureRoot,
    )
    from contexts.civilization.domain.services import civ_platform_planetary as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P219-D" and cat["adr"] == 557 and cat["sor"] == "civilization"
        and cat["capability"] == "CAP-PLT-CIV-001"
        and cat["fabric"] == "meos_civilization_os_planetary_intelligence_framework"
        and cat["foundation_gate"] == "P219" and cat["mission_gate"] == "P219-A"
        and cat["strategy_gate"] == "P219-B" and cat["domain_gate"] == "P219-C"
        and cat["intelligence_nexus_gate"] == "P218-Z" and cat["space_gate"] == "P218"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["planetary_intelligence_platform_present_required"] is True
        and cat["earth_digital_twin_present_required"] is True
        and cat["smart_planet_architecture_present_required"] is True
        and cat["global_infrastructure_intelligence_present_required"] is True
        and cat["autonomous_planetary_operations_foundation_present_required"] is True
        and cat["meos_planetary_intelligence_core_present_required"] is True
        and cat["planetary_knowledge_graph_present_required"] is True
        and cat["planetary_ai_engine_contract_present_required"] is True
        and cat["planetary_event_architecture_present_required"] is True
        and cat["planetary_cqrs_model_present_required"] is True
        and cat["meos_planetary_integration_map_present_required"] is True
        and cat["architecture_layers"]["layer_count"] == 6
        and cat["architecture_layers"]["evolution_stage_count"] == 5
        and cat["global_systems"]["system_count"] == 8
        and cat["earth_digital_twin"]["engine_count"] == 4
        and cat["earth_digital_twin"]["entity_count"] == 5
        and cat["bounded_contexts"]["context_count"] == 3
        and cat["aggregates"]["aggregate_count"] == 4
        and cat["events"]["core_event_count"] == 12
        and cat["cqrs"]["command_count"] == 5 and cat["cqrs"]["query_count"] == 5
        and cat["knowledge_graph"]["node_count"] == 10
        and cat["knowledge_graph"]["edge_count"] == 7
        and cat["ai_engine"]["agent_count"] == 5
        and cat["microservices"]["service_count"] == 10
        and cat["never_replace_p219_foundation"] is True
        and cat["never_replace_p219_a_mission"] is True
        and cat["never_replace_p219_b_strategy"] is True
        and cat["never_replace_p219_c_domain"] is True
        and cat["never_cross_context_aggregate_imports"] is True
        and cat["never_opaque_unexplainable_planetary_decisions"] is True
        and cat["never_ungated_planetary_decision_autonomy"] is True
        and cat["never_direct_physical_control_without_workflow_gate"] is True
        and cat["foundation_for_p219_e"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        PlanetaryIntelligencePlatformRoot.enable(tenant_id="t1", planetary_ref="p1").is_missing() is False,
        EarthDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        SmartPlanetArchitectureRoot.enable(tenant_id="t1", smart_ref="s1").is_missing() is False,
        GlobalInfrastructureIntelligenceRoot.enable(tenant_id="t1", global_ref="g1").is_missing() is False,
        AutonomousPlanetaryOpsRoot.enable(tenant_id="t1", ops_ref="o1").is_missing() is False,
        MeosPlanetaryIntelligenceCoreRoot.enable(tenant_id="t1", core_ref="c1").is_missing() is False,
        PlanetaryKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="kg1").is_missing() is False,
        PlanetaryAiEngineRoot.enable(tenant_id="t1", ai_ref="ai1").is_missing() is False,
        PlanetaryEventArchitectureRoot.enable(tenant_id="t1", events_ref="e1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/civilization/infrastructure/acl/civ_planetary_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p219", "via_p219_a", "via_p219_b", "via_p219_c", "via_p218_z", "via_p218", "via_p217",
        "via_p216_z", "via_p215_z", "via_p214_z",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p219_foundation", "never_replace_p219_a_mission", "never_replace_p219_b_strategy",
        "never_replace_p219_c_domain", "never_replace_p218_z_intelligence_nexus", "never_replace_space",
        "never_merge_p218_t_space_civilization", "never_cross_context_aggregate_imports",
        "never_opaque_unexplainable_planetary_decisions",
        "never_ungated_planetary_decision_autonomy",
        "never_skip_human_authority_planetary",
        "never_skip_ethical_planetary_governance",
        "never_violate_human_sovereignty_planetary",
        "never_direct_physical_control_without_workflow_gate",
        "module_local_planetary_intelligence_forbidden",
    ))
    router = (root / "backend/contexts/civilization/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@civilization_router.get("/planetary")',
        "/planetary/architecture", "/planetary/smart-planet", "/planetary/global-systems",
        "/planetary/digital-twin", "/planetary/bounded-contexts", "/planetary/aggregates",
        "/planetary/events", "/planetary/cqrs", "/planetary/knowledge-graph",
        "/planetary/ai", "/planetary/autonomous-ops", "/planetary/microservices",
        "/planetary/integration", "/planetary/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_PLANETARY.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Planetary Intelligence Platform is missing",
        "Never Earth Digital Twin is missing",
        "Never Smart Planet Architecture is missing",
        "Never Global Infrastructure Intelligence is missing",
        "Never Autonomous Planetary Operations Foundation is missing",
        "Never MEOS Planetary Intelligence Core is missing",
        "Never Planetary Knowledge Graph is missing",
        "Never Planetary AI Engine Contract is missing",
        "Never Planetary Event Architecture is missing",
        "Never Planetary CQRS Model is missing",
        "Never MEOS Planetary Integration Map is missing",
        "Never Replace P219 Foundation",
        "Never Replace P219-A Mission",
        "Never Replace P219-B Strategy",
        "Never Replace P219-C Domain",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace P215-Z Quantum",
        "Never Replace P216-Z Robotics",
        "Never Replace P217 Biotechnology",
        "Never Replace P218 Space",
        "Never Replace P218-Z Intelligence Nexus",
        "Never Merge P218-T Space Civilization Phase",
        "Never Cross-Context Aggregate Imports",
        "Never Opaque Unexplainable Planetary Decisions",
        "Never Ungated Planetary Decision Autonomy",
        "Never Skip Human Authority Planetary",
        "Never Skip Ethical Planetary Governance",
        "Never Violate Human Sovereignty Planetary",
        "Never Direct Physical Control Without Workflow Gate",
        "unified intelligent ecosystem",
        "P219-E",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P219-D", "adr": 557, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "civilization",
        "capability": "CAP-PLT-CIV-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
