"""Civilization P219-L innovation intelligence foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/565-enterprise-civilization-operating-system-innovation.md",
    "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_INNOVATION.md",
    "docs/architecture/civilization/CIVILIZATION_INNOVATION_CAPABILITIES.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_INNOVATION_ARCHITECTURE.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_INNOVATION_DDD_CQRS.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_INNOVATION_SECURITY.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_INNOVATION_VALIDATION.v1.yaml",
    "docs/architecture/civilization/P219_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/civilization/domain/services/civ_platform_innovation.py",
    "backend/contexts/civilization/domain/aggregates/civ_innovation_aggregates.py",
    "backend/contexts/civilization/infrastructure/acl/civ_innovation_acl.py",
    "backend/contexts/civilization/application/civ_innovation_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/civilization_innovation_intelligence_platform",
    "backend/contexts/global_innovation_network_bc",
    "backend/contexts/technology_evolution_platform_bc",
)


def validate_civ_innovation_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.civilization.domain.aggregates.civ_innovation_aggregates import (
        CivilizationInnovationIntelligencePlatformRoot,
        GlobalInnovationNetworkRoot,
        InnovationDigitalTwinRoot,
        InnovationEventArchitectureRoot,
        InnovationKnowledgeGraphRoot,
        InnovationPortfolioIntelligenceRoot,
        MeosCivilizationInnovationIntelligenceCoreRoot,
        ResearchIntelligencePlatformRoot,
        TechnologyEvolutionPlatformRoot,
    )
    from contexts.civilization.domain.services import civ_platform_innovation as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P219-L" and cat["adr"] == 565 and cat["sor"] == "civilization"
        and cat["capability"] == "CAP-PLT-CIV-001"
        and cat["fabric"] == "meos_civilization_os_civilization_innovation_intelligence_framework"
        and cat["foundation_gate"] == "P219" and cat["mission_gate"] == "P219-A"
        and cat["strategy_gate"] == "P219-B" and cat["domain_gate"] == "P219-C"
        and cat["planetary_gate"] == "P219-D" and cat["ai_os_gate"] == "P219-E"
        and cat["simulation_gate"] == "P219-F" and cat["resources_gate"] == "P219-G"
        and cat["economy_gate"] == "P219-H" and cat["knowledge_gate"] == "P219-I"
        and cat["human_gate"] == "P219-J" and cat["governance_gate"] == "P219-K"
        and cat["intelligence_nexus_gate"] == "P218-Z" and cat["space_gate"] == "P218"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["civilization_innovation_intelligence_platform_present_required"] is True
        and cat["global_innovation_network_present_required"] is True
        and cat["technology_evolution_platform_present_required"] is True
        and cat["research_intelligence_platform_present_required"] is True
        and cat["innovation_portfolio_intelligence_present_required"] is True
        and cat["innovation_digital_twin_present_required"] is True
        and cat["meos_civilization_innovation_intelligence_core_present_required"] is True
        and cat["innovation_knowledge_graph_present_required"] is True
        and cat["innovation_event_architecture_present_required"] is True
        and cat["innovation_cqrs_model_present_required"] is True
        and cat["meos_innovation_integration_map_present_required"] is True
        and cat["architecture"]["evolution_stage_count"] == 6
        and cat["architecture"]["layer_count"] == 6
        and cat["architecture"]["network_domain_count"] == 8
        and cat["architecture"]["research_lifecycle_step_count"] == 8
        and cat["architecture"]["technology_domain_count"] == 10
        and cat["architecture"]["portfolio_type_count"] == 5
        and cat["agents"]["agent_count"] == 5
        and cat["knowledge_graph"]["entity_count"] == 10
        and cat["knowledge_graph"]["relationship_count"] == 8
        and cat["digital_twin"]["twin_count"] == 5
        and cat["bounded_contexts"]["context_count"] == 4
        and cat["aggregates"]["aggregate_count"] == 5
        and cat["events"]["core_event_count"] == 14
        and cat["cqrs"]["command_count"] == 6 and cat["cqrs"]["query_count"] == 6
        and cat["microservices"]["service_count"] == 10
        and cat["never_replace_p219_foundation"] is True
        and cat["never_replace_p219_k_governance"] is True
        and cat["never_ungated_innovation_commercialization"] is True
        and cat["never_skip_responsible_innovation_governance"] is True
        and cat["never_opaque_unexplainable_innovation_decisions"] is True
        and cat["no_module_local_llm"] is True
        and cat["foundation_for_p219_m"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        CivilizationInnovationIntelligencePlatformRoot.enable(tenant_id="t1", innovation_ref="i1").is_missing() is False,
        GlobalInnovationNetworkRoot.enable(tenant_id="t1", network_ref="n1").is_missing() is False,
        TechnologyEvolutionPlatformRoot.enable(tenant_id="t1", technology_ref="t1").is_missing() is False,
        ResearchIntelligencePlatformRoot.enable(tenant_id="t1", research_ref="r1").is_missing() is False,
        InnovationPortfolioIntelligenceRoot.enable(tenant_id="t1", portfolio_ref="p1").is_missing() is False,
        InnovationDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        MeosCivilizationInnovationIntelligenceCoreRoot.enable(tenant_id="t1", core_ref="core1").is_missing() is False,
        InnovationKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="k1").is_missing() is False,
        InnovationEventArchitectureRoot.enable(tenant_id="t1", events_ref="e1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/civilization/infrastructure/acl/civ_innovation_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p219", "via_p219_a", "via_p219_b", "via_p219_c", "via_p219_d", "via_p219_e",
        "via_p219_f", "via_p219_g", "via_p219_h", "via_p219_i", "via_p219_j", "via_p219_k",
        "via_policy_engine", "via_workflow", "via_audit",
        "via_p218_z", "via_p218", "via_p217", "via_p216_z", "via_p215_z", "via_p214_z",
        "via_identity", "via_core_platform",
        "never_replace_p219_foundation", "never_replace_p219_a_mission", "never_replace_p219_b_strategy",
        "never_replace_p219_c_domain", "never_replace_p219_d_planetary", "never_replace_p219_e_ai_os",
        "never_replace_p219_f_simulation", "never_replace_p219_g_resources", "never_replace_p219_h_economy",
        "never_replace_p219_i_knowledge", "never_replace_p219_j_human", "never_replace_p219_k_governance",
        "never_replace_policy_engine", "never_replace_workflow", "never_replace_audit",
        "never_replace_p218_z_intelligence_nexus", "never_replace_space",
        "never_merge_p218_t_space_civilization", "never_cross_context_aggregate_imports",
        "never_opaque_unexplainable_innovation_decisions",
        "never_ungated_innovation_commercialization",
        "never_skip_responsible_innovation_governance",
        "never_skip_human_authority_innovation",
        "never_skip_ethical_innovation",
        "never_violate_human_sovereignty_innovation",
        "never_bypass_trusted_innovation_validation",
        "module_local_llm_forbidden",
        "module_local_civilization_innovation_forbidden",
    ))
    router = (root / "backend/contexts/civilization/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@civilization_router.get("/innovation")',
        "/innovation/architecture", "/innovation/network", "/innovation/research",
        "/innovation/technology", "/innovation/portfolio", "/innovation/digital-twin",
        "/innovation/knowledge-graph", "/innovation/agents", "/innovation/bounded-contexts",
        "/innovation/aggregates", "/innovation/events", "/innovation/cqrs",
        "/innovation/integration", "/innovation/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_INNOVATION.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Civilization Innovation Intelligence Platform is missing",
        "Never Global Innovation Network is missing",
        "Never Technology Evolution Platform is missing",
        "Never Research Intelligence Platform is missing",
        "Never Innovation Portfolio Intelligence is missing",
        "Never Innovation Digital Twin is missing",
        "Never MEOS Civilization Innovation Intelligence Core is missing",
        "Never Innovation Knowledge Graph is missing",
        "Never Innovation Event Architecture is missing",
        "Never Innovation CQRS Model is missing",
        "Never MEOS Innovation Integration Map is missing",
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
        "Never Opaque Unexplainable Innovation Decisions",
        "Never Ungated Innovation Commercialization",
        "Never Skip Responsible Innovation Governance",
        "Never Skip Human Authority Innovation",
        "Never Skip Ethical Innovation",
        "Never Violate Human Sovereignty Innovation",
        "Never Bypass Trusted Innovation Validation",
        "discovering, connecting, evaluating and accelerating scientific",
        "P219-M",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P219-L", "adr": 565, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "civilization",
        "capability": "CAP-PLT-CIV-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
