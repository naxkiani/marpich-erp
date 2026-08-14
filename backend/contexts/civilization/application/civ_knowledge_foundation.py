"""Civilization P219-I knowledge civilization foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/562-enterprise-civilization-operating-system-knowledge.md",
    "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_KNOWLEDGE.md",
    "docs/architecture/civilization/CIVILIZATION_KNOWLEDGE_CAPABILITIES.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_KNOWLEDGE_ARCHITECTURE.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_KNOWLEDGE_DDD_CQRS.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_KNOWLEDGE_SECURITY.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_KNOWLEDGE_VALIDATION.v1.yaml",
    "docs/architecture/civilization/P219_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/civilization/domain/services/civ_platform_knowledge.py",
    "backend/contexts/civilization/domain/aggregates/civ_knowledge_aggregates.py",
    "backend/contexts/civilization/infrastructure/acl/civ_knowledge_acl.py",
    "backend/contexts/civilization/application/civ_knowledge_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/knowledge_civilization_platform",
    "backend/contexts/universal_knowledge_graph_bc",
    "backend/contexts/scientific_intelligence_network_bc",
)


def validate_civ_knowledge_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.civilization.domain.aggregates.civ_knowledge_aggregates import (
        CivilizationLearningFoundationRoot,
        CollectiveIntelligenceArchitectureRoot,
        KnowledgeDigitalTwinRoot,
        KnowledgeEventArchitectureRoot,
        KnowledgeReasoningEngineRoot,
        MeosKnowledgeCivilizationCoreRoot,
        MeosKnowledgeCivilizationPlatformRoot,
        ScientificIntelligenceNetworkRoot,
        UniversalKnowledgeGraphRoot,
    )
    from contexts.civilization.domain.services import civ_platform_knowledge as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P219-I" and cat["adr"] == 562 and cat["sor"] == "civilization"
        and cat["capability"] == "CAP-PLT-CIV-001"
        and cat["fabric"] == "meos_civilization_os_knowledge_civilization_framework"
        and cat["foundation_gate"] == "P219" and cat["mission_gate"] == "P219-A"
        and cat["strategy_gate"] == "P219-B" and cat["domain_gate"] == "P219-C"
        and cat["planetary_gate"] == "P219-D" and cat["ai_os_gate"] == "P219-E"
        and cat["simulation_gate"] == "P219-F" and cat["resources_gate"] == "P219-G"
        and cat["economy_gate"] == "P219-H"
        and cat["intelligence_nexus_gate"] == "P218-Z" and cat["space_gate"] == "P218"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["meos_knowledge_civilization_platform_present_required"] is True
        and cat["universal_knowledge_graph_present_required"] is True
        and cat["scientific_intelligence_network_present_required"] is True
        and cat["collective_intelligence_architecture_present_required"] is True
        and cat["knowledge_reasoning_engine_present_required"] is True
        and cat["civilization_learning_foundation_present_required"] is True
        and cat["meos_knowledge_civilization_core_present_required"] is True
        and cat["knowledge_digital_twin_present_required"] is True
        and cat["knowledge_event_architecture_present_required"] is True
        and cat["knowledge_cqrs_model_present_required"] is True
        and cat["meos_knowledge_integration_map_present_required"] is True
        and cat["architecture"]["evolution_stage_count"] == 6
        and cat["architecture"]["knowledge_domain_count"] == 10
        and cat["architecture"]["ukg_layer_count"] == 4
        and cat["architecture"]["entity_type_count"] == 11
        and cat["architecture"]["relationship_count"] == 9
        and cat["scientific"]["domain_count"] == 8
        and cat["scientific"]["agent_count"] == 4
        and cat["learning"]["agent_count"] == 4
        and cat["agents"]["agent_count"] == 8
        and cat["collective"]["component_count"] == 5
        and cat["bounded_contexts"]["context_count"] == 4
        and cat["aggregates"]["aggregate_count"] == 5
        and cat["events"]["core_event_count"] == 13
        and cat["cqrs"]["command_count"] == 6 and cat["cqrs"]["query_count"] == 5
        and cat["microservices"]["service_count"] == 10
        and cat["never_replace_p219_foundation"] is True
        and cat["never_replace_p219_h_economy"] is True
        and cat["never_replace_enterprise_search"] is True
        and cat["never_replace_document_exchange"] is True
        and cat["never_ungated_knowledge_publication"] is True
        and cat["never_bypass_trusted_knowledge_validation"] is True
        and cat["never_opaque_unexplainable_knowledge_decisions"] is True
        and cat["no_module_local_llm"] is True
        and cat["foundation_for_p219_j"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        MeosKnowledgeCivilizationPlatformRoot.enable(tenant_id="t1", knowledge_ref="k1").is_missing() is False,
        UniversalKnowledgeGraphRoot.enable(tenant_id="t1", ukg_ref="u1").is_missing() is False,
        ScientificIntelligenceNetworkRoot.enable(tenant_id="t1", scientific_ref="s1").is_missing() is False,
        CollectiveIntelligenceArchitectureRoot.enable(tenant_id="t1", collective_ref="c1").is_missing() is False,
        KnowledgeReasoningEngineRoot.enable(tenant_id="t1", reasoning_ref="r1").is_missing() is False,
        CivilizationLearningFoundationRoot.enable(tenant_id="t1", learning_ref="l1").is_missing() is False,
        MeosKnowledgeCivilizationCoreRoot.enable(tenant_id="t1", core_ref="core1").is_missing() is False,
        KnowledgeDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        KnowledgeEventArchitectureRoot.enable(tenant_id="t1", events_ref="e1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/civilization/infrastructure/acl/civ_knowledge_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p219", "via_p219_a", "via_p219_b", "via_p219_c", "via_p219_d", "via_p219_e",
        "via_p219_f", "via_p219_g", "via_p219_h", "via_enterprise_search", "via_document_exchange",
        "via_p218_z", "via_p218", "via_p217", "via_p216_z", "via_p215_z", "via_p214_z",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p219_foundation", "never_replace_p219_a_mission", "never_replace_p219_b_strategy",
        "never_replace_p219_c_domain", "never_replace_p219_d_planetary", "never_replace_p219_e_ai_os",
        "never_replace_p219_f_simulation", "never_replace_p219_g_resources", "never_replace_p219_h_economy",
        "never_replace_enterprise_search", "never_replace_document_exchange",
        "never_replace_p218_z_intelligence_nexus", "never_replace_space",
        "never_merge_p218_t_space_civilization", "never_cross_context_aggregate_imports",
        "never_opaque_unexplainable_knowledge_decisions",
        "never_ungated_knowledge_publication",
        "never_skip_human_authority_knowledge",
        "never_skip_ethical_knowledge_governance",
        "never_violate_human_sovereignty_knowledge",
        "never_bypass_trusted_knowledge_validation",
        "module_local_llm_forbidden",
        "module_local_knowledge_civilization_forbidden",
    ))
    router = (root / "backend/contexts/civilization/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@civilization_router.get("/knowledge")',
        "/knowledge/architecture", "/knowledge/graph", "/knowledge/scientific",
        "/knowledge/collective", "/knowledge/learning", "/knowledge/reasoning",
        "/knowledge/digital-twin", "/knowledge/agents", "/knowledge/bounded-contexts",
        "/knowledge/aggregates", "/knowledge/events", "/knowledge/cqrs",
        "/knowledge/integration", "/knowledge/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_KNOWLEDGE.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never MEOS Knowledge Civilization Platform is missing",
        "Never Universal Knowledge Graph is missing",
        "Never Scientific Intelligence Network is missing",
        "Never Collective Intelligence Architecture is missing",
        "Never Knowledge Reasoning Engine is missing",
        "Never Civilization Learning Foundation is missing",
        "Never MEOS Knowledge Civilization Core is missing",
        "Never Knowledge Digital Twin is missing",
        "Never Knowledge Event Architecture is missing",
        "Never Knowledge CQRS Model is missing",
        "Never MEOS Knowledge Integration Map is missing",
        "Never Replace P219 Foundation",
        "Never Replace P219-A Mission",
        "Never Replace P219-B Strategy",
        "Never Replace P219-C Domain",
        "Never Replace P219-D Planetary",
        "Never Replace P219-E AI OS",
        "Never Replace P219-F Simulation",
        "Never Replace P219-G Resources",
        "Never Replace P219-H Economy",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace Enterprise Search",
        "Never Replace Document Exchange",
        "Never Replace P215-Z Quantum",
        "Never Replace P216-Z Robotics",
        "Never Replace P217 Biotechnology",
        "Never Replace P218 Space",
        "Never Replace P218-Z Intelligence Nexus",
        "Never Merge P218-T Space Civilization Phase",
        "Never Module-Local LLM",
        "Never Cross-Context Aggregate Imports",
        "Never Opaque Unexplainable Knowledge Decisions",
        "Never Ungated Knowledge Publication",
        "Never Skip Human Authority Knowledge",
        "Never Skip Ethical Knowledge Governance",
        "Never Violate Human Sovereignty Knowledge",
        "Never Bypass Trusted Knowledge Validation",
        "preserving, connecting, understanding and expanding humanity's collective",
        "P219-J",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P219-I", "adr": 562, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "civilization",
        "capability": "CAP-PLT-CIV-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
