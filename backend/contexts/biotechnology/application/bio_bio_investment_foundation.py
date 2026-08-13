"""Biotechnology P217-R Bio Investment foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/517-enterprise-biotechnology-bio-investment.md",
    "docs/architecture/ENTERPRISE_BIOTECHNOLOGY_BIO_INVESTMENT.md",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_INVESTMENT_ARCHITECTURE.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_INVESTMENT_MODELS.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_INVESTMENT_DDD_CQRS.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_INVESTMENT_SECURITY.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_INVESTMENT_VALIDATION.v1.yaml",
    "docs/architecture/biotechnology/P217_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/biotechnology/domain/services/bio_platform_bio_investment.py",
    "backend/contexts/biotechnology/domain/aggregates/bio_bio_investment_aggregates.py",
    "backend/contexts/biotechnology/infrastructure/acl/bio_bio_investment_acl.py",
    "backend/contexts/biotechnology/application/bio_bio_investment_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/bio_investment_platform",
    "backend/contexts/biotech_venture_intelligence_platform",
    "backend/contexts/scientific_funding_network_platform",
)
def validate_bio_investment_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.biotechnology.domain.aggregates.bio_bio_investment_aggregates import (
        BioInvestmentPlatformRoot, VentureIntelligenceRoot, FundingNetworkRoot,
        FinanceIntelligenceRoot, ValuationEngineRoot, InvestmentKnowledgeGraphRoot,
        InvestmentDigitalTwinRoot, InvestmentAgentsRoot, BioInvestmentGovernanceRoot,
        BioInvestmentSecurityRoot,
    )
    from contexts.biotechnology.domain.services import bio_platform_bio_investment as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P217-R" and cat["adr"] == 517 and cat["sor"] == "biotechnology"
        and cat["capability"] == "CAP-PLT-BIO-001"
        and cat["fabric"] == "meos_bio_investment_intelligence_fabric"
        and cat["foundation_gate"] == "P217" and cat["mission_gate"] == "P217-A"
        and cat["strategy_gate"] == "P217-B" and cat["domain_gate"] == "P217-C"
        and cat["infrastructure_gate"] == "P217-D" and cat["bio_ai_gate"] == "P217-E"
        and cat["synthetic_gate"] == "P217-F" and cat["simulation_gate"] == "P217-G"
        and cat["digital_health_gate"] == "P217-H" and cat["precision_medicine_gate"] == "P217-I"
        and cat["clinical_research_gate"] == "P217-J" and cat["drug_discovery_gate"] == "P217-K"
        and cat["bio_manufacturing_gate"] == "P217-L" and cat["bio_supply_chain_gate"] == "P217-M"
        and cat["bio_regulatory_gate"] == "P217-N" and cat["bio_sustainability_gate"] == "P217-O"
        and cat["bio_marketplace_gate"] == "P217-P" and cat["bio_innovation_gate"] == "P217-Q"
        and cat["robotics_gate"] == "P216-Z" and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["bio_investment_platform_present_required"] is True
        and cat["venture_intelligence_present_required"] is True
        and cat["funding_network_present_required"] is True
        and cat["finance_intelligence_present_required"] is True
        and cat["valuation_engine_present_required"] is True
        and cat["investment_knowledge_graph_present_required"] is True
        and cat["investment_digital_twin_present_required"] is True
        and cat["ai_agents_present_required"] is True
        and cat["quantum_readiness_present_required"] is True
        and cat["governance_present_required"] is True
        and cat["security_architecture_present_required"] is True
        and cat["meos_integration_present_required"] is True
        and cat["architecture"]["layer_count"] == 6
        and cat["venture_intelligence"]["capability_count"] == 4
        and cat["funding_network"]["funding_source_count"] == 6
        and cat["finance_intelligence"]["engine_count"] == 4
        and cat["valuation_engine"]["dimension_count"] == 4
        and cat["investment_agents"]["agent_count"] == 6
        and cat["domain_models"]["domain_count"] == 3
        and cat["bounded_contexts"]["context_count"] == 7
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 8
        and cat["never_replace_p217_foundation"] is True
        and cat["never_replace_p217_q_bio_innovation"] is True
        and cat["never_replace_financial_kernel"] is True
        and cat["never_replace_hospital_emr"] is True
        and cat["bio_ai_via_p214z_acl_only"] is True
        and cat["investment_twins_via_p217g_acl_only"] is True
        and cat["industrial_investment_via_p217l_acl_only"] is True
        and cat["investment_compliance_via_p217n_acl_only"] is True
        and cat["commercial_opportunities_via_p217p_acl_only"] is True
        and cat["innovation_opportunities_via_p217q_acl_only"] is True
        and cat["robotics_via_p216z_acl_only"] is True
        and cat["quantum_optimization_via_p215z_acl_only"] is True
        and cat["no_module_local_llm"] is True
        and cat["never_opaque_unexplainable_decisions"] is True
        and cat["never_skip_human_investment_oversight"] is True
        and cat["never_unverified_investment_recommendation"] is True
        and cat["never_skip_financial_transparency_controls"] is True
        and cat["opaque_bio_safety_strategy_forbidden"] is True
        and cat["foundation_for_p217_s"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        BioInvestmentPlatformRoot.enable(tenant_id="t1", platform_ref="p1").is_missing() is False,
        VentureIntelligenceRoot.enable(tenant_id="t1", venture_ref="v1").is_missing() is False,
        FundingNetworkRoot.enable(tenant_id="t1", funding_ref="f1").is_missing() is False,
        FinanceIntelligenceRoot.enable(tenant_id="t1", finance_ref="fi1").is_missing() is False,
        ValuationEngineRoot.enable(tenant_id="t1", valuation_ref="val1").is_missing() is False,
        InvestmentKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="k1").is_missing() is False,
        InvestmentDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        InvestmentAgentsRoot.enable(tenant_id="t1", agents_ref="ag1").is_missing() is False,
        BioInvestmentGovernanceRoot.enable(tenant_id="t1", governance_ref="gov1").is_missing() is False,
        BioInvestmentSecurityRoot.enable(tenant_id="t1", security_ref="s1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/biotechnology/infrastructure/acl/bio_bio_investment_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p217", "via_p217_a", "via_p217_b", "via_p217_c", "via_p217_d", "via_p217_e", "via_p217_f",
        "via_p217_g", "via_p217_h", "via_p217_i", "via_p217_j", "via_p217_k", "via_p217_l", "via_p217_m", "via_p217_n", "via_p217_o", "via_p217_p", "via_p217_q",
        "via_p216_z", "via_p215_z", "via_p214_z", "via_financial_kernel",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p217_foundation", "never_replace_p217_a_mission", "never_replace_p217_b_strategy",
        "never_replace_p217_c_domain", "never_replace_p217_d_infrastructure",
        "never_replace_p217_e_bio_ai", "never_replace_p217_f_synthetic",
        "never_replace_p217_g_simulation", "never_replace_p217_h_digital_health",
        "never_replace_p217_i_precision_medicine", "never_replace_p217_j_clinical_research",
        "never_replace_p217_k_drug_discovery", "never_replace_p217_l_bio_manufacturing",
        "never_replace_p217_m_bio_supply_chain", "never_replace_p217_n_bio_regulatory",
        "never_replace_p217_o_bio_sustainability", "never_replace_p217_p_bio_marketplace",
        "never_replace_p217_q_bio_innovation", "never_replace_financial_kernel",
        "never_replace_p215_z", "never_replace_p216_z", "never_replace_ai_platform",
        "never_replace_core_platform", "bio_ai_via_p214z_acl_only",
        "investment_twins_via_p217g_acl_only", "industrial_investment_via_p217l_acl_only",
        "investment_compliance_via_p217n_acl_only", "commercial_opportunities_via_p217p_acl_only",
        "innovation_opportunities_via_p217q_acl_only",
        "robotics_via_p216z_acl_only", "quantum_optimization_via_p215z_acl_only",
        "no_module_local_llm", "never_opaque_unexplainable_decisions",
        "never_skip_human_investment_oversight",
        "never_unverified_investment_recommendation",
        "never_skip_financial_transparency_controls", "opaque_bio_safety_strategy_forbidden",
        "never_replace_hospital_emr", "module_local_biotechnology_bio_investment_forbidden",
    ))
    router = (root / "backend/contexts/biotechnology/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@biotechnology_router.get("/bio-investment")', "/bio-investment/vision",
        "/bio-investment/architecture", "/bio-investment/venture-intelligence",
        "/bio-investment/funding-network", "/bio-investment/finance-intelligence",
        "/bio-investment/valuation", "/bio-investment/knowledge-graph",
        "/bio-investment/digital-twin", "/bio-investment/agents",
        "/bio-investment/domain-model", "/bio-investment/robotics-integration",
        "/bio-investment/quantum-readiness", "/bio-investment/governance",
        "/bio-investment/security", "/bio-investment/integration",
        "/bio-investment/roadmap", "/bio-investment/cqrs", "/bio-investment/events",
        "/bio-investment/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_BIOTECHNOLOGY_BIO_INVESTMENT.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Bio Investment Platform is missing",
        "Never Venture Intelligence is missing",
        "Never Funding Network is missing",
        "Never Finance Intelligence is missing",
        "Never Valuation Engine is missing",
        "Never Investment Knowledge Graph is missing",
        "Never Investment Digital Twin is missing",
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
        "Never Replace Financial Kernel",
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
        "Never Skip Human Investment Oversight",
        "Never Unverified Investment Recommendation",
        "Never Skip Financial Transparency Controls",
        "Create an intelligent biotechnology capital ecosystem that connects scientific innovation",
        "P217", "P217-Q", "P216-Z", "P215-Z", "P214-Z", "P217-S",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P217-R", "adr": 517, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "biotechnology",
        "capability": "CAP-PLT-BIO-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
