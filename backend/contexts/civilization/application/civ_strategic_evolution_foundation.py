"""Civilization P219-X strategic evolution foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/577-enterprise-civilization-operating-system-strategic-evolution.md",
    "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_STRATEGIC_EVOLUTION.md",
    "docs/architecture/civilization/CIVILIZATION_STRATEGIC_EVOLUTION_CAPABILITIES.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_STRATEGIC_EVOLUTION_ARCHITECTURE.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_STRATEGIC_EVOLUTION_DDD_CQRS.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_STRATEGIC_EVOLUTION_SECURITY.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_STRATEGIC_EVOLUTION_VALIDATION.v1.yaml",
    "docs/architecture/civilization/P219_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/civilization/domain/services/civ_platform_strategic_evolution.py",
    "backend/contexts/civilization/domain/aggregates/civ_strategic_evolution_aggregates.py",
    "backend/contexts/civilization/infrastructure/acl/civ_strategic_evolution_acl.py",
    "backend/contexts/civilization/application/civ_strategic_evolution_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/strategic_evolution_platform",
    "backend/contexts/adaptive_transformation_platform_bc",
    "backend/contexts/enterprise_transformation_intelligence_bc",
)


def validate_civ_strategic_evolution_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.civilization.domain.aggregates.civ_strategic_evolution_aggregates import (
        AdaptiveTransformationPlatformRoot,
        BusinessCapabilityEvolutionPlatformRoot,
        EnterpriseTransformationIntelligencePlatformRoot,
        EvolutionDigitalTwinRoot,
        MeosStrategicEvolutionAdaptiveTransformationCoreRoot,
        StrategicEvolutionEventArchitectureRoot,
        StrategicEvolutionKnowledgeGraphRoot,
        StrategicEvolutionPlatformRoot,
        StrategicPortfolioEvolutionPlatformRoot,
    )
    from contexts.civilization.domain.services import civ_platform_strategic_evolution as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P219-X" and cat["adr"] == 577 and cat["sor"] == "civilization"
        and cat["capability"] == "CAP-PLT-CIV-001"
        and cat["fabric"] == "meos_civilization_os_strategic_evolution_adaptive_transformation_framework"
        and cat["foundation_gate"] == "P219" and cat["mission_gate"] == "P219-A"
        and cat["strategy_gate"] == "P219-B" and cat["domain_gate"] == "P219-C"
        and cat["planetary_gate"] == "P219-D" and cat["ai_os_gate"] == "P219-E"
        and cat["simulation_gate"] == "P219-F" and cat["resources_gate"] == "P219-G"
        and cat["economy_gate"] == "P219-H" and cat["knowledge_gate"] == "P219-I"
        and cat["human_gate"] == "P219-J" and cat["governance_gate"] == "P219-K"
        and cat["innovation_gate"] == "P219-L" and cat["security_gate"] == "P219-M"
        and cat["sustainability_gate"] == "P219-N" and cat["prosperity_gate"] == "P219-O"
        and cat["collaboration_gate"] == "P219-P" and cat["consciousness_gate"] == "P219-Q"
        and cat["evolution_gate"] == "P219-R" and cat["futures_gate"] == "P219-S"
        and cat["intel_gov_gate"] == "P219-T" and cat["auto_ops_gate"] == "P219-U"
        and cat["gen_intel_gate"] == "P219-V" and cat["collective_gate"] == "P219-W"
        and cat["intelligence_nexus_gate"] == "P218-Z" and cat["space_gate"] == "P218"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["strategic_evolution_platform_present_required"] is True
        and cat["adaptive_transformation_platform_present_required"] is True
        and cat["strategic_portfolio_evolution_platform_present_required"] is True
        and cat["business_capability_evolution_platform_present_required"] is True
        and cat["enterprise_transformation_intelligence_platform_present_required"] is True
        and cat["meos_strategic_evolution_adaptive_transformation_core_present_required"] is True
        and cat["strategic_evolution_knowledge_graph_present_required"] is True
        and cat["strategic_evolution_event_architecture_present_required"] is True
        and cat["strategic_evolution_cqrs_model_present_required"] is True
        and cat["meos_strategic_evolution_integration_map_present_required"] is True
        and cat["architecture"]["maturity_stage_count"] == 6
        and cat["architecture"]["layer_count"] == 6
        and cat["architecture"]["portfolio_domain_count"] == 10
        and cat["architecture"]["transformation_lifecycle_step_count"] == 8
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
        and cat["never_replace_p219_b_strategy"] is True
        and cat["never_replace_p219_r_evolution"] is True
        and cat["never_replace_p219_s_futures"] is True
        and cat["never_replace_p219_w_collective"] is True
        and cat["never_ungated_strategic_transformation_execution"] is True
        and cat["never_opaque_unexplainable_transformation_recommendations"] is True
        and cat["never_autonomous_enterprise_reconfiguration"] is True
        and cat["never_bypass_human_accountability_strategic_evolution"] is True
        and cat["no_module_local_llm"] is True
        and cat["foundation_for_p219_y"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        StrategicEvolutionPlatformRoot.enable(
            tenant_id="t1", evolution_ref="e1"
        ).is_missing() is False,
        AdaptiveTransformationPlatformRoot.enable(
            tenant_id="t1", transform_ref="tr1"
        ).is_missing() is False,
        StrategicPortfolioEvolutionPlatformRoot.enable(
            tenant_id="t1", portfolio_ref="p1"
        ).is_missing() is False,
        BusinessCapabilityEvolutionPlatformRoot.enable(
            tenant_id="t1", capability_ref="c1"
        ).is_missing() is False,
        EnterpriseTransformationIntelligencePlatformRoot.enable(
            tenant_id="t1", intel_ref="i1"
        ).is_missing() is False,
        MeosStrategicEvolutionAdaptiveTransformationCoreRoot.enable(
            tenant_id="t1", core_ref="core1"
        ).is_missing() is False,
        StrategicEvolutionKnowledgeGraphRoot.enable(
            tenant_id="t1", kg_ref="kg1"
        ).is_missing() is False,
        StrategicEvolutionEventArchitectureRoot.enable(
            tenant_id="t1", events_ref="ev1"
        ).is_missing() is False,
        EvolutionDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
    ]
    acl_text = (
        root / "backend/contexts/civilization/infrastructure/acl/civ_strategic_evolution_acl.py"
    ).read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p219", "via_p219_b", "via_p219_r", "via_p219_s", "via_p219_w",
        "via_policy_engine", "via_workflow", "via_audit",
        "via_p218_z", "via_p214_z", "via_core_platform", "via_identity",
        "never_replace_p219_foundation", "never_replace_p219_b_strategy",
        "never_replace_p219_r_evolution", "never_replace_p219_s_futures",
        "never_replace_p219_w_collective",
        "never_ungated_strategic_transformation_execution",
        "never_opaque_unexplainable_transformation_recommendations",
        "never_autonomous_enterprise_reconfiguration",
        "never_bypass_human_authority_strategic_evolution",
        "never_bypass_human_accountability_strategic_evolution",
        "never_skip_ethical_transformation_governance",
        "never_violate_institutional_strategy_ownership",
        "never_bypass_trusted_transformation_validation",
        "never_bypass_human_supervision_strategic_evolution",
        "module_local_llm_forbidden",
        "module_local_strategic_evolution_forbidden",
    ))
    router = (root / "backend/contexts/civilization/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@civilization_router.get("/strategic-evolution")',
        "/strategic-evolution/architecture", "/strategic-evolution/transformation",
        "/strategic-evolution/portfolio", "/strategic-evolution/capability",
        "/strategic-evolution/intelligence", "/strategic-evolution/digital-twin",
        "/strategic-evolution/knowledge-graph", "/strategic-evolution/agents",
        "/strategic-evolution/bounded-contexts", "/strategic-evolution/aggregates",
        "/strategic-evolution/events", "/strategic-evolution/cqrs",
        "/strategic-evolution/integration", "/strategic-evolution/readiness",
    ))
    law = (
        root / "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_STRATEGIC_EVOLUTION.md"
    ).read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Strategic Evolution Platform is missing",
        "Never Adaptive Transformation Platform is missing",
        "Never Strategic Portfolio Evolution Platform is missing",
        "Never Business Capability Evolution Platform is missing",
        "Never Enterprise Transformation Intelligence Platform is missing",
        "Never MEOS Strategic Evolution & Adaptive Transformation Core is missing",
        "Never Strategic Evolution Knowledge Graph is missing",
        "Never Strategic Evolution Event Architecture is missing",
        "Never Strategic Evolution CQRS Model is missing",
        "Never MEOS Strategic Evolution Integration Map is missing",
        "Never Replace P219 Foundation",
        "Never Replace P219-B Strategy",
        "Never Replace P219-R Evolution",
        "Never Replace P219-S Futures",
        "Never Replace P219-W Collective Intelligence",
        "Never Ungated Strategic Transformation Execution",
        "Never Opaque Unexplainable Transformation Recommendations",
        "Never Autonomous Enterprise Reconfiguration",
        "Never Bypass Human Accountability Strategic Evolution",
        "evolving strategic portfolios, business capabilities and transformation programs",
        "P219-Y",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P219-X", "adr": 577, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "civilization",
        "capability": "CAP-PLT-CIV-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
