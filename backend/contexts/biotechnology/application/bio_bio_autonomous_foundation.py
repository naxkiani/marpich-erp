"""Biotechnology P217-U Bio Autonomous foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/520-enterprise-biotechnology-bio-autonomous.md",
    "docs/architecture/ENTERPRISE_BIOTECHNOLOGY_BIO_AUTONOMOUS.md",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_AUTONOMOUS_ARCHITECTURE.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_AUTONOMOUS_MODELS.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_AUTONOMOUS_DDD_CQRS.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_AUTONOMOUS_SECURITY.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_AUTONOMOUS_VALIDATION.v1.yaml",
    "docs/architecture/biotechnology/P217_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/biotechnology/domain/services/bio_platform_bio_autonomous.py",
    "backend/contexts/biotechnology/domain/aggregates/bio_bio_autonomous_aggregates.py",
    "backend/contexts/biotechnology/infrastructure/acl/bio_bio_autonomous_acl.py",
    "backend/contexts/biotechnology/application/bio_bio_autonomous_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/bio_autonomous_platform",
    "backend/contexts/autonomous_biology_platform",
    "backend/contexts/bio_ai_autonomy_platform",
)
def validate_bio_autonomous_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.biotechnology.domain.aggregates.bio_bio_autonomous_aggregates import (
        BioAutonomousPlatformRoot, AutonomousBiologyRoot, BioAiAutonomyRoot,
        SelfOptimizingEcosystemRoot, AutonomousDigitalTwinRoot, AutonomousKnowledgeGraphRoot,
        AutonomousAgentsRoot, AdaptiveIntelligenceRoot, AutonomyGovernanceRoot,
        BioAutonomousGovernanceRoot, BioAutonomousSecurityRoot,
    )
    from contexts.biotechnology.domain.services import bio_platform_bio_autonomous as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P217-U" and cat["adr"] == 520 and cat["sor"] == "biotechnology"
        and cat["capability"] == "CAP-PLT-BIO-001"
        and cat["fabric"] == "meos_bio_autonomous_intelligence_fabric"
        and cat["foundation_gate"] == "P217" and cat["mission_gate"] == "P217-A"
        and cat["strategy_gate"] == "P217-B" and cat["domain_gate"] == "P217-C"
        and cat["infrastructure_gate"] == "P217-D" and cat["bio_ai_gate"] == "P217-E"
        and cat["synthetic_gate"] == "P217-F" and cat["simulation_gate"] == "P217-G"
        and cat["digital_health_gate"] == "P217-H" and cat["precision_medicine_gate"] == "P217-I"
        and cat["clinical_research_gate"] == "P217-J" and cat["drug_discovery_gate"] == "P217-K"
        and cat["bio_manufacturing_gate"] == "P217-L" and cat["bio_supply_chain_gate"] == "P217-M"
        and cat["bio_regulatory_gate"] == "P217-N" and cat["bio_sustainability_gate"] == "P217-O"
        and cat["bio_marketplace_gate"] == "P217-P" and cat["bio_innovation_gate"] == "P217-Q"
        and cat["bio_investment_gate"] == "P217-R" and cat["bio_security_gate"] == "P217-S"
        and cat["bio_future_gate"] == "P217-T"
        and cat["robotics_gate"] == "P216-Z" and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["bio_autonomous_platform_present_required"] is True
        and cat["autonomous_biology_present_required"] is True
        and cat["bio_ai_autonomy_present_required"] is True
        and cat["self_optimizing_ecosystem_present_required"] is True
        and cat["autonomous_bio_digital_twin_present_required"] is True
        and cat["autonomous_knowledge_graph_present_required"] is True
        and cat["ai_autonomous_agents_present_required"] is True
        and cat["safety_governance_present_required"] is True
        and cat["quantum_readiness_present_required"] is True
        and cat["governance_present_required"] is True
        and cat["security_architecture_present_required"] is True
        and cat["meos_integration_present_required"] is True
        and cat["architecture"]["layer_count"] == 6
        and cat["bio_ai_autonomy_engine"]["capability_count"] == 4
        and cat["autonomous_biology_os"]["capability_count"] == 4
        and cat["self_optimizing_ecosystem"]["closed_loop_step_count"] == 6
        and cat["autonomous_agents"]["agent_count"] == 6
        and cat["domain_models"]["domain_count"] == 3
        and cat["bounded_contexts"]["context_count"] == 7
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 8
        and cat["never_replace_p217_foundation"] is True
        and cat["never_replace_p217_t_bio_future"] is True
        and cat["never_replace_p217_s_bio_security"] is True
        and cat["never_replace_hospital_emr"] is True
        and cat["bio_ai_via_p214z_acl_only"] is True
        and cat["autonomous_twins_via_p217g_acl_only"] is True
        and cat["future_evolution_via_p217t_acl_only"] is True
        and cat["autonomous_safety_via_p217s_acl_only"] is True
        and cat["robotics_via_p216z_acl_only"] is True
        and cat["quantum_optimization_via_p215z_acl_only"] is True
        and cat["no_module_local_llm"] is True
        and cat["never_opaque_unexplainable_decisions"] is True
        and cat["never_opaque_autonomous_decisions"] is True
        and cat["never_skip_human_autonomy_oversight"] is True
        and cat["never_unsupervised_autonomous_bio_action"] is True
        and cat["never_skip_responsible_bio_autonomy_controls"] is True
        and cat["opaque_bio_safety_strategy_forbidden"] is True
        and cat["foundation_for_p217_v"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        BioAutonomousPlatformRoot.enable(tenant_id="t1", platform_ref="p1").is_missing() is False,
        AutonomousBiologyRoot.enable(tenant_id="t1", biology_ref="b1").is_missing() is False,
        BioAiAutonomyRoot.enable(tenant_id="t1", autonomy_ref="a1").is_missing() is False,
        SelfOptimizingEcosystemRoot.enable(tenant_id="t1", ecosystem_ref="e1").is_missing() is False,
        AutonomousDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        AutonomousKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="k1").is_missing() is False,
        AutonomousAgentsRoot.enable(tenant_id="t1", agents_ref="ag1").is_missing() is False,
        AdaptiveIntelligenceRoot.enable(tenant_id="t1", adaptive_ref="ad1").is_missing() is False,
        AutonomyGovernanceRoot.enable(tenant_id="t1", governance_ref="sg1").is_missing() is False,
        BioAutonomousGovernanceRoot.enable(tenant_id="t1", governance_ref="gov1").is_missing() is False,
        BioAutonomousSecurityRoot.enable(tenant_id="t1", security_ref="s1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/biotechnology/infrastructure/acl/bio_bio_autonomous_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p217", "via_p217_a", "via_p217_b", "via_p217_c", "via_p217_d", "via_p217_e", "via_p217_f",
        "via_p217_g", "via_p217_h", "via_p217_i", "via_p217_j", "via_p217_k", "via_p217_l", "via_p217_m", "via_p217_n", "via_p217_o", "via_p217_p", "via_p217_q", "via_p217_r", "via_p217_s", "via_p217_t",
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
        "never_replace_p217_s_bio_security", "never_replace_p217_t_bio_future",
        "never_replace_p215_z", "never_replace_p216_z", "never_replace_ai_platform",
        "never_replace_core_platform", "bio_ai_via_p214z_acl_only",
        "autonomous_twins_via_p217g_acl_only", "future_evolution_via_p217t_acl_only",
        "autonomous_safety_via_p217s_acl_only",
        "robotics_via_p216z_acl_only", "quantum_optimization_via_p215z_acl_only",
        "no_module_local_llm", "never_opaque_unexplainable_decisions",
        "never_opaque_autonomous_decisions",
        "never_skip_human_autonomy_oversight",
        "never_unsupervised_autonomous_bio_action",
        "never_skip_responsible_bio_autonomy_controls", "opaque_bio_safety_strategy_forbidden",
        "never_replace_hospital_emr", "module_local_biotechnology_bio_autonomous_forbidden",
    ))
    router = (root / "backend/contexts/biotechnology/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@biotechnology_router.get("/bio-autonomous")', "/bio-autonomous/vision",
        "/bio-autonomous/architecture", "/bio-autonomous/autonomous-biology",
        "/bio-autonomous/bio-ai-autonomy", "/bio-autonomous/self-optimizing-ecosystem",
        "/bio-autonomous/digital-twin", "/bio-autonomous/knowledge-graph",
        "/bio-autonomous/agents", "/bio-autonomous/domain-model",
        "/bio-autonomous/robotics-integration", "/bio-autonomous/quantum-readiness",
        "/bio-autonomous/governance", "/bio-autonomous/security",
        "/bio-autonomous/integration", "/bio-autonomous/roadmap",
        "/bio-autonomous/cqrs", "/bio-autonomous/events", "/bio-autonomous/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_BIOTECHNOLOGY_BIO_AUTONOMOUS.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Bio Autonomous Platform is missing",
        "Never Autonomous Biology is missing",
        "Never Bio-AI Autonomy is missing",
        "Never Self-Optimizing Ecosystem is missing",
        "Never Autonomous Bio Digital Twin is missing",
        "Never Autonomous Knowledge Graph is missing",
        "Never AI Autonomous Agents are missing",
        "Never Safety Governance is missing",
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
        "Never Replace P217-S Bio Security",
        "Never Replace P217-T Bio Future",
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
        "Never Skip Human Autonomy Oversight",
        "Never Unsupervised Autonomous Bio Action",
        "Never Skip Responsible Bio Autonomy Controls",
        "Never Opaque Autonomous Decisions",
        "Create a next-generation biotechnology intelligence ecosystem capable of autonomously monitoring",
        "P217", "P217-T", "P217-S", "P216-Z", "P215-Z", "P214-Z", "P217-V",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P217-U", "adr": 520, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "biotechnology",
        "capability": "CAP-PLT-BIO-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
