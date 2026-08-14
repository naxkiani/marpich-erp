"""Biotechnology P217-G Biological Simulation foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/506-enterprise-biotechnology-simulation.md",
    "docs/architecture/ENTERPRISE_BIOTECHNOLOGY_SIMULATION.md",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_SIMULATION_ARCHITECTURE.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_SIMULATION_MODELS.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_SIMULATION_DDD_CQRS.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_SIMULATION_SECURITY.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_SIMULATION_VALIDATION.v1.yaml",
    "docs/architecture/biotechnology/P217_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/biotechnology/domain/services/bio_platform_simulation.py",
    "backend/contexts/biotechnology/domain/aggregates/bio_simulation_aggregates.py",
    "backend/contexts/biotechnology/infrastructure/acl/bio_simulation_acl.py",
    "backend/contexts/biotechnology/application/bio_simulation_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/biological_simulation_platform",
    "backend/contexts/bio_digital_twin_platform",
    "backend/contexts/life_system_modeling_platform",
)
def validate_simulation_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.biotechnology.domain.aggregates.bio_simulation_aggregates import (
        SimulationPlatformRoot, DigitalTwinArchitectureRoot, SimulationEngineRoot,
        LifeModelingFrameworkRoot, SimulationIntelligenceRoot, SimulationModelLifecycleRoot,
        SimulationDomainModelRoot, SimulationGovernanceRoot, SimulationSecurityRoot,
    )
    from contexts.biotechnology.domain.services import bio_platform_simulation as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P217-G" and cat["adr"] == 506 and cat["sor"] == "biotechnology"
        and cat["capability"] == "CAP-PLT-BIO-001"
        and cat["fabric"] == "meos_biological_simulation_intelligence_fabric"
        and cat["foundation_gate"] == "P217" and cat["mission_gate"] == "P217-A"
        and cat["strategy_gate"] == "P217-B" and cat["domain_gate"] == "P217-C"
        and cat["infrastructure_gate"] == "P217-D" and cat["bio_ai_gate"] == "P217-E"
        and cat["synthetic_gate"] == "P217-F"
        and cat["robotics_gate"] == "P216-Z" and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["bio_simulation_platform_present_required"] is True
        and cat["digital_twin_architecture_present_required"] is True
        and cat["computational_simulation_engine_present_required"] is True
        and cat["life_modeling_framework_present_required"] is True
        and cat["multi_scale_architecture_present_required"] is True
        and cat["ai_integration_present_required"] is True
        and cat["quantum_readiness_present_required"] is True
        and cat["robotics_integration_present_required"] is True
        and cat["governance_present_required"] is True
        and cat["security_architecture_present_required"] is True
        and cat["architecture"]["layer_count"] == 6
        and cat["digital_twins"]["domain_count"] == 5
        and cat["simulation_engine"]["component_count"] == 5
        and cat["life_modeling"]["level_count"] == 5
        and cat["simulation_intelligence"]["capability_count"] == 5
        and cat["bounded_contexts"]["context_count"] == 7
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 8
        and cat["never_replace_p217_foundation"] is True
        and cat["never_replace_p217_f_synthetic"] is True
        and cat["bio_ai_via_p214z_acl_only"] is True
        and cat["quantum_simulation_via_p215z_acl_only"] is True
        and cat["physical_validation_via_p216z_acl_only"] is True
        and cat["no_module_local_llm"] is True
        and cat["never_opaque_unexplainable_decisions"] is True
        and cat["never_unvalidated_simulation_claims"] is True
        and cat["opaque_bio_safety_strategy_forbidden"] is True
        and cat["foundation_for_p217_h"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        SimulationPlatformRoot.enable(tenant_id="t1", platform_ref="p1").is_missing() is False,
        DigitalTwinArchitectureRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        SimulationEngineRoot.enable(tenant_id="t1", engine_ref="e1").is_missing() is False,
        LifeModelingFrameworkRoot.enable(tenant_id="t1", modeling_ref="m1").is_missing() is False,
        SimulationIntelligenceRoot.enable(tenant_id="t1", intelligence_ref="i1").is_missing() is False,
        SimulationModelLifecycleRoot.enable(tenant_id="t1", lifecycle_ref="l1").is_missing() is False,
        SimulationDomainModelRoot.enable(tenant_id="t1", domain_ref="d1").is_missing() is False,
        SimulationGovernanceRoot.enable(tenant_id="t1", governance_ref="g1").is_missing() is False,
        SimulationSecurityRoot.enable(tenant_id="t1", security_ref="s1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/biotechnology/infrastructure/acl/bio_simulation_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p217", "via_p217_a", "via_p217_b", "via_p217_c", "via_p217_d", "via_p217_e", "via_p217_f",
        "via_p216_z", "via_p215_z", "via_p214_z",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p217_foundation", "never_replace_p217_a_mission", "never_replace_p217_b_strategy",
        "never_replace_p217_c_domain", "never_replace_p217_d_infrastructure",
        "never_replace_p217_e_bio_ai", "never_replace_p217_f_synthetic",
        "never_replace_p215_z", "never_replace_p216_z", "never_replace_ai_platform",
        "never_replace_core_platform", "bio_ai_via_p214z_acl_only",
        "quantum_simulation_via_p215z_acl_only", "physical_validation_via_p216z_acl_only",
        "no_module_local_llm", "never_opaque_unexplainable_decisions",
        "never_unvalidated_simulation_claims", "opaque_bio_safety_strategy_forbidden",
        "module_local_biotechnology_simulation_forbidden",
    ))
    router = (root / "backend/contexts/biotechnology/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@biotechnology_router.get("/simulation")', "/simulation/vision", "/simulation/architecture",
        "/simulation/digital-twins", "/simulation/engine", "/simulation/life-modeling",
        "/simulation/intelligence", "/simulation/model-lifecycle", "/simulation/ai-integration",
        "/simulation/quantum-readiness", "/simulation/robotics-integration", "/simulation/domain-model",
        "/simulation/governance", "/simulation/security", "/simulation/integration",
        "/simulation/roadmap", "/simulation/cqrs", "/simulation/events",
        "/simulation/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_BIOTECHNOLOGY_SIMULATION.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Bio Simulation Platform is missing",
        "Never Digital Twin Architecture is missing",
        "Never Computational Simulation Engine is missing",
        "Never Life Modeling Framework is missing",
        "Never Multi-scale Architecture is missing",
        "Never AI Integration is missing",
        "Never Quantum Readiness is missing",
        "Never Robotics Integration is missing",
        "Never Governance is missing",
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
        "Never Replace P217-F Synthetic",
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
        "Never Unvalidated Simulation Claims",
        "Create a computational intelligence ecosystem",
        "P217", "P217-F", "P216-Z", "P215-Z", "P214-Z", "P217-H",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P217-G", "adr": 506, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "biotechnology",
        "capability": "CAP-PLT-BIO-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
