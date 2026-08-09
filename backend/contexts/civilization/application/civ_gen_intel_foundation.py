"""Civilization P219-V general intelligence coordination foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/575-enterprise-civilization-operating-system-general-intelligence-coordination.md",
    "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_GENERAL_INTELLIGENCE_COORDINATION.md",
    "docs/architecture/civilization/CIVILIZATION_GEN_INTEL_CAPABILITIES.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_GEN_INTEL_ARCHITECTURE.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_GEN_INTEL_DDD_CQRS.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_GEN_INTEL_SECURITY.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_GEN_INTEL_VALIDATION.v1.yaml",
    "docs/architecture/civilization/P219_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/civilization/domain/services/civ_platform_gen_intel.py",
    "backend/contexts/civilization/domain/aggregates/civ_gen_intel_aggregates.py",
    "backend/contexts/civilization/infrastructure/acl/civ_gen_intel_acl.py",
    "backend/contexts/civilization/application/civ_gen_intel_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/civilization_general_intelligence_coordination_platform",
    "backend/contexts/cross_domain_intelligence_platform_bc",
    "backend/contexts/unified_intelligence_collaboration_bc",
)


def validate_civ_gen_intel_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.civilization.domain.aggregates.civ_gen_intel_aggregates import (
        CivilizationGeneralIntelligenceCoordinationPlatformRoot,
        CoordinationDigitalTwinRoot,
        CrossDomainIntelligencePlatformRoot,
        DecisionSupportPlatformRoot,
        IntelligenceCoordinationEventArchitectureRoot,
        IntelligenceKnowledgeGraphRoot,
        KnowledgeFusionPlatformRoot,
        MeosCivilizationGeneralIntelligenceCoordinationCoreRoot,
        MultiAgentCoordinationPlatformRoot,
    )
    from contexts.civilization.domain.services import civ_platform_gen_intel as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P219-V" and cat["adr"] == 575 and cat["sor"] == "civilization"
        and cat["capability"] == "CAP-PLT-CIV-001"
        and cat["fabric"] == "meos_civilization_os_civilization_general_intelligence_coordination_framework"
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
        and cat["intelligence_nexus_gate"] == "P218-Z" and cat["space_gate"] == "P218"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["civilization_general_intelligence_coordination_platform_present_required"] is True
        and cat["knowledge_fusion_platform_present_required"] is True
        and cat["multi_agent_coordination_platform_present_required"] is True
        and cat["cross_domain_intelligence_platform_present_required"] is True
        and cat["decision_support_platform_present_required"] is True
        and cat["coordination_digital_twin_present_required"] is True
        and cat["meos_civilization_general_intelligence_coordination_core_present_required"] is True
        and cat["intelligence_knowledge_graph_present_required"] is True
        and cat["intelligence_coordination_event_architecture_present_required"] is True
        and cat["intelligence_coordination_cqrs_model_present_required"] is True
        and cat["meos_intelligence_coordination_integration_map_present_required"] is True
        and cat["architecture"]["maturity_stage_count"] == 7
        and cat["architecture"]["layer_count"] == 6
        and cat["architecture"]["knowledge_domain_count"] == 10
        and cat["architecture"]["knowledge_source_count"] == 8
        and cat["architecture"]["agent_category_count"] == 8
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
        and cat["never_replace_p214_z"] is True
        and cat["never_replace_p218_z_intelligence_nexus"] is True
        and cat["never_replace_p219_e_ai_os"] is True
        and cat["never_replace_p219_i_knowledge"] is True
        and cat["never_replace_p219_u_autonomous_operations"] is True
        and cat["never_claim_autonomous_general_intelligence"] is True
        and cat["never_ungated_intelligence_coordination_decisions"] is True
        and cat["never_opaque_unexplainable_coordination_reasoning"] is True
        and cat["never_bypass_human_centered_intelligence"] is True
        and cat["no_module_local_llm"] is True
        and cat["foundation_for_p219_w"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        CivilizationGeneralIntelligenceCoordinationPlatformRoot.enable(
            tenant_id="t1", cgi_ref="c1"
        ).is_missing() is False,
        KnowledgeFusionPlatformRoot.enable(tenant_id="t1", fusion_ref="f1").is_missing() is False,
        MultiAgentCoordinationPlatformRoot.enable(
            tenant_id="t1", agent_ref="a1"
        ).is_missing() is False,
        CrossDomainIntelligencePlatformRoot.enable(
            tenant_id="t1", cross_ref="x1"
        ).is_missing() is False,
        DecisionSupportPlatformRoot.enable(
            tenant_id="t1", decision_ref="d1"
        ).is_missing() is False,
        CoordinationDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        MeosCivilizationGeneralIntelligenceCoordinationCoreRoot.enable(
            tenant_id="t1", core_ref="core1"
        ).is_missing() is False,
        IntelligenceKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="k1").is_missing() is False,
        IntelligenceCoordinationEventArchitectureRoot.enable(
            tenant_id="t1", events_ref="ev1"
        ).is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/civilization/infrastructure/acl/civ_gen_intel_acl.py").read_text(
        encoding="utf-8"
    )
    acl_ok = all(x in acl_text for x in (
        "via_p219", "via_p219_e", "via_p219_f", "via_p219_i", "via_p219_u",
        "via_policy_engine", "via_workflow", "via_audit",
        "via_p218_z", "via_p214_z", "via_core_platform", "via_identity",
        "never_replace_p219_foundation", "never_replace_p219_e_ai_os",
        "never_replace_p219_i_knowledge", "never_replace_p219_u_autonomous_operations",
        "never_replace_p214_z", "never_replace_p218_z_intelligence_nexus",
        "never_claim_autonomous_general_intelligence",
        "never_opaque_unexplainable_coordination_reasoning",
        "never_ungated_intelligence_coordination_decisions",
        "never_skip_ethical_intelligence_coordination",
        "never_skip_human_authority_intelligence_coordination",
        "never_violate_human_sovereignty_intelligence_coordination",
        "never_bypass_trusted_intelligence_validation",
        "never_bypass_human_supervision_intelligence_coordination",
        "never_bypass_human_centered_intelligence",
        "module_local_llm_forbidden",
        "module_local_civilization_general_intelligence_coordination_forbidden",
    ))
    router = (root / "backend/contexts/civilization/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@civilization_router.get("/general-intelligence")',
        "/general-intelligence/architecture", "/general-intelligence/cross-domain",
        "/general-intelligence/knowledge-fusion", "/general-intelligence/agents",
        "/general-intelligence/decision-support", "/general-intelligence/digital-twin",
        "/general-intelligence/knowledge-graph", "/general-intelligence/reasoning",
        "/general-intelligence/bounded-contexts", "/general-intelligence/aggregates",
        "/general-intelligence/events", "/general-intelligence/cqrs",
        "/general-intelligence/integration", "/general-intelligence/readiness",
    ))
    law = (
        root / "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_GENERAL_INTELLIGENCE_COORDINATION.md"
    ).read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Civilization General Intelligence Coordination Platform is missing",
        "Never Knowledge Fusion Platform is missing",
        "Never Multi-Agent Coordination Platform is missing",
        "Never Cross-Domain Intelligence Platform is missing",
        "Never Decision Support Platform is missing",
        "Never Coordination Digital Twin is missing",
        "Never MEOS Civilization General Intelligence Coordination Core is missing",
        "Never Intelligence Knowledge Graph is missing",
        "Never Intelligence Coordination Event Architecture is missing",
        "Never Intelligence Coordination CQRS Model is missing",
        "Never MEOS Intelligence Coordination Integration Map is missing",
        "Never Replace P219 Foundation",
        "Never Replace P219-E AI OS",
        "Never Replace P219-I Knowledge",
        "Never Replace P219-U Autonomous Operations",
        "Never Claim Autonomous General Intelligence",
        "Never Opaque Unexplainable Coordination Reasoning",
        "Never Ungated Intelligence Coordination Decisions",
        "Never Bypass Human-Centered Intelligence",
        "integrating knowledge, analytical models and specialized AI capabilities",
        "P219-W",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P219-V", "adr": 575, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "civilization",
        "capability": "CAP-PLT-CIV-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
