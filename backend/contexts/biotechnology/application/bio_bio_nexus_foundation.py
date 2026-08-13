"""Biotechnology P217-Z Bio Nexus foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/525-enterprise-biotechnology-bio-nexus.md",
    "docs/architecture/ENTERPRISE_BIOTECHNOLOGY_BIO_NEXUS.md",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_NEXUS_ARCHITECTURE.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_NEXUS_MODELS.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_NEXUS_DDD_CQRS.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_NEXUS_SECURITY.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_NEXUS_VALIDATION.v1.yaml",
    "docs/architecture/biotechnology/P217_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/biotechnology/domain/services/bio_platform_bio_nexus.py",
    "backend/contexts/biotechnology/domain/aggregates/bio_bio_nexus_aggregates.py",
    "backend/contexts/biotechnology/infrastructure/acl/bio_bio_nexus_acl.py",
    "backend/contexts/biotechnology/application/bio_bio_nexus_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/bio_nexus_platform",
    "backend/contexts/bio_supreme_control_plane",
    "backend/contexts/autonomous_biological_nexus_platform",
)
def validate_bio_nexus_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.biotechnology.domain.aggregates.bio_bio_nexus_aggregates import (
        UltimateBioMasterRoot, BioSupremeControlPlaneRoot, AutonomousBiologicalNexusRoot,
        BioCivilizationIntelligenceCoreRoot, UniversalBioKnowledgeGraphRoot,
        UltimateBioDigitalTwinRoot, SupremeBioAgentsRoot, FinalBioIntelligenceArchitectureRoot,
        HumanSupremeOversightRoot, BioNexusSecurityRoot, BioNexusGovernanceRoot,
    )
    from contexts.biotechnology.domain.services import bio_platform_bio_nexus as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P217-Z" and cat["adr"] == 525 and cat["sor"] == "biotechnology"
        and cat["capability"] == "CAP-PLT-BIO-001"
        and cat["fabric"] == "meos_final_bio_intelligence_architecture"
        and cat["bio_trust_gate"] == "P217-Y" and cat["bio_evolution_gate"] == "P217-X"
        and cat["bio_civilization_gate"] == "P217-W" and cat["bio_gi_gate"] == "P217-V"
        and cat["bio_security_gate"] == "P217-S"
        and cat["robotics_gate"] == "P216-Z" and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["ultimate_bio_master_architecture_present_required"] is True
        and cat["meos_bio_supreme_control_plane_present_required"] is True
        and cat["autonomous_biological_intelligence_nexus_present_required"] is True
        and cat["bio_civilization_intelligence_core_present_required"] is True
        and cat["universal_bio_knowledge_graph_present_required"] is True
        and cat["ultimate_bio_digital_twin_present_required"] is True
        and cat["supreme_bio_intelligence_agents_present_required"] is True
        and cat["meos_final_bio_intelligence_architecture_present_required"] is True
        and cat["architecture"]["layer_count"] == 6
        and cat["bio_supreme_control_plane"]["domain_count"] == 4
        and cat["autonomous_biological_nexus"]["capability_count"] == 4
        and cat["bio_civilization_intelligence_core"]["capability_count"] == 4
        and cat["supreme_agents"]["agent_count"] == 6
        and cat["domain_models"]["domain_count"] == 3
        and cat["bounded_contexts"]["context_count"] == 7
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 8
        and cat["never_replace_p217_y_bio_trust"] is True
        and cat["never_replace_p217_x_bio_evolution"] is True
        and cat["never_replace_p217_w_bio_civilization"] is True
        and cat["never_replace_compliance_platform"] is True
        and cat["never_replace_hospital_emr"] is True
        and cat["bio_ai_via_p214z_acl_only"] is True
        and cat["trust_via_p217y_acl_only"] is True
        and cat["evolution_via_p217x_acl_only"] is True
        and cat["civilization_intelligence_via_p217w_acl_only"] is True
        and cat["no_module_local_llm"] is True
        and cat["never_opaque_unexplainable_decisions"] is True
        and cat["never_skip_human_supreme_oversight"] is True
        and cat["never_skip_bio_supreme_control_plane_controls"] is True
        and cat["never_skip_autonomous_nexus_safety_controls"] is True
        and cat["never_skip_civilization_core_governance"] is True
        and cat["never_unvalidated_nexus_capability_release"] is True
        and cat["series_closure_for_p217"] is True
        and cat["foundation_for_p218"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        UltimateBioMasterRoot.enable(tenant_id="t1", master_ref="m1").is_missing() is False,
        BioSupremeControlPlaneRoot.enable(tenant_id="t1", control_plane_ref="cp1").is_missing() is False,
        AutonomousBiologicalNexusRoot.enable(tenant_id="t1", nexus_ref="n1").is_missing() is False,
        BioCivilizationIntelligenceCoreRoot.enable(tenant_id="t1", core_ref="c1").is_missing() is False,
        UniversalBioKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="k1").is_missing() is False,
        UltimateBioDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        SupremeBioAgentsRoot.enable(tenant_id="t1", agents_ref="a1").is_missing() is False,
        FinalBioIntelligenceArchitectureRoot.enable(tenant_id="t1", architecture_ref="ar1").is_missing() is False,
        HumanSupremeOversightRoot.enable(tenant_id="t1", oversight_ref="o1").is_missing() is False,
        BioNexusSecurityRoot.enable(tenant_id="t1", security_ref="s1").is_missing() is False,
        BioNexusGovernanceRoot.enable(tenant_id="t1", governance_ref="g1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/biotechnology/infrastructure/acl/bio_bio_nexus_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p217", "via_p217_g", "via_p217_s", "via_p217_v", "via_p217_w", "via_p217_x", "via_p217_y",
        "via_p216_z", "via_p215_z", "via_p214_z",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p217_foundation", "never_replace_p217_y_bio_trust",
        "never_replace_p217_x_bio_evolution", "never_replace_p217_w_bio_civilization",
        "never_replace_compliance_platform", "never_replace_core_platform",
        "bio_ai_via_p214z_acl_only", "trust_via_p217y_acl_only", "evolution_via_p217x_acl_only",
        "civilization_intelligence_via_p217w_acl_only", "security_via_p217s_acl_only",
        "no_module_local_llm", "never_opaque_unexplainable_decisions",
        "never_skip_human_supreme_oversight", "never_skip_bio_supreme_control_plane_controls",
        "never_skip_autonomous_nexus_safety_controls", "never_skip_civilization_core_governance",
        "never_unvalidated_nexus_capability_release",
        "never_replace_hospital_emr", "module_local_biotechnology_bio_nexus_forbidden",
    ))
    router = (root / "backend/contexts/biotechnology/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@biotechnology_router.get("/bio-nexus")', "/bio-nexus/vision",
        "/bio-nexus/architecture", "/bio-nexus/control-plane", "/bio-nexus/abin",
        "/bio-nexus/civilization-core", "/bio-nexus/knowledge-graph", "/bio-nexus/digital-twin",
        "/bio-nexus/agents", "/bio-nexus/domain-model",
        "/bio-nexus/robotics-integration", "/bio-nexus/quantum-readiness",
        "/bio-nexus/governance", "/bio-nexus/security",
        "/bio-nexus/integration", "/bio-nexus/roadmap",
        "/bio-nexus/cqrs", "/bio-nexus/events", "/bio-nexus/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_BIOTECHNOLOGY_BIO_NEXUS.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Ultimate Bio Master Architecture is missing",
        "Never MEOS Bio Supreme Control Plane is missing",
        "Never Autonomous Biological Intelligence Nexus is missing",
        "Never Bio Civilization Intelligence Core is missing",
        "Never Universal Bio Knowledge Graph is missing",
        "Never Ultimate Bio Digital Twin is missing",
        "Never Supreme Bio Intelligence Agents are missing",
        "Never MEOS Final Bio Intelligence Architecture is missing",
        "Never Replace P217-Y Bio Trust",
        "Never Replace P217-X Bio Evolution",
        "Never Replace P217-W Bio Civilization",
        "Never Replace Core Platform",
        "Never Replace Compliance Platform",
        "Never Module-Local LLM",
        "Never Skip Human Supreme Oversight",
        "Never Skip Bio Supreme Control Plane Controls",
        "Never Skip Autonomous Nexus Safety Controls",
        "Never Skip Civilization Core Governance",
        "Never Unvalidated Nexus Capability Release",
        "Create the final intelligence architecture",
        "P217-Y", "P217-X", "P217-W", "P214-Z", "P218",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P217-Z", "adr": 525, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "biotechnology",
        "capability": "CAP-PLT-BIO-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
