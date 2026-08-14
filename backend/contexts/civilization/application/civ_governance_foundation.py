"""Civilization P219-K governance intelligence foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/564-enterprise-civilization-operating-system-governance.md",
    "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_GOVERNANCE.md",
    "docs/architecture/civilization/CIVILIZATION_GOVERNANCE_CAPABILITIES.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_GOVERNANCE_ARCHITECTURE.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_GOVERNANCE_DDD_CQRS.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_GOVERNANCE_SECURITY.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_GOVERNANCE_VALIDATION.v1.yaml",
    "docs/architecture/civilization/P219_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/civilization/domain/services/civ_platform_governance.py",
    "backend/contexts/civilization/domain/aggregates/civ_governance_aggregates.py",
    "backend/contexts/civilization/infrastructure/acl/civ_governance_acl.py",
    "backend/contexts/civilization/application/civ_governance_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/civilization_governance_intelligence_platform",
    "backend/contexts/global_policy_intelligence_bc",
    "backend/contexts/autonomous_governance_systems_bc",
)


def validate_civ_governance_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.civilization.domain.aggregates.civ_governance_aggregates import (
        AutonomousGovernanceSystemRoot,
        CivilizationGovernanceIntelligencePlatformRoot,
        DecisionIntelligenceEngineRoot,
        EthicsIntelligenceRoot,
        GlobalPolicyIntelligenceRoot,
        GovernanceDigitalTwinRoot,
        GovernanceEventArchitectureRoot,
        GovernanceKnowledgeGraphRoot,
        MeosCivilizationGovernanceIntelligenceCoreRoot,
    )
    from contexts.civilization.domain.services import civ_platform_governance as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P219-K" and cat["adr"] == 564 and cat["sor"] == "civilization"
        and cat["capability"] == "CAP-PLT-CIV-001"
        and cat["fabric"] == "meos_civilization_os_civilization_governance_intelligence_framework"
        and cat["foundation_gate"] == "P219" and cat["mission_gate"] == "P219-A"
        and cat["strategy_gate"] == "P219-B" and cat["domain_gate"] == "P219-C"
        and cat["planetary_gate"] == "P219-D" and cat["ai_os_gate"] == "P219-E"
        and cat["simulation_gate"] == "P219-F" and cat["resources_gate"] == "P219-G"
        and cat["economy_gate"] == "P219-H" and cat["knowledge_gate"] == "P219-I"
        and cat["human_gate"] == "P219-J"
        and cat["intelligence_nexus_gate"] == "P218-Z" and cat["space_gate"] == "P218"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["civilization_governance_intelligence_platform_present_required"] is True
        and cat["global_policy_intelligence_present_required"] is True
        and cat["decision_intelligence_engine_present_required"] is True
        and cat["autonomous_governance_system_present_required"] is True
        and cat["governance_digital_twin_present_required"] is True
        and cat["governance_knowledge_graph_present_required"] is True
        and cat["meos_civilization_governance_intelligence_core_present_required"] is True
        and cat["ethics_intelligence_present_required"] is True
        and cat["governance_event_architecture_present_required"] is True
        and cat["governance_cqrs_model_present_required"] is True
        and cat["meos_governance_integration_map_present_required"] is True
        and cat["architecture"]["evolution_stage_count"] == 6
        and cat["architecture"]["layer_count"] == 6
        and cat["architecture"]["policy_domain_count"] == 10
        and cat["architecture"]["decision_pipeline_step_count"] == 8
        and cat["agents"]["agent_count"] == 5
        and cat["knowledge_graph"]["entity_count"] == 10
        and cat["knowledge_graph"]["relationship_count"] == 8
        and cat["digital_twin"]["twin_count"] == 5
        and cat["bounded_contexts"]["context_count"] == 5
        and cat["aggregates"]["aggregate_count"] == 6
        and cat["events"]["core_event_count"] == 17
        and cat["cqrs"]["command_count"] == 7 and cat["cqrs"]["query_count"] == 6
        and cat["microservices"]["service_count"] == 10
        and cat["never_replace_p219_foundation"] is True
        and cat["never_replace_p219_j_human"] is True
        and cat["never_replace_policy_engine"] is True
        and cat["never_replace_workflow"] is True
        and cat["never_replace_compliance"] is True
        and cat["never_replace_audit"] is True
        and cat["never_ungated_governance_action_execution"] is True
        and cat["never_autonomous_binding_governance_without_human_approval"] is True
        and cat["never_local_approval_engine"] is True
        and cat["never_opaque_unexplainable_governance_decisions"] is True
        and cat["no_module_local_llm"] is True
        and cat["foundation_for_p219_l"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        CivilizationGovernanceIntelligencePlatformRoot.enable(tenant_id="t1", governance_ref="g1").is_missing() is False,
        GlobalPolicyIntelligenceRoot.enable(tenant_id="t1", policy_ref="p1").is_missing() is False,
        DecisionIntelligenceEngineRoot.enable(tenant_id="t1", decision_ref="d1").is_missing() is False,
        AutonomousGovernanceSystemRoot.enable(tenant_id="t1", autonomous_ref="a1").is_missing() is False,
        GovernanceDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        GovernanceKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="k1").is_missing() is False,
        MeosCivilizationGovernanceIntelligenceCoreRoot.enable(tenant_id="t1", core_ref="core1").is_missing() is False,
        EthicsIntelligenceRoot.enable(tenant_id="t1", ethics_ref="e1").is_missing() is False,
        GovernanceEventArchitectureRoot.enable(tenant_id="t1", events_ref="ev1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/civilization/infrastructure/acl/civ_governance_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p219", "via_p219_a", "via_p219_b", "via_p219_c", "via_p219_d", "via_p219_e",
        "via_p219_f", "via_p219_g", "via_p219_h", "via_p219_i", "via_p219_j",
        "via_policy_engine", "via_workflow", "via_compliance", "via_audit",
        "via_p218_z", "via_p218", "via_p217", "via_p216_z", "via_p215_z", "via_p214_z",
        "via_identity", "via_core_platform",
        "never_replace_p219_foundation", "never_replace_p219_a_mission", "never_replace_p219_b_strategy",
        "never_replace_p219_c_domain", "never_replace_p219_d_planetary", "never_replace_p219_e_ai_os",
        "never_replace_p219_f_simulation", "never_replace_p219_g_resources", "never_replace_p219_h_economy",
        "never_replace_p219_i_knowledge", "never_replace_p219_j_human",
        "never_replace_policy_engine", "never_replace_workflow", "never_replace_compliance", "never_replace_audit",
        "never_replace_p218_z_intelligence_nexus", "never_replace_space",
        "never_merge_p218_t_space_civilization", "never_cross_context_aggregate_imports",
        "never_opaque_unexplainable_governance_decisions",
        "never_ungated_governance_action_execution",
        "never_autonomous_binding_governance_without_human_approval",
        "never_skip_human_authority_governance",
        "never_skip_ethical_governance",
        "never_violate_human_sovereignty_governance",
        "never_bypass_trusted_governance_validation",
        "never_local_approval_engine",
        "module_local_llm_forbidden",
        "module_local_civilization_governance_forbidden",
    ))
    router = (root / "backend/contexts/civilization/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@civilization_router.get("/governance")',
        "/governance/architecture", "/governance/policy", "/governance/decision",
        "/governance/autonomous", "/governance/digital-twin", "/governance/knowledge-graph",
        "/governance/agents", "/governance/bounded-contexts", "/governance/aggregates",
        "/governance/events", "/governance/cqrs", "/governance/ethics",
        "/governance/integration", "/governance/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_GOVERNANCE.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Civilization Governance Intelligence Platform is missing",
        "Never Global Policy Intelligence is missing",
        "Never Decision Intelligence Engine is missing",
        "Never Autonomous Governance System is missing",
        "Never Governance Digital Twin is missing",
        "Never Governance Knowledge Graph is missing",
        "Never MEOS Civilization Governance Intelligence Core is missing",
        "Never Ethics Intelligence is missing",
        "Never Governance Event Architecture is missing",
        "Never Governance CQRS Model is missing",
        "Never MEOS Governance Integration Map is missing",
        "Never Replace P219 Foundation",
        "Never Replace P219-A Mission",
        "Never Replace P219-B Strategy",
        "Never Replace P219-C Domain",
        "Never Replace P219-D Planetary",
        "Never Replace P219-E AI OS",
        "Never Replace P219-F Simulation",
        "Never Replace P219-G Resources",
        "Never Replace P219-H Economy",
        "Never Replace P219-I Knowledge",
        "Never Replace P219-J Human",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace Policy Engine",
        "Never Replace Workflow",
        "Never Replace Compliance",
        "Never Replace Audit",
        "Never Replace P215-Z Quantum",
        "Never Replace P216-Z Robotics",
        "Never Replace P217 Biotechnology",
        "Never Replace P218 Space",
        "Never Replace P218-Z Intelligence Nexus",
        "Never Merge P218-T Space Civilization Phase",
        "Never Module-Local LLM",
        "Never Cross-Context Aggregate Imports",
        "Never Opaque Unexplainable Governance Decisions",
        "Never Ungated Governance Action Execution",
        "Never Autonomous Binding Governance Without Human Approval",
        "Never Skip Human Authority Governance",
        "Never Skip Ethical Governance",
        "Never Violate Human Sovereignty Governance",
        "Never Bypass Trusted Governance Validation",
        "Never Local Approval Engine",
        "designing, validating, simulating and continuously improving policies",
        "P219-L",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P219-K", "adr": 564, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "civilization",
        "capability": "CAP-PLT-CIV-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
