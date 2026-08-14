"""Civilization P219-J human civilization intelligence foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/563-enterprise-civilization-operating-system-human.md",
    "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_HUMAN.md",
    "docs/architecture/civilization/CIVILIZATION_HUMAN_CAPABILITIES.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_HUMAN_ARCHITECTURE.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_HUMAN_DDD_CQRS.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_HUMAN_SECURITY.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_HUMAN_VALIDATION.v1.yaml",
    "docs/architecture/civilization/P219_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/civilization/domain/services/civ_platform_human.py",
    "backend/contexts/civilization/domain/aggregates/civ_human_aggregates.py",
    "backend/contexts/civilization/infrastructure/acl/civ_human_acl.py",
    "backend/contexts/civilization/application/civ_human_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/human_civilization_intelligence_platform",
    "backend/contexts/human_digital_twin_bc",
    "backend/contexts/workforce_intelligence_bc",
)


def validate_civ_human_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.civilization.domain.aggregates.civ_human_aggregates import (
        HumanCapabilityIntelligenceRoot,
        HumanDevelopmentIntelligenceRoot,
        HumanDigitalTwinPlatformRoot,
        HumanEventArchitectureRoot,
        HumanIntelligencePlatformRoot,
        HumanKnowledgeGraphRoot,
        HumanWellbeingIntelligenceRoot,
        MeosHumanCivilizationIntelligenceCoreRoot,
        WorkforceIntelligenceRoot,
    )
    from contexts.civilization.domain.services import civ_platform_human as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P219-J" and cat["adr"] == 563 and cat["sor"] == "civilization"
        and cat["capability"] == "CAP-PLT-CIV-001"
        and cat["fabric"] == "meos_civilization_os_human_civilization_intelligence_framework"
        and cat["foundation_gate"] == "P219" and cat["mission_gate"] == "P219-A"
        and cat["strategy_gate"] == "P219-B" and cat["domain_gate"] == "P219-C"
        and cat["planetary_gate"] == "P219-D" and cat["ai_os_gate"] == "P219-E"
        and cat["simulation_gate"] == "P219-F" and cat["resources_gate"] == "P219-G"
        and cat["economy_gate"] == "P219-H" and cat["knowledge_gate"] == "P219-I"
        and cat["intelligence_nexus_gate"] == "P218-Z" and cat["space_gate"] == "P218"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["human_intelligence_platform_present_required"] is True
        and cat["human_digital_twin_platform_present_required"] is True
        and cat["human_development_intelligence_present_required"] is True
        and cat["workforce_intelligence_present_required"] is True
        and cat["human_capability_intelligence_present_required"] is True
        and cat["human_knowledge_graph_present_required"] is True
        and cat["meos_human_civilization_intelligence_core_present_required"] is True
        and cat["human_wellbeing_intelligence_present_required"] is True
        and cat["human_event_architecture_present_required"] is True
        and cat["human_cqrs_model_present_required"] is True
        and cat["meos_human_integration_map_present_required"] is True
        and cat["architecture"]["evolution_stage_count"] == 6
        and cat["architecture"]["human_domain_count"] == 9
        and cat["architecture"]["twin_component_count"] == 8
        and cat["architecture"]["capability_domain_count"] == 10
        and cat["architecture"]["development_dimension_count"] == 8
        and cat["architecture"]["wellbeing_dimension_count"] == 6
        and cat["workforce"]["agent_count"] == 4
        and cat["agents"]["agent_count"] == 4
        and cat["knowledge_graph"]["entity_count"] == 10
        and cat["knowledge_graph"]["relationship_count"] == 8
        and cat["bounded_contexts"]["context_count"] == 4
        and cat["aggregates"]["aggregate_count"] == 5
        and cat["events"]["core_event_count"] == 11
        and cat["cqrs"]["command_count"] == 6 and cat["cqrs"]["query_count"] == 5
        and cat["microservices"]["service_count"] == 10
        and cat["never_replace_p219_foundation"] is True
        and cat["never_replace_p219_i_knowledge"] is True
        and cat["never_replace_identity"] is True
        and cat["never_violate_privacy_by_design"] is True
        and cat["never_ungated_human_profile_mutation"] is True
        and cat["never_bypass_trusted_human_twin_validation"] is True
        and cat["never_opaque_unexplainable_human_decisions"] is True
        and cat["no_module_local_llm"] is True
        and cat["foundation_for_p219_k"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        HumanIntelligencePlatformRoot.enable(tenant_id="t1", human_ref="h1").is_missing() is False,
        HumanDigitalTwinPlatformRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        HumanDevelopmentIntelligenceRoot.enable(tenant_id="t1", development_ref="d1").is_missing() is False,
        WorkforceIntelligenceRoot.enable(tenant_id="t1", workforce_ref="w1").is_missing() is False,
        HumanCapabilityIntelligenceRoot.enable(tenant_id="t1", capability_ref="c1").is_missing() is False,
        HumanKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="k1").is_missing() is False,
        MeosHumanCivilizationIntelligenceCoreRoot.enable(tenant_id="t1", core_ref="core1").is_missing() is False,
        HumanWellbeingIntelligenceRoot.enable(tenant_id="t1", wellbeing_ref="wb1").is_missing() is False,
        HumanEventArchitectureRoot.enable(tenant_id="t1", events_ref="e1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/civilization/infrastructure/acl/civ_human_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p219", "via_p219_a", "via_p219_b", "via_p219_c", "via_p219_d", "via_p219_e",
        "via_p219_f", "via_p219_g", "via_p219_h", "via_p219_i", "via_identity",
        "via_p218_z", "via_p218", "via_p217", "via_p216_z", "via_p215_z", "via_p214_z",
        "via_policy_engine", "via_workflow", "via_audit", "via_core_platform",
        "never_replace_p219_foundation", "never_replace_p219_a_mission", "never_replace_p219_b_strategy",
        "never_replace_p219_c_domain", "never_replace_p219_d_planetary", "never_replace_p219_e_ai_os",
        "never_replace_p219_f_simulation", "never_replace_p219_g_resources", "never_replace_p219_h_economy",
        "never_replace_p219_i_knowledge", "never_replace_identity",
        "never_replace_p218_z_intelligence_nexus", "never_replace_space",
        "never_merge_p218_t_space_civilization", "never_cross_context_aggregate_imports",
        "never_opaque_unexplainable_human_decisions",
        "never_ungated_human_profile_mutation",
        "never_skip_human_authority",
        "never_skip_ethical_human_governance",
        "never_violate_human_sovereignty",
        "never_violate_privacy_by_design",
        "never_bypass_trusted_human_twin_validation",
        "module_local_llm_forbidden",
        "module_local_human_civilization_forbidden",
    ))
    router = (root / "backend/contexts/civilization/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@civilization_router.get("/human")',
        "/human/architecture", "/human/digital-twin", "/human/capability",
        "/human/development", "/human/workforce", "/human/wellbeing",
        "/human/knowledge-graph", "/human/agents", "/human/bounded-contexts",
        "/human/aggregates", "/human/events", "/human/cqrs",
        "/human/integration", "/human/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_HUMAN.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Human Intelligence Platform is missing",
        "Never Human Digital Twin Platform is missing",
        "Never Human Development Intelligence is missing",
        "Never Workforce Intelligence is missing",
        "Never Human Capability Intelligence is missing",
        "Never Human Knowledge Graph is missing",
        "Never MEOS Human Civilization Intelligence Core is missing",
        "Never Human Wellbeing Intelligence is missing",
        "Never Human Event Architecture is missing",
        "Never Human CQRS Model is missing",
        "Never MEOS Human Integration Map is missing",
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
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace Identity",
        "Never Replace P215-Z Quantum",
        "Never Replace P216-Z Robotics",
        "Never Replace P217 Biotechnology",
        "Never Replace P218 Space",
        "Never Replace P218-Z Intelligence Nexus",
        "Never Merge P218-T Space Civilization Phase",
        "Never Module-Local LLM",
        "Never Cross-Context Aggregate Imports",
        "Never Opaque Unexplainable Human Decisions",
        "Never Ungated Human Profile Mutation",
        "Never Skip Human Authority",
        "Never Skip Ethical Human Governance",
        "Never Violate Human Sovereignty",
        "Never Violate Privacy By Design",
        "Never Bypass Trusted Human Twin Validation",
        "understanding, modeling and continuously improving human capabilities",
        "P219-K",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P219-J", "adr": 563, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "civilization",
        "capability": "CAP-PLT-CIV-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
