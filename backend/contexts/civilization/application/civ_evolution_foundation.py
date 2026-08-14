"""Civilization P219-R evolution intelligence foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/571-enterprise-civilization-operating-system-evolution.md",
    "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_EVOLUTION.md",
    "docs/architecture/civilization/CIVILIZATION_EVOLUTION_CAPABILITIES.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_EVOLUTION_ARCHITECTURE.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_EVOLUTION_DDD_CQRS.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_EVOLUTION_SECURITY.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_EVOLUTION_VALIDATION.v1.yaml",
    "docs/architecture/civilization/P219_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/civilization/domain/services/civ_platform_evolution.py",
    "backend/contexts/civilization/domain/aggregates/civ_evolution_aggregates.py",
    "backend/contexts/civilization/infrastructure/acl/civ_evolution_acl.py",
    "backend/contexts/civilization/application/civ_evolution_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/civilization_evolution_intelligence_platform",
    "backend/contexts/adaptive_civilization_evolution_bc",
    "backend/contexts/long_term_strategy_platform_bc",
)


def validate_civ_evolution_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.civilization.domain.aggregates.civ_evolution_aggregates import (
        AdaptiveCivilizationEvolutionPlatformRoot,
        CivilizationEvolutionIntelligencePlatformRoot,
        EvolutionDigitalTwinRoot,
        EvolutionEventArchitectureRoot,
        EvolutionKnowledgeGraphRoot,
        EvolutionOptimizationFrameworkRoot,
        FutureScenarioEngineRoot,
        LongTermStrategyPlatformRoot,
        MeosCivilizationEvolutionIntelligenceCoreRoot,
    )
    from contexts.civilization.domain.services import civ_platform_evolution as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P219-R" and cat["adr"] == 571 and cat["sor"] == "civilization"
        and cat["capability"] == "CAP-PLT-CIV-001"
        and cat["fabric"] == "meos_civilization_os_civilization_evolution_intelligence_framework"
        and cat["foundation_gate"] == "P219" and cat["mission_gate"] == "P219-A"
        and cat["strategy_gate"] == "P219-B" and cat["domain_gate"] == "P219-C"
        and cat["planetary_gate"] == "P219-D" and cat["ai_os_gate"] == "P219-E"
        and cat["simulation_gate"] == "P219-F" and cat["resources_gate"] == "P219-G"
        and cat["economy_gate"] == "P219-H" and cat["knowledge_gate"] == "P219-I"
        and cat["human_gate"] == "P219-J" and cat["governance_gate"] == "P219-K"
        and cat["innovation_gate"] == "P219-L" and cat["security_gate"] == "P219-M"
        and cat["sustainability_gate"] == "P219-N" and cat["prosperity_gate"] == "P219-O"
        and cat["collaboration_gate"] == "P219-P" and cat["consciousness_gate"] == "P219-Q"
        and cat["intelligence_nexus_gate"] == "P218-Z" and cat["space_gate"] == "P218"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["civilization_evolution_intelligence_platform_present_required"] is True
        and cat["adaptive_civilization_evolution_platform_present_required"] is True
        and cat["long_term_strategy_platform_present_required"] is True
        and cat["future_scenario_engine_present_required"] is True
        and cat["evolution_digital_twin_present_required"] is True
        and cat["evolution_optimization_framework_present_required"] is True
        and cat["meos_civilization_evolution_intelligence_core_present_required"] is True
        and cat["evolution_knowledge_graph_present_required"] is True
        and cat["evolution_event_architecture_present_required"] is True
        and cat["evolution_cqrs_model_present_required"] is True
        and cat["meos_evolution_integration_map_present_required"] is True
        and cat["architecture"]["evolution_stage_count"] == 7
        and cat["architecture"]["layer_count"] == 6
        and cat["architecture"]["dynamics_domain_count"] == 10
        and cat["architecture"]["planning_horizon_count"] == 7
        and cat["architecture"]["adaptive_domain_count"] == 8
        and cat["architecture"]["optimization_objective_count"] == 8
        and cat["architecture"]["optimization_lifecycle_step_count"] == 7
        and cat["architecture"]["scenario_type_count"] == 8
        and cat["agents"]["agent_count"] == 5
        and cat["knowledge_graph"]["entity_count"] == 10
        and cat["knowledge_graph"]["relationship_count"] == 8
        and cat["digital_twin"]["twin_count"] == 4
        and cat["bounded_contexts"]["context_count"] == 4
        and cat["aggregates"]["aggregate_count"] == 5
        and cat["events"]["core_event_count"] == 12
        and cat["cqrs"]["command_count"] == 6 and cat["cqrs"]["query_count"] == 6
        and cat["microservices"]["service_count"] == 10
        and cat["never_replace_p219_foundation"] is True
        and cat["never_replace_p219_q_consciousness"] is True
        and cat["never_replace_p219_f_simulation"] is True
        and cat["never_replace_p219_e_ai_os"] is True
        and cat["never_ungated_evolution_transformation_execution"] is True
        and cat["never_treat_forecast_as_binding_policy"] is True
        and cat["never_bypass_human_supervision_evolution"] is True
        and cat["never_opaque_unexplainable_evolution_decisions"] is True
        and cat["no_module_local_llm"] is True
        and cat["foundation_for_p219_s"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        CivilizationEvolutionIntelligencePlatformRoot.enable(
            tenant_id="t1", evolution_ref="e1"
        ).is_missing() is False,
        AdaptiveCivilizationEvolutionPlatformRoot.enable(
            tenant_id="t1", adaptive_ref="a1"
        ).is_missing() is False,
        LongTermStrategyPlatformRoot.enable(tenant_id="t1", strategy_ref="s1").is_missing() is False,
        FutureScenarioEngineRoot.enable(tenant_id="t1", scenario_ref="sc1").is_missing() is False,
        EvolutionDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        EvolutionOptimizationFrameworkRoot.enable(
            tenant_id="t1", optimization_ref="o1"
        ).is_missing() is False,
        MeosCivilizationEvolutionIntelligenceCoreRoot.enable(
            tenant_id="t1", core_ref="core1"
        ).is_missing() is False,
        EvolutionKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="k1").is_missing() is False,
        EvolutionEventArchitectureRoot.enable(tenant_id="t1", events_ref="ev1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/civilization/infrastructure/acl/civ_evolution_acl.py").read_text(
        encoding="utf-8"
    )
    acl_ok = all(x in acl_text for x in (
        "via_p219", "via_p219_e", "via_p219_f", "via_p219_k", "via_p219_q",
        "via_policy_engine", "via_workflow", "via_audit",
        "via_p218_z", "via_p214_z", "via_core_platform", "via_identity",
        "never_replace_p219_foundation", "never_replace_p219_e_ai_os",
        "never_replace_p219_f_simulation", "never_replace_p219_k_governance",
        "never_replace_p219_q_consciousness",
        "never_opaque_unexplainable_evolution_decisions",
        "never_ungated_evolution_transformation_execution",
        "never_treat_forecast_as_binding_policy",
        "never_skip_ethical_evolution_governance",
        "never_skip_human_authority_evolution",
        "never_violate_human_sovereignty_evolution",
        "never_bypass_trusted_evolution_validation",
        "never_bypass_human_supervision_evolution",
        "module_local_llm_forbidden",
        "module_local_civilization_evolution_forbidden",
    ))
    router = (root / "backend/contexts/civilization/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@civilization_router.get("/evolution")',
        "/evolution/architecture", "/evolution/strategy", "/evolution/adaptive",
        "/evolution/scenarios", "/evolution/optimization", "/evolution/digital-twin",
        "/evolution/knowledge-graph", "/evolution/agents", "/evolution/bounded-contexts",
        "/evolution/aggregates", "/evolution/events", "/evolution/cqrs",
        "/evolution/integration", "/evolution/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_EVOLUTION.md").read_text(
        encoding="utf-8"
    )
    doc_ok = all(x in law for x in (
        "Never Civilization Evolution Intelligence Platform is missing",
        "Never Adaptive Civilization Evolution Platform is missing",
        "Never Long-Term Strategy Platform is missing",
        "Never Future Scenario Engine is missing",
        "Never Evolution Digital Twin is missing",
        "Never Evolution Optimization Framework is missing",
        "Never MEOS Civilization Evolution Intelligence Core is missing",
        "Never Evolution Knowledge Graph is missing",
        "Never Evolution Event Architecture is missing",
        "Never Evolution CQRS Model is missing",
        "Never MEOS Evolution Integration Map is missing",
        "Never Replace P219 Foundation",
        "Never Replace P219-E AI OS",
        "Never Replace P219-F Simulation",
        "Never Replace P219-Q Consciousness",
        "Never Opaque Unexplainable Evolution Decisions",
        "Never Ungated Evolution Transformation Execution",
        "Never Treat Forecast As Binding Policy",
        "Never Bypass Human Supervision Evolution",
        "understanding civilization dynamics, predicting future trajectories",
        "P219-S",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P219-R", "adr": 571, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "civilization",
        "capability": "CAP-PLT-CIV-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
