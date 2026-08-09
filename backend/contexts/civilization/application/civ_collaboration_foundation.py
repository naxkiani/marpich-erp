"""Civilization P219-P collaboration intelligence foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/569-enterprise-civilization-operating-system-collaboration.md",
    "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_COLLABORATION.md",
    "docs/architecture/civilization/CIVILIZATION_COLLABORATION_CAPABILITIES.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_COLLABORATION_ARCHITECTURE.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_COLLABORATION_DDD_CQRS.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_COLLABORATION_SECURITY.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_COLLABORATION_VALIDATION.v1.yaml",
    "docs/architecture/civilization/P219_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/civilization/domain/services/civ_platform_collaboration.py",
    "backend/contexts/civilization/domain/aggregates/civ_collaboration_aggregates.py",
    "backend/contexts/civilization/infrastructure/acl/civ_collaboration_acl.py",
    "backend/contexts/civilization/application/civ_collaboration_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/civilization_collaboration_intelligence_platform",
    "backend/contexts/global_collaboration_network_bc",
    "backend/contexts/collective_problem_solving_platform_bc",
)


def validate_civ_collaboration_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.civilization.domain.aggregates.civ_collaboration_aggregates import (
        CivilizationCollaborationIntelligencePlatformRoot,
        CivilizationCoordinationPlatformRoot,
        CollaborationDigitalTwinRoot,
        CollaborationEventArchitectureRoot,
        CollaborationKnowledgeGraphRoot,
        CollectiveProblemSolvingPlatformRoot,
        GlobalCollaborationNetworkRoot,
        MeosCivilizationCollaborationIntelligenceCoreRoot,
    )
    from contexts.civilization.domain.services import civ_platform_collaboration as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P219-P" and cat["adr"] == 569 and cat["sor"] == "civilization"
        and cat["capability"] == "CAP-PLT-CIV-001"
        and cat["fabric"] == "meos_civilization_os_civilization_collaboration_intelligence_framework"
        and cat["foundation_gate"] == "P219" and cat["mission_gate"] == "P219-A"
        and cat["strategy_gate"] == "P219-B" and cat["domain_gate"] == "P219-C"
        and cat["planetary_gate"] == "P219-D" and cat["ai_os_gate"] == "P219-E"
        and cat["simulation_gate"] == "P219-F" and cat["resources_gate"] == "P219-G"
        and cat["economy_gate"] == "P219-H" and cat["knowledge_gate"] == "P219-I"
        and cat["human_gate"] == "P219-J" and cat["governance_gate"] == "P219-K"
        and cat["innovation_gate"] == "P219-L" and cat["security_gate"] == "P219-M"
        and cat["sustainability_gate"] == "P219-N" and cat["prosperity_gate"] == "P219-O"
        and cat["intelligence_nexus_gate"] == "P218-Z" and cat["space_gate"] == "P218"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["civilization_collaboration_intelligence_platform_present_required"] is True
        and cat["global_collaboration_network_present_required"] is True
        and cat["collective_problem_solving_platform_present_required"] is True
        and cat["civilization_coordination_platform_present_required"] is True
        and cat["collaboration_digital_twin_present_required"] is True
        and cat["collaboration_knowledge_graph_present_required"] is True
        and cat["meos_civilization_collaboration_intelligence_core_present_required"] is True
        and cat["collaboration_event_architecture_present_required"] is True
        and cat["collaboration_cqrs_model_present_required"] is True
        and cat["meos_collaboration_integration_map_present_required"] is True
        and cat["architecture"]["evolution_stage_count"] == 6
        and cat["architecture"]["layer_count"] == 6
        and cat["architecture"]["participant_count"] == 8
        and cat["architecture"]["network_domain_count"] == 9
        and cat["architecture"]["problem_domain_count"] == 10
        and cat["architecture"]["problem_solving_lifecycle_step_count"] == 8
        and cat["architecture"]["coordination_level_count"] == 9
        and cat["agents"]["agent_count"] == 5
        and cat["knowledge_graph"]["entity_count"] == 10
        and cat["knowledge_graph"]["relationship_count"] == 8
        and cat["digital_twin"]["twin_count"] == 5
        and cat["bounded_contexts"]["context_count"] == 4
        and cat["aggregates"]["aggregate_count"] == 5
        and cat["events"]["core_event_count"] == 13
        and cat["cqrs"]["command_count"] == 6 and cat["cqrs"]["query_count"] == 6
        and cat["microservices"]["service_count"] == 10
        and cat["never_replace_p219_foundation"] is True
        and cat["never_replace_p219_o_prosperity"] is True
        and cat["never_replace_p219_i_knowledge"] is True
        and cat["never_replace_p219_k_governance"] is True
        and cat["never_ungated_collaborative_decision_execution"] is True
        and cat["never_treat_consensus_score_as_binding_policy"] is True
        and cat["never_bypass_collective_consent_safeguards"] is True
        and cat["never_opaque_unexplainable_collaboration_decisions"] is True
        and cat["no_module_local_llm"] is True
        and cat["foundation_for_p219_q"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        CivilizationCollaborationIntelligencePlatformRoot.enable(
            tenant_id="t1", collaboration_ref="c1"
        ).is_missing() is False,
        GlobalCollaborationNetworkRoot.enable(tenant_id="t1", network_ref="n1").is_missing() is False,
        CollectiveProblemSolvingPlatformRoot.enable(
            tenant_id="t1", collective_ref="col1"
        ).is_missing() is False,
        CivilizationCoordinationPlatformRoot.enable(
            tenant_id="t1", coordination_ref="coord1"
        ).is_missing() is False,
        CollaborationDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        CollaborationKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="k1").is_missing() is False,
        MeosCivilizationCollaborationIntelligenceCoreRoot.enable(
            tenant_id="t1", core_ref="core1"
        ).is_missing() is False,
        CollaborationEventArchitectureRoot.enable(tenant_id="t1", events_ref="e1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/civilization/infrastructure/acl/civ_collaboration_acl.py").read_text(
        encoding="utf-8"
    )
    acl_ok = all(x in acl_text for x in (
        "via_p219", "via_p219_a", "via_p219_b", "via_p219_c", "via_p219_d", "via_p219_e",
        "via_p219_f", "via_p219_g", "via_p219_h", "via_p219_i", "via_p219_j", "via_p219_k",
        "via_p219_l", "via_p219_m", "via_p219_n", "via_p219_o",
        "via_policy_engine", "via_workflow", "via_audit",
        "via_p218_z", "via_p218", "via_p217", "via_p216_z", "via_p215_z", "via_p214_z",
        "via_core_platform", "via_identity",
        "never_replace_p219_foundation", "never_replace_p219_a_mission", "never_replace_p219_b_strategy",
        "never_replace_p219_c_domain", "never_replace_p219_d_planetary", "never_replace_p219_e_ai_os",
        "never_replace_p219_f_simulation", "never_replace_p219_g_resources", "never_replace_p219_h_economy",
        "never_replace_p219_i_knowledge", "never_replace_p219_j_human", "never_replace_p219_k_governance",
        "never_replace_p219_l_innovation", "never_replace_p219_m_security", "never_replace_p219_n_sustainability",
        "never_replace_p219_o_prosperity",
        "never_replace_policy_engine", "never_replace_workflow", "never_replace_audit",
        "never_replace_p218_z_intelligence_nexus", "never_replace_space",
        "never_merge_p218_t_space_civilization", "never_cross_context_aggregate_imports",
        "never_opaque_unexplainable_collaboration_decisions",
        "never_ungated_collaborative_decision_execution",
        "never_treat_consensus_score_as_binding_policy",
        "never_skip_ethical_collaboration_governance",
        "never_skip_human_authority_collaboration",
        "never_violate_human_sovereignty_collaboration",
        "never_bypass_trusted_collaboration_validation",
        "never_bypass_collective_consent_safeguards",
        "module_local_llm_forbidden",
        "module_local_civilization_collaboration_forbidden",
    ))
    router = (root / "backend/contexts/civilization/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@civilization_router.get("/collaboration")',
        "/collaboration/architecture", "/collaboration/network", "/collaboration/collective",
        "/collaboration/coordination", "/collaboration/digital-twin",
        "/collaboration/knowledge-graph", "/collaboration/agents", "/collaboration/bounded-contexts",
        "/collaboration/aggregates", "/collaboration/events", "/collaboration/cqrs",
        "/collaboration/integration", "/collaboration/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_COLLABORATION.md").read_text(
        encoding="utf-8"
    )
    doc_ok = all(x in law for x in (
        "Never Civilization Collaboration Intelligence Platform is missing",
        "Never Global Collaboration Network is missing",
        "Never Collective Problem Solving Platform is missing",
        "Never Civilization Coordination Platform is missing",
        "Never Collaboration Digital Twin is missing",
        "Never Collaboration Knowledge Graph is missing",
        "Never MEOS Civilization Collaboration Intelligence Core is missing",
        "Never Collaboration Event Architecture is missing",
        "Never Collaboration CQRS Model is missing",
        "Never MEOS Collaboration Integration Map is missing",
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
        "Never Replace P219-K Governance",
        "Never Replace P219-L Innovation",
        "Never Replace P219-M Security",
        "Never Replace P219-N Sustainability",
        "Never Replace P219-O Prosperity",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace Policy Engine",
        "Never Replace Workflow",
        "Never Replace Audit",
        "Never Replace P215-Z Quantum",
        "Never Replace P216-Z Robotics",
        "Never Replace P217 Biotechnology",
        "Never Replace P218 Space",
        "Never Replace P218-Z Intelligence Nexus",
        "Never Merge P218-T Space Civilization Phase",
        "Never Module-Local LLM",
        "Never Cross-Context Aggregate Imports",
        "Never Opaque Unexplainable Collaboration Decisions",
        "Never Ungated Collaborative Decision Execution",
        "Never Treat Consensus Score As Binding Policy",
        "Never Skip Ethical Collaboration Governance",
        "Never Skip Human Authority Collaboration",
        "Never Violate Human Sovereignty Collaboration",
        "Never Bypass Trusted Collaboration Validation",
        "Never Bypass Collective Consent Safeguards",
        "enabling humans, AI, institutions and autonomous systems to solve global",
        "P219-Q",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P219-P", "adr": 569, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "civilization",
        "capability": "CAP-PLT-CIV-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
