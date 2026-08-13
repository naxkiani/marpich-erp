"""Biotechnology P217-X Ultimate Bio Evolution foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/522-enterprise-biotechnology-bio-evolution.md",
    "docs/architecture/ENTERPRISE_BIOTECHNOLOGY_BIO_EVOLUTION.md",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_EVOLUTION_ARCHITECTURE.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_EVOLUTION_MODELS.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_EVOLUTION_DDD_CQRS.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_EVOLUTION_SECURITY.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_EVOLUTION_VALIDATION.v1.yaml",
    "docs/architecture/biotechnology/P217_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/biotechnology/domain/services/bio_platform_bio_evolution.py",
    "backend/contexts/biotechnology/domain/aggregates/bio_bio_evolution_aggregates.py",
    "backend/contexts/biotechnology/infrastructure/acl/bio_bio_evolution_acl.py",
    "backend/contexts/biotechnology/application/bio_bio_evolution_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/bio_evolution_platform",
    "backend/contexts/post_biological_intelligence_platform",
    "backend/contexts/bio_singularity_platform",
)
def validate_bio_evolution_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.biotechnology.domain.aggregates.bio_bio_evolution_aggregates import (
        FutureBioArchitectureRoot, PostBiologicalIntelligenceRoot, HumanBioAiConvergenceRoot,
        BioSingularityFrameworkRoot, UltimateBioDigitalTwinRoot, EvolutionKnowledgeGraphRoot,
        FutureIntelligenceAgentsRoot, BioEvolutionRoot, UltimateBioGovernanceRoot,
        ConvergenceSafetyRoot, BioEvolutionSecurityRoot,
    )
    from contexts.biotechnology.domain.services import bio_platform_bio_evolution as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P217-X" and cat["adr"] == 522 and cat["sor"] == "biotechnology"
        and cat["capability"] == "CAP-PLT-BIO-001"
        and cat["fabric"] == "meos_ultimate_bio_evolution_fabric"
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
        and cat["bio_future_gate"] == "P217-T" and cat["bio_autonomous_gate"] == "P217-U"
        and cat["bio_gi_gate"] == "P217-V" and cat["bio_civilization_gate"] == "P217-W"
        and cat["robotics_gate"] == "P216-Z" and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["future_bio_architecture_present_required"] is True
        and cat["post_biological_intelligence_present_required"] is True
        and cat["human_bio_ai_convergence_present_required"] is True
        and cat["bio_singularity_framework_present_required"] is True
        and cat["ultimate_bio_digital_twin_present_required"] is True
        and cat["evolution_knowledge_graph_present_required"] is True
        and cat["future_intelligence_agents_present_required"] is True
        and cat["ultimate_bio_governance_present_required"] is True
        and cat["quantum_readiness_present_required"] is True
        and cat["security_architecture_present_required"] is True
        and cat["meos_integration_present_required"] is True
        and cat["architecture"]["layer_count"] == 6
        and cat["post_biological_intelligence"]["capability_count"] == 3
        and cat["human_bio_ai_convergence"]["capability_count"] == 3
        and cat["bio_singularity_framework"]["component_count"] == 3
        and cat["evolution_agents"]["agent_count"] == 6
        and cat["domain_models"]["domain_count"] == 3
        and cat["bounded_contexts"]["context_count"] == 7
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 8
        and cat["never_replace_p217_foundation"] is True
        and cat["never_replace_p217_v_bio_gi"] is True
        and cat["never_replace_p217_w_bio_civilization"] is True
        and cat["never_replace_hospital_emr"] is True
        and cat["bio_ai_via_p214z_acl_only"] is True
        and cat["evolution_twins_via_p217g_acl_only"] is True
        and cat["bio_gi_cognition_via_p217v_acl_only"] is True
        and cat["civilization_intelligence_via_p217w_acl_only"] is True
        and cat["autonomy_execution_via_p217u_acl_only"] is True
        and cat["robotics_via_p216z_acl_only"] is True
        and cat["quantum_optimization_via_p215z_acl_only"] is True
        and cat["no_module_local_llm"] is True
        and cat["never_opaque_unexplainable_decisions"] is True
        and cat["never_skip_human_singularity_oversight"] is True
        and cat["never_unvalidated_singularity_scenario_release"] is True
        and cat["never_skip_responsible_evolution_governance"] is True
        and cat["never_skip_convergence_safety_controls"] is True
        and cat["never_skip_human_benefit_first_principle"] is True
        and cat["opaque_bio_safety_strategy_forbidden"] is True
        and cat["foundation_for_p217_y"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        FutureBioArchitectureRoot.enable(tenant_id="t1", architecture_ref="a1").is_missing() is False,
        PostBiologicalIntelligenceRoot.enable(tenant_id="t1", intelligence_ref="i1").is_missing() is False,
        HumanBioAiConvergenceRoot.enable(tenant_id="t1", convergence_ref="c1").is_missing() is False,
        BioSingularityFrameworkRoot.enable(tenant_id="t1", singularity_ref="s1").is_missing() is False,
        UltimateBioDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        EvolutionKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="k1").is_missing() is False,
        FutureIntelligenceAgentsRoot.enable(tenant_id="t1", agents_ref="ag1").is_missing() is False,
        BioEvolutionRoot.enable(tenant_id="t1", evolution_ref="e1").is_missing() is False,
        UltimateBioGovernanceRoot.enable(tenant_id="t1", governance_ref="gov1").is_missing() is False,
        ConvergenceSafetyRoot.enable(tenant_id="t1", safety_ref="sf1").is_missing() is False,
        BioEvolutionSecurityRoot.enable(tenant_id="t1", security_ref="sec1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/biotechnology/infrastructure/acl/bio_bio_evolution_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p217", "via_p217_a", "via_p217_b", "via_p217_c", "via_p217_d", "via_p217_e", "via_p217_f",
        "via_p217_g", "via_p217_h", "via_p217_i", "via_p217_j", "via_p217_k", "via_p217_l", "via_p217_m", "via_p217_n", "via_p217_o", "via_p217_p", "via_p217_q", "via_p217_r", "via_p217_s", "via_p217_t", "via_p217_u", "via_p217_v", "via_p217_w",
        "via_p216_z", "via_p215_z", "via_p214_z",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p217_foundation", "never_replace_p217_v_bio_gi", "never_replace_p217_w_bio_civilization",
        "never_replace_p217_u_bio_autonomous",
        "never_replace_p215_z", "never_replace_p216_z", "never_replace_ai_platform",
        "never_replace_core_platform", "bio_ai_via_p214z_acl_only",
        "evolution_twins_via_p217g_acl_only", "bio_gi_cognition_via_p217v_acl_only",
        "civilization_intelligence_via_p217w_acl_only", "autonomy_execution_via_p217u_acl_only",
        "robotics_via_p216z_acl_only", "quantum_optimization_via_p215z_acl_only",
        "no_module_local_llm", "never_opaque_unexplainable_decisions",
        "never_skip_human_singularity_oversight",
        "never_unvalidated_singularity_scenario_release",
        "never_skip_responsible_evolution_governance",
        "never_skip_convergence_safety_controls",
        "never_skip_human_benefit_first_principle", "opaque_bio_safety_strategy_forbidden",
        "never_replace_hospital_emr", "module_local_biotechnology_bio_evolution_forbidden",
    ))
    router = (root / "backend/contexts/biotechnology/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@biotechnology_router.get("/bio-evolution")', "/bio-evolution/vision",
        "/bio-evolution/architecture", "/bio-evolution/post-biological-intelligence",
        "/bio-evolution/convergence", "/bio-evolution/singularity",
        "/bio-evolution/digital-twin", "/bio-evolution/knowledge-graph",
        "/bio-evolution/agents", "/bio-evolution/domain-model",
        "/bio-evolution/robotics-integration", "/bio-evolution/quantum-readiness",
        "/bio-evolution/governance", "/bio-evolution/security",
        "/bio-evolution/integration", "/bio-evolution/roadmap",
        "/bio-evolution/cqrs", "/bio-evolution/events", "/bio-evolution/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_BIOTECHNOLOGY_BIO_EVOLUTION.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Future Bio Architecture is missing",
        "Never Post-Biological Intelligence is missing",
        "Never Human-Bio-AI Convergence is missing",
        "Never Bio Singularity Framework is missing",
        "Never Ultimate Bio Digital Twin is missing",
        "Never Evolution Knowledge Graph is missing",
        "Never Future Intelligence Agents are missing",
        "Never Ultimate Bio Governance is missing",
        "Never Quantum Readiness is missing",
        "Never Security Architecture is missing",
        "Never MEOS Integration is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never Sibling Biotechnology BC",
        "Never Replace P217 Foundation",
        "Never Replace P217-V Bio-GI",
        "Never Replace P217-W Bio Civilization",
        "Never Replace P217-U Bio Autonomous",
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
        "Never Skip Human Singularity Oversight",
        "Never Unvalidated Singularity Scenario Release",
        "Never Skip Responsible Evolution Governance",
        "Never Skip Convergence Safety Controls",
        "Never Skip Human Benefit First Principle",
        "Create the next evolutionary architecture where biological intelligence",
        "P217", "P217-V", "P217-W", "P216-Z", "P215-Z", "P214-Z", "P217-Y",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P217-X", "adr": 522, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "biotechnology",
        "capability": "CAP-PLT-BIO-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
