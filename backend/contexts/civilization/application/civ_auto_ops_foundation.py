"""Civilization P219-U autonomous operations foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/574-enterprise-civilization-operating-system-autonomous-operations.md",
    "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_AUTONOMOUS_OPERATIONS.md",
    "docs/architecture/civilization/CIVILIZATION_AUTO_OPS_CAPABILITIES.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_AUTO_OPS_ARCHITECTURE.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_AUTO_OPS_DDD_CQRS.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_AUTO_OPS_SECURITY.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_AUTO_OPS_VALIDATION.v1.yaml",
    "docs/architecture/civilization/P219_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/civilization/domain/services/civ_platform_auto_ops.py",
    "backend/contexts/civilization/domain/aggregates/civ_auto_ops_aggregates.py",
    "backend/contexts/civilization/infrastructure/acl/civ_auto_ops_acl.py",
    "backend/contexts/civilization/application/civ_auto_ops_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/autonomous_civilization_operations_platform",
    "backend/contexts/mission_orchestration_platform_bc",
    "backend/contexts/civilization_operations_automation_bc",
)


def validate_civ_auto_ops_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.civilization.domain.aggregates.civ_auto_ops_aggregates import (
        AutonomousCivilizationOperationsPlatformRoot,
        MeosAutonomousCivilizationOperationsCoreRoot,
        MissionOrchestrationPlatformRoot,
        OperationsDigitalTwinRoot,
        OperationsEventArchitectureRoot,
        OperationsIntelligencePlatformRoot,
        OperationsKnowledgeGraphRoot,
        ResourceOptimizationPlatformRoot,
        WorkflowAutomationPlatformRoot,
    )
    from contexts.civilization.domain.services import civ_platform_auto_ops as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P219-U" and cat["adr"] == 574 and cat["sor"] == "civilization"
        and cat["capability"] == "CAP-PLT-CIV-001"
        and cat["fabric"] == "meos_civilization_os_autonomous_civilization_operations_framework"
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
        and cat["intel_gov_gate"] == "P219-T"
        and cat["intelligence_nexus_gate"] == "P218-Z" and cat["space_gate"] == "P218"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["autonomous_civilization_operations_platform_present_required"] is True
        and cat["mission_orchestration_platform_present_required"] is True
        and cat["operations_intelligence_platform_present_required"] is True
        and cat["workflow_automation_platform_present_required"] is True
        and cat["resource_optimization_platform_present_required"] is True
        and cat["operations_digital_twin_present_required"] is True
        and cat["meos_autonomous_civilization_operations_core_present_required"] is True
        and cat["operations_knowledge_graph_present_required"] is True
        and cat["operations_event_architecture_present_required"] is True
        and cat["operations_cqrs_model_present_required"] is True
        and cat["meos_operations_integration_map_present_required"] is True
        and cat["architecture"]["maturity_stage_count"] == 6
        and cat["architecture"]["layer_count"] == 6
        and cat["architecture"]["operational_domain_count"] == 10
        and cat["architecture"]["mission_lifecycle_step_count"] == 8
        and cat["architecture"]["mission_type_count"] == 9
        and cat["architecture"]["workflow_category_count"] == 8
        and cat["architecture"]["resource_count"] == 8
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
        and cat["never_replace_p219_t_intelligence_governance"] is True
        and cat["never_replace_workflow"] is True
        and cat["never_replace_p219_f_simulation"] is True
        and cat["never_ungated_autonomous_operations_execution"] is True
        and cat["never_opaque_unexplainable_operations_automation"] is True
        and cat["never_bypass_human_supervision_operations"] is True
        and cat["never_bypass_human_governed_autonomy"] is True
        and cat["never_skip_human_review_gates_operations"] is True
        and cat["no_module_local_llm"] is True
        and cat["foundation_for_p219_v"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        AutonomousCivilizationOperationsPlatformRoot.enable(
            tenant_id="t1", ops_ref="o1"
        ).is_missing() is False,
        MissionOrchestrationPlatformRoot.enable(
            tenant_id="t1", mission_ref="m1"
        ).is_missing() is False,
        OperationsIntelligencePlatformRoot.enable(
            tenant_id="t1", intel_ref="i1"
        ).is_missing() is False,
        WorkflowAutomationPlatformRoot.enable(
            tenant_id="t1", workflow_ref="w1"
        ).is_missing() is False,
        ResourceOptimizationPlatformRoot.enable(
            tenant_id="t1", resource_ref="r1"
        ).is_missing() is False,
        OperationsDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        MeosAutonomousCivilizationOperationsCoreRoot.enable(
            tenant_id="t1", core_ref="core1"
        ).is_missing() is False,
        OperationsKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="k1").is_missing() is False,
        OperationsEventArchitectureRoot.enable(
            tenant_id="t1", events_ref="ev1"
        ).is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/civilization/infrastructure/acl/civ_auto_ops_acl.py").read_text(
        encoding="utf-8"
    )
    acl_ok = all(x in acl_text for x in (
        "via_p219", "via_p219_e", "via_p219_f", "via_p219_k", "via_p219_t",
        "via_policy_engine", "via_workflow", "via_audit",
        "via_p218_z", "via_p214_z", "via_core_platform", "via_identity",
        "never_replace_p219_foundation", "never_replace_p219_e_ai_os",
        "never_replace_p219_f_simulation", "never_replace_p219_k_governance",
        "never_replace_p219_t_intelligence_governance", "never_replace_workflow",
        "never_opaque_unexplainable_operations_automation",
        "never_ungated_autonomous_operations_execution",
        "never_skip_human_review_gates_operations",
        "never_skip_ethical_operations_governance",
        "never_skip_human_authority_operations",
        "never_violate_human_sovereignty_operations",
        "never_bypass_trusted_operations_validation",
        "never_bypass_human_supervision_operations",
        "never_bypass_human_governed_autonomy",
        "module_local_llm_forbidden",
        "module_local_autonomous_civilization_operations_forbidden",
    ))
    router = (root / "backend/contexts/civilization/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@civilization_router.get("/autonomous-operations")',
        "/autonomous-operations/architecture", "/autonomous-operations/missions",
        "/autonomous-operations/workflows", "/autonomous-operations/resources",
        "/autonomous-operations/intelligence", "/autonomous-operations/digital-twin",
        "/autonomous-operations/knowledge-graph", "/autonomous-operations/agents",
        "/autonomous-operations/bounded-contexts", "/autonomous-operations/aggregates",
        "/autonomous-operations/events", "/autonomous-operations/cqrs",
        "/autonomous-operations/integration", "/autonomous-operations/readiness",
    ))
    law = (
        root / "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_AUTONOMOUS_OPERATIONS.md"
    ).read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Autonomous Civilization Operations Platform is missing",
        "Never Mission Orchestration Platform is missing",
        "Never Operations Intelligence Platform is missing",
        "Never Workflow Automation Platform is missing",
        "Never Resource Optimization Platform is missing",
        "Never Operations Digital Twin is missing",
        "Never MEOS Autonomous Civilization Operations Core is missing",
        "Never Operations Knowledge Graph is missing",
        "Never Operations Event Architecture is missing",
        "Never Operations CQRS Model is missing",
        "Never MEOS Operations Integration Map is missing",
        "Never Replace P219 Foundation",
        "Never Replace P219-E AI OS",
        "Never Replace P219-T Intelligence Governance",
        "Never Replace Workflow",
        "Never Opaque Unexplainable Operations Automation",
        "Never Ungated Autonomous Operations Execution",
        "Never Bypass Human-Governed Autonomy",
        "coordinating complex multi-domain operations, improving execution efficiency",
        "P219-V",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P219-U", "adr": 574, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "civilization",
        "capability": "CAP-PLT-CIV-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
