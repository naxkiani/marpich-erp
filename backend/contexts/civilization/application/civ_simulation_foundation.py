"""Civilization P219-F Earth Intelligence Twin / simulation foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/559-enterprise-civilization-operating-system-simulation.md",
    "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_SIMULATION.md",
    "docs/architecture/civilization/CIVILIZATION_SIMULATION_CAPABILITIES.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_SIMULATION_ARCHITECTURE.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_SIMULATION_DDD_CQRS.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_SIMULATION_SECURITY.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_SIMULATION_VALIDATION.v1.yaml",
    "docs/architecture/civilization/P219_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/civilization/domain/services/civ_platform_simulation.py",
    "backend/contexts/civilization/domain/aggregates/civ_simulation_aggregates.py",
    "backend/contexts/civilization/infrastructure/acl/civ_simulation_acl.py",
    "backend/contexts/civilization/application/civ_simulation_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/earth_intelligence_twin_platform",
    "backend/contexts/planetary_digital_twin_bc",
    "backend/contexts/civilization_simulation_engine_bc",
)


def validate_civ_simulation_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.civilization.domain.aggregates.civ_simulation_aggregates import (
        CivilizationSimulationEngineRoot,
        DigitalTwinAiEngineRoot,
        DigitalTwinDomainModelRoot,
        EarthIntelligenceKnowledgeGraphRoot,
        EarthSimulationPlatformRoot,
        FutureScenarioIntelligenceRoot,
        MeosEarthIntelligenceTwinRoot,
        PlanetaryDigitalTwinArchitectureRoot,
        SimulationEventArchitectureRoot,
    )
    from contexts.civilization.domain.services import civ_platform_simulation as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P219-F" and cat["adr"] == 559 and cat["sor"] == "civilization"
        and cat["capability"] == "CAP-PLT-CIV-001"
        and cat["fabric"] == "meos_civilization_os_earth_intelligence_twin_framework"
        and cat["foundation_gate"] == "P219" and cat["mission_gate"] == "P219-A"
        and cat["strategy_gate"] == "P219-B" and cat["domain_gate"] == "P219-C"
        and cat["planetary_gate"] == "P219-D" and cat["ai_os_gate"] == "P219-E"
        and cat["intelligence_nexus_gate"] == "P218-Z" and cat["space_gate"] == "P218"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["meos_earth_intelligence_twin_present_required"] is True
        and cat["planetary_digital_twin_architecture_present_required"] is True
        and cat["earth_simulation_platform_present_required"] is True
        and cat["civilization_simulation_engine_present_required"] is True
        and cat["future_scenario_intelligence_present_required"] is True
        and cat["digital_twin_domain_model_present_required"] is True
        and cat["earth_intelligence_knowledge_graph_present_required"] is True
        and cat["digital_twin_ai_intelligence_engine_present_required"] is True
        and cat["simulation_event_architecture_present_required"] is True
        and cat["simulation_cqrs_model_present_required"] is True
        and cat["meos_simulation_integration_map_present_required"] is True
        and cat["architecture"]["layer_count"] == 6
        and cat["architecture"]["evolution_stage_count"] == 6
        and cat["simulation_domains"]["domain_count"] == 8
        and cat["scenarios"]["category_count"] == 6
        and cat["scenarios"]["lifecycle_step_count"] == 6
        and cat["ai_engine"]["agent_count"] == 5
        and cat["bounded_contexts"]["context_count"] == 3
        and cat["aggregates"]["aggregate_count"] == 4
        and cat["events"]["core_event_count"] == 9
        and cat["cqrs"]["command_count"] == 5 and cat["cqrs"]["query_count"] == 5
        and cat["knowledge_graph"]["node_count"] == 11
        and cat["knowledge_graph"]["edge_count"] == 7
        and cat["microservices"]["service_count"] == 10
        and cat["never_replace_p219_foundation"] is True
        and cat["never_replace_p219_e_ai_os"] is True
        and cat["never_ungated_simulation_decision_execution"] is True
        and cat["never_treat_scenario_recommendation_as_binding_policy"] is True
        and cat["never_opaque_unexplainable_simulation_decisions"] is True
        and cat["no_module_local_llm"] is True
        and cat["foundation_for_p219_g"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        MeosEarthIntelligenceTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        PlanetaryDigitalTwinArchitectureRoot.enable(tenant_id="t1", architecture_ref="a1").is_missing() is False,
        EarthSimulationPlatformRoot.enable(tenant_id="t1", sim_ref="s1").is_missing() is False,
        CivilizationSimulationEngineRoot.enable(tenant_id="t1", civ_sim_ref="c1").is_missing() is False,
        FutureScenarioIntelligenceRoot.enable(tenant_id="t1", scenario_ref="sc1").is_missing() is False,
        DigitalTwinDomainModelRoot.enable(tenant_id="t1", domain_ref="d1").is_missing() is False,
        EarthIntelligenceKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="kg1").is_missing() is False,
        DigitalTwinAiEngineRoot.enable(tenant_id="t1", ai_ref="ai1").is_missing() is False,
        SimulationEventArchitectureRoot.enable(tenant_id="t1", events_ref="e1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/civilization/infrastructure/acl/civ_simulation_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p219", "via_p219_a", "via_p219_b", "via_p219_c", "via_p219_d", "via_p219_e",
        "via_p218_z", "via_p218", "via_p217", "via_p216_z", "via_p215_z", "via_p214_z",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p219_foundation", "never_replace_p219_a_mission", "never_replace_p219_b_strategy",
        "never_replace_p219_c_domain", "never_replace_p219_d_planetary", "never_replace_p219_e_ai_os",
        "never_replace_p218_z_intelligence_nexus", "never_replace_space",
        "never_merge_p218_t_space_civilization", "never_cross_context_aggregate_imports",
        "never_opaque_unexplainable_simulation_decisions",
        "never_ungated_simulation_decision_execution",
        "never_skip_human_authority_simulation",
        "never_skip_ethical_simulation_governance",
        "never_violate_human_sovereignty_simulation",
        "never_treat_scenario_recommendation_as_binding_policy",
        "module_local_llm_forbidden",
        "module_local_simulation_twin_forbidden",
    ))
    router = (root / "backend/contexts/civilization/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@civilization_router.get("/simulation")',
        "/simulation/architecture", "/simulation/domains", "/simulation/civilization",
        "/simulation/scenarios", "/simulation/knowledge-graph", "/simulation/ai",
        "/simulation/bounded-contexts", "/simulation/aggregates", "/simulation/events",
        "/simulation/cqrs", "/simulation/microservices", "/simulation/integration",
        "/simulation/relationships", "/simulation/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_SIMULATION.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never MEOS Earth Intelligence Twin is missing",
        "Never Planetary Digital Twin Architecture is missing",
        "Never Earth Simulation Platform is missing",
        "Never Civilization Simulation Engine is missing",
        "Never Future Scenario Intelligence is missing",
        "Never Digital Twin Domain Model is missing",
        "Never Earth Intelligence Knowledge Graph is missing",
        "Never Digital Twin AI Intelligence Engine is missing",
        "Never Simulation Event Architecture is missing",
        "Never Simulation CQRS Model is missing",
        "Never MEOS Simulation Integration Map is missing",
        "Never Replace P219 Foundation",
        "Never Replace P219-A Mission",
        "Never Replace P219-B Strategy",
        "Never Replace P219-C Domain",
        "Never Replace P219-D Planetary",
        "Never Replace P219-E AI OS",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace P215-Z Quantum",
        "Never Replace P216-Z Robotics",
        "Never Replace P217 Biotechnology",
        "Never Replace P218 Space",
        "Never Replace P218-Z Intelligence Nexus",
        "Never Merge P218-T Space Civilization Phase",
        "Never Module-Local LLM",
        "Never Cross-Context Aggregate Imports",
        "Never Opaque Unexplainable Simulation Decisions",
        "Never Ungated Simulation Decision Execution",
        "Never Skip Human Authority Simulation",
        "Never Skip Ethical Simulation Governance",
        "Never Violate Human Sovereignty Simulation",
        "Never Treat Scenario Recommendation as Binding Policy",
        "continuously evolving digital representation of Earth",
        "P219-G",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P219-F", "adr": 559, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "civilization",
        "capability": "CAP-PLT-CIV-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
