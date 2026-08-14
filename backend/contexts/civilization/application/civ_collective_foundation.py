"""Civilization P219-W collective intelligence foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/576-enterprise-civilization-operating-system-collective-intelligence.md",
    "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_COLLECTIVE_INTELLIGENCE.md",
    "docs/architecture/civilization/CIVILIZATION_COLLECTIVE_CAPABILITIES.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_COLLECTIVE_ARCHITECTURE.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_COLLECTIVE_DDD_CQRS.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_COLLECTIVE_SECURITY.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_COLLECTIVE_VALIDATION.v1.yaml",
    "docs/architecture/civilization/P219_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/civilization/domain/services/civ_platform_collective.py",
    "backend/contexts/civilization/domain/aggregates/civ_collective_aggregates.py",
    "backend/contexts/civilization/infrastructure/acl/civ_collective_acl.py",
    "backend/contexts/civilization/application/civ_collective_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/collective_intelligence_platform",
    "backend/contexts/global_coordination_platform_bc",
    "backend/contexts/distributed_knowledge_collaboration_bc",
)


def validate_civ_collective_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.civilization.domain.aggregates.civ_collective_aggregates import (
        CollectiveIntelligenceEventArchitectureRoot,
        CollectiveIntelligenceKnowledgeGraphRoot,
        CollectiveIntelligencePlatformRoot,
        CollectiveLearningPlatformRoot,
        ConsensusDecisionSupportPlatformRoot,
        CoordinationDigitalTwinRoot,
        GlobalCoordinationPlatformRoot,
        KnowledgeCollaborationPlatformRoot,
        MeosCollectiveIntelligenceGlobalCoordinationCoreRoot,
    )
    from contexts.civilization.domain.services import civ_platform_collective as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P219-W" and cat["adr"] == 576 and cat["sor"] == "civilization"
        and cat["capability"] == "CAP-PLT-CIV-001"
        and cat["fabric"] == "meos_civilization_os_collective_intelligence_global_coordination_framework"
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
        and cat["gen_intel_gate"] == "P219-V"
        and cat["intelligence_nexus_gate"] == "P218-Z" and cat["space_gate"] == "P218"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["collective_intelligence_platform_present_required"] is True
        and cat["global_coordination_platform_present_required"] is True
        and cat["knowledge_collaboration_platform_present_required"] is True
        and cat["consensus_decision_support_platform_present_required"] is True
        and cat["coordination_digital_twin_present_required"] is True
        and cat["meos_collective_intelligence_global_coordination_core_present_required"] is True
        and cat["collective_intelligence_knowledge_graph_present_required"] is True
        and cat["collective_intelligence_event_architecture_present_required"] is True
        and cat["collective_intelligence_cqrs_model_present_required"] is True
        and cat["meos_collective_intelligence_integration_map_present_required"] is True
        and cat["architecture"]["maturity_stage_count"] == 6
        and cat["architecture"]["layer_count"] == 6
        and cat["architecture"]["community_domain_count"] == 10
        and cat["architecture"]["knowledge_source_count"] == 8
        and cat["architecture"]["consensus_lifecycle_step_count"] == 7
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
        and cat["never_replace_p219_p_collaboration"] is True
        and cat["never_replace_p219_v_general_intelligence"] is True
        and cat["never_replace_p219_i_knowledge"] is True
        and cat["never_replace_institutional_governance"] is True
        and cat["never_centralized_autonomous_control_of_collective_intelligence"] is True
        and cat["never_ungated_collective_decision_execution"] is True
        and cat["never_opaque_unexplainable_collective_recommendations"] is True
        and cat["never_bypass_human_accountability_collective_intelligence"] is True
        and cat["no_module_local_llm"] is True
        and cat["foundation_for_p219_x"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        CollectiveIntelligencePlatformRoot.enable(
            tenant_id="t1", collective_ref="c1"
        ).is_missing() is False,
        GlobalCoordinationPlatformRoot.enable(tenant_id="t1", coord_ref="g1").is_missing() is False,
        KnowledgeCollaborationPlatformRoot.enable(
            tenant_id="t1", knowledge_ref="k1"
        ).is_missing() is False,
        ConsensusDecisionSupportPlatformRoot.enable(
            tenant_id="t1", consensus_ref="cs1"
        ).is_missing() is False,
        CoordinationDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        MeosCollectiveIntelligenceGlobalCoordinationCoreRoot.enable(
            tenant_id="t1", core_ref="core1"
        ).is_missing() is False,
        CollectiveIntelligenceKnowledgeGraphRoot.enable(
            tenant_id="t1", kg_ref="kg1"
        ).is_missing() is False,
        CollectiveIntelligenceEventArchitectureRoot.enable(
            tenant_id="t1", events_ref="ev1"
        ).is_missing() is False,
        CollectiveLearningPlatformRoot.enable(
            tenant_id="t1", learning_ref="l1"
        ).is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/civilization/infrastructure/acl/civ_collective_acl.py").read_text(
        encoding="utf-8"
    )
    acl_ok = all(x in acl_text for x in (
        "via_p219", "via_p219_i", "via_p219_p", "via_p219_v",
        "via_policy_engine", "via_workflow", "via_audit",
        "via_p218_z", "via_p214_z", "via_core_platform", "via_identity",
        "never_replace_p219_foundation", "never_replace_p219_p_collaboration",
        "never_replace_p219_v_general_intelligence", "never_replace_p219_i_knowledge",
        "never_replace_institutional_governance",
        "never_centralized_autonomous_control_of_collective_intelligence",
        "never_opaque_unexplainable_collective_recommendations",
        "never_ungated_collective_decision_execution",
        "never_skip_ethical_collective_collaboration",
        "never_skip_human_authority_collective_decisions",
        "never_violate_human_sovereignty_collective_intelligence",
        "never_bypass_trusted_collective_validation",
        "never_bypass_human_supervision_collective_intelligence",
        "never_bypass_human_accountability_collective_intelligence",
        "module_local_llm_forbidden",
        "module_local_collective_intelligence_forbidden",
    ))
    router = (root / "backend/contexts/civilization/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@civilization_router.get("/collective-intelligence")',
        "/collective-intelligence/architecture", "/collective-intelligence/coordination",
        "/collective-intelligence/knowledge", "/collective-intelligence/consensus",
        "/collective-intelligence/learning", "/collective-intelligence/digital-twin",
        "/collective-intelligence/knowledge-graph", "/collective-intelligence/agents",
        "/collective-intelligence/bounded-contexts", "/collective-intelligence/aggregates",
        "/collective-intelligence/events", "/collective-intelligence/cqrs",
        "/collective-intelligence/integration", "/collective-intelligence/readiness",
    ))
    law = (
        root / "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_COLLECTIVE_INTELLIGENCE.md"
    ).read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Collective Intelligence Platform is missing",
        "Never Global Coordination Platform is missing",
        "Never Knowledge Collaboration Platform is missing",
        "Never Consensus Decision Support Platform is missing",
        "Never Coordination Digital Twin is missing",
        "Never MEOS Collective Intelligence & Global Coordination Core is missing",
        "Never Collective Intelligence Knowledge Graph is missing",
        "Never Collective Intelligence Event Architecture is missing",
        "Never Collective Intelligence CQRS Model is missing",
        "Never MEOS Collective Intelligence Integration Map is missing",
        "Never Replace P219 Foundation",
        "Never Replace P219-P Collaboration",
        "Never Replace P219-V General Intelligence Coordination",
        "Never Replace P219-I Knowledge",
        "Never Replace Institutional Governance",
        "Never Centralized Autonomous Control Of Collective Intelligence",
        "Never Opaque Unexplainable Collective Recommendations",
        "Never Ungated Collective Decision Execution",
        "Never Bypass Human Accountability Collective Intelligence",
        "integrating distributed expertise, institutional knowledge and AI-assisted analysis",
        "P219-X",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P219-W", "adr": 576, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "civilization",
        "capability": "CAP-PLT-CIV-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
