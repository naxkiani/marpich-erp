"""Civilization P219-H civilization economy platform foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/561-enterprise-civilization-operating-system-economy.md",
    "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_ECONOMY.md",
    "docs/architecture/civilization/CIVILIZATION_ECONOMY_CAPABILITIES.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_ECONOMY_ARCHITECTURE.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_ECONOMY_DDD_CQRS.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_ECONOMY_SECURITY.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_ECONOMY_VALIDATION.v1.yaml",
    "docs/architecture/civilization/P219_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/civilization/domain/services/civ_platform_economy.py",
    "backend/contexts/civilization/domain/aggregates/civ_economy_aggregates.py",
    "backend/contexts/civilization/infrastructure/acl/civ_economy_acl.py",
    "backend/contexts/civilization/application/civ_economy_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/civilization_economy_platform",
    "backend/contexts/global_economic_intelligence_bc",
    "backend/contexts/future_economy_systems_bc",
)


def validate_civ_economy_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.civilization.domain.aggregates.civ_economy_aggregates import (
        AutonomousEconomicAgentsRoot,
        CivilizationEconomyIntelligencePlatformRoot,
        EconomicDigitalTwinRoot,
        EconomicEventArchitectureRoot,
        EconomicKnowledgeGraphRoot,
        EconomicSimulationCapabilityRoot,
        FutureEconomyIntelligenceRoot,
        GlobalEconomicIntelligenceRoot,
        MeosCivilizationEconomyPlatformRoot,
    )
    from contexts.civilization.domain.services import civ_platform_economy as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P219-H" and cat["adr"] == 561 and cat["sor"] == "civilization"
        and cat["capability"] == "CAP-PLT-CIV-001"
        and cat["fabric"] == "meos_civilization_os_civilization_economy_framework"
        and cat["foundation_gate"] == "P219" and cat["mission_gate"] == "P219-A"
        and cat["strategy_gate"] == "P219-B" and cat["domain_gate"] == "P219-C"
        and cat["planetary_gate"] == "P219-D" and cat["ai_os_gate"] == "P219-E"
        and cat["simulation_gate"] == "P219-F" and cat["resources_gate"] == "P219-G"
        and cat["intelligence_nexus_gate"] == "P218-Z" and cat["space_gate"] == "P218"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["civilization_economy_intelligence_platform_present_required"] is True
        and cat["global_economic_intelligence_present_required"] is True
        and cat["economic_digital_twin_present_required"] is True
        and cat["future_economy_intelligence_present_required"] is True
        and cat["autonomous_economic_agents_present_required"] is True
        and cat["economic_simulation_capability_present_required"] is True
        and cat["meos_civilization_economy_platform_present_required"] is True
        and cat["economic_knowledge_graph_present_required"] is True
        and cat["economic_event_architecture_present_required"] is True
        and cat["economic_cqrs_model_present_required"] is True
        and cat["meos_economy_integration_map_present_required"] is True
        and cat["architecture"]["layer_count"] == 6
        and cat["architecture"]["evolution_stage_count"] == 5
        and cat["architecture"]["economic_domain_count"] == 8
        and cat["architecture"]["structure_step_count"] == 7
        and cat["architecture"]["intelligence_dimension_count"] == 5
        and cat["future_economy"]["model_count"] == 7
        and cat["agents"]["agent_count"] == 5
        and cat["digital_twin"]["twin_count"] == 5
        and cat["optimization"]["cycle_step_count"] == 6
        and cat["bounded_contexts"]["context_count"] == 4
        and cat["aggregates"]["aggregate_count"] == 5
        and cat["events"]["core_event_count"] == 6
        and cat["cqrs"]["command_count"] == 6 and cat["cqrs"]["query_count"] == 5
        and cat["knowledge_graph"]["node_count"] == 9
        and cat["knowledge_graph"]["edge_count"] == 6
        and cat["microservices"]["service_count"] == 10
        and cat["never_replace_p219_foundation"] is True
        and cat["never_replace_p219_g_resources"] is True
        and cat["never_replace_financial_kernel"] is True
        and cat["never_ungated_economic_policy_execution"] is True
        and cat["never_treat_economic_forecast_as_binding_policy"] is True
        and cat["never_opaque_unexplainable_economic_decisions"] is True
        and cat["no_module_local_llm"] is True
        and cat["foundation_for_p219_i"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        CivilizationEconomyIntelligencePlatformRoot.enable(tenant_id="t1", economy_ref="e1").is_missing() is False,
        GlobalEconomicIntelligenceRoot.enable(tenant_id="t1", global_ref="g1").is_missing() is False,
        EconomicDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        FutureEconomyIntelligenceRoot.enable(tenant_id="t1", future_ref="f1").is_missing() is False,
        AutonomousEconomicAgentsRoot.enable(tenant_id="t1", agents_ref="a1").is_missing() is False,
        EconomicSimulationCapabilityRoot.enable(tenant_id="t1", sim_ref="s1").is_missing() is False,
        MeosCivilizationEconomyPlatformRoot.enable(tenant_id="t1", platform_ref="p1").is_missing() is False,
        EconomicKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="kg1").is_missing() is False,
        EconomicEventArchitectureRoot.enable(tenant_id="t1", events_ref="ev1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/civilization/infrastructure/acl/civ_economy_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p219", "via_p219_a", "via_p219_b", "via_p219_c", "via_p219_d", "via_p219_e",
        "via_p219_f", "via_p219_g", "via_financial_kernel",
        "via_p218_z", "via_p218", "via_p217", "via_p216_z", "via_p215_z", "via_p214_z",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p219_foundation", "never_replace_p219_a_mission", "never_replace_p219_b_strategy",
        "never_replace_p219_c_domain", "never_replace_p219_d_planetary", "never_replace_p219_e_ai_os",
        "never_replace_p219_f_simulation", "never_replace_p219_g_resources",
        "never_replace_financial_kernel", "never_replace_p218_z_intelligence_nexus", "never_replace_space",
        "never_merge_p218_t_space_civilization", "never_cross_context_aggregate_imports",
        "never_opaque_unexplainable_economic_decisions",
        "never_ungated_economic_policy_execution",
        "never_skip_human_authority_economy",
        "never_skip_ethical_economic_governance",
        "never_violate_human_sovereignty_economy",
        "never_treat_economic_forecast_as_binding_policy",
        "module_local_llm_forbidden",
        "module_local_economy_intelligence_forbidden",
    ))
    router = (root / "backend/contexts/civilization/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@civilization_router.get("/economy")',
        "/economy/architecture", "/economy/markets", "/economy/investment",
        "/economy/future", "/economy/digital-twin", "/economy/agents",
        "/economy/optimization", "/economy/bounded-contexts", "/economy/aggregates",
        "/economy/events", "/economy/cqrs", "/economy/knowledge-graph",
        "/economy/integration", "/economy/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_ECONOMY.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Civilization Economy Intelligence Platform is missing",
        "Never Global Economic Intelligence is missing",
        "Never Economic Digital Twin is missing",
        "Never Future Economy Intelligence is missing",
        "Never Autonomous Economic Agents is missing",
        "Never Economic Simulation Capability is missing",
        "Never MEOS Civilization Economy Platform is missing",
        "Never Economic Knowledge Graph is missing",
        "Never Economic Event Architecture is missing",
        "Never Economic CQRS Model is missing",
        "Never MEOS Economy Integration Map is missing",
        "Never Replace P219 Foundation",
        "Never Replace P219-A Mission",
        "Never Replace P219-B Strategy",
        "Never Replace P219-C Domain",
        "Never Replace P219-D Planetary",
        "Never Replace P219-E AI OS",
        "Never Replace P219-F Simulation",
        "Never Replace P219-G Resources",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace Financial Kernel",
        "Never Replace P215-Z Quantum",
        "Never Replace P216-Z Robotics",
        "Never Replace P217 Biotechnology",
        "Never Replace P218 Space",
        "Never Replace P218-Z Intelligence Nexus",
        "Never Merge P218-T Space Civilization Phase",
        "Never Module-Local LLM",
        "Never Cross-Context Aggregate Imports",
        "Never Opaque Unexplainable Economic Decisions",
        "Never Ungated Economic Policy Execution",
        "Never Skip Human Authority Economy",
        "Never Skip Ethical Economic Governance",
        "Never Violate Human Sovereignty Economy",
        "Never Treat Economic Forecast as Binding Policy",
        "supporting intelligent economic decisions for humanity",
        "P219-I",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P219-H", "adr": 561, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "civilization",
        "capability": "CAP-PLT-CIV-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
