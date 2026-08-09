"""Civilization P219-O prosperity intelligence foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/568-enterprise-civilization-operating-system-prosperity.md",
    "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_PROSPERITY.md",
    "docs/architecture/civilization/CIVILIZATION_PROSPERITY_CAPABILITIES.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_PROSPERITY_ARCHITECTURE.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_PROSPERITY_DDD_CQRS.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_PROSPERITY_SECURITY.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_PROSPERITY_VALIDATION.v1.yaml",
    "docs/architecture/civilization/P219_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/civilization/domain/services/civ_platform_prosperity.py",
    "backend/contexts/civilization/domain/aggregates/civ_prosperity_aggregates.py",
    "backend/contexts/civilization/infrastructure/acl/civ_prosperity_acl.py",
    "backend/contexts/civilization/application/civ_prosperity_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/civilization_prosperity_intelligence_platform",
    "backend/contexts/global_quality_of_life_intelligence_bc",
    "backend/contexts/human_flourishing_platform_bc",
)


def validate_civ_prosperity_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.civilization.domain.aggregates.civ_prosperity_aggregates import (
        CivilizationProsperityIntelligencePlatformRoot,
        GlobalQualityOfLifeIntelligenceRoot,
        HumanFlourishingPlatformRoot,
        MeosCivilizationProsperityIntelligenceCoreRoot,
        OpportunityIntelligencePlatformRoot,
        ProsperityDigitalTwinRoot,
        ProsperityEventArchitectureRoot,
        ProsperityKnowledgeGraphRoot,
        ProsperityOptimizationEngineRoot,
    )
    from contexts.civilization.domain.services import civ_platform_prosperity as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P219-O" and cat["adr"] == 568 and cat["sor"] == "civilization"
        and cat["capability"] == "CAP-PLT-CIV-001"
        and cat["fabric"] == "meos_civilization_os_civilization_prosperity_intelligence_framework"
        and cat["foundation_gate"] == "P219" and cat["mission_gate"] == "P219-A"
        and cat["strategy_gate"] == "P219-B" and cat["domain_gate"] == "P219-C"
        and cat["planetary_gate"] == "P219-D" and cat["ai_os_gate"] == "P219-E"
        and cat["simulation_gate"] == "P219-F" and cat["resources_gate"] == "P219-G"
        and cat["economy_gate"] == "P219-H" and cat["knowledge_gate"] == "P219-I"
        and cat["human_gate"] == "P219-J" and cat["governance_gate"] == "P219-K"
        and cat["innovation_gate"] == "P219-L" and cat["security_gate"] == "P219-M"
        and cat["sustainability_gate"] == "P219-N"
        and cat["intelligence_nexus_gate"] == "P218-Z" and cat["space_gate"] == "P218"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["civilization_prosperity_intelligence_platform_present_required"] is True
        and cat["global_quality_of_life_intelligence_present_required"] is True
        and cat["human_flourishing_platform_present_required"] is True
        and cat["opportunity_intelligence_platform_present_required"] is True
        and cat["prosperity_optimization_engine_present_required"] is True
        and cat["prosperity_digital_twin_present_required"] is True
        and cat["meos_civilization_prosperity_intelligence_core_present_required"] is True
        and cat["prosperity_knowledge_graph_present_required"] is True
        and cat["prosperity_event_architecture_present_required"] is True
        and cat["prosperity_cqrs_model_present_required"] is True
        and cat["meos_prosperity_integration_map_present_required"] is True
        and cat["architecture"]["evolution_stage_count"] == 6
        and cat["architecture"]["layer_count"] == 6
        and cat["architecture"]["human_prosperity_domain_count"] == 10
        and cat["architecture"]["quality_of_life_dimension_count"] == 10
        and cat["architecture"]["flourishing_dimension_count"] == 10
        and cat["architecture"]["opportunity_domain_count"] == 8
        and cat["architecture"]["optimization_level_count"] == 7
        and cat["architecture"]["optimization_engine_step_count"] == 7
        and cat["agents"]["agent_count"] == 5
        and cat["knowledge_graph"]["entity_count"] == 11
        and cat["knowledge_graph"]["relationship_count"] == 8
        and cat["digital_twin"]["twin_count"] == 5
        and cat["bounded_contexts"]["context_count"] == 4
        and cat["aggregates"]["aggregate_count"] == 5
        and cat["events"]["core_event_count"] == 12
        and cat["cqrs"]["command_count"] == 6 and cat["cqrs"]["query_count"] == 5
        and cat["microservices"]["service_count"] == 10
        and cat["never_replace_p219_foundation"] is True
        and cat["never_replace_p219_n_sustainability"] is True
        and cat["never_replace_p219_h_economy"] is True
        and cat["never_replace_p219_j_human"] is True
        and cat["never_ungated_prosperity_optimization_execution"] is True
        and cat["never_treat_prosperity_score_as_binding_policy"] is True
        and cat["never_bypass_opportunity_equality_safeguards"] is True
        and cat["never_opaque_unexplainable_prosperity_decisions"] is True
        and cat["no_module_local_llm"] is True
        and cat["foundation_for_p219_p"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        CivilizationProsperityIntelligencePlatformRoot.enable(
            tenant_id="t1", prosperity_ref="p1"
        ).is_missing() is False,
        GlobalQualityOfLifeIntelligenceRoot.enable(tenant_id="t1", qol_ref="q1").is_missing() is False,
        HumanFlourishingPlatformRoot.enable(
            tenant_id="t1", flourishing_ref="f1"
        ).is_missing() is False,
        OpportunityIntelligencePlatformRoot.enable(
            tenant_id="t1", opportunity_ref="o1"
        ).is_missing() is False,
        ProsperityOptimizationEngineRoot.enable(
            tenant_id="t1", optimization_ref="opt1"
        ).is_missing() is False,
        ProsperityDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        MeosCivilizationProsperityIntelligenceCoreRoot.enable(
            tenant_id="t1", core_ref="core1"
        ).is_missing() is False,
        ProsperityKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="k1").is_missing() is False,
        ProsperityEventArchitectureRoot.enable(tenant_id="t1", events_ref="e1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/civilization/infrastructure/acl/civ_prosperity_acl.py").read_text(
        encoding="utf-8"
    )
    acl_ok = all(x in acl_text for x in (
        "via_p219", "via_p219_a", "via_p219_b", "via_p219_c", "via_p219_d", "via_p219_e",
        "via_p219_f", "via_p219_g", "via_p219_h", "via_p219_i", "via_p219_j", "via_p219_k",
        "via_p219_l", "via_p219_m", "via_p219_n",
        "via_policy_engine", "via_workflow", "via_audit",
        "via_p218_z", "via_p218", "via_p217", "via_p216_z", "via_p215_z", "via_p214_z",
        "via_core_platform", "via_identity",
        "never_replace_p219_foundation", "never_replace_p219_a_mission", "never_replace_p219_b_strategy",
        "never_replace_p219_c_domain", "never_replace_p219_d_planetary", "never_replace_p219_e_ai_os",
        "never_replace_p219_f_simulation", "never_replace_p219_g_resources", "never_replace_p219_h_economy",
        "never_replace_p219_i_knowledge", "never_replace_p219_j_human", "never_replace_p219_k_governance",
        "never_replace_p219_l_innovation", "never_replace_p219_m_security", "never_replace_p219_n_sustainability",
        "never_replace_policy_engine", "never_replace_workflow", "never_replace_audit",
        "never_replace_p218_z_intelligence_nexus", "never_replace_space",
        "never_merge_p218_t_space_civilization", "never_cross_context_aggregate_imports",
        "never_opaque_unexplainable_prosperity_decisions",
        "never_ungated_prosperity_optimization_execution",
        "never_treat_prosperity_score_as_binding_policy",
        "never_skip_ethical_prosperity_governance",
        "never_skip_human_authority_prosperity",
        "never_violate_human_sovereignty_prosperity",
        "never_bypass_trusted_prosperity_validation",
        "never_bypass_opportunity_equality_safeguards",
        "module_local_llm_forbidden",
        "module_local_civilization_prosperity_forbidden",
    ))
    router = (root / "backend/contexts/civilization/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@civilization_router.get("/prosperity")',
        "/prosperity/architecture", "/prosperity/quality-of-life", "/prosperity/flourishing",
        "/prosperity/opportunity", "/prosperity/optimization", "/prosperity/digital-twin",
        "/prosperity/knowledge-graph", "/prosperity/agents", "/prosperity/bounded-contexts",
        "/prosperity/aggregates", "/prosperity/events", "/prosperity/cqrs",
        "/prosperity/integration", "/prosperity/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_PROSPERITY.md").read_text(
        encoding="utf-8"
    )
    doc_ok = all(x in law for x in (
        "Never Civilization Prosperity Intelligence Platform is missing",
        "Never Global Quality of Life Intelligence is missing",
        "Never Human Flourishing Platform is missing",
        "Never Opportunity Intelligence Platform is missing",
        "Never Prosperity Optimization Engine is missing",
        "Never Prosperity Digital Twin is missing",
        "Never MEOS Civilization Prosperity Intelligence Core is missing",
        "Never Prosperity Knowledge Graph is missing",
        "Never Prosperity Event Architecture is missing",
        "Never Prosperity CQRS Model is missing",
        "Never MEOS Prosperity Integration Map is missing",
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
        "Never Opaque Unexplainable Prosperity Decisions",
        "Never Ungated Prosperity Optimization Execution",
        "Never Treat Prosperity Score As Binding Policy",
        "Never Skip Ethical Prosperity Governance",
        "Never Skip Human Authority Prosperity",
        "Never Violate Human Sovereignty Prosperity",
        "Never Bypass Trusted Prosperity Validation",
        "Never Bypass Opportunity Equality Safeguards",
        "continuously improving quality of life, opportunity, wellbeing and human",
        "P219-P",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P219-O", "adr": 568, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "civilization",
        "capability": "CAP-PLT-CIV-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
