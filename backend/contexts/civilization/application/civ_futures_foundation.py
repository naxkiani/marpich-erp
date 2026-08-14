"""Civilization P219-S futures intelligence foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/572-enterprise-civilization-operating-system-futures.md",
    "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_FUTURES.md",
    "docs/architecture/civilization/CIVILIZATION_FUTURES_CAPABILITIES.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_FUTURES_ARCHITECTURE.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_FUTURES_DDD_CQRS.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_FUTURES_SECURITY.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_FUTURES_VALIDATION.v1.yaml",
    "docs/architecture/civilization/P219_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/civilization/domain/services/civ_platform_futures.py",
    "backend/contexts/civilization/domain/aggregates/civ_futures_aggregates.py",
    "backend/contexts/civilization/infrastructure/acl/civ_futures_acl.py",
    "backend/contexts/civilization/application/civ_futures_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/civilization_futures_intelligence_platform",
    "backend/contexts/strategic_foresight_platform_bc",
    "backend/contexts/global_scenario_intelligence_bc",
)


def validate_civ_futures_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.civilization.domain.aggregates.civ_futures_aggregates import (
        CivilizationFuturesIntelligencePlatformRoot,
        FutureDigitalTwinRoot,
        FuturesEventArchitectureRoot,
        FuturesKnowledgeGraphRoot,
        HorizonScanningPlatformRoot,
        MeosCivilizationFuturesIntelligenceCoreRoot,
        ScenarioIntelligencePlatformRoot,
        StrategicForesightEngineRoot,
        StrategicResilienceFrameworkRoot,
    )
    from contexts.civilization.domain.services import civ_platform_futures as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P219-S" and cat["adr"] == 572 and cat["sor"] == "civilization"
        and cat["capability"] == "CAP-PLT-CIV-001"
        and cat["fabric"] == "meos_civilization_os_civilization_futures_intelligence_framework"
        and cat["foundation_gate"] == "P219" and cat["mission_gate"] == "P219-A"
        and cat["strategy_gate"] == "P219-B" and cat["domain_gate"] == "P219-C"
        and cat["planetary_gate"] == "P219-D" and cat["ai_os_gate"] == "P219-E"
        and cat["simulation_gate"] == "P219-F" and cat["resources_gate"] == "P219-G"
        and cat["economy_gate"] == "P219-H" and cat["knowledge_gate"] == "P219-I"
        and cat["human_gate"] == "P219-J" and cat["governance_gate"] == "P219-K"
        and cat["innovation_gate"] == "P219-L" and cat["security_gate"] == "P219-M"
        and cat["sustainability_gate"] == "P219-N" and cat["prosperity_gate"] == "P219-O"
        and cat["collaboration_gate"] == "P219-P" and cat["consciousness_gate"] == "P219-Q"
        and cat["evolution_gate"] == "P219-R"
        and cat["intelligence_nexus_gate"] == "P218-Z" and cat["space_gate"] == "P218"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["civilization_futures_intelligence_platform_present_required"] is True
        and cat["strategic_foresight_engine_present_required"] is True
        and cat["horizon_scanning_platform_present_required"] is True
        and cat["scenario_intelligence_platform_present_required"] is True
        and cat["strategic_resilience_framework_present_required"] is True
        and cat["future_digital_twin_present_required"] is True
        and cat["meos_civilization_futures_intelligence_core_present_required"] is True
        and cat["futures_knowledge_graph_present_required"] is True
        and cat["futures_event_architecture_present_required"] is True
        and cat["futures_cqrs_model_present_required"] is True
        and cat["meos_futures_integration_map_present_required"] is True
        and cat["architecture"]["foresight_stage_count"] == 6
        and cat["architecture"]["layer_count"] == 6
        and cat["architecture"]["observation_domain_count"] == 10
        and cat["architecture"]["horizon_scanning_domain_count"] == 10
        and cat["architecture"]["scenario_category_count"] == 7
        and cat["architecture"]["resilience_domain_count"] == 7
        and cat["agents"]["agent_count"] == 5
        and cat["knowledge_graph"]["entity_count"] == 10
        and cat["knowledge_graph"]["relationship_count"] == 8
        and cat["digital_twin"]["twin_count"] == 5
        and cat["bounded_contexts"]["context_count"] == 4
        and cat["aggregates"]["aggregate_count"] == 5
        and cat["events"]["core_event_count"] == 12
        and cat["cqrs"]["command_count"] == 6 and cat["cqrs"]["query_count"] == 6
        and cat["microservices"]["service_count"] == 10
        and cat["never_replace_p219_foundation"] is True
        and cat["never_replace_p219_r_evolution"] is True
        and cat["never_replace_p219_f_simulation"] is True
        and cat["never_replace_p219_e_ai_os"] is True
        and cat["never_ungated_futures_strategy_execution"] is True
        and cat["never_treat_scenario_as_binding_policy"] is True
        and cat["never_bypass_human_supervision_futures"] is True
        and cat["never_opaque_unexplainable_futures_decisions"] is True
        and cat["no_module_local_llm"] is True
        and cat["foundation_for_p219_t"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        CivilizationFuturesIntelligencePlatformRoot.enable(
            tenant_id="t1", futures_ref="f1"
        ).is_missing() is False,
        StrategicForesightEngineRoot.enable(
            tenant_id="t1", foresight_ref="fo1"
        ).is_missing() is False,
        HorizonScanningPlatformRoot.enable(tenant_id="t1", horizon_ref="h1").is_missing() is False,
        ScenarioIntelligencePlatformRoot.enable(
            tenant_id="t1", scenario_ref="sc1"
        ).is_missing() is False,
        StrategicResilienceFrameworkRoot.enable(
            tenant_id="t1", resilience_ref="r1"
        ).is_missing() is False,
        FutureDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        MeosCivilizationFuturesIntelligenceCoreRoot.enable(
            tenant_id="t1", core_ref="core1"
        ).is_missing() is False,
        FuturesKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="k1").is_missing() is False,
        FuturesEventArchitectureRoot.enable(tenant_id="t1", events_ref="ev1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/civilization/infrastructure/acl/civ_futures_acl.py").read_text(
        encoding="utf-8"
    )
    acl_ok = all(x in acl_text for x in (
        "via_p219", "via_p219_e", "via_p219_f", "via_p219_k", "via_p219_r",
        "via_policy_engine", "via_workflow", "via_audit",
        "via_p218_z", "via_p214_z", "via_core_platform", "via_identity",
        "never_replace_p219_foundation", "never_replace_p219_e_ai_os",
        "never_replace_p219_f_simulation", "never_replace_p219_k_governance",
        "never_replace_p219_r_evolution",
        "never_opaque_unexplainable_futures_decisions",
        "never_ungated_futures_strategy_execution",
        "never_treat_scenario_as_binding_policy",
        "never_skip_ethical_futures_governance",
        "never_skip_human_authority_futures",
        "never_violate_human_sovereignty_futures",
        "never_bypass_trusted_futures_validation",
        "never_bypass_human_supervision_futures",
        "module_local_llm_forbidden",
        "module_local_civilization_futures_forbidden",
    ))
    router = (root / "backend/contexts/civilization/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@civilization_router.get("/futures")',
        "/futures/architecture", "/futures/foresight", "/futures/horizon",
        "/futures/scenarios", "/futures/resilience", "/futures/strategy",
        "/futures/digital-twin", "/futures/knowledge-graph", "/futures/agents",
        "/futures/bounded-contexts", "/futures/aggregates", "/futures/events",
        "/futures/cqrs", "/futures/integration", "/futures/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_FUTURES.md").read_text(
        encoding="utf-8"
    )
    doc_ok = all(x in law for x in (
        "Never Civilization Futures Intelligence Platform is missing",
        "Never Strategic Foresight Engine is missing",
        "Never Horizon Scanning Platform is missing",
        "Never Scenario Intelligence Platform is missing",
        "Never Strategic Resilience Framework is missing",
        "Never Future Digital Twin is missing",
        "Never MEOS Civilization Futures Intelligence Core is missing",
        "Never Futures Knowledge Graph is missing",
        "Never Futures Event Architecture is missing",
        "Never Futures CQRS Model is missing",
        "Never MEOS Futures Integration Map is missing",
        "Never Replace P219 Foundation",
        "Never Replace P219-E AI OS",
        "Never Replace P219-F Simulation",
        "Never Replace P219-R Evolution",
        "Never Opaque Unexplainable Futures Decisions",
        "Never Ungated Futures Strategy Execution",
        "Never Treat Scenario As Binding Policy",
        "Never Bypass Human Supervision Futures",
        "understand long-term trends, identify emerging opportunities and risks",
        "P219-T",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P219-S", "adr": 572, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "civilization",
        "capability": "CAP-PLT-CIV-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
