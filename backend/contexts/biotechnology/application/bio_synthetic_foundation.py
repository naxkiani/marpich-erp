"""Biotechnology P217-F Synthetic Biology foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/505-enterprise-biotechnology-synthetic.md",
    "docs/architecture/ENTERPRISE_BIOTECHNOLOGY_SYNTHETIC.md",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_SYNTHETIC_ARCHITECTURE.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_SYNTHETIC_MODELS.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_SYNTHETIC_DDD_CQRS.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_SYNTHETIC_SECURITY.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_SYNTHETIC_VALIDATION.v1.yaml",
    "docs/architecture/biotechnology/P217_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/biotechnology/domain/services/bio_platform_synthetic.py",
    "backend/contexts/biotechnology/domain/aggregates/bio_synthetic_aggregates.py",
    "backend/contexts/biotechnology/infrastructure/acl/bio_synthetic_acl.py",
    "backend/contexts/biotechnology/application/bio_synthetic_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/synthetic_biology_platform",
    "backend/contexts/bio_design_intelligence_platform",
    "backend/contexts/synthetic_life_systems_platform",
)
def validate_synthetic_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.biotechnology.domain.aggregates.bio_synthetic_aggregates import (
        SyntheticBiologyPlatformRoot, BioDesignIntelligenceRoot, EngineeringAutomationRoot,
        SyntheticLifeSystemsRoot, BioManufacturingRoot, SyntheticAgentsRoot,
        DigitalTwinIntegrationRoot, ResponsibleSyntheticBioRoot, SyntheticBioSecurityRoot,
    )
    from contexts.biotechnology.domain.services import bio_platform_synthetic as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P217-F" and cat["adr"] == 505 and cat["sor"] == "biotechnology"
        and cat["capability"] == "CAP-PLT-BIO-001"
        and cat["fabric"] == "meos_synthetic_biology_intelligence_fabric"
        and cat["foundation_gate"] == "P217" and cat["mission_gate"] == "P217-A"
        and cat["strategy_gate"] == "P217-B" and cat["domain_gate"] == "P217-C"
        and cat["infrastructure_gate"] == "P217-D" and cat["bio_ai_gate"] == "P217-E"
        and cat["robotics_gate"] == "P216-Z" and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["synthetic_biology_platform_present_required"] is True
        and cat["bio_design_intelligence_present_required"] is True
        and cat["engineering_automation_present_required"] is True
        and cat["synthetic_life_architecture_present_required"] is True
        and cat["domain_model_present_required"] is True
        and cat["ai_agent_ecosystem_present_required"] is True
        and cat["safety_governance_present_required"] is True
        and cat["digital_twin_integration_present_required"] is True
        and cat["bio_manufacturing_intelligence_present_required"] is True
        and cat["security_architecture_present_required"] is True
        and cat["architecture"]["layer_count"] == 5
        and cat["design_intelligence"]["capability_count"] == 4
        and cat["engineering_automation"]["domain_count"] == 4
        and cat["synthetic_lifecycle"]["phase_count"] == 5
        and cat["domain_models"]["domain_count"] == 4
        and cat["synthetic_agents"]["agent_count"] == 5
        and cat["bounded_contexts"]["context_count"] == 7
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 8
        and cat["never_replace_p217_foundation"] is True
        and cat["never_replace_p217_e_bio_ai"] is True
        and cat["bio_ai_via_p214z_acl_only"] is True
        and cat["lab_robotics_via_p216z_acl_only"] is True
        and cat["no_module_local_llm"] is True
        and cat["never_opaque_unexplainable_decisions"] is True
        and cat["never_unsupervised_synthetic_release"] is True
        and cat["opaque_bio_safety_strategy_forbidden"] is True
        and cat["foundation_for_p217_g"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        SyntheticBiologyPlatformRoot.enable(tenant_id="t1", platform_ref="p1").is_missing() is False,
        BioDesignIntelligenceRoot.enable(tenant_id="t1", design_ref="d1").is_missing() is False,
        EngineeringAutomationRoot.enable(tenant_id="t1", automation_ref="a1").is_missing() is False,
        SyntheticLifeSystemsRoot.enable(tenant_id="t1", lifecycle_ref="l1").is_missing() is False,
        BioManufacturingRoot.enable(tenant_id="t1", manufacturing_ref="m1").is_missing() is False,
        SyntheticAgentsRoot.enable(tenant_id="t1", agents_ref="ag1").is_missing() is False,
        DigitalTwinIntegrationRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        ResponsibleSyntheticBioRoot.enable(tenant_id="t1", governance_ref="g1").is_missing() is False,
        SyntheticBioSecurityRoot.enable(tenant_id="t1", security_ref="s1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/biotechnology/infrastructure/acl/bio_synthetic_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p217", "via_p217_a", "via_p217_b", "via_p217_c", "via_p217_d", "via_p217_e",
        "via_p216_z", "via_p215_z", "via_p214_z",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p217_foundation", "never_replace_p217_a_mission", "never_replace_p217_b_strategy",
        "never_replace_p217_c_domain", "never_replace_p217_d_infrastructure", "never_replace_p217_e_bio_ai",
        "never_replace_p215_z", "never_replace_p216_z", "never_replace_ai_platform",
        "never_replace_core_platform", "bio_ai_via_p214z_acl_only", "lab_robotics_via_p216z_acl_only",
        "no_module_local_llm", "never_opaque_unexplainable_decisions",
        "never_unsupervised_synthetic_release", "opaque_bio_safety_strategy_forbidden",
        "module_local_biotechnology_synthetic_forbidden",
    ))
    router = (root / "backend/contexts/biotechnology/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@biotechnology_router.get("/synthetic")', "/synthetic/vision", "/synthetic/architecture",
        "/synthetic/design", "/synthetic/automation", "/synthetic/lifecycle",
        "/synthetic/domains", "/synthetic/manufacturing", "/synthetic/digital-twin",
        "/synthetic/agents", "/synthetic/governance", "/synthetic/security",
        "/synthetic/integration", "/synthetic/roadmap", "/synthetic/cqrs", "/synthetic/events",
        "/synthetic/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_BIOTECHNOLOGY_SYNTHETIC.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Synthetic Biology Platform is missing",
        "Never Bio Design Intelligence is missing",
        "Never Engineering Automation is missing",
        "Never Synthetic Life Architecture is missing",
        "Never Domain Model is missing",
        "Never AI Agent Ecosystem is missing",
        "Never Safety Governance is missing",
        "Never Digital Twin Integration is missing",
        "Never Bio Manufacturing Intelligence is missing",
        "Never Security Architecture is missing",
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
        "Never Unsupervised Synthetic Release",
        "Create an intelligent biological engineering ecosystem",
        "P217", "P217-E", "P216-Z", "P215-Z", "P214-Z", "P217-G",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P217-F", "adr": 505, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "biotechnology",
        "capability": "CAP-PLT-BIO-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
