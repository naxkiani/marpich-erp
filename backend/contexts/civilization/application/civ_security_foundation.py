"""Civilization P219-M security intelligence foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/566-enterprise-civilization-operating-system-security.md",
    "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_SECURITY.md",
    "docs/architecture/civilization/CIVILIZATION_SECURITY_CAPABILITIES.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_SECURITY_ARCHITECTURE.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_SECURITY_DDD_CQRS.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_SECURITY_SECURITY.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_SECURITY_VALIDATION.v1.yaml",
    "docs/architecture/civilization/P219_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/civilization/domain/services/civ_platform_security.py",
    "backend/contexts/civilization/domain/aggregates/civ_security_aggregates.py",
    "backend/contexts/civilization/infrastructure/acl/civ_security_acl.py",
    "backend/contexts/civilization/application/civ_security_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/civilization_security_intelligence_platform",
    "backend/contexts/global_risk_intelligence_bc",
    "backend/contexts/adaptive_security_architecture_bc",
)


def validate_civ_security_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.civilization.domain.aggregates.civ_security_aggregates import (
        AdaptiveSecurityArchitectureRoot,
        CivilizationResiliencePlatformRoot,
        CivilizationSecurityIntelligencePlatformRoot,
        GlobalRiskIntelligencePlatformRoot,
        MeosCivilizationSecurityIntelligenceCoreRoot,
        SecurityDigitalTwinRoot,
        SecurityEventArchitectureRoot,
        SecurityKnowledgeGraphRoot,
        ThreatIntelligenceNetworkRoot,
    )
    from contexts.civilization.domain.services import civ_platform_security as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P219-M" and cat["adr"] == 566 and cat["sor"] == "civilization"
        and cat["capability"] == "CAP-PLT-CIV-001"
        and cat["fabric"] == "meos_civilization_os_civilization_security_intelligence_framework"
        and cat["foundation_gate"] == "P219" and cat["mission_gate"] == "P219-A"
        and cat["strategy_gate"] == "P219-B" and cat["domain_gate"] == "P219-C"
        and cat["planetary_gate"] == "P219-D" and cat["ai_os_gate"] == "P219-E"
        and cat["simulation_gate"] == "P219-F" and cat["resources_gate"] == "P219-G"
        and cat["economy_gate"] == "P219-H" and cat["knowledge_gate"] == "P219-I"
        and cat["human_gate"] == "P219-J" and cat["governance_gate"] == "P219-K"
        and cat["innovation_gate"] == "P219-L"
        and cat["intelligence_nexus_gate"] == "P218-Z" and cat["space_gate"] == "P218"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["civilization_security_intelligence_platform_present_required"] is True
        and cat["global_risk_intelligence_platform_present_required"] is True
        and cat["threat_intelligence_network_present_required"] is True
        and cat["adaptive_security_architecture_present_required"] is True
        and cat["civilization_resilience_platform_present_required"] is True
        and cat["security_digital_twin_present_required"] is True
        and cat["meos_civilization_security_intelligence_core_present_required"] is True
        and cat["security_knowledge_graph_present_required"] is True
        and cat["security_event_architecture_present_required"] is True
        and cat["security_cqrs_model_present_required"] is True
        and cat["meos_security_integration_map_present_required"] is True
        and cat["architecture"]["evolution_stage_count"] == 6
        and cat["architecture"]["layer_count"] == 6
        and cat["architecture"]["risk_domain_count"] == 10
        and cat["architecture"]["threat_category_count"] == 8
        and cat["architecture"]["resilience_domain_count"] == 9
        and cat["architecture"]["resilience_lifecycle_step_count"] == 7
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
        and cat["never_replace_p219_l_innovation"] is True
        and cat["never_replace_identity"] is True
        and cat["never_ungated_autonomous_security_response"] is True
        and cat["never_bypass_zero_trust_controls"] is True
        and cat["never_opaque_unexplainable_security_decisions"] is True
        and cat["no_module_local_llm"] is True
        and cat["foundation_for_p219_n"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        CivilizationSecurityIntelligencePlatformRoot.enable(tenant_id="t1", security_ref="s1").is_missing() is False,
        GlobalRiskIntelligencePlatformRoot.enable(tenant_id="t1", risk_ref="r1").is_missing() is False,
        ThreatIntelligenceNetworkRoot.enable(tenant_id="t1", threat_ref="th1").is_missing() is False,
        AdaptiveSecurityArchitectureRoot.enable(tenant_id="t1", adaptive_ref="a1").is_missing() is False,
        CivilizationResiliencePlatformRoot.enable(tenant_id="t1", resilience_ref="res1").is_missing() is False,
        SecurityDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        MeosCivilizationSecurityIntelligenceCoreRoot.enable(tenant_id="t1", core_ref="core1").is_missing() is False,
        SecurityKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="k1").is_missing() is False,
        SecurityEventArchitectureRoot.enable(tenant_id="t1", events_ref="e1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/civilization/infrastructure/acl/civ_security_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p219", "via_p219_a", "via_p219_b", "via_p219_c", "via_p219_d", "via_p219_e",
        "via_p219_f", "via_p219_g", "via_p219_h", "via_p219_i", "via_p219_j", "via_p219_k", "via_p219_l",
        "via_identity", "via_policy_engine", "via_workflow", "via_audit",
        "via_p218_z", "via_p218", "via_p217", "via_p216_z", "via_p215_z", "via_p214_z",
        "via_core_platform",
        "never_replace_p219_foundation", "never_replace_p219_a_mission", "never_replace_p219_b_strategy",
        "never_replace_p219_c_domain", "never_replace_p219_d_planetary", "never_replace_p219_e_ai_os",
        "never_replace_p219_f_simulation", "never_replace_p219_g_resources", "never_replace_p219_h_economy",
        "never_replace_p219_i_knowledge", "never_replace_p219_j_human", "never_replace_p219_k_governance",
        "never_replace_p219_l_innovation", "never_replace_identity",
        "never_replace_policy_engine", "never_replace_workflow", "never_replace_audit",
        "never_replace_p218_z_intelligence_nexus", "never_replace_space",
        "never_merge_p218_t_space_civilization", "never_cross_context_aggregate_imports",
        "never_opaque_unexplainable_security_decisions",
        "never_ungated_autonomous_security_response",
        "never_skip_human_authority_security",
        "never_skip_ethical_security_governance",
        "never_violate_human_sovereignty_security",
        "never_bypass_trusted_security_validation",
        "never_bypass_zero_trust_controls",
        "module_local_llm_forbidden",
        "module_local_civilization_security_forbidden",
    ))
    router = (root / "backend/contexts/civilization/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@civilization_router.get("/security")',
        "/security/architecture", "/security/risk", "/security/threat",
        "/security/resilience", "/security/adaptive", "/security/digital-twin",
        "/security/knowledge-graph", "/security/agents", "/security/bounded-contexts",
        "/security/aggregates", "/security/events", "/security/cqrs",
        "/security/integration", "/security/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_SECURITY.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Civilization Security Intelligence Platform is missing",
        "Never Global Risk Intelligence Platform is missing",
        "Never Threat Intelligence Network is missing",
        "Never Adaptive Security Architecture is missing",
        "Never Civilization Resilience Platform is missing",
        "Never Security Digital Twin is missing",
        "Never MEOS Civilization Security Intelligence Core is missing",
        "Never Security Knowledge Graph is missing",
        "Never Security Event Architecture is missing",
        "Never Security CQRS Model is missing",
        "Never MEOS Security Integration Map is missing",
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
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace Identity",
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
        "Never Opaque Unexplainable Security Decisions",
        "Never Ungated Autonomous Security Response",
        "Never Skip Human Authority Security",
        "Never Skip Ethical Security Governance",
        "Never Violate Human Sovereignty Security",
        "Never Bypass Trusted Security Validation",
        "Never Bypass Zero Trust Controls",
        "protecting planetary infrastructure, human civilization, critical knowledge",
        "P219-N",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P219-M", "adr": 566, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "civilization",
        "capability": "CAP-PLT-CIV-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
