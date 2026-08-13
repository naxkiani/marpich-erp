"""Biotechnology P217-S Bio Security foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/518-enterprise-biotechnology-bio-security.md",
    "docs/architecture/ENTERPRISE_BIOTECHNOLOGY_BIO_SECURITY.md",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_SECURITY_ARCHITECTURE.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_SECURITY_MODELS.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_SECURITY_DDD_CQRS.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_SECURITY_SECURITY.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_SECURITY_VALIDATION.v1.yaml",
    "docs/architecture/biotechnology/P217_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/biotechnology/domain/services/bio_platform_bio_security.py",
    "backend/contexts/biotechnology/domain/aggregates/bio_bio_security_aggregates.py",
    "backend/contexts/biotechnology/infrastructure/acl/bio_bio_security_acl.py",
    "backend/contexts/biotechnology/application/bio_bio_security_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/bio_security_platform",
    "backend/contexts/bio_cybersecurity_platform",
    "backend/contexts/biological_risk_intelligence_platform",
)
def validate_bio_security_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.biotechnology.domain.aggregates.bio_bio_security_aggregates import (
        BioSecurityPlatformRoot, BioCybersecurityRoot, BiologicalRiskRoot,
        ThreatIntelligenceRoot, ResilienceArchitectureRoot, SecurityKnowledgeGraphRoot,
        SecurityDigitalTwinRoot, SecurityAgentsRoot, BioSecurityGovernanceRoot,
        BioSecuritySecurityRoot,
    )
    from contexts.biotechnology.domain.services import bio_platform_bio_security as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P217-S" and cat["adr"] == 518 and cat["sor"] == "biotechnology"
        and cat["capability"] == "CAP-PLT-BIO-001"
        and cat["fabric"] == "meos_bio_security_intelligence_fabric"
        and cat["foundation_gate"] == "P217" and cat["mission_gate"] == "P217-A"
        and cat["strategy_gate"] == "P217-B" and cat["domain_gate"] == "P217-C"
        and cat["infrastructure_gate"] == "P217-D" and cat["bio_ai_gate"] == "P217-E"
        and cat["synthetic_gate"] == "P217-F" and cat["simulation_gate"] == "P217-G"
        and cat["digital_health_gate"] == "P217-H" and cat["precision_medicine_gate"] == "P217-I"
        and cat["clinical_research_gate"] == "P217-J" and cat["drug_discovery_gate"] == "P217-K"
        and cat["bio_manufacturing_gate"] == "P217-L" and cat["bio_supply_chain_gate"] == "P217-M"
        and cat["bio_regulatory_gate"] == "P217-N" and cat["bio_sustainability_gate"] == "P217-O"
        and cat["bio_marketplace_gate"] == "P217-P" and cat["bio_innovation_gate"] == "P217-Q"
        and cat["bio_investment_gate"] == "P217-R"
        and cat["robotics_gate"] == "P216-Z" and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["bio_security_platform_present_required"] is True
        and cat["bio_cybersecurity_present_required"] is True
        and cat["biological_risk_intelligence_present_required"] is True
        and cat["threat_intelligence_present_required"] is True
        and cat["resilience_architecture_present_required"] is True
        and cat["security_knowledge_graph_present_required"] is True
        and cat["security_digital_twin_present_required"] is True
        and cat["ai_agents_present_required"] is True
        and cat["quantum_readiness_present_required"] is True
        and cat["governance_present_required"] is True
        and cat["security_architecture_present_required"] is True
        and cat["meos_integration_present_required"] is True
        and cat["architecture"]["layer_count"] == 6
        and cat["bio_cybersecurity"]["domain_count"] == 4
        and cat["biological_risk"]["engine_count"] == 3
        and cat["threat_intelligence"]["source_count"] == 5
        and cat["security_agents"]["agent_count"] == 6
        and cat["domain_models"]["domain_count"] == 3
        and cat["bounded_contexts"]["context_count"] == 7
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 8
        and cat["never_replace_p217_foundation"] is True
        and cat["never_replace_p217_r_bio_investment"] is True
        and cat["never_replace_identity_platform"] is True
        and cat["never_replace_audit_platform"] is True
        and cat["never_replace_hospital_emr"] is True
        and cat["bio_ai_via_p214z_acl_only"] is True
        and cat["security_twins_via_p217g_acl_only"] is True
        and cat["compliance_intelligence_via_p217n_acl_only"] is True
        and cat["environmental_security_via_p217o_acl_only"] is True
        and cat["commerce_security_via_p217p_acl_only"] is True
        and cat["research_protection_via_p217q_acl_only"] is True
        and cat["financial_security_via_p217r_acl_only"] is True
        and cat["robotics_via_p216z_acl_only"] is True
        and cat["quantum_optimization_via_p215z_acl_only"] is True
        and cat["no_module_local_llm"] is True
        and cat["never_opaque_unexplainable_decisions"] is True
        and cat["never_skip_human_security_oversight"] is True
        and cat["never_autonomous_defense_without_approval"] is True
        and cat["never_skip_zero_trust_controls"] is True
        and cat["opaque_bio_safety_strategy_forbidden"] is True
        and cat["foundation_for_p217_t"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        BioSecurityPlatformRoot.enable(tenant_id="t1", platform_ref="p1").is_missing() is False,
        BioCybersecurityRoot.enable(tenant_id="t1", cybersecurity_ref="c1").is_missing() is False,
        BiologicalRiskRoot.enable(tenant_id="t1", risk_ref="r1").is_missing() is False,
        ThreatIntelligenceRoot.enable(tenant_id="t1", threat_ref="t1").is_missing() is False,
        ResilienceArchitectureRoot.enable(tenant_id="t1", resilience_ref="res1").is_missing() is False,
        SecurityKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="k1").is_missing() is False,
        SecurityDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        SecurityAgentsRoot.enable(tenant_id="t1", agents_ref="ag1").is_missing() is False,
        BioSecurityGovernanceRoot.enable(tenant_id="t1", governance_ref="gov1").is_missing() is False,
        BioSecuritySecurityRoot.enable(tenant_id="t1", security_ref="s1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/biotechnology/infrastructure/acl/bio_bio_security_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p217", "via_p217_a", "via_p217_b", "via_p217_c", "via_p217_d", "via_p217_e", "via_p217_f",
        "via_p217_g", "via_p217_h", "via_p217_i", "via_p217_j", "via_p217_k", "via_p217_l", "via_p217_m", "via_p217_n", "via_p217_o", "via_p217_p", "via_p217_q", "via_p217_r",
        "via_p216_z", "via_p215_z", "via_p214_z",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p217_foundation", "never_replace_p217_a_mission", "never_replace_p217_b_strategy",
        "never_replace_p217_c_domain", "never_replace_p217_d_infrastructure",
        "never_replace_p217_e_bio_ai", "never_replace_p217_f_synthetic",
        "never_replace_p217_g_simulation", "never_replace_p217_h_digital_health",
        "never_replace_p217_i_precision_medicine", "never_replace_p217_j_clinical_research",
        "never_replace_p217_k_drug_discovery", "never_replace_p217_l_bio_manufacturing",
        "never_replace_p217_m_bio_supply_chain", "never_replace_p217_n_bio_regulatory",
        "never_replace_p217_o_bio_sustainability", "never_replace_p217_p_bio_marketplace",
        "never_replace_p217_q_bio_innovation", "never_replace_p217_r_bio_investment",
        "never_replace_identity_platform", "never_replace_audit_platform",
        "never_replace_p215_z", "never_replace_p216_z", "never_replace_ai_platform",
        "never_replace_core_platform", "bio_ai_via_p214z_acl_only",
        "security_twins_via_p217g_acl_only", "compliance_intelligence_via_p217n_acl_only",
        "environmental_security_via_p217o_acl_only", "commerce_security_via_p217p_acl_only",
        "research_protection_via_p217q_acl_only", "financial_security_via_p217r_acl_only",
        "robotics_via_p216z_acl_only", "quantum_optimization_via_p215z_acl_only",
        "no_module_local_llm", "never_opaque_unexplainable_decisions",
        "never_skip_human_security_oversight",
        "never_autonomous_defense_without_approval",
        "never_skip_zero_trust_controls", "opaque_bio_safety_strategy_forbidden",
        "never_replace_hospital_emr", "module_local_biotechnology_bio_security_forbidden",
    ))
    router = (root / "backend/contexts/biotechnology/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@biotechnology_router.get("/bio-security")', "/bio-security/vision",
        "/bio-security/architecture", "/bio-security/cybersecurity",
        "/bio-security/risk-intelligence", "/bio-security/threat-intelligence",
        "/bio-security/knowledge-graph", "/bio-security/digital-twin",
        "/bio-security/resilience", "/bio-security/agents",
        "/bio-security/domain-model", "/bio-security/robotics-integration",
        "/bio-security/quantum-readiness", "/bio-security/governance",
        "/bio-security/security", "/bio-security/integration",
        "/bio-security/roadmap", "/bio-security/cqrs", "/bio-security/events",
        "/bio-security/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_BIOTECHNOLOGY_BIO_SECURITY.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Bio Security Platform is missing",
        "Never Bio Cybersecurity is missing",
        "Never Biological Risk Intelligence is missing",
        "Never Threat Intelligence is missing",
        "Never Resilience Architecture is missing",
        "Never Security Knowledge Graph is missing",
        "Never Security Digital Twin is missing",
        "Never AI Agents are missing",
        "Never Quantum Readiness is missing",
        "Never Governance is missing",
        "Never Security Architecture is missing",
        "Never MEOS Integration is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never Sibling Biotechnology BC",
        "Never Replace P217 Foundation",
        "Never Replace P217-A Mission",
        "Never Replace P217-B Strategy",
        "Never Replace P217-C Domain",
        "Never Replace P217-D Infrastructure",
        "Never Replace P217-E Bio-AI",
        "Never Replace P217-F Synthetic",
        "Never Replace P217-G Simulation",
        "Never Replace P217-H Digital Health",
        "Never Replace P217-I Precision Medicine",
        "Never Replace P217-J Clinical Research",
        "Never Replace P217-K Drug Discovery",
        "Never Replace P217-L Bio Manufacturing",
        "Never Replace P217-M Bio Supply Chain",
        "Never Replace P217-N Bio Regulatory",
        "Never Replace P217-O Bio Sustainability",
        "Never Replace P217-P Bio Marketplace",
        "Never Replace P217-Q Bio Innovation",
        "Never Replace P217-R Bio Investment",
        "Never Replace Identity Platform",
        "Never Replace Audit Platform",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace Quantum Supreme (P215-Z)",
        "Never Replace Robotics Supreme (P216-Z)",
        "Never Replace Hospital EMR SoR",
        "Never Replace Laboratory LIMS SoR",
        "Never Replace Pharmacy SoR",
        "Never Module-Local LLM",
        "Never Opaque Unexplainable Decisions",
        "Never Skip Genomic Privacy Strategy",
        "Never Skip Ethical Bioengineering Strategy",
        "Never Skip Scientific Integrity Strategy",
        "Never Opaque Bio Safety Strategy",
        "Never Skip Human Security Oversight",
        "Never Autonomous Defense Without Approval",
        "Never Skip Zero Trust Controls",
        "Create a trusted biotechnology security ecosystem capable of protecting biological innovation",
        "P217", "P217-R", "P216-Z", "P215-Z", "P214-Z", "P217-T",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P217-S", "adr": 518, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "biotechnology",
        "capability": "CAP-PLT-BIO-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
