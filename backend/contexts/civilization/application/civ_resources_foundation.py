"""Civilization P219-G planetary resource intelligence foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/560-enterprise-civilization-operating-system-resources.md",
    "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_RESOURCES.md",
    "docs/architecture/civilization/CIVILIZATION_RESOURCES_CAPABILITIES.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_RESOURCES_ARCHITECTURE.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_RESOURCES_DDD_CQRS.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_RESOURCES_SECURITY.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_RESOURCES_VALIDATION.v1.yaml",
    "docs/architecture/civilization/P219_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/civilization/domain/services/civ_platform_resources.py",
    "backend/contexts/civilization/domain/aggregates/civ_resources_aggregates.py",
    "backend/contexts/civilization/infrastructure/acl/civ_resources_acl.py",
    "backend/contexts/civilization/application/civ_resources_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/planetary_resource_intelligence_platform",
    "backend/contexts/energy_water_food_intelligence_bc",
    "backend/contexts/resource_optimization_core_bc",
)


def validate_civ_resources_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.civilization.domain.aggregates.civ_resources_aggregates import (
        EnergyIntelligencePlatformRoot,
        FoodIntelligencePlatformRoot,
        MeosPlanetaryResourceIntelligenceCoreRoot,
        PlanetaryResourceIntelligencePlatformRoot,
        ResourceDigitalTwinRoot,
        ResourceEventArchitectureRoot,
        ResourceKnowledgeGraphRoot,
        ResourceOptimizationEngineRoot,
        WaterIntelligencePlatformRoot,
    )
    from contexts.civilization.domain.services import civ_platform_resources as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P219-G" and cat["adr"] == 560 and cat["sor"] == "civilization"
        and cat["capability"] == "CAP-PLT-CIV-001"
        and cat["fabric"] == "meos_civilization_os_planetary_resource_intelligence_framework"
        and cat["foundation_gate"] == "P219" and cat["mission_gate"] == "P219-A"
        and cat["strategy_gate"] == "P219-B" and cat["domain_gate"] == "P219-C"
        and cat["planetary_gate"] == "P219-D" and cat["ai_os_gate"] == "P219-E"
        and cat["simulation_gate"] == "P219-F"
        and cat["intelligence_nexus_gate"] == "P218-Z" and cat["space_gate"] == "P218"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["planetary_resource_intelligence_platform_present_required"] is True
        and cat["energy_intelligence_platform_present_required"] is True
        and cat["water_intelligence_platform_present_required"] is True
        and cat["food_intelligence_platform_present_required"] is True
        and cat["resource_optimization_engine_present_required"] is True
        and cat["resource_digital_twin_present_required"] is True
        and cat["meos_planetary_resource_intelligence_core_present_required"] is True
        and cat["resource_knowledge_graph_present_required"] is True
        and cat["resource_event_architecture_present_required"] is True
        and cat["resource_cqrs_model_present_required"] is True
        and cat["meos_resource_integration_map_present_required"] is True
        and cat["architecture"]["layer_count"] == 6
        and cat["architecture"]["evolution_stage_count"] == 5
        and cat["architecture"]["managed_domain_count"] == 6
        and cat["energy"]["agent_count"] == 4
        and cat["water"]["agent_count"] == 4
        and cat["food"]["agent_count"] == 4
        and cat["agents"]["agent_count"] == 12
        and cat["optimization"]["cycle_step_count"] == 6
        and cat["digital_twin"]["twin_count"] == 5
        and cat["bounded_contexts"]["context_count"] == 4
        and cat["aggregates"]["aggregate_count"] == 5
        and cat["events"]["core_event_count"] == 11
        and cat["cqrs"]["command_count"] == 6 and cat["cqrs"]["query_count"] == 5
        and cat["knowledge_graph"]["node_count"] == 10
        and cat["knowledge_graph"]["edge_count"] == 7
        and cat["microservices"]["service_count"] == 10
        and cat["never_replace_p219_foundation"] is True
        and cat["never_replace_p219_f_simulation"] is True
        and cat["never_ungated_resource_allocation_execution"] is True
        and cat["never_bypass_circular_economy_safeguards"] is True
        and cat["never_opaque_unexplainable_resource_decisions"] is True
        and cat["no_module_local_llm"] is True
        and cat["foundation_for_p219_h"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        PlanetaryResourceIntelligencePlatformRoot.enable(tenant_id="t1", resource_ref="r1").is_missing() is False,
        EnergyIntelligencePlatformRoot.enable(tenant_id="t1", energy_ref="e1").is_missing() is False,
        WaterIntelligencePlatformRoot.enable(tenant_id="t1", water_ref="w1").is_missing() is False,
        FoodIntelligencePlatformRoot.enable(tenant_id="t1", food_ref="f1").is_missing() is False,
        ResourceOptimizationEngineRoot.enable(tenant_id="t1", opt_ref="o1").is_missing() is False,
        ResourceDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        MeosPlanetaryResourceIntelligenceCoreRoot.enable(tenant_id="t1", core_ref="c1").is_missing() is False,
        ResourceKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="kg1").is_missing() is False,
        ResourceEventArchitectureRoot.enable(tenant_id="t1", events_ref="ev1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/civilization/infrastructure/acl/civ_resources_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p219", "via_p219_a", "via_p219_b", "via_p219_c", "via_p219_d", "via_p219_e", "via_p219_f",
        "via_p218_z", "via_p218", "via_p217", "via_p216_z", "via_p215_z", "via_p214_z",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p219_foundation", "never_replace_p219_a_mission", "never_replace_p219_b_strategy",
        "never_replace_p219_c_domain", "never_replace_p219_d_planetary", "never_replace_p219_e_ai_os",
        "never_replace_p219_f_simulation", "never_replace_p218_z_intelligence_nexus", "never_replace_space",
        "never_merge_p218_t_space_civilization", "never_cross_context_aggregate_imports",
        "never_opaque_unexplainable_resource_decisions",
        "never_ungated_resource_allocation_execution",
        "never_skip_human_authority_resource",
        "never_skip_ethical_resource_governance",
        "never_violate_human_sovereignty_resource",
        "never_bypass_circular_economy_safeguards",
        "module_local_llm_forbidden",
        "module_local_resource_intelligence_forbidden",
    ))
    router = (root / "backend/contexts/civilization/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@civilization_router.get("/resources")',
        "/resources/architecture", "/resources/energy", "/resources/water",
        "/resources/food", "/resources/optimization", "/resources/digital-twin",
        "/resources/agents", "/resources/bounded-contexts", "/resources/aggregates",
        "/resources/events", "/resources/cqrs", "/resources/knowledge-graph",
        "/resources/integration", "/resources/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_RESOURCES.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Planetary Resource Intelligence Platform is missing",
        "Never Energy Intelligence Platform is missing",
        "Never Water Intelligence Platform is missing",
        "Never Food Intelligence Platform is missing",
        "Never Resource Optimization Engine is missing",
        "Never Resource Digital Twin is missing",
        "Never MEOS Planetary Resource Intelligence Core is missing",
        "Never Resource Knowledge Graph is missing",
        "Never Resource Event Architecture is missing",
        "Never Resource CQRS Model is missing",
        "Never MEOS Resource Integration Map is missing",
        "Never Replace P219 Foundation",
        "Never Replace P219-A Mission",
        "Never Replace P219-B Strategy",
        "Never Replace P219-C Domain",
        "Never Replace P219-D Planetary",
        "Never Replace P219-E AI OS",
        "Never Replace P219-F Simulation",
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
        "Never Opaque Unexplainable Resource Decisions",
        "Never Ungated Resource Allocation Execution",
        "Never Skip Human Authority Resource",
        "Never Skip Ethical Resource Governance",
        "Never Violate Human Sovereignty Resource",
        "Never Bypass Circular Economy Safeguards",
        "sustainable human development and long-term planetary resilience",
        "P219-H",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P219-G", "adr": 560, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "civilization",
        "capability": "CAP-PLT-CIV-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
