"""Civilization P219-Z unified enterprise control plane foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/579-enterprise-civilization-operating-system-unified-enterprise-core.md",
    "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_UNIFIED_ENTERPRISE_CORE.md",
    "docs/architecture/civilization/CIVILIZATION_UNIFIED_CONTROL_CAPABILITIES.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_UNIFIED_CONTROL_ARCHITECTURE.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_UNIFIED_CONTROL_DDD_CQRS.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_UNIFIED_CONTROL_SECURITY.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_UNIFIED_CONTROL_VALIDATION.v1.yaml",
    "docs/architecture/civilization/P219_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/civilization/domain/services/civ_platform_unified_control.py",
    "backend/contexts/civilization/domain/aggregates/civ_unified_control_aggregates.py",
    "backend/contexts/civilization/infrastructure/acl/civ_unified_control_acl.py",
    "backend/contexts/civilization/application/civ_unified_control_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/unified_enterprise_control_plane",
    "backend/contexts/enterprise_governance_fabric_bc",
    "backend/contexts/cross_domain_orchestration_platform_bc",
)


def validate_civ_unified_control_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.civilization.domain.aggregates.civ_unified_control_aggregates import (
        CrossDomainOrchestrationPlatformRoot,
        EnterpriseDigitalTwinFederationRoot,
        EnterpriseGovernanceFabricRoot,
        IntegratedEnterpriseIntelligencePlatformRoot,
        MeosUnifiedEnterpriseCoreRoot,
        StrategicDecisionSupportPlatformRoot,
        UnifiedControlKnowledgeGraphRoot,
        UnifiedEnterpriseControlPlaneRoot,
        UnifiedEnterpriseCoordinationPlatformRoot,
    )
    from contexts.civilization.domain.services import civ_platform_unified_control as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P219-Z" and cat["adr"] == 579 and cat["sor"] == "civilization"
        and cat["capability"] == "CAP-PLT-CIV-001"
        and cat["fabric"] == "meos_civilization_os_unified_enterprise_control_plane_framework"
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
        and cat["strategic_evolution_gate"] == "P219-X" and cat["trust_ethics_gate"] == "P219-Y"
        and cat["intelligence_nexus_gate"] == "P218-Z" and cat["space_gate"] == "P218"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["unified_enterprise_control_plane_present_required"] is True
        and cat["integrated_enterprise_intelligence_platform_present_required"] is True
        and cat["unified_enterprise_coordination_platform_present_required"] is True
        and cat["enterprise_governance_fabric_present_required"] is True
        and cat["cross_domain_orchestration_platform_present_required"] is True
        and cat["enterprise_digital_twin_federation_present_required"] is True
        and cat["strategic_decision_support_platform_present_required"] is True
        and cat["meos_unified_enterprise_core_present_required"] is True
        and cat["unified_control_knowledge_graph_present_required"] is True
        and cat["unified_control_event_architecture_present_required"] is True
        and cat["unified_control_cqrs_model_present_required"] is True
        and cat["meos_unified_enterprise_integration_map_present_required"] is True
        and cat["architecture"]["maturity_stage_count"] == 6
        and cat["architecture"]["layer_count"] == 6
        and cat["architecture"]["orchestration_domain_count"] == 10
        and cat["architecture"]["control_lifecycle_step_count"] == 8
        and cat["agents"]["agent_count"] == 5
        and cat["knowledge_graph"]["entity_count"] == 10
        and cat["knowledge_graph"]["relationship_count"] == 8
        and cat["digital_twin"]["twin_count"] == 5
        and cat["bounded_contexts"]["context_count"] == 5
        and cat["aggregates"]["aggregate_count"] == 5
        and cat["events"]["core_event_count"] == 12
        and cat["cqrs"]["command_count"] == 6 and cat["cqrs"]["query_count"] == 6
        and cat["microservices"]["service_count"] == 10
        and cat["never_replace_p219_foundation"] is True
        and cat["never_replace_p219_y_trust_ethics"] is True
        and cat["never_replace_p219_x_strategic_evolution"] is True
        and cat["never_replace_p218_z_intelligence_nexus"] is True
        and cat["never_centralized_autonomous_enterprise_control"] is True
        and cat["never_opaque_unexplainable_control_plane_recommendations"] is True
        and cat["never_ungated_cross_domain_orchestration_execution"] is True
        and cat["never_bypass_human_accountability_unified_control"] is True
        and cat["no_module_local_llm"] is True
        and cat["foundation_for_p220"] is True
        and cat["p219_series_complete"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        UnifiedEnterpriseControlPlaneRoot.enable(
            tenant_id="t1", control_ref="c1"
        ).is_missing() is False,
        IntegratedEnterpriseIntelligencePlatformRoot.enable(
            tenant_id="t1", intel_ref="i1"
        ).is_missing() is False,
        UnifiedEnterpriseCoordinationPlatformRoot.enable(
            tenant_id="t1", coord_ref="co1"
        ).is_missing() is False,
        EnterpriseGovernanceFabricRoot.enable(
            tenant_id="t1", fabric_ref="f1"
        ).is_missing() is False,
        CrossDomainOrchestrationPlatformRoot.enable(
            tenant_id="t1", orch_ref="o1"
        ).is_missing() is False,
        EnterpriseDigitalTwinFederationRoot.enable(
            tenant_id="t1", federation_ref="tf1"
        ).is_missing() is False,
        StrategicDecisionSupportPlatformRoot.enable(
            tenant_id="t1", decision_ref="d1"
        ).is_missing() is False,
        MeosUnifiedEnterpriseCoreRoot.enable(
            tenant_id="t1", core_ref="core1"
        ).is_missing() is False,
        UnifiedControlKnowledgeGraphRoot.enable(
            tenant_id="t1", kg_ref="kg1"
        ).is_missing() is False,
    ]
    acl_text = (
        root / "backend/contexts/civilization/infrastructure/acl/civ_unified_control_acl.py"
    ).read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p219", "via_p219_y", "via_p219_x", "via_p218_z",
        "via_policy_engine", "via_workflow", "via_audit",
        "via_p214_z", "via_core_platform", "via_identity",
        "never_replace_p219_foundation", "never_replace_p219_y_trust_ethics",
        "never_replace_p219_x_strategic_evolution",
        "never_replace_p218_z_intelligence_nexus",
        "never_centralized_autonomous_enterprise_control",
        "never_opaque_unexplainable_control_plane_recommendations",
        "never_ungated_cross_domain_orchestration_execution",
        "never_bypass_human_authority_unified_control",
        "never_bypass_human_accountability_unified_control",
        "never_skip_governance_fabric_gates",
        "never_violate_institutional_domain_ownership",
        "never_bypass_trusted_control_validation",
        "never_bypass_human_supervision_unified_control",
        "module_local_llm_forbidden",
        "module_local_unified_control_forbidden",
    ))
    router = (root / "backend/contexts/civilization/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@civilization_router.get("/unified-control")',
        "/unified-control/architecture", "/unified-control/intelligence",
        "/unified-control/orchestration", "/unified-control/governance-fabric",
        "/unified-control/twin-federation", "/unified-control/decision-support",
        "/unified-control/digital-twin", "/unified-control/knowledge-graph",
        "/unified-control/agents", "/unified-control/bounded-contexts",
        "/unified-control/aggregates", "/unified-control/events",
        "/unified-control/cqrs", "/unified-control/integration",
        "/unified-control/readiness",
    ))
    law = (
        root / "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_UNIFIED_ENTERPRISE_CORE.md"
    ).read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Unified Enterprise Control Plane is missing",
        "Never Integrated Enterprise Intelligence Platform is missing",
        "Never Unified Enterprise Coordination Platform is missing",
        "Never Enterprise Governance Fabric is missing",
        "Never Cross-Domain Orchestration Platform is missing",
        "Never Enterprise Digital Twin Federation is missing",
        "Never Strategic Decision Support Platform is missing",
        "Never MEOS Unified Enterprise Core is missing",
        "Never Unified Control Knowledge Graph is missing",
        "Never Unified Control Event Architecture is missing",
        "Never Unified Control CQRS Model is missing",
        "Never MEOS Unified Enterprise Integration Map is missing",
        "Never Replace P219 Foundation",
        "Never Replace P219-Y Trust Ethics Alignment",
        "Never Replace P219-X Strategic Evolution",
        "Never Replace P218-Z Intelligence Nexus",
        "Never Centralized Autonomous Enterprise Control",
        "Never Opaque Unexplainable Control Plane Recommendations",
        "Never Ungated Cross-Domain Orchestration Execution",
        "Never Bypass Human Accountability Unified Control",
        "integrates enterprise intelligence",
        "P219 series complete",
        "P220",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P219-Z", "adr": 579, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "civilization",
        "capability": "CAP-PLT-CIV-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
